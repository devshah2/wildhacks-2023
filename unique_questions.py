from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def find_unique(questions):
    # given a list of questions, return a list of unique questions
    # questions: list[str]
    # returns: list[str]
    
    embeddings = [model.encode(x) for x in questions]
    unique = []
    for i in range(len(questions)):
        if not any([util.pytorch_cos_sim(embeddings[i],embeddings[j])>0.9 for j in range(i)]):
            unique.append(questions[i])
    return unique
