import streamlit as st
from googletrans import Translator
from indictrans import Transliterator
import openai
from gtts import gTTS
from io import BytesIO
import requests

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
    tts = gTTS(text=text, lang="hi", slow=False)
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes.read()

def transcribe_audio(audio_data, api_key):
    url = "https://api.assemblyai.com/v2/transcript"

    headers = {
        "authorization": api_key,
    }

    files = {
        "audio": audio_data,
    }

    response = requests.post(url, headers=headers, files=files)
    response_data = response.json()

    if response.status_code == 201:
        transcript_id = response_data["id"]
        return transcript_id
    else:
        raise Exception("Error transcribing audio.")

def get_transcription(transcript_id, api_key):
    url = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"

    headers = {
        "authorization": api_key,
    }

    response = requests.get(url, headers=headers)
    response_data = response.json()

    if response.status_code == 200:
        transcript_status = response_data["status"]
        if transcript_status == "completed":
            transcript_text = response_data["text"]
            return transcript_text
        elif transcript_status == "queued" or transcript_status == "processing":
            return None
    else:
        raise Exception("Error retrieving transcription.")

def run_chatbot():    
    default_prompt = "Answer in details in Hinglish language. Aap ek Microentreprenuer ke Mentor hai. Microentreprenuer ka sawaal:"
    user_input = st.text_input("Enter your query in Hinglish:")
    user_audio = st.file_uploader("Or upload an audio file:", type=["wav", "mp3"])

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

    if user_audio:
        try:
            assemblyai_api_key = "0b0a5dff3d4a4893af85204dc660f88b"
            transcript_id = transcribe_audio(user_audio.read(), assemblyai_api_key)
            transcript_text = None

            while transcript_text is None:
                transcript_text = get_transcription(transcript_id, assemblyai_api_key)

            hindi_text = Transliterator(source='eng', target='hin').transform(transcript_text)
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
