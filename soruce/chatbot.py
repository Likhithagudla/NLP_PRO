import streamlit as st
from twilio.rest import Client
import os
import pygame
import streamlit as st
import speech_recognition as sr
from gtts import gTTS
from googletrans import LANGUAGES, Translator

translator = Translator()
pygame.mixer.init()

language_mapping = {name: code for code, name in LANGUAGES.items()}

def get_language_code(language_name):
    return language_mapping.get(language_name, language_name)

def translator_function(text, from_language, to_language):
    return translator.translate(text, src=from_language, dest=to_language)

def text_to_voice(text_data, to_language):
    myobj = gTTS(text=text_data, lang=to_language, slow=False)
    myobj.save("cache_file.mp3")
    pygame.mixer.Sound("cache_file.mp3").play()
    os.remove("cache_file.mp3")

def recognize_speech(from_language):
    rec = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("🎤 Listening...")
        rec.pause_threshold = 1
        audio = rec.listen(source, phrase_time_limit=10)
    try:
        recognized_text = rec.recognize_google(audio, language=from_language)
        return recognized_text
    except sr.UnknownValueError:
        st.error("Sorry, I did not understand that. 😕")
        return None
    except sr.RequestError as e:
        st.error(f"Could not request results; {e}")
        return None

# Streamlit UI layout
st.title("🤖 Interactive Language Translator Chatbot")

# Language selection
from_language_name = st.selectbox("🌍 Select Source Language:", list(LANGUAGES.values()))
to_language_name = st.selectbox("🌍 Select Target Language:", list(LANGUAGES.values()))

from_language = get_language_code(from_language_name)
to_language = get_language_code(to_language_name)

# Initialize chat history and state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "is_listening" not in st.session_state:
    st.session_state.is_listening = False
if "voice_output" not in st.session_state:
    st.session_state.voice_output = True

# Display chat history with styling
for message in st.session_state.chat_history:
    if message["role"] == "User":
        st.markdown(f"**🧑 You:** {message['text']}")
    else:
        st.markdown(f"**🤖 Bot:** {message['text']}")

# User input
user_input = st.text_input("🧑 You:", "")

# Buttons for predefined responses
if st.button("🔄 Translate Again"):
    if user_input:
        st.session_state.chat_history.append({"role": "User", "text": user_input})
        translated_message = translator_function(user_input, from_language, to_language)
        bot_response = translated_message.text
        st.session_state.chat_history.append({"role": "Bot", "text": bot_response})
        st.write(f"**🤖 Bot:** {bot_response}")
        if st.session_state.voice_output:
            text_to_voice(bot_response, to_language)
        st.text_input("🧑 You:", "", key="new_input")

if st.button("❌ Clear Chat"):
    st.session_state.chat_history = []

if st.button("🔊 Toggle Voice Output"):
    st.session_state.voice_output = not st.session_state.voice_output
    status = "ON" if st.session_state.voice_output else "OFF"
    st.write(f"Voice output is now {status}.")

# Process user input or speech
if user_input:
    st.session_state.chat_history.append({"role": "User", "text": user_input})
    translated_message = translator_function(user_input, from_language, to_language)
    bot_response = translated_message.text
    st.session_state.chat_history.append({"role": "Bot", "text": bot_response})
    st.write(f"**🤖 Bot:** {bot_response}")
    if st.session_state.voice_output:
        text_to_voice(bot_response, to_language)
    st.text_input("🧑 You:", "", key="new_input")

# Start/Stop buttons for speech recognition
if st.button("🎙️ Start Listening"):
    st.session_state.is_listening = True

if st.button("🛑 Stop Listening"):
    st.session_state.is_listening = False

# Handle speech recognition if listening
if st.session_state.is_listening:
    recognized_text = recognize_speech(from_language)
    if recognized_text:
        st.session_state.chat_history.append({"role": "User", "text": recognized_text})
        translated_message = translator_function(recognized_text, from_language, to_language)
        bot_response = translated_message.text
        st.session_state.chat_history.append({"role": "Bot", "text": bot_response})
        st.write(f"**🤖 Bot:** {bot_response}")
        if st.session_state.voice_output:
            text_to_voice(bot_response, to_language)


# Twilio credentials
account_sid = 'ACd4583e067761300bc1848d692a6f0213'
auth_token = 'ff8710c97fc76df92b1822d45e7564a9'
twilio_number = '+16467592698'
client = Client(account_sid, auth_token)

st.title("Call Translator")

phone_number = st.text_input("Enter the phone number to call:")

if st.button("Make Call"):
    if phone_number:
        try:
            # Initiate the call
            call = client.calls.create(
                to=phone_number,
                from_=twilio_number,
                url='https://demo.twilio.com/welcome/voice/'  # URL where your Flask server is hosted
            )
            st.write(f"Call initiated. Call SID: {call.sid}")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.error("Please enter a valid phone number.")
