import speech_recognition as sr
import sounddevice as sd
import wavio
import pyttsx3
import datetime
import wikipedia
import pywhatkit
import webbrowser
import os
import pyjokes

# Initialize TTS engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def record_audio(duration=5, fs=44100, filename="input.wav"):
    print("Listening...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait()
    wavio.write(filename, recording, fs, sampwidth=2)
    return filename

def take_command():
    filename = record_audio(duration=5)
    r = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = r.record(source)
    try:
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}")
    except:
        return "None"
    return query.lower()

def open_app(query):
    if 'chrome' in query:
        os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
    elif 'vs code' in query:
        os.startfile("C:\\Users\\Dell\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe")
    elif 'calculator' in query:
        os.system("calc")
    else:
        speak("Application not found.")

def jarvis():
    speak("Hello, I am luna. How can I help you?")
    
    while True:
        query = take_command()
        if query == "None":
            continue
        
        # Wikipedia
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            try:
                result = wikipedia.summary(query, sentences=2)
                speak(result)
            except:
                speak("Sorry, no results found.")
        
        # YouTube
        elif 'play' in query:
            song = query.replace('play', '')
            speak(f"Playing {song} on YouTube")
            pywhatkit.playonyt(song)
        
        # Open websites
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
        elif 'open google' in query:
            webbrowser.open("google.com")
        
        # Tell time
        elif 'time' in query:
            time = datetime.datetime.now().strftime('%H:%M:%S')
            speak(f"The time is {time}")
        
        # Open apps
        elif 'open' in query:
            open_app(query)
        
        # Tell jokes
        elif 'joke' in query:
            joke = pyjokes.get_joke()
            speak(joke)
        
        # Exit Jarvis
        elif 'quit' in query or 'exit' in query:
            speak("Goodbye!")
            break
        
        else:
            speak("I can search that for you on Google.")
            pywhatkit.search(query)

# Run Jarvis
jarvis()
 