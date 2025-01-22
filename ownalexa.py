import os
import streamlit as st
import pyttsx3
import datetime
import wikipedia
import pyjokes
import webbrowser
import speech_recognition as sr
import threading

# Disable pyautogui if you're using pywhatkit in a headless environment
os.environ["DISPLAY"] = ":0"  # Set DISPLAY if you're in a GUI environment

import pywhatkit as kit  # Only import this if you're certain you're not hitting pyautogui dependencies

# Your previous code follows...


# Initialize the text-to-speech engine
engine = None

def init_engine():
    global engine
    try:
        engine = pyttsx3.init()
        # Set properties for voice
        engine.setProperty('rate', 150)  # Speed of speech
        engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)
    except Exception as e:
        st.error(f"Error initializing pyttsx3 engine: {e}")

def speak(text):
    """Function to convert text to speech"""
    if engine:
        # Use threading to run speech in a background thread
        def run_speech():
            engine.say(text)
            engine.runAndWait()

        # Start the speech thread
        thread = threading.Thread(target=run_speech)
        thread.daemon = True  # Allow the thread to exit when the main program ends
        thread.start()
    else:
        st.write("Speech engine is not initialized.")

def listen():
    """Function to listen for a command"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjusts for ambient noise
        audio = recognizer.listen(source)

    try:
        st.write("Recognizing...")
        command = recognizer.recognize_google(audio).lower()  # Recognize speech and convert it to text
        st.write(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        st.error("Sorry, I did not understand that.")
        return None
    except sr.RequestError:
        st.error("Sorry, my speech service is down.")
        return None

def wish_me():
    """Function to greet the user based on the time of day"""
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")

def execute_command(command):
    """Function to execute commands based on user input"""
    if 'hello' in command or 'hi' in command:
        speak("Hello! How can I help you today?")
        return "Hello! How can I help you today?"

    elif 'wikipedia' in command:
        speak("Searching Wikipedia...")
        command = command.replace("wikipedia", "")
        result = wikipedia.summary(command, sentences=2)
        speak(result)
        return result

    elif 'joke' in command:
        joke = pyjokes.get_joke()
        speak(joke)
        return joke

    elif 'time' in command:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The current time is {current_time}")
        return f"The current time is {current_time}"

    elif 'date' in command:
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {current_date}")
        return f"Today's date is {current_date}"

    elif 'open youtube' in command:
        speak("Opening YouTube...")
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube..."

    elif 'open gmail' in command:
        speak("Opening gmail...")
        webbrowser.open("https://www.gmail.com")
        return "Opening Gmail..."

    elif 'play' in command and 'song' in command:
        song = command.replace("play", "").replace("song", "").strip()
        speak(f"Playing {song} for you on YouTube...")
        kit.playonyt(song)
        return f"Playing {song} for you on YouTube..."

    elif 'search' in command or 'google' in command:
        query = command.replace("search", "").replace("google", "").strip()
        if query:
            speak(f"Searching Google for {query}...")
            kit.search(query)
            return f"Searching Google for {query}..."
        else:
            speak("Please specify what you want to search for.")
            return "Please specify what you want to search for."

    elif 'quit' in command or 'exit' in command:
        speak("Goodbye!")
        return "Goodbye!"

def main():
    """Main function to run the assistant in Streamlit"""
    init_engine()  # Initialize the TTS engine
    wish_me()
    speak("I am ready to assist you.")
    
    st.title("Voice Assistant with Streamlit")
    st.write("Click the button below to give a voice command:")

    if st.button("Start Listening"):
        command = listen()  # Listen for a command
        if command:
            response = execute_command(command)  # Execute the command if it's recognized
            st.write(f"Response: {response}")

if __name__ == "__main__":
    main()
