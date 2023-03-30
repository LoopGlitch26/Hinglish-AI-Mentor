# Hinglish Chatbot

This project aims to create a chatbot that can communicate with users in Hinglish (a combination of Hindi and English languages) and provide responses in the same language. The chatbot is powered by `OpenAI's GPT-3` language model and uses `Azure Cognitive Services Translator API` and `Google Translate API` for language translation. 

The code uses the `googletrans` (for translation) and `indictrans` (for transliteration) libraries to convert Hinglish input to Hindi and then from Hindi to English, respectively. Once the input is in English, it is passed to the OpenAI API, which generates a response using the `text-davinci-003` language model.
