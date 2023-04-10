import streamlit as st
from googletrans import Translator
from indictrans import Transliterator
import openai
from gtts import gTTS
from io import BytesIO

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
   
def text_to_speech(text, speed=1.5):
    audio_bytes = BytesIO()
    tts = gTTS(text=text, lang="hi", slow=False)
    for idx, segment in enumerate(tts.audio._segments):
        new_duration = round(segment.duration * (1/speed), 3)
        segment._data = segment._spawn(segment._data, overrides={'frame_rate': int(tts.frame_rate/speed)})
        segment._duration = new_duration
        if idx == 0:
            combined_segments = segment
        else:
            combined_segments += segment
    combined_segments.export(audio_bytes, format="wav")
    audio_bytes.seek(0)
    return audio_bytes.read()
   
def run_chatbot():    
    default_prompt = "Answer in details in Hinglish language. Aap ek Microentreprenuer ke Mentor hai. Microentreprenuer ka sawaal:"
    user_input = st.text_input("Enter your query in Hinglish:")
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
