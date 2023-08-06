import pyttsx3
import speech_recognition as sr

speaker = pyttsx3.init('sapi5')
voices = speaker.getProperty('voices')
speaker.setProperty('voice', voices[0].id)
speaker.setProperty('volume', 1)
speaker.setProperty('rate', 145)

def voiceIn(prompt):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(f"{prompt}\nListening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(query)
    except Exception as e: 
        query = input("Please type that: ")
        print(query)
    return query

def voiceOut(text):
    speaker.say(text)
    speaker.runAndWait()

def sprint(text):
    print(text)
    speaker.say(text)
    speaker.runAndWait()

def speakOut():
    what = voiceIn('')
    voiceOut(what)