import streamlit as st
import subprocess
import pywhatkit as kit
import datetime
import wikipedia
import pyjokes
import webbrowser
import speech_recognition as sr
import threading
from gtts import gTTS
import os
import playsound

# Function to convert text to speech
def speak(text):
    if not text.strip():
        return
    try:
        tts = gTTS(text=text, lang='en')
        filename = "response.mp3"
        tts.save(filename)
        playsound.playsound(filename)
        os.remove(filename)
    except Exception as e:
        st.error(f"Speech error: {e}")

# Greeting based on time
def wish_me():
    hour = datetime.datetime.now().hour
    if hour < 12:
        return "Good morning!"
    elif 12 <= hour < 18:
        return "Good afternoon!"
    else:
        return "Good evening!"

# Listen to user speech
def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening... Speak now!")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio).lower()
            return command
        except sr.UnknownValueError:
            return "Sorry, I could not understand. Please try again."
        except sr.RequestError:
            return "Could not request results. Please check your internet connection."

# Open a system application
def open_application(command):
    apps = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "whatsapp": "C:\\Program Files\\Google\\Chrome\\Application\\whatsapp.exe",
        "word": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
        "excel": "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE",
        "powerpoint": "C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE"
    }

    for app in apps:
        if app in command:
            speak(f"Opening {app}")
            subprocess.Popen(apps[app])
            return f"Opening {app}"
    return "Sorry, I don't have that application in my list."

# Main logic to execute command
def execute_command(command):
    response = ""

    if 'hello' in command or 'hi' in command:
        response = "Hello! How can I help you today?"

    elif 'wikipedia' in command:
        query = command.replace("wikipedia", "").strip()
        try:
            result = wikipedia.summary(query, sentences=2)
            response = result
        except wikipedia.exceptions.DisambiguationError:
            response = "There are multiple results. Please be more specific."
        except wikipedia.exceptions.PageError:
            response = "I couldn't find anything on Wikipedia."

    elif 'joke' in command:
        response = pyjokes.get_joke()

    elif 'time' in command:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        response = f"The current time is {current_time}"

    elif 'date' in command:
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        response = f"Today's date is {current_date}"

    elif 'open' in command:
        response = open_application(command)

    elif 'youtube' in command:
        webbrowser.open("https://www.youtube.com")
        response = "Opening YouTube..."

    elif 'gmail' in command:
        webbrowser.open("https://www.gmail.com")
        response = "Opening Gmail..."

    elif 'whatsapp' in command:
        webbrowser.open("https://web.whatsapp.com")
        response = "Opening WhatsApp..."

    elif 'play' in command:
        song = command.replace("play", "").strip()
        if song:
            response = f"Playing {song} on YouTube..."
            threading.Thread(target=lambda: kit.playonyt(song), daemon=True).start()
        else:
            response = "Please say the song name."

    elif 'search' in command or 'google' in command:
        query = command.replace("search", "").replace("google", "").strip()
        if query:
            response = f"Searching Google for {query}..."
            threading.Thread(target=lambda: kit.search(query), daemon=True).start()
        else:
            response = "Please specify what to search for."

    elif 'exit' in command or 'quit' in command:
        response = "Goodbye!"
        speak(response)
        st.stop()

    return response

# Optional: Listen for "hey assistant"
def listen_for_activation():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Waiting for activation phrase: 'Hey assistant'")
        recognizer.adjust_for_ambient_noise(source)
        while True:
            try:
                audio = recognizer.listen(source, timeout=None)
                command = recognizer.recognize_google(audio).lower()
                if "hey assistant" in command:
                    speak("Yes, I am listening.")
                    return True
            except sr.UnknownValueError:
                continue
            except sr.RequestError:
                st.error("Could not connect to the recognition service.")
                return False

# Streamlit UI
def main():
    st.title(" Voice Assistant with Streamlit")
    st.write(wish_me())
    st.write("Click the button below and speak your command:")

    if st.button(" Start Listening"):
        activated = True  # Change to listen_for_activation() if you want wake-word
        if activated:
            command = listen_command()
            if command:
                st.write(f" You said: *{command}*")
                response = execute_command(command)
                st.write(f" Response: *{response}*")
                speak(response)

if _name_ == "_main_":
    main()
