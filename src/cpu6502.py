from registers import Registers
from opcodes import OpCode


class Cpu6502(object):

    def __init__(self, memory_controller):

        self.registers = Registers()
        self.accumulator = 0
        self.x_index = 0
        self.y_index = 0
        self.sp = 0xFD
        self.pc = 0

        self.memory_controller = memory_controller
	
    def run(self, cycles):

        while cycles > 0:
            opcode = self.memory_controller.read(self.pc)
            self.registers.pc += 1            
            cycle_count = OpCode.execute(opcode, self.registers, self.memory_controller)
            cycles = cycles - cycle_count

    def run_until_signalled(self, signal):

        total_cycles = 0
        while not signal():
            opcode = self.memory_controller.read(self.registers.pc)
            self.registers.pc += 1
            total_cycles += OpCode.execute(opcode, self.registers, self.memory_controller)

        return total_cycles