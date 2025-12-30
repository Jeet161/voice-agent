import speech_recognition as sr
import pyttsx3
import datetime
import calendar
import wikipedia
import pywhatkit
import webbrowser
import os
import pyjokes

# ----------------- TTS SETUP -----------------
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)   # 0 = Male, 1 = Female
engine.setProperty('rate', 140)
engine.setProperty('volume', 1.0)

def speak(text):
    print("🤖 Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

# ----------------- SPEECH INPUT -----------------
def take_command():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("🎤 Listening...")
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, timeout=5, phrase_time_limit=5)

        query = r.recognize_google(audio, language='en-in')
        query = query.lower().strip()
        print("🗣 You said:", query)
        return query

    except sr.UnknownValueError:
        print("⚠ Could not understand audio")
        return ""

    except sr.RequestError:
        speak("Speech service is unavailable")
        return ""

    except sr.WaitTimeoutError:
        print("⚠ Listening timed out")
        return ""

# ----------------- OPEN APPLICATIONS -----------------
def open_app(query):
    try:
        if 'chrome' in query:
            speak("Opening Chrome")
            os.startfile(r"C:\Program Files\Google\Chrome\Application\chrome.exe")

        elif 'vs code' in query or 'vscode' in query:
            speak("Opening Visual Studio Code")
            os.startfile(r"C:\Users\Dell\AppData\Local\Programs\Microsoft VS Code\Code.exe")

        elif 'calculator' in query or 'calc' in query:
            speak("Opening Calculator")
            os.system("calc")

        else:
            speak("Application not found")

    except:
        speak("Unable to open the application")

# ----------------- MAIN JARVIS -----------------
def jarvis():
    speak("Hello Jeet. I am your personal assistant. How can I help you?")

    while True:
        query = take_command()

        if query == "":
            continue

        # Wikipedia
        if 'wikipedia' in query:
            speak("Searching Wikipedia")
            query = query.replace("wikipedia", "").strip()
            try:
                result = wikipedia.summary(query, sentences=2)
                speak(result)
            except:
                speak("No results found")
         
         # Date
        elif 'date' in query:
            today = datetime.datetime.now()
            speak(f"Today's date is {today.strftime('%A, %d %B %Y')}")

        # Calendar
        elif 'calendar' in query:
            try:
                speak("Which year and month do you want the calendar for?")
                speak("Please say the year")
                year_query = take_command()
                year = int(''.join(filter(str.isdigit, year_query)))  # extract digits

                speak("Please say the month number")
                month_query = take_command()
                month = int(''.join(filter(str.isdigit, month_query)))

                cal_text = calendar.month(year, month)
                print(cal_text)  # print in console
                speak(f"Here is the calendar for {month}/{year}. Check your console.")
            except:
                speak("I couldn't understand the month or year. Try again.")       
                

        # YouTube
        elif query.startswith("play"):
            song = query.replace("play", "").strip()
            speak(f"Playing {song} on YouTube")
            pywhatkit.playonyt(song)

        # Open websites
        elif 'open youtube' in query:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        elif 'open google' in query:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")

        # Time
        elif 'time' in query:
            now = datetime.datetime.now().strftime('%H:%M:%S')
            speak(f"The time is {now}")

        # Open apps
        elif 'open' in query:
            open_app(query)

        # Joke
        elif 'joke' in query:
            speak(pyjokes.get_joke())

        # Exit
        elif 'exit' in query or 'quit' in query or 'stop' in query:
            speak("Goodbye Jeet")
            break

        # Google Search
        else:
            speak("Searching on Google")
            pywhatkit.search(query)

# ----------------- RUN -----------------
jarvis()
