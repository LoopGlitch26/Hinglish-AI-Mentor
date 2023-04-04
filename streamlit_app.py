import streamlit as st
from googletrans import Translator
from indictrans import Transliterator
import openai
import speech_recognition as sr
from gtts import gTTS
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

def run_chatbot(audio_input):
    # Convert speech to text
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_input) as source:
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
            tts.save('response.mp3')
            st.audio('response.mp3', format='audio/mp3')
        except Exception as e:
            st.error("Error: " + str(e))

if __name__ == "__main__":
    st.set_page_config(page_title="Hinglish Chatbot")
    st.title("Hinglish Chatbot")

    # Create WebRTC audio input
    webrtc_ctx = webrtc.StreamlitWebRTC(audio=True, key="audio-input")
    audio_input = webrtc_ctx.audio_receiver()

    # Run the chatbot
    if st.button("Start Chatbot"):
        run_chatbot(audio_input)
