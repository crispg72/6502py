import unittest

from unittest.mock import patch, Mock
from memory_controller import MemoryController
from registers import Registers
from opcodes import OpCode


class OpCodeTestsIncAndDec(unittest.TestCase):

    def execute_inc_positive(self, actual_opcode, expected_clocks, pc_value, mock_memory_controller, **kwargs):

        opcode = OpCode()
        registers = Registers()

        if kwargs:
            for arg in kwargs:
                setattr(registers, arg, kwargs[arg])

        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(actual_opcode, registers, mock_memory_controller)
        self.assertEqual(count, expected_clocks)
        self.assertEqual(registers.pc, pc_value)
        self.assertFalse(registers.zero_flag)
        self.assertFalse(registers.negative_flag)

    def test_execute_inc_zeropage_positive(self):

        mock_memory_controller = Mock()
        mock_memory_controller.read.side_effect = [0x21, 6]
        # we're mocking 0xE6 0x21 and [0x21] = 6
        self.execute_inc_positive(0xE6, 5, 2, mock_memory_controller)
        self.assertEqual(mock_memory_controller.read.call_count, 2)
        mock_memory_controller.write.assert_called_with(0x21, 7)

    def test_execute_inc_absolute_positive(self):

        mock_memory_controller = Mock()
        mock_memory_controller.read.side_effect = [0x00, 0x21, 6]
        # we're mocking 0xEE 0x00 0x21 and [0x2100] = 6
        self.execute_inc_positive(0xEE, 6, 3, mock_memory_controller)
        self.assertEqual(mock_memory_controller.read.call_count, 3)
        mock_memory_controller.write.assert_called_with(0x2100, 7)

    def test_execute_inc_zeropageX_positive(self):

        mock_memory_controller = Mock()
        mock_memory_controller.read.side_effect = [0x21, 6]
        # we're mocking 0xF6 0x21 and [0x24] = 6

        self.execute_inc_positive(0xF6, 6, 2, mock_memory_controller, x_index = 3)
        self.assertEqual(mock_memory_controller.read.call_count, 2)
        mock_memory_controller.write.assert_called_with(0x24, 7)

    def test_execute_inc_absoluteX_positive(self):

        mock_memory_controller = Mock()
        mock_memory_controller.read.side_effect = [0, 0x20, 6]
        # we're mocking 0xFE 0x00 0x20 and [0x2003] = 6
        self.execute_inc_positive(0xFE, 7, 3, mock_memory_controller, x_index = 3)
        self.assertEqual(mock_memory_controller.read.call_count, 3)
        mock_memory_controller.write.assert_called_with(0x2003, 7)

    def test_execute_inc_zeropage_negative(self):

        opcode = OpCode()
        registers = Registers()

        mock_memory_controller = Mock()
        mock_memory_controller.read.side_effect = [0x21, 0xfe]

        # we're mocking 0xE6 0x21 and [0x21] = 0xfe
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0xE6, registers, mock_memory_controller)
        self.assertEqual(count, 5)
        self.assertEqual(mock_memory_controller.read.call_count, 2)
        self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
        self.assertEqual(mock_memory_controller.read.call_args_list[1], unittest.mock.call(0x21))
        mock_memory_controller.write.assert_called_with(0x21, 0xff)
        self.assertEqual(registers.pc, 2)
        self.assertFalse(registers.zero_flag)
        self.assertTrue(registers.negative_flag)

    def test_execute_inc_zeropage_zero(self):

        opcode = OpCode()
        registers = Registers()

        mock_memory_controller = Mock()
        mock_memory_controller.read.side_effect = [0x21, 0xff]

        # we're mocking 0xE6 0x21 and [0x21] = 0xff
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0xE6, registers, mock_memory_controller)
        self.assertEqual(count, 5)
        self.assertEqual(mock_memory_controller.read.call_count, 2)
        self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
        self.assertEqual(mock_memory_controller.read.call_args_list[1], unittest.mock.call(0x21))
        mock_memory_controller.write.assert_called_with(0x21, 0)
        self.assertEqual(registers.pc, 2)
        self.assertTrue(registers.zero_flag)
        self.assertFalse(registers.negative_flag)

    def execute_dec_positive(self, actual_opcode, expected_clocks, mock_memory_controller, **kwargs):

        opcode = OpCode()
        registers = Registers()

        if kwargs:
            for arg in kwargs:
                setattr(registers, arg, kwargs[arg])

        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(actual_opcode, registers, mock_memory_controller)
        self.assertEqual(count, expected_clocks)
        self.assertEqual(registers.pc, mock_memory_controller.read.call_count)
        self.assertFalse(registers.zero_flag)
        self.assertFalse(registers.negative_flag)

    def test_execute_dec_zeropage_positive(self):

        mock_memory_controller = Mock()
        mock_memory_controller.read.side_effect = [0x21, 6]

        # we're mocking 0xC6 0x21 and [0x21] = 6
        self.execute_dec_positive(0xC6, 5, mock_memory_controller)
        self.assertEqual(mock_memory_controller.read.call_count, 2)
        mock_memory_controller.write.assert_called_with(0x21, 5)

    def test_execute_dec_zeropageX_positive(self):

        mock_memory_controller = Mock()
        mock_memory_controller.read.side_effect = [0x21, 6]
        # we're mocking 0xD6 0x21 and [0x24] = 6

        self.execute_dec_positive(0xD6, 6, mock_memory_controller, x_index = 3)
        self.assertEqual(mock_memory_controller.read.call_count, 2)
        mock_memory_controller.write.assert_called_with(0x24, 5)

    def test_execute_dec_absolute_positive(self):

        mock_memory_controller = Mock()
        mock_memory_controller.read.side_effect = [0x00, 0x21, 6]
        # we're mocking 0xCE 0x00, 0x21 and [0x2100] = 6

        self.execute_dec_positive(0xCE, 6, mock_memory_controller)
        self.assertEqual(mock_memory_controller.read.call_count, 3)
        mock_memory_controller.write.assert_called_with(0x2100, 5)

    def test_execute_dec_absoluteX_positive(self):

        mock_memory_controller = Mock()
        mock_memory_controller.read.side_effect = [0x00, 0x21, 6]
        # we're mocking 0xDE 0x00, 0x21 and [0x2103] = 6

        self.execute_dec_positive(0xDE, 7, mock_memory_controller, x_index = 3)
        self.assertEqual(mock_memory_controller.read.call_count, 3)
        mock_memory_controller.write.assert_called_with(0x2103, 5)

    def test_execute_dec_zeropage_negative(self):

        opcode = OpCode()
        registers = Registers()

        mock_memory_controller = Mock()
        mock_memory_controller.read.side_effect = [0x21, 0xfe]

        # we're mocking 0xC6 0x21 and [0x21] = 0xfe
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0xC6, registers, mock_memory_controller)
        self.assertEqual(count, 5)
        self.assertEqual(mock_memory_controller.read.call_count, 2)
        self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
        self.assertEqual(mock_memory_controller.read.call_args_list[1], unittest.mock.call(0x21))
        mock_memory_controller.write.assert_called_with(0x21, 0xfd)
        self.assertEqual(registers.pc, 2)
        self.assertFalse(registers.zero_flag)
        self.assertTrue(registers.negative_flag)

    def test_execute_dec_zeropage_zero(self):

        opcode = OpCode()
        registers = Registers()

        mock_memory_controller = Mock()
        mock_memory_controller.read.side_effect = [0x21, 1]

        # we're mocking 0xC6 0x21 and [0x21] = 1
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0xC6, registers, mock_memory_controller)
        self.assertEqual(count, 5)
        self.assertEqual(mock_memory_controller.read.call_count, 2)
        self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
        self.assertEqual(mock_memory_controller.read.call_args_list[1], unittest.mock.call(0x21))
        mock_memory_controller.write.assert_called_with(0x21, 0)
        self.assertEqual(registers.pc, 2)
        self.assertTrue(registers.zero_flag)
        self.assertFalse(registers.negative_flag)

if __name__ == '__main__':
    unittest.main()