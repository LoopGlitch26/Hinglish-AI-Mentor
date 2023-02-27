import streamlit as st
import openai

# Initialize the OpenAI API key
openai.api_key = "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"

# Define a function to handle the chatbot response
def chatbot_response(prompt):
    completions = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = completions.choices[0].text
    return message

# Set the title of the Streamlit app
st.title("Mentor AI Chatbot by Bravish")

# Create a text input field for the user to input their message
user_input = st.text_input("You: ")

# When the user clicks the "Submit" button, generate a response from the chatbot
if st.button("Submit"):
    if user_input.lower() == "try again":
        st.write("Chatbot: Terminating the chatbot...")
    else:
        response = chatbot_response(user_input)
        st.write("Chatbot: ", response)

