import time
import cite_transcript_model

def answer_questions(transcript, shutdown, questions, threshold=0.1, updates=15):
    print("Starting answer thread!")
    while not shutdown.is_set():
        time.sleep(updates)
        for q in questions:
            if(questions[q].get_answer()==None):
                questions[q].answer = cite_transcript_model.cite_transcript(transcript.get_full(),questions[q].get_data())
    print("ending answer thread")
