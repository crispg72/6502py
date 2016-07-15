

class Registers(object):

    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__
        
    def __init__(self):

        self.accumulator = 0
        self.x_index = 0
        self.y_index = 0
        self.sp = 0xFD
        self.pc = 0

        self.carry_flag = False
        self.zero_flag = False
        self.interrupt_disable_flag = True
        self.decimal_mode_flag = False
        self.sw_interrupt = False
        self.overflow_flag = False
        self.negative_flag = False

    def set_NZ(self, value):

        self.negative_flag = (value & 0x80)
        self.zero_flag = (value == 0)

    def status_register(self):

        bits = 1 if self.overflow_flag else 0
        bits |= 0x20 if self.decimal_mode_flag else 0
        bits |= 0x40 if self.interrupt_disable_flag else 0
        bits |= 0x10 if self.carry_flag else 0
        bits |= 0x20 if self.zero_flag else 0
        bits |= 0x40 if self.negative_flag else 0
        return bits
