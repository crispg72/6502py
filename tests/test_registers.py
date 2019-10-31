from unittest.mock import patch
from emupy6502.memory_controller import MemoryController
from emupy6502.registers import Registers
from emupy6502.opcodes import OpCode


def test_set_NZ_non_zero_positive():

    registers = Registers()
    registers.set_NZ(1)
    assert registers.negative_flag == False
    assert registers.zero_flag == False

def test_set_NZ_zero_positive():

    registers = Registers()
    registers.set_NZ(0)
    assert registers.negative_flag == False
    assert registers.zero_flag

def test_set_NZ_non_zero_negative():

    registers = Registers()
    registers.set_NZ(-3)
    assert registers.negative_flag
    assert registers.zero_flag == False

def test_set_NZV_non_zero_negative_no_overflow():

    registers = Registers()
    registers.accumulator = 4
    registers.set_NZV(-3, 1)
    assert registers.negative_flag == False
    assert registers.zero_flag == False
    assert registers.overflow_flag == False

def test_set_NZV_non_zero_not_negative_overflow():

    registers = Registers()
    registers.accumulator = 0x80
    # Here we act as if we have done -128 + -1
    registers.set_NZV(0xff, 0x7f)
    assert registers.negative_flag == False
    assert registers.zero_flag == False
    assert registers.overflow_flag

def test_set_NZV_non_zero_negative_overflow():

    registers = Registers()
    registers.accumulator = 0x7f
    # Here we act as if we have done 127 + 1
    registers.set_NZV(1, 0x80)
    assert registers.negative_flag
    assert registers.zero_flag == False
    assert registers.overflow_flag