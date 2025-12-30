import speech_recognition as sr
import pyttsx3
import datetime
import calendar
import wikipedia
import pywhatkit
import webbrowser
import os
import pyjokes
import time

# ----------------- TTS FUNCTION -----------------
def speak(text):
    print("🤖 Jarvis:", text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 140)
    engine.setProperty('volume', 1.0)
    engine.say(text)
    engine.runAndWait()
    time.sleep(0.3)

# ----------------- SPEECH INPUT -----------------
def take_command():
    r = sr.Recognizer()

    # 🔧 TUNING FOR FULL SENTENCE LISTENING
    r.pause_threshold = 1.2 # allow pauses while speaking
    r.non_speaking_duration = 0.5
    r.energy_threshold = 300         # stable energy level
    r.dynamic_energy_threshold = True

    with sr.Microphone() as source:
        try:
            print("🎤 Listening...")
            
            # better mic calibration
            r.adjust_for_ambient_noise(source, duration=1)

            audio = r.listen(
                source,
                timeout=8,              # wait longer for speech to start
                phrase_time_limit=15    # allow longer sentences
            )

            query = r.recognize_google(audio, language='en-in')
            query = query.lower().strip()
            print("🗣 You said:", query)
            return query
        except (sr.WaitTimeoutError, sr.UnknownValueError):
            return ""
        
        except sr.RequestError:
            speak("Speech service is not available.")
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
        elif 'calculator' in query:
            speak("Opening Calculator")
            os.system("calc")
        else:
            speak("Application not found")
    except:
        speak("Unable to open application")

# ----------------- CALENDAR -----------------
def show_calendar():
    speak("Please say the year and month")
    date_query = take_command()
    numbers = [int(s) for s in date_query.split() if s.isdigit()]
    if len(numbers) >= 2:
        year, month = numbers[0], numbers[1]
        if 1 <= month <= 12:
            print(calendar.month(year, month))
            speak(f"Here is the calendar for {month} {year}")
        else:
            speak("Invalid month")
    else:
        speak("Could not understand")


def get_phone_number():
    speak("Please say the phone number")

    number_text = take_command()
    if not number_text:
        speak("I did not hear the number")
        return None

    digit_map = {
        "zero": "0", "one": "1", "two": "2", "three": "3",
        "four": "4", "five": "5", "six": "6",
        "seven": "7", "eight": "8", "nine": "9"
    }

    phone_number = ""

    for word in number_text.split():
        # if spoken as digit (91933)
        if word.isdigit():
            phone_number += word
        # if spoken as word (nine)
        elif word in digit_map:
            phone_number += digit_map[word]

    # remove spaces just in case                                           # just need to connect whatsapp
    
    phone_number = phone_number.replace(" ", "")

    # basic validation
    if len(phone_number) < 12:
        speak("The number seems incorrect. Please try again.")
        return None

    speak(f"I understood the number as {phone_number}")
    return "+" + phone_number



# ----------------- WHATSAPP MESSAGE -----------------
def send_whatsapp_message():
    phone = get_phone_number()
    if phone is None:
        return

    speak("Please speak the message")
    message = take_command()

    if not message:
        speak("I did not hear the message")
        return

    speak("Sending your WhatsApp message")

    try:
        pywhatkit.sendwhatmsg_instantly(
            phone,
            message,
            wait_time=15,
            tab_close=True
        )
        speak("Message sent successfully")
    except Exception as e:
        speak("There was an error sending the message")
        print(e)
        
def calculate(query):
    try:
        for a, b in [
            ("what is",""), ("calculate",""),
            ("plus","+"), ("minus","-"),
            ("x","*"), ("into","*"),
            ("multiplied by","*"), ("multiply","*"),
            ("divided by","/"), ("divide","/")
        ]:
            query = query.replace(a, b)

        query = "".join(c for c in query if c in "0123456789+-*/. ")

        speak(f"The result is {eval(query)}") 
        

    except:
        speak("Sorry, I could not calculate that.")


# ----------------- MAIN JARVIS -----------------
def jarvis():
    speak("Hello Jeet. How can I help you?")

    while True:
        query = take_command()
        if query == "":
            continue

        if 'wikipedia' in query:
            speak("Searching Wikipedia")
            query = query.replace("wikipedia", "")
            try:
                speak(wikipedia.summary(query, sentences=2))
            except:
                speak("No results found")

        elif 'date' in query:
            today = datetime.datetime.now()
            speak(today.strftime("Today's date is %A %d %B %Y"))

        elif 'calendar' in query:
            show_calendar()

        elif query.startswith("play"):
            song = query.replace("play", "")
            speak(f"Playing {song}")
            pywhatkit.playonyt(song)

        elif 'open youtube' in query:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        elif 'open google' in query:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")

        elif 'time' in query:
            speak(datetime.datetime.now().strftime("The time is %H %M"))

        elif 'open' in query:
            open_app(query)

        elif 'joke' in query:
            speak(pyjokes.get_joke())
            
        elif 'calculate' in query:
            calculate(query)
            
        elif 'whatsapp' in query or 'send message' in query:
            send_whatsapp_message()

        elif 'bye' in query or 'shut yourself' in query or 'stop' in query or 'quit' in query:
            speak("Goodbye Jeet")
            break
        

        else:
            speak("Searching on Google")
            pywhatkit.search(query)

# ----------------- RUN -----------------
if __name__ == "__main__":
    jarvis()
