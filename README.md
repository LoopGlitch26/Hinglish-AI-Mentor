# Hinglish Chatbot

This project aims to create a chatbot that can communicate with users in Hinglish (a combination of Hindi and English languages) and provide responses in the same language. This app can be used for microentreprenuers' mentoring purposes, to increse business revenue through upskilling & saving cost of mentorship.

The chatbot is powered by `OpenAI's GPT-3` language model and uses `Azure Cognitive Services Translator API` and `Google Translate API` for language translation. The code uses the `googletrans` (for translation) and `indictrans` (for transliteration) libraries to convert Hinglish input to Hindi and then from Hindi to English, respectively. Once the input is in English, it is passed to the OpenAI API, which generates a response using the `text-davinci-003` language model.

### Streamlit Deployed: https://hinglish-chatbot-loopglitch26.streamlit.app/
### VC version: https://hinglish-vc-chatbot-loopglitch26.streamlit.app/

![Screenshot 2023-04-16 at 10 39 18 PM](https://user-images.githubusercontent.com/53336715/232328958-c8d16859-dd07-46b6-8252-3c49c39cb763.png)
![Screenshot 2023-04-16 at 10 39 51 PM](https://user-images.githubusercontent.com/53336715/232328964-bc31b9dd-63b5-444c-acc4-a1bc157135d4.png)

### Flowchart:

![Screenshot 2023-06-17 at 6 34 10 AM](https://github.com/LoopGlitch26/Hinglish-AI-Mentor/assets/53336715/57d51d44-772b-4bca-9d84-376c57cfed0b)

## Future Work

* Fix input voice to text feature
* Add multilingual feature
* Suggestions 
