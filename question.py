
import threading

class Question:

    def __init__(self, uuid, data, votes=0):
        self.uuid = uuid
        self.data = data
        self.votes = votes
        self.mut = threading.Lock()

    def votes_increment(self):
        self.mut.acquire()
        self.votes += 1
        self.mut.release()

    def votes_decrement(self):
        self.mut.acquire()
        self.votes -= 1
        self.mut.release()
