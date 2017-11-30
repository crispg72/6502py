from emupy6502.addressing_modes import AddressingModes

#################################################################################
# SYSTEM

def nop(registers, operand, memory_controller):
    pass

def brk(registers, operand, memory_controller):
    memory_controller.write(registers.sp, registers.pc & 0xff)
    memory_controller.write(registers.sp-1, (registers.pc >> 8) & 0xff)
    memory_controller.write(registers.sp-2, registers.status_register())

    low_address = memory_controller.read(0xfffe)
    high_address = memory_controller.read(0xffff)
    registers.pc = (high_address << 8) | low_address

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
# STORES

def sta(registers, operand, memory_controller):
    memory_controller.write(operand, registers.accumulator)

def stx(registers, operand, memory_controller):
    memory_controller.write(operand, registers.x_index)

def sty(registers, operand, memory_controller):
    memory_controller.write(operand, registers.y_index)

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

#################################################################################
# ARITHMETIC

def adc(registers, operand, memory_controller):
    result = registers.accumulator + (operand + (1 if registers.carry_flag else 0))

    registers.set_NZV(operand, result & 0xff) 
    registers.accumulator = result & 0xff
    registers.carry_flag = result > 255

def adcM(registers, operand, memory_controller):
    adc(registers, memory_controller.read(operand), memory_controller)

def sbc(registers, operand, memory_controller):
    result = registers.accumulator - (1 if not registers.carry_flag else 0) - operand

    signbits_differ = (operand ^ registers.accumulator) & 0x80
    resultsign_differs = (registers.accumulator ^ result) & 0x80

    registers.overflow_flag = resultsign_differs and signbits_differ
    registers.carry_flag = (result >= 0)
    registers.accumulator = result & 0xff
    registers.set_NZ(registers.accumulator)

def sbcM(registers, operand, memory_controller):
    sbc(registers, memory_controller.read(operand), memory_controller)

#################################################################################
# LOGICAL

def logical_and(registers, operand, memory_controller):
    registers.accumulator = registers.accumulator & operand
    registers.set_NZ(registers.accumulator)

def logical_andM(registers, operand, memory_controller):
    logical_and(registers, memory_controller.read(operand), memory_controller)

def logical_eor(registers, operand, memory_controller):
    registers.accumulator = registers.accumulator ^ operand
    registers.set_NZ(registers.accumulator)

def logical_eorM(registers, operand, memory_controller):
    logical_eor(registers, memory_controller.read(operand), memory_controller)

def logical_or(registers, operand, memory_controller):
    registers.accumulator = registers.accumulator | operand
    registers.set_NZ(registers.accumulator)

def logical_orM(registers, operand, memory_controller):
    logical_or(registers, memory_controller.read(operand), memory_controller)

#################################################################################
# BIT SHIFTS

def asl(registers, operand):
    operand = operand * 2
    registers.carry_flag = (operand & 0x100) != 0
    operand = operand & 0xff
    registers.set_NZ(operand) 
    return operand

def aslA(registers, operand, memory_controller):
    registers.accumulator = asl(registers, registers.accumulator)

def aslM(registers, operand, memory_controller):
    memory_controller.write(operand, asl(registers, memory_controller.read(operand)))

def rol(registers, operand):
    operand = operand * 2
    operand += (1 if registers.carry_flag else 0)
    registers.carry_flag = (operand & 0x100) != 0
    operand = operand & 0xff
    registers.set_NZ(operand) 
    return operand

def rolA(registers, operand, memory_controller):
    registers.accumulator = rol(registers, registers.accumulator)

def rolM(registers, operand, memory_controller):
    memory_controller.write(operand, rol(registers, memory_controller.read(operand)))

#################################################################################
# COMPARES

def set_compare_flags(registers, difference):
    registers.set_NZ(difference)
    registers.carry_flag = (difference >= 0)

def cmp(registers, operand, memory_controller):
    set_compare_flags(registers, registers.accumulator - operand)

def cpx(registers, operand, memory_controller):
    set_compare_flags(registers, registers.x_index - operand)

def cpy(registers, operand, memory_controller):
    set_compare_flags(registers, registers.y_index - operand)

#################################################################################
# INC AND DEC

def inc(registers, operand, memory_controller):
    value = memory_controller.read(operand)
    value += 1
    value = value & 0xff
    registers.set_NZ(value)
    memory_controller.write(operand, value)

def dec(registers, operand, memory_controller):
    value = memory_controller.read(operand)
    value -= 1
    value = value & 0xff
    registers.set_NZ(value)
    memory_controller.write(operand, value)

class OpCode(object):

    opcode_table = [
        #|  0 |  1   |  2   |  3   |  4   |  5   |  6   |  7   |  8   |  9   |  A   |  B   |  C   |  D   |  E   |  F   |
        ["brk", "oraM", "nop", "slo", "nop", "ora", "aslM", "slo", "php", "ora", "aslA", "nop", "nop", "ora", "aslM", "slo"],  # 0
        ["bpl", "oraM", "nop", "slo", "nop", "ora", "aslM", "slo", "clc", "oraM", "nop", "slo", "nop", "oraM", "aslM", "slo"],  # 1
        ["jsr", "andM", "nop", "rla", "bit", "and", "rolM", "rla", "plp", "and", "rolA", "nop", "bit", "and", "rolM", "rla"],  # 2
        ["bmi", "andM", "nop", "rla", "nop", "and", "rol", "rla", "sec", "andM", "nop", "rla", "nop", "andM", "rol", "rla"],  # 3
        ["rti", "eorM", "nop", "sre", "nop", "eor", "lsr", "sre", "pha", "eor", "lsr", "nop", "jmp", "eor", "lsr", "sre"],  # 4
        ["bvc", "eorM", "nop", "sre", "nop", "eor", "lsr", "sre", "cli", "eorM", "nop", "sre", "nop", "eorM", "lsr", "sre"],  # 5
        ["rts", "adcM", "nop", "rra", "nop", "adc", "ror", "rra", "pla", "adc", "ror", "nop", "jmp", "adc", "ror", "rra"],  # 6
        ["bvs", "adcM", "nop", "rra", "nop", "adc", "ror", "rra", "sei", "adcM", "nop", "rra", "nop", "adcM", "ror", "rra"],  # 7
        ["nop", "sta", "nop", "sax", "sty", "sta", "stx", "sax", "dey", "nop", "txa", "nop", "sty", "sta", "stx", "sax"],  # 8
        ["bcc", "sta", "nop", "nop", "sty", "sta", "stx", "sax", "tya", "sta", "txs", "nop", "nop", "sta", "nop", "nop"],  # 9
        ["ldy", "ldaix", "ldx", "lax", "ldy", "lda", "ldx", "lax", "tay", "lda", "tax", "nop", "ldy", "lda", "ldx", "lax"],  # A
        ["bcs", "ldaa", "nop", "lax", "ldy", "lda", "ldx", "lax", "clv", "ldaa", "tsx", "lax", "ldya", "ldaa", "ldxa", "lax"],  # B
        ["cpy", "cmp", "nop", "dcp", "cpy", "cmp", "dec", "dcp", "iny", "cmp", "dex", "nop", "cpy", "cmp", "dec", "dcp"],  # C
        ["bne", "cmp", "nop", "dcp", "nop", "cmp", "dec", "dcp", "cld", "cmp", "nop", "dcp", "nop", "cmp", "dec", "dcp"],  # D
        ["cpx", "sbcM", "nop", "isb", "cpx", "sbc", "inc", "isb", "inx", "sbc", "nop", "sbc", "cpx", "sbc", "inc", "isb"],  # E
        ["beq", "sbcM", "nop", "isb", "nop", "sbc", "inc", "isb", "sed", "sbcM", "nop", "isb", "nop", "sbcM", "inc", "isb"]]  # F

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
        "adc": adc,
        "adcM": adcM,
        "sta": sta,
        "stx": stx,
        "sty": sty,
        "aslA": aslA,
        "aslM": aslM,
        "brk": brk,
        "cmp": cmp,
        "cpx": cpx,
        "cpy": cpy,
        "rolA": rolA,
        "rolM": rolM,
        "sbc": sbc,
        "sbcM": sbcM,
        "inc": inc,
        "dec": dec,
        "and": logical_and,
        "andM": logical_andM,
        "eor": logical_eor,
        "eorM": logical_eorM,
        "ora": logical_or,
        "oraM": logical_orM,
        "jmp": jmp
    }

    def __init__(self):

        self.addressing_modes = AddressingModes()

    def execute(self, opcode, registers, memory_controller):

        addressing_modes = self.addressing_modes

        low_nibble = opcode & 0xf
        high_nibble = (opcode & 0xf0) >> 4

        AddressingModes.cycle_count = self.cycle_counts[high_nibble][low_nibble]

        operand = addressing_modes.handle(opcode, registers, memory_controller)
        self.dispatch_table[self.opcode_table[high_nibble][low_nibble]](registers, operand, memory_controller)
        return AddressingModes.cycle_count
