import re
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline

model_name = "deepset/roberta-base-squad2"
nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)
model = AutoModelForQuestionAnswering.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

def cite_transcript(context,question):
    # find answer to question in context
    # context: string (transcript)
    # question: string (question)
    # returns: string (answer)

    starts=[0]+[m.start()+1 for m in re.finditer('\.', context)]+[m.start()+1 for m in re.finditer('[\r\n]+', context)]
    QA_input = {
            'question': question,
            'context': context}
    out=nlp(QA_input)
    score=out["score"]
    start=out["start"]
    end=out["end"]
    ans=out["answer"]
    #if(score<=0.1):
    #    return
    ss=max([0]+[x for x in starts if x<=start])
    ee=min([len(context)]+[x for x in starts if x>=end])
    return context[ss:ee]

import time
def send_transcript_thread(transcript, shutdown, words=10, timestep=5): 
    print("Starting send_transcript thread!")
    lecture=""
    with open("example_lecture.txt","r") as f:
        lecture=f.readlines()
    print(lecture)
    while not shutdown.is_set():
        text=lecture[:words]
        text=text[words:]
        transcript.append(text + ' ')
        print(transcript.get_full())
        time.sleep(timestep)
    print("ending send_transcript")