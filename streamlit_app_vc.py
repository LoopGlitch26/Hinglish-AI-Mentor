import streamlit as st
from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechRecognizer, SpeechSynthesizer, SpeechSynthesisOutputFormat
from googletrans import Translator
from indictrans import Transliterator
import openai

# Azure Cognitive Services configuration
azure_key = st.secrets["azure_key"]
azure_region = st.secrets["azure_region"]
speech_config = SpeechConfig(subscription=azure_key, region=azure_region)
speech_recognizer = SpeechRecognizer(speech_config=speech_config)
speech_synthesizer = SpeechSynthesizer(speech_config=speech_config)

# OpenAI configuration
openai.api_key = st.secrets["openai_api_key"]

def chatbot_response(prompt):
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = completions.choices[0].text
    return message

def run_voice_assistant():
    # Start recording audio from microphone
    st.info("Speak now...")
    audio_stream = st._get_current_stream().recorder.record(duration=10.0, offset=None)

    try:
        # Recognize speech using Azure Cognitive Services
        audio_data = AudioDataStream(audio_stream)
        result = speech_recognizer.recognize_once(audio_data)

        # Convert Hinglish to Hindi
        user_input = result.text
        hindi_text = Transliterator(source='eng', target='hin').transform(user_input)

        # Convert Hindi to English
        english_text = Translator().translate(hindi_text, dest='en').text

        # Ask the OpenAI API
        response = chatbot_response(english_text)

        # Convert OpenAI API response to Hindi
        hindi_response = Translator().translate(response, dest='hi').text

        # Convert Hindi response to Hinglish
        hinglish_response = Transliterator(source='hin', target='eng').transform(hindi_response)

        # Synthesize speech using Azure Cognitive Services
        speech_synthesizer.speak_text_async(hindi_response)
        audio_result = speech_synthesizer.get_audio_result()
        audio_data_stream = AudioDataStream(audio_result)
        st.audio(audio_data_stream, format='audio/wav')

        # Output Hinglish response
        st.success(f"Voice Assistant (Hinglish): {hinglish_response}")
    except Exception as e:
        st.error("Error: " + str(e))

if __name__ == "__main__":
    st.set_page_config(page_title="Hinglish Voice Assistant")
    st.title("Hinglish Voice Assistant")
    run_voice_assistant()
