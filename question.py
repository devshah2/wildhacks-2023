
import threading

class Question:

    def __init__(self, uuid, data, votes=0, answer=None):
        self.uuid = uuid
        self.data = data
        self.votes = votes
        self.mut = threading.Lock()
        self.answer = answer
        self.author = 'Anonymous'

    def votes_increment(self):
        self.mut.acquire()
        self.votes += 1
        self.mut.release()

    def votes_decrement(self):
        self.mut.acquire()
        self.votes -= 1
        self.mut.release()
