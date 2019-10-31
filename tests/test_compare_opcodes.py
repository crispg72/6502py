import unittest

from unittest.mock import patch, Mock
from emupy6502.memory_controller import MemoryController
from emupy6502.registers import Registers
from emupy6502.opcodes import OpCode


def test_execute_cmp_immediate_lessthan():

    opcode = OpCode()
    registers = Registers()
    registers.accumulator = 3

    mock_memory_controller = Mock()
    mock_memory_controller.read.side_effect = [0x21]

    # we're mocking 0xC9 0x21 
    registers.pc += 1 #need to fake the cpu reading the opcode
    count = opcode.execute(0xC9, registers, mock_memory_controller)
    assert count == 2
    assert mock_memory_controller.read.call_count == 1
    assert mock_memory_controller.read.call_args_list[0] == unittest.mock.call(1)
    assert registers.pc == 2
    assert registers.zero_flag == False
    assert registers.carry_flag == False
    assert registers.negative_flag

def test_execute_cmp_immediate_greaterthan():

    opcode = OpCode()
    registers = Registers()
    registers.accumulator = 4

    mock_memory_controller = Mock()
    mock_memory_controller.read.side_effect = [0x3]

    # we're mocking 0xC9 0x21 
    registers.pc += 1 #need to fake the cpu reading the opcode
    count = opcode.execute(0xC9, registers, mock_memory_controller)
    assert count == 2
    assert mock_memory_controller.read.call_count == 1
    assert mock_memory_controller.read.call_args_list[0] == unittest.mock.call(1)
    assert registers.pc == 2
    assert registers.zero_flag == False
    assert registers.carry_flag
    assert registers.negative_flag == False

def test_execute_cmp_immediate_equalto():

    opcode = OpCode()
    registers = Registers()
    registers.accumulator = 4

    mock_memory_controller = Mock()
    mock_memory_controller.read.side_effect = [0x4]

    # we're mocking 0xC9 0x21 
    registers.pc += 1 #need to fake the cpu reading the opcode
    count = opcode.execute(0xC9, registers, mock_memory_controller)
    assert count == 2
    assert mock_memory_controller.read.call_count == 1
    assert mock_memory_controller.read.call_args_list[0] == unittest.mock.call(1)
    assert registers.pc == 2
    assert registers.zero_flag
    assert registers.carry_flag
    assert registers.negative_flag == False

def test_execute_cpx_immediate_lessthan():

    opcode = OpCode()
    registers = Registers()
    registers.x_index = 3

    mock_memory_controller = Mock()
    mock_memory_controller.read.side_effect = [0x21]

    # we're mocking 0xE0 0x21 
    registers.pc += 1 #need to fake the cpu reading the opcode
    count = opcode.execute(0xE0, registers, mock_memory_controller)
    assert count == 2
    assert mock_memory_controller.read.call_count == 1
    assert mock_memory_controller.read.call_args_list[0] == unittest.mock.call(1)
    assert registers.pc == 2
    assert registers.zero_flag == False
    assert registers.carry_flag == False
    assert registers.negative_flag

def test_execute_cpx_immediate_greaterthan():

    opcode = OpCode()
    registers = Registers()
    registers.x_index = 4

    mock_memory_controller = Mock()
    mock_memory_controller.read.side_effect = [0x3]

    # we're mocking 0xE0 0x03 
    registers.pc += 1 #need to fake the cpu reading the opcode
    count = opcode.execute(0xE0, registers, mock_memory_controller)
    assert count == 2
    assert mock_memory_controller.read.call_count == 1
    assert mock_memory_controller.read.call_args_list[0] == unittest.mock.call(1)
    assert registers.pc == 2
    assert registers.zero_flag == False
    assert registers.carry_flag
    assert registers.negative_flag == False

def test_execute_cpx_immediate_equalto():

    opcode = OpCode()
    registers = Registers()
    registers.x_index = 4

    mock_memory_controller = Mock()
    mock_memory_controller.read.side_effect = [0x4]

    # we're mocking 0xE0 0x04 
    registers.pc += 1 #need to fake the cpu reading the opcode
    count = opcode.execute(0xE0, registers, mock_memory_controller)
    assert count == 2
    assert mock_memory_controller.read.call_count == 1
    assert mock_memory_controller.read.call_args_list[0] == unittest.mock.call(1)
    assert registers.pc == 2
    assert registers.zero_flag
    assert registers.carry_flag
    assert registers.negative_flag == False

def test_execute_cpy_immediate_lessthan():

    opcode = OpCode()
    registers = Registers()
    registers.y_index = 3

    mock_memory_controller = Mock()
    mock_memory_controller.read.side_effect = [0x21]

    # we're mocking 0xC0 0x21 
    registers.pc += 1 #need to fake the cpu reading the opcode
    count = opcode.execute(0xC0, registers, mock_memory_controller)
    assert count == 2
    assert mock_memory_controller.read.call_count == 1
    assert mock_memory_controller.read.call_args_list[0] == unittest.mock.call(1)
    assert registers.pc == 2
    assert registers.zero_flag == False
    assert registers.carry_flag == False
    assert registers.negative_flag

def test_execute_cpy_immediate_greaterthan():

    opcode = OpCode()
    registers = Registers()
    registers.y_index = 4

    mock_memory_controller = Mock()
    mock_memory_controller.read.side_effect = [0x3]

    # we're mocking 0xE0 0x03 
    registers.pc += 1 #need to fake the cpu reading the opcode
    count = opcode.execute(0xC0, registers, mock_memory_controller)
    assert count == 2
    assert mock_memory_controller.read.call_count == 1
    assert mock_memory_controller.read.call_args_list[0] == unittest.mock.call(1)
    assert registers.pc == 2
    assert registers.zero_flag == False
    assert registers.carry_flag
    assert registers.negative_flag == False

def test_execute_cpy_immediate_equalto():

    opcode = OpCode()
    registers = Registers()
    registers.y_index = 4

    mock_memory_controller = Mock()
    mock_memory_controller.read.side_effect = [0x4]

    # we're mocking 0xE0 0x04 
    registers.pc += 1 #need to fake the cpu reading the opcode
    count = opcode.execute(0xC0, registers, mock_memory_controller)
    assert count == 2
    assert mock_memory_controller.read.call_count == 1
    assert mock_memory_controller.read.call_args_list[0] == unittest.mock.call(1)
    assert registers.pc == 2
    assert registers.zero_flag
    assert registers.carry_flag
    assert registers.negative_flag == False

def test_execute_cmp_zeropage_lessthan():

    opcode = OpCode()
    registers = Registers()
    registers.accumulator = 3

    mock_memory_controller = Mock()
    mock_memory_controller.read.side_effect = [0x21, 6]

    # we're mocking 0xC5 0x21 and [0x21] = 6
    registers.pc += 1 #need to fake the cpu reading the opcode
    count = opcode.execute(0xC5, registers, mock_memory_controller)
    assert count == 3
    assert mock_memory_controller.read.call_count == 2
    assert mock_memory_controller.read.call_args_list[0] == unittest.mock.call(1)
    assert mock_memory_controller.read.call_args_list[1] == unittest.mock.call(0x21)
    assert registers.pc == 2
    assert registers.zero_flag == False
    assert registers.carry_flag == False
    assert registers.negative_flag

def test_execute_cmp_zeropage_greaterthan():

    opcode = OpCode()
    registers = Registers()
    registers.accumulator = 4

    mock_memory_controller = Mock()
    mock_memory_controller.read.side_effect = [0x21, 0x3]

    # we're mocking 0xC5 0x21 and [0x21] = 3
    registers.pc += 1 #need to fake the cpu reading the opcode
    count = opcode.execute(0xC5, registers, mock_memory_controller)
    assert count == 3
    assert mock_memory_controller.read.call_count == 2
    assert mock_memory_controller.read.call_args_list[0] == unittest.mock.call(1)
    assert mock_memory_controller.read.call_args_list[1] == unittest.mock.call(0x21)
    assert registers.pc == 2
    assert registers.zero_flag == False
    assert registers.carry_flag
    assert registers.negative_flag == False

def test_execute_cmp_zeropage_equalto():

    opcode = OpCode()
    registers = Registers()
    registers.accumulator = 4

    mock_memory_controller = Mock()
    mock_memory_controller.read.side_effect = [0x21, 0x4]

    # we're mocking 0xC5 0x21 
    registers.pc += 1 #need to fake the cpu reading the opcode
    count = opcode.execute(0xC5, registers, mock_memory_controller)
    assert count == 3
    assert mock_memory_controller.read.call_count == 2
    assert mock_memory_controller.read.call_args_list[0] == unittest.mock.call(1)
    assert mock_memory_controller.read.call_args_list[1] == unittest.mock.call(0x21)
    assert registers.pc == 2
    assert registers.zero_flag
    assert registers.carry_flag
    assert registers.negative_flag == False

def test_execute_cpx_zeropage_lessthan():

    opcode = OpCode()
    registers = Registers()
    registers.x_index = 3

    mock_memory_controller = Mock()
    mock_memory_controller.read.side_effect = [0x21, 6]

    # we're mocking 0xE4 0x21 and [0x21] = 6
    registers.pc += 1 #need to fake the cpu reading the opcode
    count = opcode.execute(0xE4, registers, mock_memory_controller)
    assert count == 3
    assert mock_memory_controller.read.call_count == 2
    assert mock_memory_controller.read.call_args_list[0] == unittest.mock.call(1)
    assert mock_memory_controller.read.call_args_list[1] == unittest.mock.call(0x21)
    assert registers.pc == 2
    assert registers.zero_flag == False
    assert registers.carry_flag == False
    assert registers.negative_flag

def test_execute_cpx_zeropage_greaterthan():

    opcode = OpCode()
    registers = Registers()
    registers.x_index = 4

    mock_memory_controller = Mock()
    mock_memory_controller.read.side_effect = [0x21, 0x3]

    # we're mocking 0xE4 0x21 and [0x21] = 3
    registers.pc += 1 #need to fake the cpu reading the opcode
    count = opcode.execute(0xE4, registers, mock_memory_controller)
    assert count == 3
    assert mock_memory_controller.read.call_count == 2
    assert mock_memory_controller.read.call_args_list[0] == unittest.mock.call(1)
    assert mock_memory_controller.read.call_args_list[1] == unittest.mock.call(0x21)
    assert registers.pc == 2
    assert registers.zero_flag == False
    assert registers.carry_flag
    assert registers.negative_flag == False

def test_execute_cpx_zeropage_equalto():

    opcode = OpCode()
    registers = Registers()
    registers.x_index = 4

    mock_memory_controller = Mock()
    mock_memory_controller.read.side_effect = [0x21, 0x4]

    # we're mocking 0xE4 0x21 
    registers.pc += 1 #need to fake the cpu reading the opcode
    count = opcode.execute(0xE4, registers, mock_memory_controller)
    assert count == 3
    assert mock_memory_controller.read.call_count == 2
    assert mock_memory_controller.read.call_args_list[0] == unittest.mock.call(1)
    assert mock_memory_controller.read.call_args_list[1] == unittest.mock.call(0x21)
    assert registers.pc == 2
    assert registers.zero_flag
    assert registers.carry_flag
    assert registers.negative_flag == False

def test_execute_cpy_zeropage_lessthan():

    opcode = OpCode()
    registers = Registers()
    registers.y_index = 3

    mock_memory_controller = Mock()
    mock_memory_controller.read.side_effect = [0x21, 6]

    # we're mocking 0xC4 0x21 and [0x21] = 6
    registers.pc += 1 #need to fake the cpu reading the opcode
    count = opcode.execute(0xC4, registers, mock_memory_controller)
    assert count == 3
    assert mock_memory_controller.read.call_count == 2
    assert mock_memory_controller.read.call_args_list[0] == unittest.mock.call(1)
    assert mock_memory_controller.read.call_args_list[1] == unittest.mock.call(0x21)
    assert registers.pc == 2
    assert registers.zero_flag == False
    assert registers.carry_flag == False
    assert registers.negative_flag

def test_execute_cpy_zeropage_greaterthan():

    opcode = OpCode()
    registers = Registers()
    registers.y_index = 4

    mock_memory_controller = Mock()
    mock_memory_controller.read.side_effect = [0x21, 0x3]

    # we're mocking 0xC4 0x21 and [0x21] = 3
    registers.pc += 1 #need to fake the cpu reading the opcode
    count = opcode.execute(0xC4, registers, mock_memory_controller)
    assert count == 3
    assert mock_memory_controller.read.call_count == 2
    assert mock_memory_controller.read.call_args_list[0] == unittest.mock.call(1)
    assert mock_memory_controller.read.call_args_list[1] == unittest.mock.call(0x21)
    assert registers.pc == 2
    assert registers.zero_flag == False
    assert registers.carry_flag
    assert registers.negative_flag == False

def test_execute_cpy_zeropage_equalto():

    opcode = OpCode()
    registers = Registers()
    registers.y_index = 4

    mock_memory_controller = Mock()
    mock_memory_controller.read.side_effect = [0x21, 0x4]

    # we're mocking 0xC4 0x21 
    registers.pc += 1 #need to fake the cpu reading the opcode
    count = opcode.execute(0xC4, registers, mock_memory_controller)
    assert count == 3
    assert mock_memory_controller.read.call_count == 2
    assert mock_memory_controller.read.call_args_list[0] == unittest.mock.call(1)
    assert mock_memory_controller.read.call_args_list[1] == unittest.mock.call(0x21)
    assert registers.pc == 2
    assert registers.zero_flag
    assert registers.carry_flag
    assert registers.negative_flag == False