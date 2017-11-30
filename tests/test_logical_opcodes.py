import unittest

from unittest.mock import patch, Mock
from emupy6502.memory_controller import MemoryController
from emupy6502.registers import Registers
from emupy6502.opcodes import OpCode


class OpCodeTestsLogical(unittest.TestCase):
    
    def execute_and_positive(self, actual_opcode, expected_clocks, read_side_effect, **kwargs):

        opcode = OpCode()
        registers = Registers()
        registers.accumulator = 0x05
        registers.zero_flag = True
        registers.negative_flag = True  

        if kwargs:
            for arg in kwargs:
                setattr(registers, arg, kwargs[arg])

        mock_memory_controller = Mock()
        read_side_effect.append(0x04)
        mock_memory_controller.read.side_effect = read_side_effect

        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(actual_opcode, registers, mock_memory_controller)
        self.assertEqual(len(read_side_effect), mock_memory_controller.read.call_count)
        self.assertEqual(count, expected_clocks)
        self.assertTrue(registers.accumulator == 0x04)
        self.assertFalse(registers.zero_flag)
        self.assertFalse(registers.negative_flag)

    def execute_and_zero(self, actual_opcode, expected_clocks, read_side_effect, **kwargs):

        opcode = OpCode()
        registers = Registers()
        registers.accumulator = 0x05
        registers.negative_flag = True  

        if kwargs:
            for arg in kwargs:
                setattr(registers, arg, kwargs[arg])

        mock_memory_controller = Mock()
        read_side_effect.append(0x18)
        mock_memory_controller.read.side_effect = read_side_effect

        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(actual_opcode, registers, mock_memory_controller)
        self.assertEqual(len(read_side_effect), mock_memory_controller.read.call_count)
        self.assertEqual(count, expected_clocks)
        self.assertEqual(registers.accumulator, 0x00)
        self.assertTrue(registers.zero_flag)
        self.assertFalse(registers.negative_flag)

    def execute_and_negative(self, actual_opcode, expected_clocks, read_side_effect, **kwargs):

        opcode = OpCode()
        registers = Registers()
        registers.accumulator = 0xf0
        registers.negative_flag = True  

        if kwargs:
            for arg in kwargs:
                setattr(registers, arg, kwargs[arg])

        mock_memory_controller = Mock()
        read_side_effect.append(0xa0)
        mock_memory_controller.read.side_effect = read_side_effect

        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(actual_opcode, registers, mock_memory_controller)
        self.assertEqual(len(read_side_effect), mock_memory_controller.read.call_count)
        self.assertEqual(count, expected_clocks)
        self.assertEqual(registers.accumulator, 0xa0)
        self.assertFalse(registers.zero_flag)
        self.assertTrue(registers.negative_flag)

    def test_execute_and_immediate_positive(self):

        self.execute_and_positive(0x29, 2, [])

    def test_execute_and_immediate_zero(self):

        self.execute_and_zero(0x29, 2, [])

    def test_execute_and_immediate_negative(self):

        self.execute_and_negative(0x29, 2, [])

    def test_execute_and_zeropage_positive(self):

        self.execute_and_positive(0x25, 3, [0x20])

    def test_execute_and_zeropage_zero(self):

        self.execute_and_zero(0x25, 3, [0x20])

    def test_execute_and_zeropage_negative(self):

        self.execute_and_negative(0x25, 3, [0x20])

    def test_execute_and_zeropageX_positive(self):

        self.execute_and_positive(0x35, 4, [0x20], x_index = 3)

    def test_execute_and_zeropageX_zero(self):

        self.execute_and_zero(0x35, 4, [0x20], x_index = 3)

    def test_execute_and_zeropageX_negative(self):

        self.execute_and_negative(0x35, 4, [0x20], x_index = 3)

    def test_execute_and_absolute_positive(self):

        self.execute_and_positive(0x2d, 4, [0x00, 0x20])

    def test_execute_and_absolute_zero(self):

        self.execute_and_zero(0x2d, 4, [0x00, 0x20])

    def test_execute_and_absolute_negative(self):

        self.execute_and_negative(0x2d, 4, [0x00, 0x20])

    def test_execute_and_absoluteX_positive(self):

        self.execute_and_positive(0x3d, 4, [0x00, 0x20], x_index = 3)

    def test_execute_and_absoluteX_zero(self):

        self.execute_and_zero(0x3d, 4, [0x00, 0x20], x_index = 3)

    def test_execute_and_absoluteX_negative(self):

        self.execute_and_negative(0x3d, 4, [0x00, 0x20], x_index = 3)

    def test_execute_and_absoluteX_positive_extracycle(self):

        self.execute_and_positive(0x3d, 5, [0xfe, 0x20], x_index = 3)

    def test_execute_and_absoluteX_zero_extracycle(self):

        self.execute_and_zero(0x3d, 5, [0xfe, 0x20], x_index = 3)

    def test_execute_and_absoluteX_negative_extracycle(self):

        self.execute_and_negative(0x3d, 5, [0xfe, 0x20], x_index = 3)

    def test_execute_and_absoluteY_positive(self):

        self.execute_and_positive(0x39, 4, [0x00, 0x20], y_index = 3)

    def test_execute_and_absoluteY_zero(self):

        self.execute_and_zero(0x39, 4, [0x00, 0x20], y_index = 3)

    def test_execute_and_absoluteY_negative(self):

        self.execute_and_negative(0x39, 4, [0x00, 0x20], y_index = 3)

    def test_execute_and_absoluteY_positive_extracycle(self):

        self.execute_and_positive(0x39, 5, [0xfe, 0x20], y_index = 3)

    def test_execute_and_absoluteY_zero_extracycle(self):

        self.execute_and_zero(0x39, 5, [0xfe, 0x20], y_index = 3)

    def test_execute_and_absoluteY_negative_extracycle(self):

        self.execute_and_negative(0x39, 5, [0xfe, 0x20], y_index = 3)

    def test_execute_and_indirectX_positive(self):

        self.execute_and_positive(0x21, 6, [0x20, 0x34, 0x12], x_index = 3)

    def test_execute_and_indirectX_zero(self):

        self.execute_and_zero(0x21, 6, [0x20, 0x34, 0x12], x_index = 3)

    def test_execute_and_indirectX_negative(self):

        self.execute_and_negative(0x21, 6, [0x20, 0x34, 0x12], x_index = 3)

    def test_execute_and_indirectY_positive(self):

        self.execute_and_positive(0x31, 5, [0x20, 0x34, 0x12], y_index = 3)

    def test_execute_and_indirectY_zero(self):

        self.execute_and_zero(0x31, 5, [0x20, 0x34, 0x12], y_index = 3)

    def test_execute_and_indirectY_negative(self):

        self.execute_and_negative(0x31, 5, [0x20, 0x34, 0x12], y_index = 3)

    def test_execute_and_indirectY_extracycle(self):

        self.execute_and_positive(0x31, 6, [0x20, 0xfe, 0x12], y_index = 3)

    def test_execute_and_indirectY_zero_extracycle(self):

        self.execute_and_zero(0x31, 6, [0x20, 0xfe, 0x12], y_index = 3)

    def test_execute_and_indirectY_negative_extracycle(self):

        self.execute_and_negative(0x31, 6, [0x20, 0xfe, 0x12], y_index = 3)

    def execute_eor_positive(self, actual_opcode, expected_clocks, read_side_effect, **kwargs):

        opcode = OpCode()
        registers = Registers()
        registers.accumulator = 0x05
        registers.zero_flag = True
        registers.negative_flag = True  

        if kwargs:
            for arg in kwargs:
                setattr(registers, arg, kwargs[arg])

        mock_memory_controller = Mock()
        read_side_effect.append(0x04)
        mock_memory_controller.read.side_effect = read_side_effect

        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(actual_opcode, registers, mock_memory_controller)
        self.assertEqual(len(read_side_effect), mock_memory_controller.read.call_count)
        self.assertEqual(count, expected_clocks)
        self.assertTrue(registers.accumulator == 0x01)
        self.assertFalse(registers.zero_flag)
        self.assertFalse(registers.negative_flag)

    def execute_eor_zero(self, actual_opcode, expected_clocks, read_side_effect, **kwargs):

        opcode = OpCode()
        registers = Registers()
        registers.accumulator = 0x66
        registers.negative_flag = True  

        if kwargs:
            for arg in kwargs:
                setattr(registers, arg, kwargs[arg])

        mock_memory_controller = Mock()
        read_side_effect.append(0x66)
        mock_memory_controller.read.side_effect = read_side_effect

        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(actual_opcode, registers, mock_memory_controller)
        self.assertEqual(len(read_side_effect), mock_memory_controller.read.call_count)
        self.assertEqual(count, expected_clocks)
        self.assertEqual(registers.accumulator, 0x00)
        self.assertTrue(registers.zero_flag)
        self.assertFalse(registers.negative_flag)

    def execute_eor_negative(self, actual_opcode, expected_clocks, read_side_effect, **kwargs):

        opcode = OpCode()
        registers = Registers()
        registers.accumulator = 0xf0
        registers.negative_flag = True  

        if kwargs:
            for arg in kwargs:
                setattr(registers, arg, kwargs[arg])

        mock_memory_controller = Mock()
        read_side_effect.append(0x0f)
        mock_memory_controller.read.side_effect = read_side_effect

        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(actual_opcode, registers, mock_memory_controller)
        self.assertEqual(len(read_side_effect), mock_memory_controller.read.call_count)
        self.assertEqual(count, expected_clocks)
        self.assertEqual(registers.accumulator, 0xff)
        self.assertFalse(registers.zero_flag)
        self.assertTrue(registers.negative_flag)

    def test_execute_eor_immediate_positive(self):

        self.execute_eor_positive(0x49, 2, [])

    def test_execute_eor_immediate_zero(self):

        self.execute_eor_zero(0x49, 2, [])

    def test_execute_eor_immediate_negative(self):

        self.execute_eor_negative(0x49, 2, [])

    def test_execute_eor_zeropage_positive(self):

        self.execute_eor_positive(0x45, 3, [0x20])

    def test_execute_eor_zeropage_zero(self):

        self.execute_eor_zero(0x45, 3, [0x20])

    def test_execute_eor_zeropage_negative(self):

        self.execute_eor_negative(0x45, 3, [0x20])

    def test_execute_eor_zeropageX_positive(self):

        self.execute_eor_positive(0x55, 4, [0x20], x_index = 3)

    def test_execute_eor_zeropageX_zero(self):

        self.execute_eor_zero(0x55, 4, [0x20], x_index = 3)

    def test_execute_eor_zeropageX_negative(self):

        self.execute_eor_negative(0x55, 4, [0x20], x_index = 3)

    def test_execute_eor_absolute_positive(self):

        self.execute_eor_positive(0x4d, 4, [0x00, 0x20])

    def test_execute_eor_absolute_zero(self):

        self.execute_eor_zero(0x4d, 4, [0x00, 0x20])

    def test_execute_eor_absolute_negative(self):

        self.execute_eor_negative(0x4d, 4, [0x00, 0x20])

    def test_execute_eor_absoluteX_positive(self):

        self.execute_eor_positive(0x5d, 4, [0x00, 0x20], x_index = 3)

    def test_execute_eor_absoluteX_zero(self):

        self.execute_eor_zero(0x5d, 4, [0x00, 0x20], x_index = 3)

    def test_execute_eor_absoluteX_negative(self):

        self.execute_eor_negative(0x5d, 4, [0x00, 0x20], x_index = 3)

    def test_execute_eor_absoluteX_positive_extracycle(self):

        self.execute_eor_positive(0x5d, 5, [0xfe, 0x20], x_index = 3)

    def test_execute_eor_absoluteX_zero_extracycle(self):

        self.execute_eor_zero(0x5d, 5, [0xfe, 0x20], x_index = 3)

    def test_execute_eor_absoluteX_negative_extracycle(self):

        self.execute_eor_negative(0x5d, 5, [0xfe, 0x20], x_index = 3)

    def test_execute_eor_absoluteY_positive(self):

        self.execute_eor_positive(0x59, 4, [0x00, 0x20], y_index = 3)

    def test_execute_eor_absoluteY_zero(self):

        self.execute_eor_zero(0x59, 4, [0x00, 0x20], y_index = 3)

    def test_execute_eor_absoluteY_negative(self):

        self.execute_eor_negative(0x59, 4, [0x00, 0x20], y_index = 3)

    def test_execute_eor_absoluteY_positive_extracycle(self):

        self.execute_eor_positive(0x59, 5, [0xfe, 0x20], y_index = 3)

    def test_execute_eor_absoluteY_zero_extracycle(self):

        self.execute_eor_zero(0x59, 5, [0xfe, 0x20], y_index = 3)

    def test_execute_eor_absoluteY_negative_extracycle(self):

        self.execute_eor_negative(0x59, 5, [0xfe, 0x20], y_index = 3)

    def test_execute_eor_indirectX_positive(self):

        self.execute_eor_positive(0x41, 6, [0x20, 0x34, 0x12], x_index = 3)

    def test_execute_eor_indirectX_zero(self):

        self.execute_eor_zero(0x41, 6, [0x20, 0x34, 0x12], x_index = 3)

    def test_execute_eor_indirectX_negative(self):

        self.execute_eor_negative(0x41, 6, [0x20, 0x34, 0x12], x_index = 3)

    def test_execute_eor_indirectY_positive(self):

        self.execute_eor_positive(0x51, 5, [0x20, 0x34, 0x12], y_index = 3)

    def test_execute_eor_indirectY_zero(self):

        self.execute_eor_zero(0x51, 5, [0x20, 0x34, 0x12], y_index = 3)

    def test_execute_eor_indirectY_negative(self):

        self.execute_eor_negative(0x51, 5, [0x20, 0x34, 0x12], y_index = 3)

    def test_execute_eor_indirectY_extracycle(self):

        self.execute_eor_positive(0x51, 6, [0x20, 0xfe, 0x12], y_index = 3)

    def test_execute_eor_indirectY_zero_extracycle(self):

        self.execute_eor_zero(0x51, 6, [0x20, 0xfe, 0x12], y_index = 3)

    def test_execute_eor_indirectY_negative_extracycle(self):

        self.execute_eor_negative(0x51, 6, [0x20, 0xfe, 0x12], y_index = 3)

    def execute_ora_positive(self, actual_opcode, expected_clocks, read_side_effect, **kwargs):

        opcode = OpCode()
        registers = Registers()
        registers.accumulator = 0x05
        registers.zero_flag = True
        registers.negative_flag = True  

        if kwargs:
            for arg in kwargs:
                setattr(registers, arg, kwargs[arg])

        mock_memory_controller = Mock()
        read_side_effect.append(0x13)
        mock_memory_controller.read.side_effect = read_side_effect

        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(actual_opcode, registers, mock_memory_controller)
        self.assertEqual(len(read_side_effect), mock_memory_controller.read.call_count)
        self.assertEqual(count, expected_clocks)
        self.assertTrue(registers.accumulator == 0x17)
        self.assertFalse(registers.zero_flag)
        self.assertFalse(registers.negative_flag)

    def execute_ora_zero(self, actual_opcode, expected_clocks, read_side_effect, **kwargs):

        opcode = OpCode()
        registers = Registers()
        registers.accumulator = 0x0
        registers.negative_flag = True  

        if kwargs:
            for arg in kwargs:
                setattr(registers, arg, kwargs[arg])

        mock_memory_controller = Mock()
        read_side_effect.append(0x0)
        mock_memory_controller.read.side_effect = read_side_effect

        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(actual_opcode, registers, mock_memory_controller)
        self.assertEqual(len(read_side_effect), mock_memory_controller.read.call_count)
        self.assertEqual(count, expected_clocks)
        self.assertEqual(registers.accumulator, 0x00)
        self.assertTrue(registers.zero_flag)
        self.assertFalse(registers.negative_flag)

    def execute_ora_negative(self, actual_opcode, expected_clocks, read_side_effect, **kwargs):

        opcode = OpCode()
        registers = Registers()
        registers.accumulator = 0xf2
        registers.negative_flag = True  

        if kwargs:
            for arg in kwargs:
                setattr(registers, arg, kwargs[arg])

        mock_memory_controller = Mock()
        read_side_effect.append(0x1f)
        mock_memory_controller.read.side_effect = read_side_effect

        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(actual_opcode, registers, mock_memory_controller)
        self.assertEqual(len(read_side_effect), mock_memory_controller.read.call_count)
        self.assertEqual(count, expected_clocks)
        self.assertEqual(registers.accumulator, 0xff)
        self.assertFalse(registers.zero_flag)
        self.assertTrue(registers.negative_flag)

    def test_execute_ora_immediate_positive(self):

        self.execute_ora_positive(0x09, 2, [])

    def test_execute_ora_immediate_zero(self):

        self.execute_ora_zero(0x09, 2, [])

    def test_execute_ora_immediate_negative(self):

        self.execute_ora_negative(0x09, 2, [])

    def test_execute_ora_zeropage_positive(self):

        self.execute_ora_positive(0x05, 3, [0x20])

    def test_execute_ora_zeropage_zero(self):

        self.execute_ora_zero(0x05, 3, [0x20])

    def test_execute_ora_zeropage_negative(self):

        self.execute_ora_negative(0x05, 3, [0x20])

    def test_execute_ora_zeropageX_positive(self):

        self.execute_ora_positive(0x15, 4, [0x20], x_index = 3)

    def test_execute_ora_zeropageX_zero(self):

        self.execute_ora_zero(0x15, 4, [0x20], x_index = 3)

    def test_execute_ora_zeropageX_negative(self):

        self.execute_ora_negative(0x15, 4, [0x20], x_index = 3)

    def test_execute_ora_absolute_positive(self):

        self.execute_ora_positive(0x0d, 4, [0x00, 0x20])

    def test_execute_ora_absolute_zero(self):

        self.execute_ora_zero(0x0d, 4, [0x00, 0x20])

    def test_execute_ora_absolute_negative(self):

        self.execute_ora_negative(0x0d, 4, [0x00, 0x20])

    def test_execute_ora_absoluteX_positive(self):

        self.execute_ora_positive(0x1d, 4, [0x00, 0x20], x_index = 3)

    def test_execute_ora_absoluteX_zero(self):

        self.execute_ora_zero(0x1d, 4, [0x00, 0x20], x_index = 3)

    def test_execute_ora_absoluteX_negative(self):

        self.execute_ora_negative(0x1d, 4, [0x00, 0x20], x_index = 3)

    def test_execute_ora_absoluteX_positive_extracycle(self):

        self.execute_ora_positive(0x1d, 5, [0xfe, 0x20], x_index = 3)

    def test_execute_ora_absoluteX_zero_extracycle(self):

        self.execute_ora_zero(0x1d, 5, [0xfe, 0x20], x_index = 3)

    def test_execute_ora_absoluteX_negative_extracycle(self):

        self.execute_ora_negative(0x1d, 5, [0xfe, 0x20], x_index = 3)

    def test_execute_ora_absoluteY_positive(self):

        self.execute_ora_positive(0x19, 4, [0x00, 0x20], y_index = 3)

    def test_execute_ora_absoluteY_zero(self):

        self.execute_ora_zero(0x19, 4, [0x00, 0x20], y_index = 3)

    def test_execute_ora_absoluteY_negative(self):

        self.execute_ora_negative(0x19, 4, [0x00, 0x20], y_index = 3)

    def test_execute_ora_absoluteY_positive_extracycle(self):

        self.execute_ora_positive(0x19, 5, [0xfe, 0x20], y_index = 3)

    def test_execute_ora_absoluteY_zero_extracycle(self):

        self.execute_ora_zero(0x19, 5, [0xfe, 0x20], y_index = 3)

    def test_execute_ora_absoluteY_negative_extracycle(self):

        self.execute_ora_negative(0x19, 5, [0xfe, 0x20], y_index = 3)

    def test_execute_ora_indirectX_positive(self):

        self.execute_ora_positive(0x01, 6, [0x20, 0x34, 0x12], x_index = 3)

    def test_execute_ora_indirectX_zero(self):

        self.execute_ora_zero(0x01, 6, [0x20, 0x34, 0x12], x_index = 3)

    def test_execute_ora_indirectX_negative(self):

        self.execute_ora_negative(0x01, 6, [0x20, 0x34, 0x12], x_index = 3)

    def test_execute_ora_indirectY_positive(self):

        self.execute_ora_positive(0x11, 5, [0x20, 0x34, 0x12], y_index = 3)

    def test_execute_ora_indirectY_zero(self):

        self.execute_ora_zero(0x11, 5, [0x20, 0x34, 0x12], y_index = 3)

    def test_execute_ora_indirectY_negative(self):

        self.execute_ora_negative(0x11, 5, [0x20, 0x34, 0x12], y_index = 3)

    def test_execute_ora_indirectY_extracycle(self):

        self.execute_ora_positive(0x11, 6, [0x20, 0xfe, 0x12], y_index = 3)

    def test_execute_ora_indirectY_zero_extracycle(self):

        self.execute_ora_zero(0x11, 6, [0x20, 0xfe, 0x12], y_index = 3)

    def test_execute_ora_indirectY_negative_extracycle(self):

        self.execute_ora_negative(0x11, 6, [0x20, 0xfe, 0x12], y_index = 3)

if __name__ == '__main__':
    unittest.main()