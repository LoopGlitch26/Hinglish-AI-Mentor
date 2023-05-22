import streamlit as st
from googletrans import Translator
from indictrans import Transliterator
import openai
from gtts import gTTS
from io import BytesIO
import whisper

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

def run_chatbot():
    model = whisper.load_model("whisper/asr_deepspeech_tamil_0.9.0.model")
    
    default_prompt = "Answer in details in Hinglish language. Aap ek Microentreprenuer ke Mentor hai. Microentreprenuer ka sawaal:"
    user_input = st.selectbox("Select your input method:", ["Text", "Voice"])
    
    if user_input == "Text":
        user_text = st.text_input("Enter your query in Hinglish:")
        if user_text:
            try:
                hindi_text = Transliterator(source='eng', target='hin').transform(user_text)
                english_text = Translator().translate(hindi_text, dest='en').text
                prompt = default_prompt + "\nYou: " + english_text
                response = chatbot_response(prompt)
                st.success(f"Chatbot: {response}")
                st.audio(text_to_speech(response), format="audio/wav")
            except Exception as e:
                st.error("Error: " + str(e))
    elif user_input == "Voice":
        st.warning("Click the 'Start Recording' button and speak your query.")
        record_button = st.button("Start Recording")
        if record_button:
            with st.spinner("Recording..."):
                duration = 10  # You can adjust the duration of the recording
                fs = 16000  # Sample rate (16 kHz)
                frames = int(duration * fs)
                recording = st.whisper.record(duration=duration, sample_rate=fs)
                st.warning("Recording completed!")
                st.audio(recording, format="audio/wav", start_time=0)
                decoded_text = model.transcribe(recording)
                st.info(f"You said: {decoded_text}")
                try:
                    hindi_text = Transliterator(source='eng', target='hin').transform(decoded_text)
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
