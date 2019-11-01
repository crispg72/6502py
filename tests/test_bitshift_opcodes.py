import unittest
import pytest

from unittest.mock import patch, Mock
from emupy6502.memory_controller import MemoryController
from emupy6502.registers import Registers
from emupy6502.opcodes import OpCode


@pytest.fixture
def registers():
    return Registers()

@pytest.fixture
def opcode():
    return OpCode()

@pytest.fixture
def mock_memory_controller():
    return Mock()

def test_execute_asl_accumulator_positive(opcode, registers, mock_memory_controller):

    registers.accumulator = 3

    # we're mocking 0x0A 0x21 
    registers.pc += 1 #need to fake the cpu reading the opcode
    count = opcode.execute(0x0A, registers, mock_memory_controller)
    assert count == 2
    mock_memory_controller.read.assert_not_called()
    assert registers.pc == 1
    assert registers.accumulator == 6
    assert registers.zero_flag == False
    assert registers.carry_flag == False
    assert registers.negative_flag == False

def test_execute_asl_accumulator_negative(opcode, registers, mock_memory_controller):

    registers.accumulator = -3

    # we're mocking 0x0A 0x21 
    registers.pc += 1 #need to fake the cpu reading the opcode
    count = opcode.execute(0x0A, registers, mock_memory_controller)
    assert count == 2
    mock_memory_controller.read.assert_not_called()
    assert registers.pc == 1
    assert registers.accumulator == 0xfa
    assert registers.zero_flag == False
    assert registers.carry_flag
    assert registers.negative_flag

def test_execute_asl_zeropage(opcode, registers, mock_memory_controller):

    # we're mocking 0x06 0x30
    mock_memory_controller.read.side_effect = [0x30, 0x20]
    registers.pc += 1 #need to fake the cpu reading the opcode
    count = opcode.execute(0x06, registers, mock_memory_controller)
    assert count == 5
    assert mock_memory_controller.read.call_count == 2
    assert mock_memory_controller.read.call_args_list[0] == unittest.mock.call(1)
    mock_memory_controller.write.assert_called_with(0x30, 0x40)
    assert registers.pc == 2
    assert registers.zero_flag == False
    assert registers.carry_flag == False
    assert registers.negative_flag == False        

def test_execute_asl_zeropage_x(opcode, registers, mock_memory_controller):

    registers.x_index = 3

    # we're mocking 0x16 0x21 so store to [0x0024]
    mock_memory_controller.read.side_effect = [0x21, 0x10]
    registers.pc += 1 #need to fake the cpu reading the opcode
    count = opcode.execute(0x16, registers, mock_memory_controller)
    assert count == 6

    # these are checked more thoroughly in addressing_modes_tests
    assert mock_memory_controller.read.call_count == 2
    assert mock_memory_controller.read.call_args_list[0] == unittest.mock.call(1)
    mock_memory_controller.write.assert_called_with(0x24, 0x20)
    assert registers.pc == 2
    assert registers.zero_flag == False
    assert registers.carry_flag == False
    assert registers.negative_flag == False        

def test_execute_asl_zeropage_x_wrap(opcode, registers, mock_memory_controller):

    registers.x_index = 3

    # we're mocking 0x16 0x21 so store to [0x0024]
    mock_memory_controller.read.side_effect = [0xfe, 0xf0]
    registers.pc += 1 #need to fake the cpu reading the opcode
    count = opcode.execute(0x16, registers, mock_memory_controller)
    assert count == 6

    # these are checked more thoroughly in addressing_modes_tests
    assert mock_memory_controller.read.call_count == 2
    assert mock_memory_controller.read.call_args_list[0] == unittest.mock.call(1)
    mock_memory_controller.write.assert_called_with(0x01, 0xe0)
    assert registers.pc == 2
    assert registers.zero_flag == False
    assert registers.carry_flag
    assert registers.negative_flag        

def test_execute_asl_absolute(opcode, registers, mock_memory_controller):

    registers.accumulator = 0x20

    # we're mocking 0x0E 0x0 0x20 so store to [0x2000]
    mock_memory_controller.read.side_effect = [0, 0x20, 0x21]
    registers.pc += 1 #need to fake the cpu reading the opcode
    count = opcode.execute(0x0E, registers, mock_memory_controller)
    assert count == 6

    # these are checked more thoroughly in addressing_modes_tests
    assert mock_memory_controller.read.call_count == 3
    assert mock_memory_controller.read.call_args_list[0] == unittest.mock.call(1)
    mock_memory_controller.write.assert_called_with(0x2000, 0x42)
    assert registers.pc == 3
    assert registers.zero_flag == False
    assert registers.carry_flag == False
    assert registers.negative_flag == False        

def test_execute_asl_absolute_x(opcode, registers, mock_memory_controller):

    registers.x_index = 3

    # we're mocking 0x1E 0x2100 so write is to [0x2103]
    mock_memory_controller.read.side_effect = [0, 0x21, 0xfe]
    registers.pc += 1 #need to fake the cpu reading the opcode
    count = opcode.execute(0x1E, registers, mock_memory_controller)
    assert count == 7

    # these are checked more thoroughly in addressing_modes_tests
    assert mock_memory_controller.read.call_count == 3
    mock_memory_controller.write.assert_called_with(0x2103, 0xfc)
    assert registers.pc == 3
    assert registers.zero_flag == False
    assert registers.carry_flag
    assert registers.negative_flag        

def test_execute_rol_accumulator_carry_clear_sign_clear(opcode, registers, mock_memory_controller):

    registers.accumulator = 3

    # we're mocking 0x2A
    registers.pc += 1 #need to fake the cpu reading the opcode
    count = opcode.execute(0x2A, registers, mock_memory_controller)
    assert count == 2
    mock_memory_controller.read.assert_not_called()
    assert registers.pc == 1
    assert registers.accumulator == 6
    assert registers.zero_flag == False
    assert registers.carry_flag == False
    assert registers.negative_flag == False

def test_execute_rol_accumulator_carry_set_sign_clear(opcode, registers, mock_memory_controller):

    registers.accumulator = 3
    registers.carry_flag = True

    # we're mocking 0x2A
    registers.pc += 1 #need to fake the cpu reading the opcode
    count = opcode.execute(0x2A, registers, mock_memory_controller)
    assert count == 2
    mock_memory_controller.read.assert_not_called()
    assert registers.pc == 1
    assert registers.accumulator == 7
    assert registers.zero_flag == False
    assert registers.carry_flag == False
    assert registers.negative_flag == False

def test_execute_rol_accumulator_carry_clear_sign_set(opcode, registers, mock_memory_controller):

    registers.accumulator = 0xc0

    # we're mocking 0x2A
    registers.pc += 1 #need to fake the cpu reading the opcode
    count = opcode.execute(0x2A, registers, mock_memory_controller)
    assert count == 2
    mock_memory_controller.read.assert_not_called()
    assert registers.pc == 1
    assert registers.accumulator == 0x80
    assert registers.zero_flag == False
    assert registers.carry_flag
    assert registers.negative_flag

def test_execute_rol_zeropage_carry_clear_sign_clear(opcode, registers, mock_memory_controller):

    mock_memory_controller.read.side_effect = [0x30, 3]

    # we're mocking 0x26 0x30 and [0x30] = 3
    registers.pc += 1 #need to fake the cpu reading the opcode
    count = opcode.execute(0x26, registers, mock_memory_controller)
    assert count == 5
    assert mock_memory_controller.read.call_count == 2
    mock_memory_controller.write.assert_called_with(0x30, 6)
    assert registers.pc == 2
    assert registers.zero_flag == False
    assert registers.carry_flag == False
    assert registers.negative_flag == False

def test_execute_rol_zeropage_carry_set_sign_clear(opcode, registers, mock_memory_controller):

    registers.carry_flag = True
    mock_memory_controller.read.side_effect = [0x30, 3]

    # we're mocking 0x26 0x30 and [0x30] = 3
    registers.pc += 1 #need to fake the cpu reading the opcode
    count = opcode.execute(0x26, registers, mock_memory_controller)
    assert count == 5
    assert mock_memory_controller.read.call_count == 2        
    mock_memory_controller.write.assert_called_with(0x30, 7)
    assert registers.pc == 2
    assert registers.zero_flag == False
    assert registers.carry_flag == False
    assert registers.negative_flag == False

def test_execute_rol_zeropage_carry_clear_sign_set(opcode, registers, mock_memory_controller):

    registers.accumulator = 0xc0
    mock_memory_controller.read.side_effect = [0x30, 0xc0]

    # we're mocking 0x26 0x30 and [0x30] = 0xc0
    registers.pc += 1 #need to fake the cpu reading the opcode
    count = opcode.execute(0x26, registers, mock_memory_controller)
    assert count == 5
    mock_memory_controller.write.assert_called_with(0x30, 0x80)
    assert registers.pc == 2
    assert registers.zero_flag == False
    assert registers.carry_flag
    assert registers.negative_flag

def test_execute_rol_absolute_carry_clear_sign_clear(opcode, registers, mock_memory_controller):

    mock_memory_controller.read.side_effect = [0x00, 0x30, 3]

    # we're mocking 0x2E 0x30 and [0x3000] = 3
    registers.pc += 1 #need to fake the cpu reading the opcode
    count = opcode.execute(0x2E, registers, mock_memory_controller)
    assert count == 6
    assert mock_memory_controller.read.call_count == 3
    mock_memory_controller.write.assert_called_with(0x3000, 6)
    assert registers.pc == 3
    assert registers.zero_flag == False
    assert registers.carry_flag == False
    assert registers.negative_flag == False

def test_execute_rol_absolute_carry_set_sign_clear(opcode, registers, mock_memory_controller):

    registers.carry_flag = True
    mock_memory_controller.read.side_effect = [0x00, 0x30, 3]

    # we're mocking 0x2E 0x30 and [0x3000] = 3
    registers.pc += 1 #need to fake the cpu reading the opcode
    count = opcode.execute(0x2E, registers, mock_memory_controller)
    assert count == 6
    assert mock_memory_controller.read.call_count == 3
    mock_memory_controller.write.assert_called_with(0x3000, 7)
    assert registers.pc == 3
    assert registers.zero_flag == False
    assert registers.carry_flag == False
    assert registers.negative_flag == False

def test_execute_rol_absolute_carry_clear_sign_set(opcode, registers, mock_memory_controller):

    registers.accumulator = 0xc0
    mock_memory_controller.read.side_effect = [0x00, 0x30, 0xc0]

    # we're mocking 0x2E 0x30 and [0x3000] = 3
    registers.pc += 1 #need to fake the cpu reading the opcode
    count = opcode.execute(0x2E, registers, mock_memory_controller)
    assert count == 6
    assert mock_memory_controller.read.call_count == 3
    mock_memory_controller.write.assert_called_with(0x3000, 0x80)
    assert registers.pc == 3
    assert registers.zero_flag == False
    assert registers.carry_flag
    assert registers.negative_flag