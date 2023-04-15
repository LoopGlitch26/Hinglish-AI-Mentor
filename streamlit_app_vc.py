import streamlit as st
from googletrans import Translator
from indictrans import Transliterator
import openai
from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
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

def run_chatbot():    
    default_prompt = "Answer in details in Hinglish language. Aap ek Microentreprenuer ke Mentor hai. Microentreprenuer ka sawaal:"
    
    st.write("Speak now:")
    audio_bytes = audio_recorder()
    
    if audio_bytes:
        try:
            client = speech_v1.SpeechClient()
            audio = speech_v1.RecognitionAudio(content=audio_bytes)
            config = speech_v1.RecognitionConfig(
                encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code="hi-IN",
            )
            response = client.recognize(config=config, audio=audio)
            user_input = response.results[0].alternatives[0].transcript
            st.write("You said:", user_input)

            hindi_text = Transliterator(source='eng', target='hin').transform(user_input)
            english_text = Translator().translate(hindi_text, dest='en').text
            prompt = default_prompt + "\nYou: " + english_text      
            response = chatbot_response(prompt)
            st.success(f"Chatbot: {response}")
            st.audio(text_to_speech(response), format="audio/wav")
        except Exception as e:
            st.error("Error: " + str(e))
    else:
        st.warning("No audio input detected. Please try again.")

if __name__ == "__main__":
    st.set_page_config(page_title="Hinglish Chatbot")
    st.title("Hinglish Chatbot")
    run_chatbot() 
