import streamlit as st
from googletrans import Translator
from indictrans import Transliterator
import openai
from gtts import gTTS
from io import BytesIO
import speech_recognition as sr

from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events

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
    user_input = st.text_input("Enter your query in Hinglish:")
    stt_button = Button(label="Speak", width=100)

    r = sr.Recognizer()
    mic = sr.Microphone()
    try:
        with mic as source:
            r.adjust_for_ambient_noise(source)
    except Exception as e:
        st.error("Error: " + str(e))
        return

    def transcribe_audio():
        with mic as source:
            audio = r.listen(source)
        text = r.recognize_google(audio, language='hi-IN')
        return text

    stt_button.js_on_event("button_click", CustomJS(code="""
        document.dispatchEvent(new CustomEvent("START_SPEECH"));
    """))

    result = streamlit_bokeh_events(
        stt_button,
        events="START_SPEECH",
        key="listen",
        refresh_on_update=False,
        override_height=75,
        debounce_time=0
    )

    if result:
        if "START_SPEECH" in result:
            try:
                user_input = transcribe_audio()
                st.text_input("Your query is:", user_input)
            except Exception as e:
                st.error("Error: " + str(e))

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

if __name__ == "__main__":
    st.set_page_config(page_title="Hinglish Chatbot")
    st.title("Hinglish Chatbot")
    run_chatbot()
