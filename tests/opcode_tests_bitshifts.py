import unittest

from unittest.mock import patch, Mock
from memory_controller import MemoryController
from registers import Registers
from opcodes import OpCode


class OpCodeTestsBitShifts(unittest.TestCase):

    def test_execute_asl_accumulator_positive(self):

        opcode = OpCode()
        registers = Registers()
        registers.accumulator = 3

        mock_memory_controller = Mock()

        # we're mocking 0x0A 0x21 
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0x0A, registers, mock_memory_controller)
        self.assertEqual(count, 2)
        mock_memory_controller.read.assert_not_called()
        self.assertEqual(registers.pc, 1)
        self.assertEqual(registers.accumulator, 6)
        self.assertFalse(registers.zero_flag)
        self.assertFalse(registers.carry_flag)
        self.assertFalse(registers.negative_flag)

    def test_execute_asl_accumulator_negative(self):

        opcode = OpCode()
        registers = Registers()
        registers.accumulator = -3

        mock_memory_controller = Mock()

        # we're mocking 0x0A 0x21 
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0x0A, registers, mock_memory_controller)
        self.assertEqual(count, 2)
        mock_memory_controller.read.assert_not_called()
        self.assertEqual(registers.pc, 1)
        self.assertEqual(registers.accumulator, 0xfa)
        self.assertFalse(registers.zero_flag)
        self.assertTrue(registers.carry_flag)
        self.assertTrue(registers.negative_flag)

    def test_execute_asl_zeropage(self):

        opcode = OpCode()
        registers = Registers()
        mock_memory_controller = Mock()

        # we're mocking 0x06 0x30
        mock_memory_controller.read.side_effect = [0x30, 0x20]
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0x06, registers, mock_memory_controller)
        self.assertEqual(count, 5)
        self.assertEqual(mock_memory_controller.read.call_count, 2)
        self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
        mock_memory_controller.write.assert_called_with(0x30, 0x40)
        self.assertEqual(registers.pc, 2)
        self.assertFalse(registers.zero_flag)
        self.assertFalse(registers.carry_flag)
        self.assertFalse(registers.negative_flag)        

    def test_execute_asl_zeropage_x(self):

        opcode = OpCode()
        registers = Registers()
        registers.x_index = 3

        mock_memory_controller = Mock()

        # we're mocking 0x16 0x21 so store to [0x0024]
        mock_memory_controller.read.side_effect = [0x21, 0x10]
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0x16, registers, mock_memory_controller)
        self.assertEqual(count, 6)

        # these are checked more thoroughly in addressing_modes_tests
        self.assertEqual(mock_memory_controller.read.call_count, 2)
        self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
        mock_memory_controller.write.assert_called_with(0x24, 0x20)
        self.assertEqual(registers.pc, 2)
        self.assertFalse(registers.zero_flag)
        self.assertFalse(registers.carry_flag)
        self.assertFalse(registers.negative_flag)        

    def test_execute_asl_zeropage_x_wrap(self):

        opcode = OpCode()
        registers = Registers()
        registers.x_index = 3

        mock_memory_controller = Mock()

        # we're mocking 0x16 0x21 so store to [0x0024]
        mock_memory_controller.read.side_effect = [0xfe, 0xf0]
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0x16, registers, mock_memory_controller)
        self.assertEqual(count, 6)

        # these are checked more thoroughly in addressing_modes_tests
        self.assertEqual(mock_memory_controller.read.call_count, 2)
        self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
        mock_memory_controller.write.assert_called_with(0x01, 0xe0)
        self.assertEqual(registers.pc, 2)
        self.assertFalse(registers.zero_flag)
        self.assertTrue(registers.carry_flag)
        self.assertTrue(registers.negative_flag)        

    def test_execute_asl_absolute(self):

        opcode = OpCode()
        registers = Registers()
        registers.accumulator = 0x20

        mock_memory_controller = Mock()

        # we're mocking 0x0E 0x0 0x20 so store to [0x2000]
        mock_memory_controller.read.side_effect = [0, 0x20, 0x21]
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0x0E, registers, mock_memory_controller)
        self.assertEqual(count, 6)

        # these are checked more thoroughly in addressing_modes_tests
        self.assertEqual(mock_memory_controller.read.call_count, 3)
        self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
        mock_memory_controller.write.assert_called_with(0x2000, 0x42)
        self.assertEqual(registers.pc, 3)
        self.assertFalse(registers.zero_flag)
        self.assertFalse(registers.carry_flag)
        self.assertFalse(registers.negative_flag)        

    def test_execute_asl_absolute_x(self):

        opcode = OpCode()
        registers = Registers()
        registers.x_index = 3

        mock_memory_controller = Mock()

        # we're mocking 0x1E 0x2100 so write is to [0x2103]
        mock_memory_controller.read.side_effect = [0, 0x21, 0xfe]
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0x1E, registers, mock_memory_controller)
        self.assertEqual(count, 7)

        # these are checked more thoroughly in addressing_modes_tests
        self.assertEqual(mock_memory_controller.read.call_count, 3)
        mock_memory_controller.write.assert_called_with(0x2103, 0xfc)
        self.assertEqual(registers.pc, 3)
        self.assertFalse(registers.zero_flag)
        self.assertTrue(registers.carry_flag)
        self.assertTrue(registers.negative_flag)        

    def test_execute_rol_accumulator_carry_clear_sign_clear(self):

        opcode = OpCode()
        registers = Registers()
        registers.accumulator = 3

        mock_memory_controller = Mock()

        # we're mocking 0x2A
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0x2A, registers, mock_memory_controller)
        self.assertEqual(count, 2)
        mock_memory_controller.read.assert_not_called()
        self.assertEqual(registers.pc, 1)
        self.assertEqual(registers.accumulator, 6)
        self.assertFalse(registers.zero_flag)
        self.assertFalse(registers.carry_flag)
        self.assertFalse(registers.negative_flag)

    def test_execute_rol_accumulator_carry_set_sign_clear(self):

        opcode = OpCode()
        registers = Registers()
        registers.accumulator = 3
        registers.carry_flag = True

        mock_memory_controller = Mock()

        # we're mocking 0x2A
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0x2A, registers, mock_memory_controller)
        self.assertEqual(count, 2)
        mock_memory_controller.read.assert_not_called()
        self.assertEqual(registers.pc, 1)
        self.assertEqual(registers.accumulator, 7)
        self.assertFalse(registers.zero_flag)
        self.assertFalse(registers.carry_flag)
        self.assertFalse(registers.negative_flag)

    def test_execute_rol_accumulator_carry_clear_sign_set(self):

        opcode = OpCode()
        registers = Registers()
        registers.accumulator = 0xc0

        mock_memory_controller = Mock()

        # we're mocking 0x2A
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0x2A, registers, mock_memory_controller)
        self.assertEqual(count, 2)
        mock_memory_controller.read.assert_not_called()
        self.assertEqual(registers.pc, 1)
        self.assertEqual(registers.accumulator, 0x80)
        self.assertFalse(registers.zero_flag)
        self.assertTrue(registers.carry_flag)
        self.assertTrue(registers.negative_flag)

    def test_execute_rol_zeropage_carry_clear_sign_clear(self):

        opcode = OpCode()
        registers = Registers()

        mock_memory_controller = Mock()
        mock_memory_controller.read.side_effect = [0x30, 3]

        # we're mocking 0x26 0x30 and [0x30] = 3
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0x26, registers, mock_memory_controller)
        self.assertEqual(count, 5)
        self.assertEqual(mock_memory_controller.read.call_count, 2)
        mock_memory_controller.write.assert_called_with(0x30, 6)
        self.assertEqual(registers.pc, 2)
        self.assertFalse(registers.zero_flag)
        self.assertFalse(registers.carry_flag)
        self.assertFalse(registers.negative_flag)

    def test_execute_rol_zeropage_carry_set_sign_clear(self):

        opcode = OpCode()
        registers = Registers()
        registers.carry_flag = True

        mock_memory_controller = Mock()
        mock_memory_controller.read.side_effect = [0x30, 3]

        # we're mocking 0x26 0x30 and [0x30] = 3
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0x26, registers, mock_memory_controller)
        self.assertEqual(count, 5)
        self.assertEqual(mock_memory_controller.read.call_count, 2)        
        mock_memory_controller.write.assert_called_with(0x30, 7)
        self.assertEqual(registers.pc, 2)
        self.assertFalse(registers.zero_flag)
        self.assertFalse(registers.carry_flag)
        self.assertFalse(registers.negative_flag)

    def test_execute_rol_zeropage_carry_clear_sign_set(self):

        opcode = OpCode()
        registers = Registers()
        registers.accumulator = 0xc0

        mock_memory_controller = Mock()
        mock_memory_controller.read.side_effect = [0x30, 0xc0]

        # we're mocking 0x26 0x30 and [0x30] = 0xc0
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0x26, registers, mock_memory_controller)
        self.assertEqual(count, 5)
        mock_memory_controller.read.assert_not_called()
        mock_memory_controller.write.assert_called_with(0x30, 0x80)
        self.assertEqual(registers.pc, 2)
        self.assertFalse(registers.zero_flag)
        self.assertTrue(registers.carry_flag)
        self.assertTrue(registers.negative_flag)

if __name__ == '__main__':
    unittest.main()