import streamlit as st
import io
import os
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from googletrans import Translator
from indictrans import Transliterator
import openai
from gtts import gTTS
from io import BytesIO

openai.api_key = st.secrets["openai_api_key"]

def chatbot_response(prompt):
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.8,
    )
    message = completions.choices[0].text
    return message

def text_to_speech(text):
    audio_bytes = BytesIO()
    tts = gTTS(text=text, lang="hi")
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes.read()

def transcribe_audio(audio_file):
    client = speech.SpeechClient()
    content = audio_file.read()
    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='hi-IN',
    )
    response = client.recognize(config=config, audio=audio)
    text = response.results[0].alternatives[0].transcript
    return text

def run_chatbot():    
    default_prompt = "Answer in details in Hinglish language. Aap ek Microentreprenuer ke Mentor hai. Microentreprenuer ka sawaal:"
    st.markdown("Click on the record button and speak your query...")
    if st.button("Record"):
        try:
            st.warning("Please speak now. Recording will end in 10 seconds.")
            rec = st.audio_recorder(sample_rate=16000, duration=10, format="wav")
            with rec as audio_file:
                audio_data = audio_file.read()
            st.success("Recording complete!")
            text = transcribe_audio(io.BytesIO(audio_data))
            hindi_text = Transliterator(source='eng', target='hin').transform(text)
            english_text = Translator().translate(hindi_text, dest='en').text
            prompt = default_prompt + "\nYou: " + english_text      
            response = chatbot_response(prompt)
            st.success(f"Chatbot: {response}")
            st.audio(text_to_speech(response), format="audio/wav")
        except Exception as e:
            st.error("Error: " + str(e))

if __name__ == "__main__":
    st.set_page_config(page_title="Hinglish Chatbot")
    st.title("Hinglish Chatbot")
    run_chatbot() 
