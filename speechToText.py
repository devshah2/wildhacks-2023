import speech_recognition as sr
import threading


recognizer = sr.Recognizer()


threads=[]

def process_audio(audio):
    try:
        text = recognizer.recognize_google(audio)

        print("You said: ", text)
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Could you please repeat?")
    except sr.RequestError:
        print("Sorry, I'm having trouble with the speech recognition service.")

with sr.Microphone() as source:
    while True:
        try:
            print("Speak now...")
            audio = recognizer.listen(source,phrase_time_limit=10)
            threading.Thread(target=process_audio, args=(audio,)).start()
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that. Could you please repeat?")
        except sr.RequestError:
            print("Sorry, I'm having trouble with the speech recognition service.")
            break
