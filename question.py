
import threading

class Question:

    def __init__(self, uuid, data, votes=0, answer=None, author="AI", is_student=False):
        self.uuid = uuid
        self.data = data
        self.votes = votes
        self.mut = threading.Lock()
        self.answer = answer
        self.author = author
        self.is_student = is_student

    def votes_increment(self):
        self.mut.acquire()
        self.votes += 1
        self.mut.release()

    def votes_decrement(self):
        self.mut.acquire()
        self.votes -= 1
        self.mut.release()

    def get_data(self):
        self.mut.acquire()
        data = self.data
        self.mut.release()
        return data
    
    def get_uuid(self):
        self.mut.acquire()
        uuid = self.uuid
        self.mut.release()
        return uuid

    def get_answer(self):
        self.mut.acquire()
        answer = self.answer
        self.mut.release()
        return answer
    
    def get_votes(self):
        self.mut.acquire()
        answer = self.votes
        self.mut.release()
        return answer
