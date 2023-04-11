import streamlit as st
from googletrans import Translator
from indictrans import Transliterator
import openai
import time
import io
import whisper
from gtts import gTTS
import wavio

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
    audio_bytes = io.BytesIO()
    tts = gTTS(text=text, lang="en")
    tts.save(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes.read()


def record_audio(duration):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Please start speaking...")
        audio = r.record(source, duration=duration)
        st.write("Recording completed...")
    return audio


def speech_to_text(audio):
    r = sr.Recognizer()
    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        st.write("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        st.write("Could not request results from Google Speech Recognition service; {0}".format(e))


def run_chatbot():
    default_prompt = "Answer in details in Hinglish language. Aap ek Microentreprenuer ke Mentor hai. Microentreprenuer ka sawaal: "
    inp = st.selectbox("Which input form would you like", ["Text", "Voice"])

    if inp == "Text":
        user_input = st.text_input("Enter your query in Hinglish:")
        if user_input:
            try:
                hindi_text = Transliterator(source="eng", target="hin").transform(user_input)
                english_text = Translator().translate(hindi_text, dest="en").text
                prompt = default_prompt + "\nYou: " + english_text
                response = chatbot_response(prompt)
                st.success(f"Chatbot: {response}")
                st.audio(text_to_speech(response), format="audio/mp3")
            except Exception as e:
                st.error("Error: " + str(e))

    else:
        rec = st.button("Record the question")
        if rec:
            duration = 10
            audio = record_audio(duration)
            text = speech_to_text(audio)
            if text:
                st.success(f"Recorded text: {text}")

        submit = st.button("Generate the answer")
        if submit:
            try:
                prompt = "Answer in details in Hinglish language. Aap ek Microentreprenuer ke Mentor hai. Microentreprenuer ka sawaal: " + text + " ?"
                response = chatbot_response(prompt)
                st.success(f"Chatbot: {response}")
                audio_bytes = text_to_speech(response)
                with io.BytesIO(audio_bytes) as stream:
                    with wavio.open(stream, mode="rb") as wav_file:
                        wav_data = wav_file.data
                        whisper.save_model(wav_data, "model")
                st.audio(audio_bytes, format="audio/mp3")
            except Exception as e:
                st.error("Error: " + str(e))


if __name__ == "__main__":
    run_chatbot()
