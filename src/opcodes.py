from addressing_modes import AddressingModes


def nop(registers, operand, memory_controller):
    pass

def tax(registers, operand, memory_controller):
    registers.x_index = registers.accumulator
    registers.set_NZ(registers.x_index)

def tay(registers, operand, memory_controller):
    registers.y_index = registers.accumulator
    registers.set_NZ(registers.y_index)

def txa(registers, operand, memory_controller):
    registers.accumulator = registers.x_index
    registers.set_NZ(registers.accumulator)

def tya(registers, operand, memory_controller):
    registers.accumulator = registers.y_index
    registers.set_NZ(registers.accumulator)

def tsx(registers, operand, memory_controller):
    registers.x_index = registers.sp
    registers.set_NZ(registers.x_index)

def txs(registers, operand, memory_controller):
    registers.sp = registers.x_index
    registers.set_NZ(registers.sp)

def inx(registers, operand, memory_controller):
    registers.x_index += 1
    if registers.x_index > 255:
        registers.x_index = 0

    registers.set_NZ(registers.x_index)

def iny(registers, operand, memory_controller):
    registers.y_index += 1
    if registers.y_index > 255:
        registers.y_index = 0

    registers.set_NZ(registers.y_index) 

def dex(registers, operand, memory_controller):
    registers.x_index -= 1
    if registers.x_index < 0:
        registers.x_index = 255

    registers.set_NZ(registers.x_index)

def dey(registers, operand, memory_controller):
    registers.y_index -= 1
    if registers.y_index < 0:
        registers.y_index = 255

    registers.set_NZ(registers.y_index) 

def lda(registers, operand, memory_controller):
    registers.accumulator = operand
    registers.set_NZ(registers.accumulator) 

def ldaix(registers, operand, memory_controller):
    registers.accumulator = memory_controller.read(operand)
    registers.set_NZ(registers.accumulator) 

def ldaa(registers, operand, memory_controller):
    registers.accumulator = memory_controller.read(operand)
    registers.set_NZ(registers.accumulator) 

# ldx absolute Y
def ldxa(registers, operand, memory_controller):
    registers.x_index = memory_controller.read(operand)
    registers.set_NZ(registers.x_index) 

# ldy absolute X
def ldya(registers, operand, memory_controller):
    registers.y_index = memory_controller.read(operand)
    registers.set_NZ(registers.y_index) 

def ldx(registers, operand, memory_controller):
    registers.x_index = operand
    registers.set_NZ(registers.x_index) 

def ldy(registers, operand, memory_controller):
    registers.y_index = operand
    registers.set_NZ(registers.y_index) 

#################################################################################
# JUMPS & BRANCHES

def jmp(registers, operand, memory_controller):
    registers.pc = operand

def take_branch(registers, operand):

    AddressingModes.cycle_count += 1

    if operand > 127:
        operand = operand - 256

    old_pc = registers.pc
    registers.pc += operand

    if (old_pc & 0xff00) != (registers.pc & 0xff00):
        AddressingModes.cycle_count += 1

def bpl(registers, operand, memory_controller):
    if registers.negative_flag:
        return

    take_branch(registers, operand)

def bmi(registers, operand, memory_controller):
    if not registers.negative_flag:
        return

    take_branch(registers, operand)

def bvc(registers, operand, memory_controller):
    if registers.overflow_flag:
        return

    take_branch(registers, operand)

def bvs(registers, operand, memory_controller):
    if not registers.overflow_flag:
        return

    take_branch(registers, operand)

def bcc(registers, operand, memory_controller):
    if registers.carry_flag:
        return

    take_branch(registers, operand)

def bcs(registers, operand, memory_controller):
    if not registers.carry_flag:
        return

    take_branch(registers, operand)

def bne(registers, operand, memory_controller):
    if registers.zero_flag:
        return

    take_branch(registers, operand)

def beq(registers, operand, memory_controller):
    if not registers.zero_flag:
        return

    take_branch(registers, operand)

#################################################################################
# PROCESSOR STATUS FLAGS

def clc(registers, operand, memory_controller):
    registers.carry_flag = False

def sec(registers, operand, memory_controller):
    registers.carry_flag = True

def cli(registers, operand, memory_controller):
    registers.interrupt_disable_flag = False

def sei(registers, operand, memory_controller):
    registers.interrupt_disable_flag = True

def clv(registers, operand, memory_controller):
    registers.overflow_flag = False

def cld(registers, operand, memory_controller):
    registers.decimal_mode_flag = False

def sed(registers, operand, memory_controller):
    registers.decimal_mode_flag = True


class OpCode(object):

    opcode_table = [
        #|  0 |  1   |  2   |  3   |  4   |  5   |  6   |  7   |  8   |  9   |  A   |  B   |  C   |  D   |  E   |  F   |
        ["brk", "ora", "nop", "slo", "nop", "ora", "asl", "slo", "php", "ora", "asl", "nop", "nop", "ora", "asl", "slo"],  # 0
        ["bpl", "ora", "nop", "slo", "nop", "ora", "asl", "slo", "clc", "ora", "nop", "slo", "nop", "ora", "asl", "slo"],  # 1
        ["jsr", "and", "nop", "rla", "bit", "and", "rol", "rla", "plp", "and", "rol", "nop", "bit", "and", "rol", "rla"],  # 2
        ["bmi", "and", "nop", "rla", "nop", "and", "rol", "rla", "sec", "and", "nop", "rla", "nop", "and", "rol", "rla"],  # 3
        ["rti", "eor", "nop", "sre", "nop", "eor", "lsr", "sre", "pha", "eor", "lsr", "nop", "jmp", "eor", "lsr", "sre"],  # 4
        ["bvc", "eor", "nop", "sre", "nop", "eor", "lsr", "sre", "cli", "eor", "nop", "sre", "nop", "eor", "lsr", "sre"],  # 5
        ["rts", "adc", "nop", "rra", "nop", "adc", "ror", "rra", "pla", "adc", "ror", "nop", "jmp", "adc", "ror", "rra"],  # 6
        ["bvs", "adc", "nop", "rra", "nop", "adc", "ror", "rra", "sei", "adc", "nop", "rra", "nop", "adc", "ror", "rra"],  # 7
        ["nop", "sta", "nop", "sax", "sty", "sta", "stx", "sax", "dey", "nop", "txa", "nop", "sty", "sta", "stx", "sax"],  # 8
        ["bcc", "sta", "nop", "nop", "sty", "sta", "stx", "sax", "tya", "sta", "txs", "nop", "nop", "sta", "nop", "nop"],  # 9
        ["ldy", "ldaix", "ldx", "lax", "ldy", "lda", "ldx", "lax", "tay", "lda", "tax", "nop", "ldy", "lda", "ldx", "lax"],  # A
        ["bcs", "ldaa", "nop", "lax", "ldy", "lda", "ldx", "lax", "clv", "ldaa", "tsx", "lax", "ldya", "ldaa", "ldxa", "lax"],  # B
        ["cpy", "cmp", "nop", "dcp", "cpy", "cmp", "dec", "dcp", "iny", "cmp", "dex", "nop", "cpy", "cmp", "dec", "dcp"],  # C
        ["bne", "cmp", "nop", "dcp", "nop", "cmp", "dec", "dcp", "cld", "cmp", "nop", "dcp", "nop", "cmp", "dec", "dcp"],  # D
        ["cpx", "sbc", "nop", "isb", "cpx", "sbc", "inc", "isb", "inx", "sbc", "nop", "sbc", "cpx", "sbc", "inc", "isb"],  # E
        ["beq", "sbc", "nop", "isb", "nop", "sbc", "inc", "isb", "sed", "sbc", "nop", "isb", "nop", "sbc", "inc", "isb"]]  # F

    cycle_counts = [
        #|  0  |  1  |  2  |  3  |  4  |  5  |  6  |  7  |  8  |  9  |  A  |  B  |  C  |  D  |  E  |  F  |
           [7,    6,    2,    8,    3,    3,    5,    5,    3,    2,    2,    2,    4,    4,    6,    6],  # 0
           [2,    5,    2,    8,    4,    4,    6,    6,    2,    4,    2,    7,    4,    4,    7,    7],  # 1
           [6,    6,    2,    8,    3,    3,    5,    5,    4,    2,    2,    2,    4,    4,    6,    6],  # 2
           [2,    5,    2,    8,    4,    4,    6,    6,    2,    4,    2,    7,    4,    4,    7,    7],  # 3
           [6,    6,    2,    8,    3,    3,    5,    5,    3,    2,    2,    2,    3,    4,    6,    6],  # 4
           [2,    5,    2,    8,    4,    4,    6,    6,    2,    4,    2,    7,    4,    4,    7,    7],  # 5
           [6,    6,    2,    8,    3,    3,    5,    5,    4,    2,    2,    2,    5,    4,    6,    6],  # 6
           [2,    5,    2,    8,    4,    4,    6,    6,    2,    4,    2,    7,    4,    4,    7,    7],  # 7
           [2,    6,    2,    6,    3,    3,    3,    3,    2,    2,    2,    2,    4,    4,    4,    4],  # 8
           [2,    6,    2,    6,    4,    4,    4,    4,    2,    5,    2,    5,    5,    5,    5,    5],  # 9
           [2,    6,    2,    6,    3,    3,    3,    3,    2,    2,    2,    2,    4,    4,    4,    4],  # A
           [2,    5,    2,    5,    4,    4,    4,    4,    2,    4,    2,    4,    4,    4,    4,    4],  # B
           [2,    6,    2,    8,    3,    3,    5,    5,    2,    2,    2,    2,    4,    4,    6,    6],  # C
           [2,    5,    2,    8,    4,    4,    6,    6,    2,    4,    2,    7,    4,    4,    7,    7],  # D
           [2,    6,    2,    8,    3,    3,    5,    5,    2,    2,    2,    2,    4,    4,    6,    6],  # E
           [2,    5,    2,    8,    4,    4,    6,    6,    2,    4,    2,    7,    4,    4,    7,    7]   # F
    ]

    # not strictly necessary, leaving it in for now since I may
    # store some extra information in here per instruction
    dispatch_table = {

        "nop": nop,
        "tax": tax,
        "tay": tay,
        "txa": txa,
        "tya": tya,
        "tsx": tsx,
        "txs": txs,
        "inx": inx,
        "iny": iny,
        "dex": dex,
        "dey": dey,
        "lda": lda,
        "ldaix": ldaix,
        "ldaa": ldaa,
        "ldxa": ldxa,
        "ldya": ldya,
        "ldx": ldx,
        "ldy": ldy,
        "bpl": bpl,
        "bmi": bmi,
        "bvc": bvc,
        "bvs": bvs,
        "bcc": bcc,
        "bcs": bcs,
        "bne": bne,
        "beq": beq,
        "clc": clc,
        "sec": sec,
        "cli": cli,
        "sei": sei,
        "clv": clv,
        "cld": cld,
        "sed": sed,
        "jmp": jmp
    }

    def __init__(self):
        pass

    @staticmethod
    def execute(opcode, registers, memory_controller):

        low_nibble = opcode & 0xf
        high_nibble = (opcode & 0xf0) >> 4

        AddressingModes.cycle_count = OpCode.cycle_counts[high_nibble][low_nibble]

        operand = AddressingModes.handle(opcode, registers, memory_controller)
        OpCode.dispatch_table[OpCode.opcode_table[high_nibble][low_nibble]](registers, operand, memory_controller)
        return AddressingModes.cycle_count
