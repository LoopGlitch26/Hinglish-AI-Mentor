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
            kw = st.text_input("",placeholder="Enter your query",key = "en_keyword")
            submit = form.form_submit_button("Get advice")
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
                    playback_rate = st.slider("Playback speed", min_value=0.5, max_value=2.0, value=1.5, step=0.1)
                    st.audio(mp3_play,format="audio/mp3", start_time=0, playback_rate=playback_rate)
                    st.success(res)
                except Exception as e:
                    st.error("Error: " + str(e))
                
    else :
        model=whisper.load_model("base")
        rec=st.button("Record your query")
        st.markdown("Please don't use the stop button, it terminates the process abruptly\nWait for the 'get advice' button to appear and click it")
        text=""
        if rec:
            wav_audio_data = st_audiorec()
            time.sleep(10)
            if wav_audio_data is not None:
                text = Transliterator(source='eng', target='hin').transform(model.transcribe(st.audio(wav_audio_data, format='audio/wav')))

        submit = st.button("Get advice")
        if submit:
            try:
                english_text = Translator().translate(text, dest='en').text
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
                playback_rate = st.slider("Playback speed", min_value=0.5, max_value=2.0, value=1.5, step=0.1)
                st.audio(mp3_play,format="audio/mp3", start_time=0, playback_rate=playback_rate)
                st.success(res)
            except Exception as e:
                st.error("Error: " + str(e))       
                                    
    footer = '<p style=\'text-align: center; font-size: 0.8em;\'>Copyright © Bravish</p>'
    st.markdown(footer, unsafe_allow_html=True)        
        
if __name__ == "__main__":
    st.set_page_config(page_title="Hinglish Chatbot")
    if runtime.exists():
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())

