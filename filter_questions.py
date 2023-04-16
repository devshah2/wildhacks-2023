import time
from unique_questions import find_unique

def erase_questions(questions, shutdown, updates=5):
    print("Starting erase thread!")
    while not shutdown.is_set():
        find_unique(questions)
        time.sleep(updates)
    print("ending erase thread")
