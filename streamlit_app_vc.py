import streamlit as st
from googletrans import Translator
from indictrans import Transliterator
import openai

openai.api_key = st.secrets["openai_api_key"]

def chatbot_response(prompt):
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.8,
        top_p=0.9,
        frequency_penalty=0.5,
        presence_penalty=0.5,
        output_language="hi-IN",
    )
    message = completions.choices[0].text
    return message    
    
def run_chatbot():    
    default_prompt = """
    Hinglish Mentor Chatbot:
    Please provide your query in Hinglish language.
    I will try my best to guide you like a mentor and provide helpful insights to your query.
    Your query:
    """

    user_input = st.text_input("Enter your query in Hinglish:")

    if user_input:
        try:
            hindi_text = Transliterator(source='eng', target='hin').transform(user_input)
            english_text = Translator().translate(hindi_text, dest='en').text
            prompt = default_prompt + "\nYou: " + english_text      
            response = chatbot_response(prompt)
            st.success(f"Chatbot: {response}")
        except Exception as e:
            st.error("Error: " + str(e))

if __name__ == "__main__":
    st.set_page_config(page_title="Hinglish Chatbot")
    st.title("Hinglish Chatbot")
    run_chatbot()    
