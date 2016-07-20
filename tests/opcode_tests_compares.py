import unittest

from unittest.mock import patch, Mock
from memory_controller import MemoryController
from registers import Registers
from opcodes import OpCode


class OpCodeTestsCompares(unittest.TestCase):

    def test_execute_cmp_immediate_lessthan(self):

        registers = Registers()
        registers.accumulator = 3

        mock_memory_controller = Mock()
        mock_memory_controller.read.side_effect = [0x21]

        # we're mocking 0xC9 0x21 
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = OpCode.execute(0xC9, registers, mock_memory_controller)
        self.assertEqual(count, 2)
        self.assertEqual(mock_memory_controller.read.call_count, 1)
        self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
        self.assertEqual(registers.pc, 2)
        self.assertFalse(registers.zero_flag)
        self.assertFalse(registers.carry_flag)
        self.assertTrue(registers.negative_flag)

    def test_execute_cmp_immediate_greaterthan(self):

        registers = Registers()
        registers.accumulator = 4

        mock_memory_controller = Mock()
        mock_memory_controller.read.side_effect = [0x3]

        # we're mocking 0xC9 0x21 
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = OpCode.execute(0xC9, registers, mock_memory_controller)
        self.assertEqual(count, 2)
        self.assertEqual(mock_memory_controller.read.call_count, 1)
        self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
        self.assertEqual(registers.pc, 2)
        self.assertFalse(registers.zero_flag)
        self.assertTrue(registers.carry_flag)
        self.assertFalse(registers.negative_flag)

    def test_execute_cmp_immediate_equalto(self):

        registers = Registers()
        registers.accumulator = 4

        mock_memory_controller = Mock()
        mock_memory_controller.read.side_effect = [0x4]

        # we're mocking 0xC9 0x21 
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = OpCode.execute(0xC9, registers, mock_memory_controller)
        self.assertEqual(count, 2)
        self.assertEqual(mock_memory_controller.read.call_count, 1)
        self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
        self.assertEqual(registers.pc, 2)
        self.assertTrue(registers.zero_flag)
        self.assertTrue(registers.carry_flag)
        self.assertFalse(registers.negative_flag)

    def test_execute_cpx_immediate_lessthan(self):

        registers = Registers()
        registers.x_index = 3

        mock_memory_controller = Mock()
        mock_memory_controller.read.side_effect = [0x21]

        # we're mocking 0xE0 0x21 
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = OpCode.execute(0xE0, registers, mock_memory_controller)
        self.assertEqual(count, 2)
        self.assertEqual(mock_memory_controller.read.call_count, 1)
        self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
        self.assertEqual(registers.pc, 2)
        self.assertFalse(registers.zero_flag)
        self.assertFalse(registers.carry_flag)
        self.assertTrue(registers.negative_flag)

    def test_execute_cpx_immediate_greaterthan(self):

        registers = Registers()
        registers.x_index = 4

        mock_memory_controller = Mock()
        mock_memory_controller.read.side_effect = [0x3]

        # we're mocking 0xE0 0x03 
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = OpCode.execute(0xE0, registers, mock_memory_controller)
        self.assertEqual(count, 2)
        self.assertEqual(mock_memory_controller.read.call_count, 1)
        self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
        self.assertEqual(registers.pc, 2)
        self.assertFalse(registers.zero_flag)
        self.assertTrue(registers.carry_flag)
        self.assertFalse(registers.negative_flag)

    def test_execute_cpx_immediate_equalto(self):

        registers = Registers()
        registers.x_index = 4

        mock_memory_controller = Mock()
        mock_memory_controller.read.side_effect = [0x4]

        # we're mocking 0xE0 0x04 
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = OpCode.execute(0xE0, registers, mock_memory_controller)
        self.assertEqual(count, 2)
        self.assertEqual(mock_memory_controller.read.call_count, 1)
        self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
        self.assertEqual(registers.pc, 2)
        self.assertTrue(registers.zero_flag)
        self.assertTrue(registers.carry_flag)
        self.assertFalse(registers.negative_flag)

    def test_execute_cpy_immediate_lessthan(self):

        registers = Registers()
        registers.y_index = 3

        mock_memory_controller = Mock()
        mock_memory_controller.read.side_effect = [0x21]

        # we're mocking 0xC0 0x21 
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = OpCode.execute(0xC0, registers, mock_memory_controller)
        self.assertEqual(count, 2)
        self.assertEqual(mock_memory_controller.read.call_count, 1)
        self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
        self.assertEqual(registers.pc, 2)
        self.assertFalse(registers.zero_flag)
        self.assertFalse(registers.carry_flag)
        self.assertTrue(registers.negative_flag)

    def test_execute_cpy_immediate_greaterthan(self):

        registers = Registers()
        registers.y_index = 4

        mock_memory_controller = Mock()
        mock_memory_controller.read.side_effect = [0x3]

        # we're mocking 0xE0 0x03 
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = OpCode.execute(0xC0, registers, mock_memory_controller)
        self.assertEqual(count, 2)
        self.assertEqual(mock_memory_controller.read.call_count, 1)
        self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
        self.assertEqual(registers.pc, 2)
        self.assertFalse(registers.zero_flag)
        self.assertTrue(registers.carry_flag)
        self.assertFalse(registers.negative_flag)

    def test_execute_cpy_immediate_equalto(self):

        registers = Registers()
        registers.y_index = 4

        mock_memory_controller = Mock()
        mock_memory_controller.read.side_effect = [0x4]

        # we're mocking 0xE0 0x04 
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = OpCode.execute(0xC0, registers, mock_memory_controller)
        self.assertEqual(count, 2)
        self.assertEqual(mock_memory_controller.read.call_count, 1)
        self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
        self.assertEqual(registers.pc, 2)
        self.assertTrue(registers.zero_flag)
        self.assertTrue(registers.carry_flag)
        self.assertFalse(registers.negative_flag)

    def test_execute_cmp_zeropage_lessthan(self):

        registers = Registers()
        registers.accumulator = 3

        mock_memory_controller = Mock()
        mock_memory_controller.read.side_effect = [0x21, 6]

        # we're mocking 0xC5 0x21 and [0x21] = 6
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = OpCode.execute(0xC5, registers, mock_memory_controller)
        self.assertEqual(count, 3)
        self.assertEqual(mock_memory_controller.read.call_count, 2)
        self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
        self.assertEqual(mock_memory_controller.read.call_args_list[1], unittest.mock.call(0x21))
        self.assertEqual(registers.pc, 2)
        self.assertFalse(registers.zero_flag)
        self.assertFalse(registers.carry_flag)
        self.assertTrue(registers.negative_flag)

    def test_execute_cmp_zeropage_greaterthan(self):

        registers = Registers()
        registers.accumulator = 4

        mock_memory_controller = Mock()
        mock_memory_controller.read.side_effect = [0x21, 0x3]

        # we're mocking 0xC5 0x21 and [0x21] = 3
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = OpCode.execute(0xC5, registers, mock_memory_controller)
        self.assertEqual(count, 3)
        self.assertEqual(mock_memory_controller.read.call_count, 2)
        self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
        self.assertEqual(mock_memory_controller.read.call_args_list[1], unittest.mock.call(0x21))
        self.assertEqual(registers.pc, 2)
        self.assertFalse(registers.zero_flag)
        self.assertTrue(registers.carry_flag)
        self.assertFalse(registers.negative_flag)

    def test_execute_cmp_zeropage_equalto(self):

        registers = Registers()
        registers.accumulator = 4

        mock_memory_controller = Mock()
        mock_memory_controller.read.side_effect = [0x21, 0x4]

        # we're mocking 0xC5 0x21 
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = OpCode.execute(0xC5, registers, mock_memory_controller)
        self.assertEqual(count, 3)
        self.assertEqual(mock_memory_controller.read.call_count, 2)
        self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
        self.assertEqual(mock_memory_controller.read.call_args_list[1], unittest.mock.call(0x21))
        self.assertEqual(registers.pc, 2)
        self.assertTrue(registers.zero_flag)
        self.assertTrue(registers.carry_flag)
        self.assertFalse(registers.negative_flag)

    def test_execute_cpx_zeropage_lessthan(self):

        registers = Registers()
        registers.x_index = 3

        mock_memory_controller = Mock()
        mock_memory_controller.read.side_effect = [0x21, 6]

        # we're mocking 0xE4 0x21 and [0x21] = 6
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = OpCode.execute(0xE4, registers, mock_memory_controller)
        self.assertEqual(count, 3)
        self.assertEqual(mock_memory_controller.read.call_count, 2)
        self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
        self.assertEqual(mock_memory_controller.read.call_args_list[1], unittest.mock.call(0x21))
        self.assertEqual(registers.pc, 2)
        self.assertFalse(registers.zero_flag)
        self.assertFalse(registers.carry_flag)
        self.assertTrue(registers.negative_flag)

    def test_execute_cpx_zeropage_greaterthan(self):

        registers = Registers()
        registers.x_index = 4

        mock_memory_controller = Mock()
        mock_memory_controller.read.side_effect = [0x21, 0x3]

        # we're mocking 0xE4 0x21 and [0x21] = 3
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = OpCode.execute(0xE4, registers, mock_memory_controller)
        self.assertEqual(count, 3)
        self.assertEqual(mock_memory_controller.read.call_count, 2)
        self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
        self.assertEqual(mock_memory_controller.read.call_args_list[1], unittest.mock.call(0x21))
        self.assertEqual(registers.pc, 2)
        self.assertFalse(registers.zero_flag)
        self.assertTrue(registers.carry_flag)
        self.assertFalse(registers.negative_flag)

    def test_execute_cpx_zeropage_equalto(self):

        registers = Registers()
        registers.x_index = 4

        mock_memory_controller = Mock()
        mock_memory_controller.read.side_effect = [0x21, 0x4]

        # we're mocking 0xE4 0x21 
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = OpCode.execute(0xE4, registers, mock_memory_controller)
        self.assertEqual(count, 3)
        self.assertEqual(mock_memory_controller.read.call_count, 2)
        self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
        self.assertEqual(mock_memory_controller.read.call_args_list[1], unittest.mock.call(0x21))
        self.assertEqual(registers.pc, 2)
        self.assertTrue(registers.zero_flag)
        self.assertTrue(registers.carry_flag)
        self.assertFalse(registers.negative_flag)

    def test_execute_cpy_zeropage_lessthan(self):

        registers = Registers()
        registers.y_index = 3

        mock_memory_controller = Mock()
        mock_memory_controller.read.side_effect = [0x21, 6]

        # we're mocking 0xC4 0x21 and [0x21] = 6
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = OpCode.execute(0xC4, registers, mock_memory_controller)
        self.assertEqual(count, 3)
        self.assertEqual(mock_memory_controller.read.call_count, 2)
        self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
        self.assertEqual(mock_memory_controller.read.call_args_list[1], unittest.mock.call(0x21))
        self.assertEqual(registers.pc, 2)
        self.assertFalse(registers.zero_flag)
        self.assertFalse(registers.carry_flag)
        self.assertTrue(registers.negative_flag)

    def test_execute_cpy_zeropage_greaterthan(self):

        registers = Registers()
        registers.y_index = 4

        mock_memory_controller = Mock()
        mock_memory_controller.read.side_effect = [0x21, 0x3]

        # we're mocking 0xC4 0x21 and [0x21] = 3
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = OpCode.execute(0xC4, registers, mock_memory_controller)
        self.assertEqual(count, 3)
        self.assertEqual(mock_memory_controller.read.call_count, 2)
        self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
        self.assertEqual(mock_memory_controller.read.call_args_list[1], unittest.mock.call(0x21))
        self.assertEqual(registers.pc, 2)
        self.assertFalse(registers.zero_flag)
        self.assertTrue(registers.carry_flag)
        self.assertFalse(registers.negative_flag)

    def test_execute_cpy_zeropage_equalto(self):

        registers = Registers()
        registers.y_index = 4

        mock_memory_controller = Mock()
        mock_memory_controller.read.side_effect = [0x21, 0x4]

        # we're mocking 0xC4 0x21 
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = OpCode.execute(0xC4, registers, mock_memory_controller)
        self.assertEqual(count, 3)
        self.assertEqual(mock_memory_controller.read.call_count, 2)
        self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
        self.assertEqual(mock_memory_controller.read.call_args_list[1], unittest.mock.call(0x21))
        self.assertEqual(registers.pc, 2)
        self.assertTrue(registers.zero_flag)
        self.assertTrue(registers.carry_flag)
        self.assertFalse(registers.negative_flag)

if __name__ == '__main__':
    unittest.main()