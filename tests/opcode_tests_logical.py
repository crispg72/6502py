import unittest

from unittest.mock import patch, Mock
from memory_controller import MemoryController
from registers import Registers
from opcodes import OpCode


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

if __name__ == '__main__':
    unittest.main()