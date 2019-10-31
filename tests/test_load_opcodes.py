import unittest

from unittest.mock import patch
from emupy6502.memory_controller import MemoryController
from emupy6502.registers import Registers
from emupy6502.opcodes import OpCode


def test_execute_lda_immediate():

    opcode = OpCode()
    registers = Registers()
    registers.zero_flag = True
    registers.negative_flag = True  

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        mock_memory_controller.read.return_value = 0x22
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0xA9, registers, mock_memory_controller)
        assert count == 2
        mock_memory_controller.read.assert_called_with(1)
        assert registers.accumulator == 0x22
        assert registers.pc == 2
        assert registers.zero_flag == False
        assert registers.negative_flag == False

def test_execute_lda_immediate_zero():

    opcode = OpCode()
    registers = Registers()
    registers.zero_flag = False
    registers.negative_flag = True  

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        mock_memory_controller.read.return_value = 0x0
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0xA9, registers, mock_memory_controller)
        assert count == 2
        mock_memory_controller.read.assert_called_with(1)
        assert registers.accumulator == 0x0
        assert registers.pc == 2
        assert registers.zero_flag
        assert registers.negative_flag == False

def test_execute_lda_immediate_negative():

    opcode = OpCode()
    registers = Registers()
    registers.zero_flag = True
    registers.negative_flag = False  

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        mock_memory_controller.read.return_value = -1
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0xA9, registers, mock_memory_controller)
        assert count == 2
        mock_memory_controller.read.assert_called_with(1)
        assert registers.accumulator == -1
        assert registers.pc == 2
        assert registers.zero_flag == False
        assert registers.negative_flag

def test_execute_ldx_immediate():

    opcode = OpCode()
    registers = Registers()
    registers.zero_flag = True
    registers.negative_flag = True  

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        mock_memory_controller.read.return_value = 0x22
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0xA2, registers, mock_memory_controller)
        assert count == 2
        mock_memory_controller.read.assert_called_with(1)
        assert registers.x_index == 0x22
        assert registers.pc == 2
        assert registers.zero_flag == False
        assert registers.negative_flag == False

def test_execute_ldx_immediate_zero():

    opcode = OpCode()
    registers = Registers()
    registers.zero_flag = False
    registers.negative_flag = True  

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        mock_memory_controller.read.return_value = 0x0
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0xA2, registers, mock_memory_controller)
        assert count == 2
        mock_memory_controller.read.assert_called_with(1)
        assert registers.x_index == 0x0
        assert registers.pc == 2
        assert registers.zero_flag
        assert registers.negative_flag == False

def test_execute_ldx_immediate_negative():

    opcode = OpCode()
    registers = Registers()
    registers.zero_flag = True
    registers.negative_flag = False  

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        mock_memory_controller.read.return_value = -1
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0xA2, registers, mock_memory_controller)
        assert count == 2
        mock_memory_controller.read.assert_called_with(1)
        assert registers.x_index == -1
        assert registers.pc == 2
        assert registers.zero_flag == False
        assert registers.negative_flag

def test_execute_ldy_immediate():

    opcode = OpCode()
    registers = Registers()
    registers.zero_flag = True
    registers.negative_flag = True  

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        mock_memory_controller.read.return_value = 0x22
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0xA0, registers, mock_memory_controller)
        assert count == 2
        mock_memory_controller.read.assert_called_with(1)
        assert registers.y_index == 0x22
        assert registers.pc == 2
        assert registers.zero_flag == False
        assert registers.negative_flag == False

def test_execute_ldy_immediate_zero():

    opcode = OpCode()
    registers = Registers()
    registers.zero_flag = False
    registers.negative_flag = True  

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        mock_memory_controller.read.return_value = 0x0
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0xA0, registers, mock_memory_controller)
        assert count == 2
        mock_memory_controller.read.assert_called_with(1)
        assert registers.y_index == 0x0
        assert registers.pc == 2
        assert registers.zero_flag
        assert registers.negative_flag == False

def test_execute_ldy_immediate_negative():

    opcode = OpCode()
    registers = Registers()
    registers.zero_flag = True
    registers.negative_flag = False  

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        mock_memory_controller.read.return_value = -1
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0xA0, registers, mock_memory_controller)
        assert count == 2
        mock_memory_controller.read.assert_called_with(1)
        assert registers.y_index == -1
        assert registers.pc == 2
        assert registers.zero_flag == False
        assert registers.negative_flag

def test_execute_lda_zeropage():

    opcode = OpCode()
    registers = Registers()
    registers.zero_flag = True
    registers.negative_flag = True  

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        # we're mocking 0xa5 0x21 and value at [0x0021] = 1
        mock_memory_controller.read.side_effect = [0x21, 1]
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0xA5, registers, mock_memory_controller)
        assert count == 3
        assert mock_memory_controller.read.call_count == 2
        assert mock_memory_controller.read.call_args_list[1] == unittest.mock.call(0x21)
        assert mock_memory_controller.read.call_args_list[0] == unittest.mock.call(1)
        assert registers.pc == 2
        assert registers.accumulator == 1
        assert registers.zero_flag == False
        assert registers.negative_flag == False

def test_execute_ldx_zeropage():

    opcode = OpCode()
    registers = Registers()
    registers.zero_flag = True
    registers.negative_flag = True  

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        # we're mocking 0xa5 0x21 and value at [0x0021] = 1
        mock_memory_controller.read.side_effect = [0x21, 1]
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0xA6, registers, mock_memory_controller)
        assert count == 3
        assert mock_memory_controller.read.call_count == 2
        assert mock_memory_controller.read.call_args_list[1] == unittest.mock.call(0x21)
        assert mock_memory_controller.read.call_args_list[0] == unittest.mock.call(1)
        assert registers.pc == 2
        assert registers.x_index == 1
        assert registers.zero_flag == False
        assert registers.negative_flag == False

def test_execute_ldy_zeropage():

    opcode = OpCode()
    registers = Registers()
    registers.zero_flag = True
    registers.negative_flag = True  

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        # we're mocking 0xa5 0x21 and value at [0x0021] = 1
        mock_memory_controller.read.side_effect = [0x21, 1]
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0xA4, registers, mock_memory_controller)
        assert count == 3
        assert mock_memory_controller.read.call_count == 2
        assert mock_memory_controller.read.call_args_list[1] == unittest.mock.call(0x21)
        assert mock_memory_controller.read.call_args_list[0] == unittest.mock.call(1)
        assert registers.pc == 2
        assert registers.y_index == 1
        assert registers.zero_flag == False
        assert registers.negative_flag == False

def test_execute_lda_absolute():

    opcode = OpCode()
    registers = Registers()
    registers.zero_flag = True
    registers.negative_flag = True  

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        # we're mocking 0xa5 0x21 and value at [0x0021] = 1
        mock_memory_controller.read.side_effect = [0x21, 0x22, 1]
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0xAD, registers, mock_memory_controller)
        assert count == 4

        # these are checked more thoroughly in addressing_modes_tests
        assert mock_memory_controller.read.call_count == 3
        assert registers.pc == 3
        assert registers.accumulator == 1
        assert registers.zero_flag == False
        assert registers.negative_flag == False

def test_execute_ldx_absolute():

    opcode = OpCode()
    registers = Registers()
    registers.zero_flag = False
    registers.negative_flag = True  

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        # we're mocking 0xa5 0x21 and value at [0x0021] = 1
        mock_memory_controller.read.side_effect = [0x21, 0x22, 0]
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0xAE, registers, mock_memory_controller)
        assert count == 4

        # these are checked more thoroughly in addressing_modes_tests
        assert mock_memory_controller.read.call_count == 3
        assert registers.pc == 3
        assert registers.x_index == 0
        assert registers.zero_flag
        assert registers.negative_flag == False

def test_execute_ldy_absolute():

    opcode = OpCode()
    registers = Registers()
    registers.zero_flag = True
    registers.negative_flag = False  

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        # we're mocking 0xa5 0x21 and value at [0x0021] = 1
        mock_memory_controller.read.side_effect = [0x21, 0x22, 0xf0]
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0xAC, registers, mock_memory_controller)
        assert count == 4

        # these are checked more thoroughly in addressing_modes_tests
        assert mock_memory_controller.read.call_count == 3
        assert registers.pc == 3
        assert registers.x_index == 0
        assert registers.zero_flag == False
        assert registers.negative_flag

def test_execute_lda_zeropage_x():

    opcode = OpCode()
    registers = Registers()
    registers.x_index = 3
    registers.zero_flag = True
    registers.negative_flag = True  

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        # we're mocking 0xb5 0x21 and value at [0x0024] = 1
        mock_memory_controller.read.side_effect = [0x21, 1]
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0xB5, registers, mock_memory_controller)
        assert count == 4

        # these are checked more thoroughly in addressing_modes_tests
        assert mock_memory_controller.read.call_count == 2
        assert registers.pc == 2
        assert registers.accumulator == 1
        assert registers.zero_flag == False
        assert registers.negative_flag == False

def test_execute_ldx_zeropage_y():

    opcode = OpCode()
    registers = Registers()
    registers.y_index = 5
    registers.zero_flag = True
    registers.negative_flag = True  

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        # we're mocking 0xb6 0xff and value at [0x04] = 2
        mock_memory_controller.read.side_effect = [0xff, 2]
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0xB6, registers, mock_memory_controller)
        assert count == 4

        # these are checked more thoroughly in addressing_modes_tests
        assert mock_memory_controller.read.call_count == 2
        assert registers.pc == 2
        assert registers.x_index == 2
        assert registers.zero_flag == False
        assert registers.negative_flag == False

def test_execute_lda_indirect_x():

    opcode = OpCode()
    registers = Registers()
    registers.x_index = 3
    registers.zero_flag = True
    registers.negative_flag = False

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        # we're mocking 0xa1 0x21 and value at [0x0024] = 0x1234, [0x1234] = 0xcc
        mock_memory_controller.read.side_effect = [0x21, 0x34, 0x12, 0xcc]
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0xA1, registers, mock_memory_controller)
        assert count == 6

        # these are checked more thoroughly in addressing_modes_tests
        assert mock_memory_controller.read.call_count == 4
        assert registers.pc == 2
        assert registers.accumulator == 0xcc
        assert registers.zero_flag == False
        assert registers.negative_flag

def test_execute_lda_absolute_x():

    opcode = OpCode()
    registers = Registers()
    registers.x_index = 3
    registers.zero_flag = True
    registers.negative_flag = True

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        # we're mocking 0xBD 0x2100 and value at [0x2103] = 0x12
        mock_memory_controller.read.side_effect = [0, 0x21, 0x12]
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0xBD, registers, mock_memory_controller)
        assert count == 4

        # these are checked more thoroughly in addressing_modes_tests
        assert mock_memory_controller.read.call_count == 3
        assert registers.pc == 3
        assert registers.accumulator == 0x12
        assert registers.zero_flag == False
        assert registers.negative_flag == False

def test_execute_lda_absolute_x_extra_cycle():

    opcode = OpCode()
    registers = Registers()
    registers.x_index = 3
    registers.zero_flag = True
    registers.negative_flag = False

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        # we're mocking 0xBD 0x21fe and value at [0x2201] = 0xf0
        mock_memory_controller.read.side_effect = [0xfe, 0x21, 0xf0]
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0xBD, registers, mock_memory_controller)
        assert count == 5

        # these are checked more thoroughly in addressing_modes_tests
        assert mock_memory_controller.read.call_count == 3
        assert registers.pc == 3
        assert registers.accumulator == 0xf0
        assert registers.zero_flag == False
        assert registers.negative_flag

def test_execute_lda_absolute_y():

    opcode = OpCode()
    registers = Registers()
    registers.y_index = 3
    registers.zero_flag = True
    registers.negative_flag = True

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        # we're mocking 0xB9 0x2100 and value at [0x2103] = 0x12
        mock_memory_controller.read.side_effect = [0, 0x21, 0x12]
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0xB9, registers, mock_memory_controller)
        assert count == 4

        # these are checked more thoroughly in addressing_modes_tests
        assert mock_memory_controller.read.call_count == 3
        assert registers.pc == 3
        assert registers.accumulator == 0x12
        assert registers.zero_flag == False
        assert registers.negative_flag == False

def test_execute_lda_absolute_y_extra_cycle():

    opcode = OpCode()
    registers = Registers()
    registers.y_index = 3
    registers.zero_flag = True
    registers.negative_flag = False

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        # we're mocking 0xB9 0x21fe and value at [0x2201] = 0xf0
        mock_memory_controller.read.side_effect = [0xfe, 0x21, 0xf0]
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0xB9, registers, mock_memory_controller)
        assert count == 5

        # these are checked more thoroughly in addressing_modes_tests
        assert mock_memory_controller.read.call_count == 3
        assert registers.pc == 3
        assert registers.accumulator == 0xf0
        assert registers.zero_flag == False
        assert registers.negative_flag

def test_execute_ldx_absolute_y():

    opcode = OpCode()
    registers = Registers()
    registers.y_index = 3
    registers.zero_flag = True
    registers.negative_flag = True

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        # we're mocking 0xBE 0x2100 and value at [0x2103] = 0x12
        mock_memory_controller.read.side_effect = [0, 0x21, 0x12]
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0xBE, registers, mock_memory_controller)
        assert count == 4

        # these are checked more thoroughly in addressing_modes_tests
        assert mock_memory_controller.read.call_count == 3
        assert registers.pc == 3
        assert registers.x_index == 0x12
        assert registers.zero_flag == False
        assert registers.negative_flag == False

def test_execute_ldx_absolute_y_extra_cycle():

    opcode = OpCode()
    registers = Registers()
    registers.y_index = 3
    registers.zero_flag = True
    registers.negative_flag = False

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        # we're mocking 0xBE 0x21fe and value at [0x2201] = 0xf0
        mock_memory_controller.read.side_effect = [0xfe, 0x21, 0xf0]
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0xBE, registers, mock_memory_controller)
        assert count == 5

        # these are checked more thoroughly in addressing_modes_tests
        assert mock_memory_controller.read.call_count == 3
        assert registers.pc == 3
        assert registers.x_index == 0xf0
        assert registers.zero_flag == False
        assert registers.negative_flag

def test_execute_ldy_absolute_x():

    opcode = OpCode()
    registers = Registers()
    registers.x_index = 3
    registers.zero_flag = True
    registers.negative_flag = True

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        # we're mocking 0xBC 0x2100 and value at [0x2103] = 0x12
        mock_memory_controller.read.side_effect = [0, 0x21, 0x12]
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0xBC, registers, mock_memory_controller)
        assert count == 4

        # these are checked more thoroughly in addressing_modes_tests
        assert mock_memory_controller.read.call_count == 3
        assert registers.pc == 3
        assert registers.y_index == 0x12
        assert registers.zero_flag == False
        assert registers.negative_flag == False

def test_execute_ldy_absolute_x_extra_cycle():

    opcode = OpCode()
    registers = Registers()
    registers.x_index = 3
    registers.zero_flag = True
    registers.negative_flag = False

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        # we're mocking 0xBC 0x21fe and value at [0x2201] = 0xf0
        mock_memory_controller.read.side_effect = [0xfe, 0x21, 0xf0]
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0xBC, registers, mock_memory_controller)
        assert count == 5

        # these are checked more thoroughly in addressing_modes_tests
        assert mock_memory_controller.read.call_count == 3
        assert registers.pc == 3
        assert registers.y_index == 0xf0
        assert registers.zero_flag == False
        assert registers.negative_flag

def test_execute_lda_indirect_indexed_y():

    opcode = OpCode()
    registers = Registers()
    registers.y_index = 3
    registers.zero_flag = True
    registers.negative_flag = False

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        # we're mocking 0xb1 0x44 
        mock_memory_controller.read.side_effect = [0x44, 0x34, 0x12, 0xcc]
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0xB1, registers, mock_memory_controller)
        assert count == 5

        # these are checked more thoroughly in addressing_modes_tests
        assert mock_memory_controller.read.call_count == 4
        assert registers.pc == 2
        assert registers.accumulator == 0xcc
        assert registers.zero_flag == False
        assert registers.negative_flag

def test_execute_lda_indirect_indexed_y_page_boundary():

    opcode = OpCode()
    registers = Registers()
    registers.y_index = 3
    registers.zero_flag = False
    registers.negative_flag = True

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        # we're mocking 0xb1 0x44 
        mock_memory_controller.read.side_effect = [0x44, 0xfd, 0x12, 0]
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0xB1, registers, mock_memory_controller)
        assert count == 6

        # these are checked more thoroughly in addressing_modes_tests
        assert mock_memory_controller.read.call_count == 4
        assert registers.pc == 2
        assert registers.accumulator == 0
        assert registers.zero_flag
        assert registers.negative_flag == False