
class Transcript():

    def __init__(self, window_size, full=''):
        self.full = full
        self.window_size = window_size

    def get_window_bytes(self) -> bytes:
        raw = self.full.encode()
        raw = raw[len(raw)-self.window_size:len(raw)]
        # Trim the first potentially mangled sentence
        i = min(raw.find(b'.'), raw.find(b'\n'), -1)
        return raw[i+1:]

    def get_full(self):
        return self.full

    def append(self, addition: str):
        self.full += addition
