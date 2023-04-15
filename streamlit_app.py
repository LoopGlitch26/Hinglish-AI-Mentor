import os
import openai
from googletrans import Translator
from indictrans import Transliterator
import time
from io import BytesIO
from gtts import gTTS
from streamlit.web import cli as stcli
from streamlit import runtime
import streamlit as st
from dotenv import load_dotenv
import streamlit.components.v1 as components
from streamlit_audio_recorder.st_custom_components import st_audiorec
from scipy.io.wavfile import write
import wavio as wv
import whisper
import numpy as np
import soundfile as sf
from streamlit.state.session_state import SessionState
from google.cloud import speech_v1p1beta1 as speech

def main():
    openai.api_key = st.secrets["openai_api_key"]
    title='<p style="color:Red; align:center; font-size: 42px;">Hinglish ChatBot<p>'
    st.markdown(title,unsafe_allow_html=True)
    
    st.markdown("AI-powered chatbot to assist you with your business queries and provide you with relevant advice.")
    inp=st.selectbox("Which input form would you like", ['Text', 'Voice'])
    
    default_prompt = "Answer in details in Hinglish language. Aap ek Microentreprenuer ke Mentor hai. Microentreprenuer ka sawaal: "
    form = st.form(key="user_settings")
    if inp=="Text":
        with form:
            kw = st.text_input("Enter your query in Hinglish:", key="en_keyword", placeholder="Type here...")
            submit = form.form_submit_button("Get advice")
            state = SessionState.get(chat_history=[])
            if submit:
                try:
                    hindi_text = Transliterator(source='eng', target='hin').transform(kw)
                    english_text = Translator().translate(hindi_text, dest='en').text
                    response = openai.Completion.create(
                        engine="text-davinci-003", 
                        prompt=default_prompt + "\n" + english_text,
                        max_tokens=1024,
                        n = 1,
                        stop=None,
                        temperature=0.8,
                    )
                    res=response.choices[0].text
                    myobj = gTTS(text=res,lang='hi', slow=False)
                    mp3_play=BytesIO()
                    myobj.write_to_fp(mp3_play)
                    st.audio(mp3_play,format="audio/mp3", start_time=0)
                    st.success(res)
                    state.chat_history.append((text, res))
                except Exception as e:
                    st.error("Error: " + str(e))
            
            if state.chat_history:
                st.subheader("Chat history")
                for i, (q, a) in enumerate(state.chat_history):
                    st.write(f"Query {i+1}: {q}")
                    st.write(f"Answer {i+1}:           
               
    else:
        client = speech.SpeechClient()
        rec=st.button("Record your query")
        st.markdown("Please don't use the stop button, it terminates the process abruptly.\nWait for the 'get advice' button to appear and click it")
        text=""
        if rec:
            audio_config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code="hi-IN",
            )
            streaming_config = speech.StreamingRecognitionConfig(
                config=audio_config, interim_results=True,
            )

            def generate_requests(audio_data):
                request = speech.StreamingRecognizeRequest(audio_content=audio_data)
                yield request

            wav_audio_data = st_audiorec()
            if wav_audio_data is not None:
                try:
                    requests = generate_requests(wav_audio_data)
                    responses = client.streaming_recognize(streaming_config, requests)
                    text = ""
                    for response in responses:
                        for result in response.results:
                            if result.is_final:
                                text += result.alternatives[0].transcript
                    st.success("Query recorded successfully!")
                except Exception as e:
                    st.warning("An error occurred while processing your query: {}".format(str(e)))
            else:
                st.warning("No audio data was recorded")    
                                    
    footer = '<p style=\'text-align: center; font-size: 0.8em;\'>Copyright © Bravish</p>'
    st.markdown(footer, unsafe_allow_html=True)        
        
if __name__ == "__main__":
    st.set_page_config(page_title="Hinglish Chatbot")
    if runtime.exists():
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())

