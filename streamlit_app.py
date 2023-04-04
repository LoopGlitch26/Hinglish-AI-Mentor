import streamlit as st
from googletrans import Translator
from indictrans import Transliterator
import openai
import speech_recognition as sr
from gtts import gTTS
import tempfile
import streamlit_webrtc as webrtc

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
    try:
        # Define audio input and output
        audio_input = webrtc.AudioProcessor(
            device=webrtc.audio_devices.get_default_input_device_info()["name"]
        )
        audio_output = webrtc.AudioProcessor(
            device=webrtc.audio_devices.get_default_output_device_info()["name"]
        )

        # Get user audio input
        st.write("Speak your query:")
        audio_input_frames = audio_input.record(num_frames=1024)
        user_audio = audio_input_frames.to_ndarray()

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
        with open(audio_file, 'rb') as af:
            audio_output.play(af.read())
    except Exception as e:
        st.error(f"Error: {e}")

if __name__ == "__main__":
    st.set_page_config(page_title="Hindi Chatbot")
    st.title("Hindi Chatbot")
    run_chatbot()
