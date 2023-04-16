import tai3_5
import question
import cite_transcript_model

def update_questions(transcript, questions, temperature, class_lvl):
    generated = tai3_5.get_questions(class_lvl,temperature,transcript.get_window_bytes().decode())
    if(generated!=""):
        answer = cite_transcript_model.cite_transcript(transcript.get_full(),generated)
        questions.append(question(generated,0,answer))
    