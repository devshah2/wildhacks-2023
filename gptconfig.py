import threading

class GPTconfig():

    def __init__(self, temperature, class_lvl, generation_speed):
        self.temperature = temperature
        self.class_lvl = class_lvl
        self.generation_speed = generation_speed
        self.mut = threading.Lock()

    def get_temperature(self):
        self.mut.acquire()
        temperature = self.temperature
        self.mut.release()
        return temperature
    
    def get_class_lvl(self):
        self.mut.acquire()
        class_lvl = self.class_lvl
        self.mut.release()
        return class_lvl
    
    def get_generation_speed(self):
        self.mut.acquire()
        generation_speed = self.generation_speed
        self.mut.release()
        return generation_speed
    
    def set_temperature(self, temperature):
        self.mut.acquire()
        self.temperature = temperature
        self.mut.release()

    def set_class_lvl(self, class_lvl):
        self.mut.acquire()
        self.class_lvl = class_lvl
        self.mut.release()
    
    def set_generation_speed(self, generation_speed):
        self.mut.acquire()
        self.generation_speed = generation_speed
        self.mut.release()
    
