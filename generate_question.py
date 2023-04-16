import tai3_5
import question
import cite_transcript_model
import time

def update_questions(transcript, shutdown, questions, temperature, class_lvl, updates=30):
    print("Starting generation thread!")
    while not shutdown.is_set():
        time.sleep(updates)
        generated = tai3_5.get_questions(transcript.get_window_bytes().decode(),class_lvl,temperature)
        print(generated)
        if(generated!=""):
            answer = cite_transcript_model.cite_transcript(transcript.get_full(),generated)
            print(answer)
            questions.append(question.Question(generated,0,answer))
    print("ending generation thread")
        