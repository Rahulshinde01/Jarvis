import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os

#pip install pocketsphinx

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newapi = "e9ad31852d81488081eabe71e3577042"

def speak_old(text):
    engine.say(text)
    engine.runAndWait()


def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3') 

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 
    

def aiProcess(command):
    client = OpenAI(api_key="OPENAI_API_KEY",
    )

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
        {"role": "user", "content": command}
    ]
    )
    return completion.choices[0].message.content



def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():
        engine.setProperty('rate', 150) 

        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newapi}"
        response = requests.get(url)
        
        if response.status_code == 200:
            
            news_data = response.json()
            
            articles = news_data.get("articles", [])
           
            for i, article in enumerate(articles[:5], start=1):  # Fetch top 5 headlines
                headline = article["title"]
                speak(f"News {i}: {headline}")

        else:
            speak("sorry, Failed to fetch news")

    else: 
        # Let OpenAI handle the request
        output = aiProcess(c)
        speak(output) 
            

if __name__ == "__main__":
    speak("Initializing Jarvis.....")

    while True:
        # Listen for the wake work "Jarvis"
        # obtain audio from the microphone
        r = sr.Recognizer()
       

        # recognize speech using Sphinx
        print("recognizing..")
        try:
            with sr.Microphone() as source:
                print("Listening")
                audio = r.listen(source, timeout = 3, phrase_time_limit = 2)
            word =  r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("ya give me command")
                with sr.Microphone() as source:
                    print("Jarvis activate")
                    audio = r.listen(source)
                    command =  r.recognize_google(audio)
                    processCommand(command)

        except Exception as e:
            print("error; {0}".format(e))


