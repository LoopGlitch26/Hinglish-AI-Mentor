import streamlit as st
from googletrans import Translator
from indictrans import Transliterator
import openai
from gtts import gTTS
from io import BytesIO
import azure.cognitiveservices.speech as speechsdk

openai.api_key = st.secrets["openai_api_key"]

def text_to_speech(text, speaking_rate=1.0):
    speech_config = speechsdk.SpeechConfig(subscription=st.secrets["azure_key"], region=st.secrets["azure_region"])
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    ssml_string = f'<speak version="1.0" xmlns="https://www.w3.org/2001/10/synthesis" xml:lang="hi-IN"><prosody rate="{speaking_rate}">{text}</prosody></speak>'
    result = synthesizer.speak_ssml_async(ssml_string).get()
    stream = result.audio_data
    audio_bytes = stream.read_all()
    return audio_bytes

def run_chatbot():    
    default_prompt = "Answer in details in Hinglish language. Aap ek Microentreprenuer ke Mentor hai. Microentreprenuer ka sawaal:"
    
    use_voice_input = st.checkbox("Use voice input")
    if use_voice_input:
        speech_config = speechsdk.SpeechConfig(subscription=st.secrets["azure_speech_subscription_key"], region=st.secrets["azure_speech_region"])
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
        st.info("Speak your query in Hinglish...")
        result = recognizer.recognize_once_async().get()
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            user_input = result.text
        else:
            st.warning("Could not recognize speech")
            user_input = ""
    else:
        user_input = st.text_input("Enter your query in Hinglish:")
    
    if user_input:
        try:
            hindi_text = Transliterator(source='eng', target='hin').transform(user_input)
            english_text = Translator().translate(hindi_text, dest='en').text
            prompt = default_prompt + "\nYou: " + english_text      
            response = chatbot_response(prompt)
            st.success(f"Chatbot: {response}")
            st.audio(text_to_speech(response, speaking_rate=1.5), format="audio/wav")
        except Exception as e:
            st.error("Error: " + str(e))


if __name__ == "__main__":
    st.set_page_config(page_title="Hinglish Chatbot")
    st.title("Hinglish Chatbot")
    run_chatbot()
