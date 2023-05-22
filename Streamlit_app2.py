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
from scipy.io.wavfile import write
import whisper
import numpy as np
import soundfile as sf
import sounddevice as sd

def main():
    openai.api_key = st.secrets["openai_api_key"]
    title='<p style="color:Red; align:center; font-size: 42px;">Hinglish ChatBot<p>'
    st.markdown(title,unsafe_allow_html=True)
    
    st.markdown("AI-powered chatbot to assist you with your business queries and provide you with relevant advice.")
    
    business_options = ['Kirana store / किराना स्टोर', 'Beauty parlor / ब्यूटी पार्लर', 'Food stall / खाने की दुकान', 'Mobile repair shop / मोबाइल रिपेयर शॉप', 'Other']
    business_type = st.selectbox("What is your type of business?", business_options)
    if business_type == 'Other':
        business_type = st.text_input("Enter your business type:")
        
    language_options = ['Odia', 'Telugu', 'Hindi', 'English']
    selected_language = st.selectbox("Select your regional language:", language_options)

    #default_prompt = f"Answer in details in {selected_language} language. Aap ek {business_type} microentrepreneur ke mentor hai. Microentrepreneur ka sawaal: "
    default_prompt = "Answer in details in Hinglish language. Aap ek Microentreprenuer ke Mentor hai. Microentreprenuer ka sawaal: "
    
    inp = st.selectbox("Which input form would you like", ['Text', 'Voice'])

    form = st.form(key="user_settings")
    if inp=="Text":
        with form:
            kw = st.text_input("Enter your query in Hinglish:", key="en_keyword", placeholder="Type here...")
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
                    st.audio(mp3_play,format="audio/mp3", start_time=0)
                    st.success(res)
                except Exception as e:
                    st.error("Error: " + str(e))
                
    else:
        model = whisper.load_model("base")
        rec = st.button("Record your query")
        st.markdown("Please don't use the stop button, it terminates the process abruptly.\nWait for the 'get advice' button to appear and click it")
        text = ""
        if rec:
            duration = 30  # Set the duration of the recording
            fs = 16000  # Set the sample rate
            recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
            sd.wait()  # Wait until recording is complete
            wav_audio_data = recording.flatten()
            if wav_audio_data is not None:
                try:
                    text = model.transcribe(wav_audio_data)
                except Exception as e:
                    st.warning("An error occurred while processing your query: {}".format(str(e)))
            else:
                st.warning("No audio data was recorded")
      
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
                st.audio(mp3_play,format="audio/mp3", start_time=0)
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
