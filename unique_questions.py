from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# rearrange by answer exists
# always remove current one

def safe_remove(questions, uuid1, uuid2):
    uuid = uuid1 if questions[uuid2].get_answer()!=None else uuid2
    if(uuid==uuid2 and questions[uuid1].get_answer()==None):
        uuid = uuid1 if questions[uuid1].get_votes()<=questions[uuid2].get_votes() else uuid2
    if uuid in questions:
        del questions[uuid]

def find_unique(questions):
    # given a dict of questions, modify it
    # questions: dict[str]
    # returns: None
    questionTexts = [questions[x].get_data() for x in questions]
    uuids = [x for x in questions]
    
    embeddings = [model.encode(x) for x in questionTexts]

    for i in range(len(questions)):
        for j in range(i+1,len(questions)):
            if(util.pytorch_cos_sim(embeddings[i],embeddings[j])>0.9):
                print("removing duplicate")
                print(questions[uuids[i]].get_data())
                print(questions[uuids[j]].get_data())
                safe_remove(questions,uuids[i],uuids[j])
            