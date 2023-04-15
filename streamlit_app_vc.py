import streamlit as st
from googletrans import Translator
from indictrans import Transliterator
import openai
from gtts import gTTS
from io import BytesIO
import speech_recognition as sr

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
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.markdown("Click on the record button and speak your query...")
        audio = r.listen(source)
    st.success("Recording complete!")
    
    try:
        text = r.recognize_google(audio, language='hi-IN')
        hindi_text = Transliterator(source='eng', target='hin').transform(text)
        english_text = Translator().translate(hindi_text, dest='en').text
        prompt = default_prompt + "\nYou: " + english_text      
        response = chatbot_response(prompt)
        st.success(f"Chatbot: {response}")
        st.audio(text_to_speech(response), format="audio/wav")
    except sr.UnknownValueError:
        st.warning("Could not understand audio")
    except sr.RequestError as e:
        st.error(f"Error: {e}")

if __name__ == "__main__":
    st.set_page_config(page_title="Hinglish Chatbot")
    st.title("Hinglish Chatbot")
    run_chatbot() 
