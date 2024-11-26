import speech_recognition as sr
import pyttsx3
import random
import subprocess
import os
import pyautogui as pg
import webbrowser
import requests
import time
from pywinauto import Application, Desktop
import wikipedia
from hugchat import hugchat
from Face_Recognition.recoganize import AuthenticateFace

engine = pyttsx3.init('sapi5')

voices= engine.getProperty('voices')

engine.setProperty('voice', voices[0].id)

engine.setProperty('rate', 160)

driver = webbrowser.Chrome("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")

def speak(audio):
    print(audio)
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    
    while True:
        with sr.Microphone() as source:
            r.pause_threshold = 1
            print("Listening...")
            audio = r.listen(source)
            
            try:
                query = r.recognize_google(audio, language="en-in")
                print(f"user: {query}")
                return query 
            
            except sr.UnknownValueError:
                speak("Could not understand voice")
            
            except sr.RequestError:
                print("Could not request results; check your internet connection")
                speak("Could not request results; check your internet connection")

def wishMe():
    speak("Powering up Raqi...")
    speak("Establishing a secure internet connection...")
    speak("Setting up all necessary systems...")
    speak("Raqi is now online and Ready for action.")

def openApp(app_name):
    app_name = app_name.replace("start","")
    pg.hotkey('win')
    time.sleep(2)
    pg.typewrite(app_name)
    pg.hotkey('enter')

def closeApplication(app_name):
    app_name = app_name.replace("close", "").strip()

    try:
        result = subprocess.check_output("tasklist", shell=True).decode()
        print(result)       
        if app_name.lower() in result.lower():
            os.system(f"taskkill /f /im {app_name}.exe")
            speak(f"{app_name} has been closed.")
        else:
            speak(f"{app_name} is not currently running.")
    except Exception as e:
        speak("An error occurred:", e)

def searchGoogle():
    speak("sir, what do you want to search?")
    command = takeCommand().lower()  
    if "no" in command or "nothing" in command or "open" in command:
        driver.open_new("")
    else:
        speak("Opening Google...")
        search_query = command.replace(" ", "+")
        url = f"https://www.google.com/search?q={search_query}"
        driver.open(url)

def searchYoutube():
    speak("sure sir, what do you want to watch?")
    command = takeCommand()
    if "no" in command or "nothing" in command or "open" in command:
        driver.open("youtube.com")
    else:
        video = "https://www.youtube.com/results?search_query=" + command
        driver.open(video)
        speak("On your command")

def locate(command):
    wordsToRemove = ["find", "where is", "the", "location", "locate"]
    for word in wordsToRemove:
        command = command.replace(word, "")
    command = command.strip()
    driver.open("https://www.google.com/maps/place/"+command)
    speak("Found!")

def myLocation():
    speak("wait sir, let me check")
    try:
        ipAdd = requests.get('https://api.ipify.org').text
        print(ipAdd)
        url = 'https://get.geojs.io/v1/ip/geo/'+ipAdd+'.json'
        geo_requests = requests.get(url)
        geo_data = geo_requests.json()
        city = geo_data['city']
        country = geo_data['country']
        speak(f"sir! we are in {city} of country {country}")
    except Exception as e:
        speak("sir! Due to network issue, i am not able to find, where we are")
        pass

def switchToApp(app_name):
    app_name = app_name.replace('switch to', '').strip()
    windows = Desktop(backend="uia").windows()
    for window in windows:
        if app_name.lower() in window.window_text().lower():
            window.set_focus()
            return
    
    speak(f"No window with the name '{app_name}' found.")

def database(command):
    wordsToRemove = ['tell me about']
    for word in wordsToRemove:
        command = command.replace(word, "")
    command = command.strip()
    try :
        results = wikipedia.summary(command, sentences=5)
        speak(f"I found something: {results}")
    except StopIteration:
        speak(f"Your query '{command}' does not match any data in my database.")
        speak("Try asking something else.")
        speak("Sorry for the inconvenience.")

def save():
    pg.keyDown('ctrl')
    pg.hotkey('s')
    pg.keyUp('ctrl')
    pg.hotkey('enter')
    speak('saved')

def copy():
    pg.keyDown('ctrl')
    pg.hotkey('c')
    pg.keyUp('ctrl')
    speak('copied')

def copyAll():
    pg.keyDown('ctrl')
    pg.hotkey('a')
    pg.hotkey('c')
    pg.keyUp('ctrl')
    speak("Copied")

def paste():
    pg.keyDown('ctrl')
    pg.hotkey('v')
    pg.keyUp('ctrl')
    speak('pasted')

def newTab():
    pg.keyDown('ctrl')
    pg.hotkey('t')
    pg.keyUp('ctrl')

def write():
    speak("sir, what do i have to write?")
    write = takeCommand()
    if 'no' in write or 'nothing' in write:
        pg.hotkey('fn')
    else:
        pg.write(write)

def closeTab():
    pg.keyDown('ctrl')
    pg.hotkey('w')
    pg.keyUp('ctrl')

def chatBot(command):
    chatbot = hugchat.ChatBot(cookie_path="cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response =  chatbot.chat(command)
    return response