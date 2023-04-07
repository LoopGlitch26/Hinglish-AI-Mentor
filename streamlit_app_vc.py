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

# Define the Streamlit app
def main():
    st.title("Hinglish Chatbot")
        
    # Prompt the user to select their business type
    st.write("Please select your business type:")
    business_type_options = ("Kirana shop", "Mobile repair shop", "Beauty salon", "Food truck", "Others")
    business_type = st.selectbox("", business_type_options)

    if business_type == "Others":
        # Prompt the user to input their business type
        business_type = st.text_input("Please enter your business type:")

    # Prompt the user to input their business details in Hinglish
    st.write("Please provide some details about your business in Hinglish:")
    business_name = st.text_input("Business name")
    business_description = st.text_area("Business description")
    target_customers = st.text_area("Target customers")

    # Use OpenAI to act as a mentor based on the provided details
    st.write("Welcome to the mentorship program for your business, " + business_name + "!")
    st.write("Here are some tips and advice based on the information you provided:")

    # Ask the user if they would like to continue
    st.write("Kya aap jaari rakhna chahte hain?")
    ready = st.radio("", ("Haan", "Nahi"))

    # If the user is ready, start the mentorship session
    if ready == "Haan":
        # Ask the user a question in Hinglish and get the mentor's response in Hinglish
        question = st.text_input("Aap kya puchna chahte hain?")
        prompt = "Hinglish mein jawaab dein: " + business_description + " " + target_customers + " " + question
        response = chatbot_response(prompt)

        # Display the mentor's response in Hinglish
        st.write("Mentor: " + response)

        # Allow the user to respond to the mentor's advice
        while True:
            user_input = st.text_input("Aap kya kehna chahte hain?")
            if user_input:
                response = chatbot_response(user_input)
                st.write("Mentor: " + response)

"""
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
"""

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
"""    
