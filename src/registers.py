

class Registers(object):

    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__
        
    def __init__(self):

        self.accumulator = 0
        self.x_index = 0
        self.y_index = 0
        self.sp = 0xFD
        self.pc = 0
