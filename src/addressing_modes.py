from registers import Registers


def imp(registers, memory_controller):
    # implied has no effect
    return None

def acc(registers, memory_controller):
    # accumulator has no effect
    return None

def imm(registers, memory_controller):
    value = memory_controller.read(registers.pc)
    registers.pc += 1
    return value

def rel(registers, memory_controller):
    raise NotImplementedError()

def ind(registers, memory_controller):
    raise NotImplementedError()

def indx(registers, memory_controller):
    raise NotImplementedError()

def indy(registers, memory_controller):
    raise NotImplementedError()

def zp(registers, memory_controller):
    raise NotImplementedError()

def zpx(registers, memory_controller):
    raise NotImplementedError()

def zpy(registers, memory_controller):
    raise NotImplementedError()

def abso(registers, memory_controller):
    raise NotImplementedError()

def absx(registers, memory_controller):
    raise NotImplementedError()

def absy(registers, memory_controller):
    raise NotImplementedError()

class AddressingModes(object):

    '''accumulator = 1
    immediate = 2 
    absolute = 3
    zero_page = 4
    ix_zero_page = 5
    iy_zero_page = 6
    ix_absolute = 7
    iy_absolute = 8
    implied = 9
    relative = 10
    ix_indirect = 11
    iy_indirect = 11'''

    dispatch_table = [
        #|  0  |  1  |  2  |  3  |  4  |  5  |  6  |  7  |  8  |  9  |  A  |  B  |  C  |  D  |  E  |  F  | 
         [  imp, indx,  imp, indx,   zp,   zp,   zp,   zp,  imp,  imm,  acc,  imm, abso, abso, abso, abso], # 0 
         [  rel, indy,  imp, indy,  zpx,  zpx,  zpx,  zpx,  imp, absy,  imp, absy, absx, absx, absx, absx], # 1 
         [ abso, indx,  imp, indx,   zp,   zp,   zp,   zp,  imp,  imm,  acc,  imm, abso, abso, abso, abso], # 2 
         [  rel, indy,  imp, indy,  zpx,  zpx,  zpx,  zpx,  imp, absy,  imp, absy, absx, absx, absx, absx], # 3 
         [  imp, indx,  imp, indx,   zp,   zp,   zp,   zp,  imp,  imm,  acc,  imm, abso, abso, abso, abso], # 4 
         [  rel, indy,  imp, indy,  zpx,  zpx,  zpx,  zpx,  imp, absy,  imp, absy, absx, absx, absx, absx], # 5 
         [  imp, indx,  imp, indx,   zp,   zp,   zp,   zp,  imp,  imm,  acc,  imm,  ind, abso, abso, abso], # 6 
         [  rel, indy,  imp, indy,  zpx,  zpx,  zpx,  zpx,  imp, absy,  imp, absy, absx, absx, absx, absx], # 7 
         [  imm, indx,  imm, indx,   zp,   zp,   zp,   zp,  imp,  imm,  imp,  imm, abso, abso, abso, abso], # 8 
         [  rel, indy,  imp, indy,  zpx,  zpx,  zpy,  zpy,  imp, absy,  imp, absy, absx, absx, absy, absy], # 9 
         [  imm, indx,  imm, indx,   zp,   zp,   zp,   zp,  imp,  imm,  imp,  imm, abso, abso, abso, abso], # A 
         [  rel, indy,  imp, indy,  zpx,  zpx,  zpy,  zpy,  imp, absy,  imp, absy, absx, absx, absy, absy], # B 
         [  imm, indx,  imm, indx,   zp,   zp,   zp,   zp,  imp,  imm,  imp,  imm, abso, abso, abso, abso], # C 
         [  rel, indy,  imp, indy,  zpx,  zpx,  zpx,  zpx,  imp, absy,  imp, absy, absx, absx, absx, absx], # D 
         [  imm, indx,  imm, indx,   zp,   zp,   zp,   zp,  imp,  imm,  imp,  imm, abso, abso, abso, abso], # E 
         [  rel, indy,  imp, indy,  zpx,  zpx,  zpx,  zpx,  imp, absy,  imp, absy, absx, absx, absx, absx]  # F 
        ]

    @staticmethod
    def handle(opcode, registers, memory_controller):

        # should value fetched according to mode (if applicable)
        # also updates registers according to mode
        return AddressingModes.dispatch_table[(opcode & 0xf0) >> 4][opcode & 0xf](registers, memory_controller)
