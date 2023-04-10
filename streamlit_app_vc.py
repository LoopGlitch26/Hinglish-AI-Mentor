import streamlit as st
from googletrans import Translator
from indictrans import Transliterator
import openai
import speech_recognition as sr
import pyttsx3

openai.api_key = st.secrets["openai_api_key"]
translator = Translator()
transliterator = Transliterator(source='eng', target='hin')
r = sr.Recognizer()
engine = pyttsx3.init()

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

def recognize_speech():
    with sr.Microphone() as source:
        st.write("Say something!")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "I'm sorry, I didn't understand that."
        except sr.RequestError:
            return "Sorry, my speech recognition service is down at the moment."

def generate_response(text):
    try:
        hindi_text = transliterator.transform(text)
        english_text = translator.translate(hindi_text, dest='en').text
        prompt = "Answer in details in Hinglish language. Aap ek Microentreprenuer ke Mentor hai. Microentreprenuer ka sawaal:\nYou: " + english_text
        response = chatbot_response(prompt)
        st.success(f"Chatbot: {response}")
        engine.say(response)
        engine.runAndWait()
    except Exception as e:
        st.error("Error: " + str(e))

def run_chatbot():    
    st.write("Click the microphone button and speak in Hindi or Hinglish!")
    if st.button("Start Recording"):
        text = recognize_speech()
        generate_response(text)

if __name__ == "__main__":
    st.set_page_config(page_title="Hinglish Chatbot")
    st.title("Hinglish Chatbot")
    run_chatbot()
