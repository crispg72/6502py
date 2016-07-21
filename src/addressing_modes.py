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
    value = memory_controller.read(registers.pc)
    registers.pc += 1
    return value

def ind(registers, memory_controller):
    low_address = memory_controller.read(registers.pc)
    registers.pc += 1
    high_address = memory_controller.read(registers.pc)
    registers.pc +=1
    
    low_result = memory_controller.read((high_address << 8) + low_address)
    # deal with the indirect 'quirk' where it cannot straddle pages
    if low_address == 0xff:
        low_address = 0
    else:
        low_address += 1
    high_result = memory_controller.read((high_address << 8) + low_address)
    return (high_result << 8) + low_result

def indx(registers, memory_controller):
    zp_address =  memory_controller.read(registers.pc)
    registers.pc += 1
    zp_address += registers.x_index

    low_address = memory_controller.read(zp_address & 0xff)
    high_address = memory_controller.read((zp_address + 1) & 0xff)
    return (high_address << 8) + low_address

def indy(registers, memory_controller):
    zp_address = memory_controller.read(registers.pc)
    registers.pc += 1
    low_address = memory_controller.read(zp_address)
    high_address = memory_controller.read((zp_address + 1) & 0xff)

    low_address += registers.y_index
    if low_address > 255:
        AddressingModes.cycle_count += 1

    return (high_address << 8) + low_address

def zpW(registers, memory_controller):
    low_address = memory_controller.read(registers.pc)
    registers.pc += 1
    return low_address

def zp(registers, memory_controller):
    return memory_controller.read(zpW(registers, memory_controller))

def zpxW(registers, memory_controller):
    address = memory_controller.read(registers.pc)
    registers.pc += 1
    address += registers.x_index
    return address & 0xff

def zpx(registers, memory_controller):
    return memory_controller.read(zpxW(registers, memory_controller))

def zpyW(registers, memory_controller):
    address = memory_controller.read(registers.pc)
    registers.pc += 1
    address += registers.y_index
    return address & 0xff

def zpy(registers, memory_controller):
    return memory_controller.read(zpyW(registers, memory_controller))

def absoW(registers, memory_controller):
    low_address = memory_controller.read(registers.pc)
    registers.pc += 1
    high_address = memory_controller.read(registers.pc)
    registers.pc +=1
    return (high_address << 8) + low_address

def abso(registers, memory_controller):
    return memory_controller.read(absoW(registers, memory_controller))

def absx(registers, memory_controller):
    low_address = memory_controller.read(registers.pc)
    registers.pc += 1
    high_address = memory_controller.read(registers.pc)
    registers.pc +=1
    low_address += registers.x_index

    if low_address > 255:
        AddressingModes.cycle_count += 1

    return (high_address << 8) + low_address

def absy(registers, memory_controller):
    low_address = memory_controller.read(registers.pc)
    registers.pc += 1
    high_address = memory_controller.read(registers.pc)
    registers.pc +=1
    low_address += registers.y_index

    if low_address > 255:
        AddressingModes.cycle_count += 1

    return (high_address << 8) + low_address

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
         [  imp, indx,  imp, indx,   zp,   zp,  zpW,   zp,  imp,  imm,  acc,  imm, abso,  abso, absoW, abso], # 0 
         [  rel, indy,  imp, indy,  zpx,  zpx, zpxW,  zpx,  imp, absy,  imp, absy, absx,  absx, absx, absx], # 1 
         [ abso, indx,  imp, indx,   zp,   zp,  zpW,   zp,  imp,  imm,  acc,  imm, abso,  abso, abso, abso], # 2 
         [  rel, indy,  imp, indy,  zpx,  zpx,  zpx,  zpx,  imp, absy,  imp, absy, absx,  absx, absx, absx], # 3 
         [  imp, indx,  imp, indx,   zp,   zp,   zp,   zp,  imp,  imm,  acc,  imm, absoW,  abso, abso, abso], # 4 
         [  rel, indy,  imp, indy,  zpx,  zpx,  zpx,  zpx,  imp, absy,  imp, absy, absx,  absx, absx, absx], # 5 
         [  imp, indx,  imp, indx,   zp,   zp,   zp,   zp,  imp,  imm,  acc,  imm,  ind,  abso, abso, abso], # 6 
         [  rel, indy,  imp, indy,  zpx,  zpx,  zpx,  zpx,  imp, absy,  imp, absy, absx,  absx, absx, absx], # 7 
         [  imm, indx,  imm, indx,  zpW,  zpW,  zpW,   zp,  imp,  imm,  imp,  imm, absoW, absoW, absoW, abso], # 8 
         [  rel, indy,  imp, indy, zpxW, zpxW, zpyW,  zpy,  imp, absy,  imp, absy, absx,  absx, absy, absy], # 9 
         [  imm, indx,  imm, indx,   zp,   zp,   zp,   zp,  imp,  imm,  imp,  imm, abso,  abso, abso, abso], # A 
         [  rel, indy,  imp, indy,  zpx,  zpx,  zpy,  zpy,  imp, absy,  imp, absy, absx,  absx, absy, absy], # B 
         [  imm, indx,  imm, indx,   zp,   zp,   zp,   zp,  imp,  imm,  imp,  imm, abso,  abso, abso, abso], # C 
         [  rel, indy,  imp, indy,  zpx,  zpx,  zpx,  zpx,  imp, absy,  imp, absy, absx,  absx, absx, absx], # D 
         [  imm, indx,  imm, indx,   zp,   zp,   zp,   zp,  imp,  imm,  imp,  imm, abso,  abso, abso, abso], # E 
         [  rel, indy,  imp, indy,  zpx,  zpx,  zpx,  zpx,  imp, absy,  imp, absy, absx,  absx, absx, absx]  # F 
        ]

    # Used for marking extra cycles for crossing page boundary
    cycle_count = 0

    @staticmethod
    def handle(opcode, registers, memory_controller):

        # should value fetched according to mode (if applicable)
        # also updates registers according to mode
        return AddressingModes.dispatch_table[(opcode & 0xf0) >> 4][opcode & 0xf](registers, memory_controller)
