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
    inp=st.selectbox("Which input form would you like", ['Text', 'Voice'])
    
    default_prompt = "Answer in details in Hinglish language. Aap ek Microentreprenuer ke Mentor hai. Microentreprenuer ka sawaal: "
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
        rec = st_audio_recorder(sample_rate=16000, duration=10, key="recorder")
        st.markdown("Click on the record button and speak your query...")
        if st.button("Record"):
            try:
                with rec:
                    audio = rec.record(duration=10)
                st.success("Recording complete!")
                write("audio.wav", 16000, audio)
                audio_data, sr = sf.read("audio.wav")
                processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-xlsr-53")
                model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-xlsr-53")
                input_values = processor(audio_data, sampling_rate=sr, return_tensors="pt").input_values
                with torch.no_grad():
                    logits = model(input_values).logits
                predicted_ids = torch.argmax(logits, dim=-1)
                transcriptions = processor.batch_decode(predicted_ids)
                hindi_text = Transliterator(source='eng', target='hin').transform(transcriptions[0])
                english_text = Translator().translate(hindi_text, dest='en').text
                response = openai.Completion.create(
                    engine="text-davinci-003", 
                    prompt=default_prompt + "\n" + english_text,
                    max_tokens=1024,
                    n = 1,
                    stop=None,
                    temperature=0.8,
                )
                res = response.choices[0].text
                myobj = gTTS(text=res, lang='hi', slow=False)
                mp3_play = BytesIO()
            except Exception as e:
                st.error(f"Error: {e}")
                                    
    footer = '<p style=\'text-align: center; font-size: 0.8em;\'>Copyright © Bravish</p>'
    st.markdown(footer, unsafe_allow_html=True)        
        
if __name__ == "__main__":
    st.set_page_config(page_title="Hinglish Chatbot")
    if runtime.exists():
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())
