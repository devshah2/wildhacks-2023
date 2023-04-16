
import threading

class Question:

    def __init__(self, uuid, data, votes = 0):
        self.uuid = uuid
        self.data = data
        self.votes = votes
        self.mut = threading.Lock()

    def get_data(self):
        return self.data
    def get_votes(self):
        return self.votes
    def votes_increment(self):
        self.mut.acquire()
        self.votes += 1
        self.mut.release()
    def votes_decrement(self):
        self.mut.acquire()
        self.votes -= 1
        self.mut.release()
