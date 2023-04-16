import threading

class Transcript():

    def __init__(self, window_size, full=''):
        self.full = full
        self.window_size = window_size
        self.mut = threading.Lock()

    def get_window_bytes(self) -> bytes:
        self.mut.acquire()
        raw = self.full.encode()
        raw = raw[len(raw)-self.window_size:len(raw)]
        # Trim the first potentially mangled sentence
        i = min(raw.find(b'.'), raw.find(b'\n'), -1)
        self.mut.release()
        return raw[i+1:]

    def get_full(self):
        # This might be sync overkill but better safe than sorry
        self.mut.acquire()
        full = self.full
        self.mut.release()
        return full

    def append(self, addition: str):
        self.mut.acquire()
        self.full += addition
        self.mut.release()
