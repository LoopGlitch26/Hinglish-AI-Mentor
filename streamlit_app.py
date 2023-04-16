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

    default_prompt = f"Answer in details in {selected_language} language. Aap ek {business_type} microentrepreneur ke mentor hai. Microentrepreneur ka sawaal: "
    
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
                    if selected_language != 'English':
                        translated_res = Translator().translate(res, dest=selected_language).text
                        myobj = gTTS(text=translated_res, lang=selected_language, slow=False)
                    else:
                        myobj = gTTS(text=res, lang='en', slow=False)
                    mp3_play=BytesIO()
                    myobj.write_to_fp(mp3_play)
                    st.audio(mp3_play, format="audio/mp3", start_time=0)
                    st.success(res)
                except Exception as e:
                    st.error("Error: " + str(e))
                
    else :
        model=whisper.load_model("base")
        rec=st.button("Record your query")
        st.markdown("Please don't use the stop button, it terminates the process abruptly.\nWait for the 'get advice' button to appear and click it")
        text=""
        if rec:
            wav_audio_data = st_audiorec()
            time.sleep(10)
            if wav_audio_data is not None:
                st.warning("Recording failed")
            else:
                st.success("Recording complete")
                with st.spinner("Transcribing..."):
                    sound = np.frombuffer(wav_audio_data, dtype=np.int16)
                    sound = sound.astype('float64') / 2**15
                    sound = sound.reshape(1, -1)
                    text = whisper.predict(model, sound)[0].strip()
                    st.success("Transcription Complete")
                
                try:
                    hindi_text = Transliterator(source='eng', target='hin').transform(text)
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
                    if selected_language != 'English':
                        translated_res = Translator().translate(res, dest=selected_language).text
                        myobj = gTTS(text=translated_res, lang=selected_language, slow=False)
                    else:
                        myobj = gTTS(text=res, lang='en', slow=False)
                    mp3_play=BytesIO()
                    myobj.write_to_fp(mp3_play)
                    st.audio(mp3_play, format="audio/mp3", start_time=0)
                    st.success(res)
                except Exception as e:
                    st.error("Error: " + str(e))
                    

if __name__ == '__main__':
    main()

