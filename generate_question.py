import tai3_5
import question
import cite_transcript_model

def update_questions(transcript, questions, temperature, class_lvl):
    generated = tai3_5.get_questions(transcript.get_window_bytes().decode(),class_lvl,temperature)
    print(generated)
    if(generated!=""):
        answer = cite_transcript_model.cite_transcript(transcript.get_full(),generated)
        print(answer)
        questions.append(question.Question(generated,0,answer))
    