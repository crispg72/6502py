from emupy6502.registers import Registers
from emupy6502.opcodes import OpCode


class Cpu6502(object):

    def __init__(self, memory_controller):

        self.registers = Registers()

        self.memory_controller = memory_controller
        self.opcodes = OpCode()
	
    def run(self, cycles):

        while cycles > 0:
            opcode = self.memory_controller.read(self.pc)
            self.registers.pc += 1            
            cycle_count = OpCode.execute(opcode, self.registers, self.memory_controller)
            cycles = cycles - cycle_count

    def run_until_signalled(self, signal):

        memory_controller = self.memory_controller
        total_cycles = 0
        while not signal():
            opcode = memory_controller.read(self.registers.pc)
            self.registers.pc += 1
            total_cycles += self.opcodes.execute(opcode, self.registers, self.memory_controller)

        return total_cycles