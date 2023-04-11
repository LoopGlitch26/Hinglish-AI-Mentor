import streamlit as st
import openai
from gtts import gTTS
from io import BytesIO
import scipy.io.wavfile
import wavio
import whisper
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")

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

def text_to_speech(text, speed=1.5):
    audio_bytes = BytesIO()
    tts = gTTS(text=text, lang="hi")
    tts_speed = str(speed)
    tts.save("temp.mp3")
    wavio.write("temp.wav", scipy.io.wavfile.read("temp.mp3")[0], scipy.io.wavfile.read("temp.mp3")[1])
    with open("temp.wav", "rb") as f:
        audio_bytes.write(f.read())
    audio_bytes.seek(0)
    os.remove("temp.mp3")
    os.remove("temp.wav")
    return audio_bytes.read()

def record_audio():
    return st.audio_recorder("recording.wav", format="wav")

def process_audio(audio_data):
    scipy.io.wavfile.write("recording.wav", 44100, audio_data)
    text = whisper.transcribe("recording.wav")
    os.remove("recording.wav")
    return text

def run_chatbot():
    input_mode = st.selectbox("Select Input Mode:", ["Text", "Voice"])

    if input_mode == "Text":
        default_prompt = "Answer in details in Hinglish language. Aap ek Microentreprenuer ke Mentor hai. Microentreprenuer ka sawaal:"
        user_input = st.text_input("Enter your query in Hinglish:")

        if user_input:
            try:
                prompt = default_prompt + "\nYou: " + user_input
                response = chatbot_response(prompt)
                st.success(f"Chatbot: {response}")
                st.audio(text_to_speech(response), format="audio/wav")
            except Exception as e:
                st.error("Error: " + str(e))

    elif input_mode == "Voice":
        st.warning("Please speak your query in Hinglish:")
        audio_data = record_audio()

        if audio_data:
            try:
                text = process_audio(audio_data)
                hindi_text = Transliterator(source='eng', target='hin').transform(text)
                english_text = Translator().translate(hindi_text, dest='en').text
                prompt = "Answer in details in Hinglish language. Aap ek Microentreprenuer ke Mentor hai. Microentreprenuer ka sawaal:\nYou: " + english_text
                response = chatbot_response(prompt)
                st.success(f"Chatbot: {response}")
                st.audio(text_to_speech(response), format="audio/wav")
            except Exception as e:
                st.error("Error: " + str(e))

if __name__ == "__main__":
    st.set_page_config(page_title="Hinglish Chatbot")
    st.title("Hinglish Chatbot")
    run_chatbot()
