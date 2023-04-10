import streamlit as st
from googletrans import Translator
from indictrans import Transliterator
import openai
from gtts import gTTS
from io import BytesIO
import soundfile as sf

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

def audio_to_text(audio_file):
    data, sample_rate = sf.read(audio_file)
    return data

def text_to_speech(text):
    audio_bytes = BytesIO()
    tts = gTTS(text=text, lang="hi")
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes.read()

def run_chatbot():    
    default_prompt = "Answer in details in Hinglish language. Aap ek Microentreprenuer ke Mentor hai. Microentreprenuer ka sawaal:"
    inp = st.selectbox("Which input form would you like", ['Text', 'Voice'])
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
        audio_file = st.file_uploader("Upload audio", type=["wav"])
        if audio_file:
            try:
                text = audio_to_text(audio_file)
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
