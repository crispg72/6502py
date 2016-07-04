import addressing_modes


class 6502(object):

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

            opcode = self.memory_controller.read(self.pc++)

            self.execute(opcode, self.registers, self.memory_controller)

            cycles = cycles - self.timing_table[opcode]

    def execute(self, opcode):
