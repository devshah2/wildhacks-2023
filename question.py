
class Question:

    def __init__(self, data, votes = 0, answer = None):
        self.data = data
        self.votes = votes
        self.answer = answer

    def get_data(self):
        return self.data
    def get_votes(self):
        return self.votes
    def get_answer(self):
        return self.answer
