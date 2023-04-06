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
