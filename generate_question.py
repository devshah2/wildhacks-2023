import tai3_5
import question
import cite_transcript_model
import time
import uuid as pyuuid

def update_questions(transcript, shutdown, questions, config):
    print("Starting generation thread!")
    while not shutdown.is_set():
        time.sleep(config.get_generation_speed())
        generated = tai3_5.get_questions(transcript.get_window_bytes().decode(),config.get_get_class_lvl(),config.get_temperature())
        print(generated)
        if(generated!=""):
            answer = cite_transcript_model.cite_transcript(transcript.get_full(),generated)
            print(answer)
            uuid=pyuuid.uuid4()
            questions[uuid]=question.Question(uuid,generated,0,answer)
    print("ending generation thread")
        