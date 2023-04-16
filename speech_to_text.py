from re import RegexFlag
import speech_recognition as sr
import threading

recognizer = sr.Recognizer()

recognizer_queue = []
recognizer_queue_lock = threading.Lock()
recognizer_queue_sem = threading.Semaphore(0)

def audio_listener_callback(self, audio):
    print("audio callback begin")
    recognizer_queue.append(audio)
    recognizer_queue_sem.release()
    print("audio callback end")

def speech_recog_thread(transcript, shutdown): 
    print("Starting speech_recog thread!")
    recognizer.listen
    source = sr.Microphone()
    end_listener = recognizer.listen_in_background(source,callback=audio_listener_callback,phrase_time_limit=60)
    while not shutdown.is_set():
        try:
            print("Waiting on audio queue semaphore")
            recognizer_queue_sem.acquire()
            print("Consumer acquired!")
            audio = recognizer_queue.pop(0)
            text = recognizer.recognize_google(audio)
            transcript.append(text + '. ')
            print(transcript.get_full())
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that. Could you please repeat?")
        except sr.RequestError:
            print("Sorry, I'm having trouble with the speech recognition service.")
            break
    print("ending speech recog listener")
    end_listener(False)
    print("ended speech recog listener")
    # I know I never close the mic but the program is ending and "listen_in_background" is complaining about the context manager
