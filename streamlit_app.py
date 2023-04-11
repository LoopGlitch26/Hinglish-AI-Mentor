import streamlit as st
from googletrans import Translator
from indictrans import Transliterator
import openai
import speech_recognition as sr
import pyttsx3
import time
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
    engine = pyttsx3.init()
    engine.setProperty("rate", 150) 
    audio_bytes = BytesIO()
    engine.save_to_bytesio(audio_bytes, text)
    audio_bytes.seek(0)
    return audio_bytes.read()

def run_chatbot():    
    default_prompt = "Answer in details in Hinglish language. Aap ek Microentreprenuer ke Mentor hai. Microentreprenuer ka sawaal:"
    inp=st.selectbox("Which input form would you like", ['Text', 'Voice'])

    if inp=="Text":
        user_input = st.text_input("Enter your query in Hinglish:")
        if user_input:
            try:
                hindi_text = Transliterator(source='eng', target='hin').transform(user_input)
                english_text = Translator().translate(hindi_text, dest='en').text
                prompt = default_prompt + "\nYou: " + english_text      
                response = chatbot_response(prompt)
                st.success(f"Chatbot: {response}")
                st.audio(text_to_speech(response), format="audio/wav")
            except Exception as e:
                st.error("Error: " + str(e))

    else:
        st.warning("Please wait for the recorder to be ready before speaking.")
        r = sr.Recognizer()
        mic = sr.Microphone()
        with mic as source:
            r.adjust_for_ambient_noise(source) 
            st_audiorec("Click to record the symptoms")
            audio = r.listen(source)
            st.success("Recording completed. Generating the answer...")
            text = r.recognize_google(audio, language="en-IN")
            st.write(f"You said: {text}")
            
        try:
            response = openai.ChatCompletion.create(
                model="text-davinci-003",
                prompt=f"WWhat is the answer to my question: {text}?",
                temperature=0.8,
                max_tokens=1024,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                stop=["\n", "Chatbot:"]
            )

            chatbot_reply = response.choices[0].text.strip()
            st.success(f"Chatbot: {chatbot_reply}")
            st.audio(text_to_speech(chatbot_reply), format="audio/wav")
        except Exception as e:
            st.error("Error: " + str(e))

if __name__ == "__main__":
    st.set_page_config(page_title="Hinglish Chatbot")
    st.title("Hinglish Chatbot")
    run_chatbot() 
