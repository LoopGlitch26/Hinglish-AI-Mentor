import streamlit as st
from googletrans import Translator
from indictrans import Transliterator
import openai
import sounddevice as sd
import tempfile
import os
from pydub import AudioSegment
from pydub.playback import play

openai.api_key = st.secrets["openai_api_key"]

def chatbot_response(prompt):
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = completions.choices[0].text
    return message

def run_chatbot(frames, sample_rate):
    # Save audio input to a temporary file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        filename = f.name
        AudioSegment(
            data=frames,
            sample_width=2,
            frame_rate=sample_rate,
            channels=1
        ).export(out_f=f, format="wav")

    # Convert speech to text
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio_text = recognizer.record(source)
    user_input = recognizer.recognize_google(audio_text)

    if user_input:
        try:
            # Convert Hinglish to Hindi
            hindi_text = Transliterator(source='eng', target='hin').transform(user_input)

            # Convert Hindi to English
            english_text = Translator().translate(hindi_text, dest='en').text

            # Ask the OpenAI API
            response = chatbot_response(english_text)

            # Convert OpenAI API response to Hindi
            hindi_response = Translator().translate(response, dest='hi').text

            # Convert Hindi response to Hinglish
            hinglish_response = Transliterator(source='hin', target='eng').transform(hindi_response)

            # Output Hinglish response in audio format
            tts = gTTS(hinglish_response)
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                filename = f.name
                tts.save(filename)
                play(AudioSegment.from_mp3(filename))
            os.unlink(filename)
        except Exception as e:
            st.error("Error: " + str(e))

if __name__ == "__main__":
    st.set_page_config(page_title="Hinglish Chatbot")
    st.title("Hinglish Chatbot")

    # Create audio input
    def audio_callback(frames, sample_rate):
        run_chatbot(frames, sample_rate)
    sd.default.samplerate = 44100
    sd.default.channels = 1
    with sd.InputStream(callback=audio_callback):
        st.text("Say something...") # Display a text prompt
        st.pause() # Pause the script until user stops the audio input
