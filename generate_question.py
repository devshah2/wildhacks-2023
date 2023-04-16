import tai3_5
import question
import cite_transcript_model
import time
import uuid as pyuuid

def update_questions(transcript, shutdown, questions, temperature, class_lvl, updates=30):
    print("Starting generation thread!")
    while not shutdown.is_set():
        time.sleep(updates)
        generated = tai3_5.get_questions(transcript.get_window_bytes().decode(),class_lvl,temperature)
        print(generated)
        if(generated!=""):
            answer = cite_transcript_model.cite_transcript(transcript.get_full(),generated)
            print(answer)
            uuid=pyuuid.uuid4()
            questions[uuid]=question.Question(uuid,generated,0,answer)
    print("ending generation thread")
        
def answer_questions(transcript, shutdown, questions, threshold=0.1, updates=15):
    print("Starting answer thread!")
    while not shutdown.is_set():
        time.sleep(updates)
        for q in questions:
            if(questions[q].get_answer()==None):
                questions[q].answer = cite_transcript_model.cite_transcript(transcript.get_full(),questions[q].get_data())
    print("ending answer thread")