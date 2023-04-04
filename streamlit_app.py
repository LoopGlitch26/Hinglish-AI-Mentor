import streamlit as st
from googletrans import Translator
from indictrans import Transliterator
import openai
import speech_recognition as sr
from gtts import gTTS
import tempfile
from streamlit_webrtc import webrtc_streamer

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

def run_chatbot():
    # Get user audio input
    st.write("Speak your query:")
    audio_input = webrtc_streamer(
        key="audio-input",
        audio=True,
        desired_output_format=webrtc_streamer.OutputFormat.AUDIO,
        height=0,
        width=0,
        streaming_time_limit=7000,  # 7000 milliseconds
        throttling_refresh_rate=1,
    )
    user_audio = st.audio(audio_input, format="audio/wav")

    # Convert user audio input to Hindi text
    st.write("Converting audio to text...")
    recognizer = sr.Recognizer()
    with sr.AudioFile(user_audio) as source:
        audio_text = recognizer.recognize_google(source, language='hi-IN')
    hindi_text = audio_text

    # Convert Hindi to English
    st.write("Converting Hindi text to English...")
    english_text = Translator().translate(hindi_text, dest='en').text

    # Ask the OpenAI API
    st.write("Asking the OpenAI API...")
    response = chatbot_response(english_text)

    # Convert OpenAI API response to Hindi
    st.write("Converting OpenAI API response to Hindi...")
    hindi_response = Translator().translate(response, dest='hi').text

    # Output Hindi response
    st.success(f"Chatbot (Hindi): {hindi_response}")

    # Convert Hindi response to Hinglish
    st.write("Converting Hindi response to Hinglish...")
    hinglish_response = Transliterator(source='hin', target='eng').transform(hindi_response)

    # Convert Hinglish response to audio
    st.write("Converting text to audio...")
    tts = gTTS(hindi_response, lang='hi')
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        tts.write_to_fp(tf)
        tf.flush()
        audio_file = tf.name

    # Output chatbot audio response
    st.write("Chatbot Response:")
    st.audio(audio_file)

if __name__ == "__main__":
    st.set_page_config(page_title="Hindi Chatbot")
    st.title("Hindi Chatbot")
    run_chatbot()
