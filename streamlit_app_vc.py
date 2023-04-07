"""
import streamlit as st
import openai

# Initialize the OpenAI API key
openai.api_key = st.secrets["openai_api_key"]

# Define a function to handle the chatbot response
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

# Main function
def main():
    st.title("Hinglish Chatbot")

    # Add a default prompt to the chatbox
    openai_prompt = "Answer in Hinglish language"

    # Take user input and get response
    user_input = st.text_input("You:", key="input")
    if user_input:
        prompt = openai_prompt + "\nYou: " + user_input + "\nChatbot:"
        response = chatbot_response(prompt)
        st.write(response)

if __name__ == "__main__":
    main()
"""
    
    
    
    
    
    
    
    
import streamlit as st
from googletrans import Translator
from indictrans import Transliterator
import openai

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

def run_chatbot():
    user_input = st.text_input("Enter your query in Hinglish:")

    if user_input:
        try:
            # Convert Hinglish to Hindi
            hindi_text = Transliterator(source='eng', target='hin').transform(user_input)

            # Convert Hindi to English
            english_text = Translator().translate(hindi_text, dest='en').text

            # Ask the OpenAI API
            # response = chatbot_response(english_text)
            
            # Add a default prompt to the chatbox
            openai_prompt = "Answer in Hinglish language. You are a Mentor providing guidance to a Microentreprenuer."

            # Take user input and get response
            # user_input = st.text_input("You:", key="input")
            if user_input:
                prompt = openai_prompt + "\nYou: " + english_text + "\nChatbot:"
                response = chatbot_response(prompt)
                # st.write(response)
                st.write(f"Chatbot (Hinglish): {response}")


            # Convert OpenAI API response to Hindi
            # hindi_response = Translator().translate(response, dest='hi').text

            # Convert Hindi response to Hinglish
            # hinglish_response = Transliterator(source='hin', target='eng').transform(hindi_response)

            # Output Hinglish response
            # st.success(f"Chatbot (Hinglish): {hinglish_response}")

        except Exception as e:
            st.error("Error: " + str(e))

if __name__ == "__main__":
    st.set_page_config(page_title="Hinglish Chatbot")
    st.title("Hinglish Chatbot")
    run_chatbot()
    
