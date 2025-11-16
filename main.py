import speech_recognition as sr
import pyttsx3
import time
import webbrowser
import musicLibrary
import requests
from google import genai
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

GEMINI_API_KEY = os.getenv("googleapi")
NEWS_API_KEY = os.getenv("newsapi")
googleapi = GEMINI_API_KEY
newsapi = NEWS_API_KEY

recognizer = sr.Recognizer()

def first_speak(text):
    print("Friday is online")
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def speak(text):
    print("Friday Speaking")
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def processcommand(command):
    if "open google" in command.lower():
        speak("Google Access Granted")
        webbrowser.open("https://www.google.com")
    elif "open youtube" in command.lower():
        speak("Youtube Access Granted")
        webbrowser.open("https://www.youtube.com")
    elif "open linkedin" in command.lower():
        speak("Linkedin Access Granted")
        webbrowser.open("https://www.linkedin.com")
    elif "open amazon" in command.lower():
        speak("Amazon Access Granted")
        webbrowser.open("https://www.amazon.com")
    elif "open facebook" in command.lower():
        speak("Facebook Access Granted")
        webbrowser.open("https://www.facebook.com")
    elif "open instagram" in command.lower():
        speak("Instagram Access Granted")
        webbrowser.open("https://www.google.com/search?q=instagarm&rlz=1C1VDKB_enIN1187IN1187&oq=instagarm&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIRCAEQABgKGAsYgwEYsQMYgAQyEQgCEAAYChgLGIMBGLEDGIAEMhEIAxAAGAoYCxiDARixAxiABDILCAQQABgKGAsYgAQyDggFEAAYChgLGLEDGIAEMgYIBhBFGDwyBggHEAUYQNIBCDQxODhqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8")
    elif command.lower().startswith("play"):
        song=command.lower().split(" ")[1]
        link=musicLibrary.music[song]
        speak("playing track")
        webbrowser.open(link)
    elif "thank" in command.lower():
        speak("My Pleasure")
    elif "news" in command.lower():
        r=requests.get(f'https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}')
        if r.status_code==200:
            data=r.json()
            articles=data.get("articles",[])
            for article in articles:
                speak(article["title"])
        else:
            print("news not found")    
    else:
        try:
            client = genai.Client(api_key=googleapi)

            response = client.models.generate_content(model="gemini-2.5-flash",contents=command+". give small inputs",)
            speak(response.text)
        except Exception as e:
            print(e)
            speak("Unable to catch your input")
        

if __name__ == "__main__":
    first_speak("Friday is online")
    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("Listening...")
                audio = recognizer.listen(source,timeout=3,phrase_time_limit=3)
                print("Recognizing...")
            word = recognizer.recognize_google(audio)
            if "friday" in word.lower():
                speak("yes sir")
                # listen for command
                with sr.Microphone() as source:
                    print("Friday Activated...")
                    print("Listening...")
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)
                    if "stop" in command.lower():
                        speak("Deactivating Friday")
                        break
                    processcommand(command)
        except Exception as e:
            print(e)