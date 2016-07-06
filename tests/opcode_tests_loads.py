import unittest

from unittest.mock import patch
from memory_controller import MemoryController
from registers import Registers
from opcodes import OpCode


class OpCodeTests(unittest.TestCase):
    
    def test_execute_lda_immediate(self):

        registers = Registers()
        registers.zero_flag = True
        registers.negative_flag = True  

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            mock_memory_controller.read.return_value = 0x22
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = OpCode.execute(0xA9, registers, mock_memory_controller)
            self.assertEqual(count, 2)
            mock_memory_controller.read.assert_called_with(1)
            self.assertTrue(registers.accumulator == 0x22)
            self.assertEqual(registers.pc, 2)
            self.assertFalse(registers.zero_flag)
            self.assertFalse(registers.negative_flag)

    def test_execute_lda_immediate_zero(self):

        registers = Registers()
        registers.zero_flag = False
        registers.negative_flag = True  

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            mock_memory_controller.read.return_value = 0x0
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = OpCode.execute(0xA9, registers, mock_memory_controller)
            self.assertEqual(count, 2)
            mock_memory_controller.read.assert_called_with(1)
            self.assertTrue(registers.accumulator == 0x0)
            self.assertEqual(registers.pc, 2)
            self.assertTrue(registers.zero_flag)
            self.assertFalse(registers.negative_flag)

    def test_execute_lda_immediate_negative(self):

        registers = Registers()
        registers.zero_flag = True
        registers.negative_flag = False  

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            mock_memory_controller.read.return_value = -1
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = OpCode.execute(0xA9, registers, mock_memory_controller)
            self.assertEqual(count, 2)
            mock_memory_controller.read.assert_called_with(1)
            self.assertTrue(registers.accumulator == -1)
            self.assertEqual(registers.pc, 2)
            self.assertFalse(registers.zero_flag)
            self.assertTrue(registers.negative_flag)

    def test_execute_ldx_immediate(self):

        registers = Registers()
        registers.zero_flag = True
        registers.negative_flag = True  

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            mock_memory_controller.read.return_value = 0x22
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = OpCode.execute(0xA2, registers, mock_memory_controller)
            self.assertEqual(count, 2)
            mock_memory_controller.read.assert_called_with(1)
            self.assertTrue(registers.x_index == 0x22)
            self.assertEqual(registers.pc, 2)
            self.assertFalse(registers.zero_flag)
            self.assertFalse(registers.negative_flag)

    def test_execute_ldx_immediate_zero(self):

        registers = Registers()
        registers.zero_flag = False
        registers.negative_flag = True  

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            mock_memory_controller.read.return_value = 0x0
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = OpCode.execute(0xA2, registers, mock_memory_controller)
            self.assertEqual(count, 2)
            mock_memory_controller.read.assert_called_with(1)
            self.assertTrue(registers.x_index == 0x0)
            self.assertEqual(registers.pc, 2)
            self.assertTrue(registers.zero_flag)
            self.assertFalse(registers.negative_flag)

    def test_execute_ldx_immediate_negative(self):

        registers = Registers()
        registers.zero_flag = True
        registers.negative_flag = False  

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            mock_memory_controller.read.return_value = -1
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = OpCode.execute(0xA2, registers, mock_memory_controller)
            self.assertEqual(count, 2)
            mock_memory_controller.read.assert_called_with(1)
            self.assertTrue(registers.x_index == -1)
            self.assertEqual(registers.pc, 2)
            self.assertFalse(registers.zero_flag)
            self.assertTrue(registers.negative_flag)

    def test_execute_ldy_immediate(self):

        registers = Registers()
        registers.zero_flag = True
        registers.negative_flag = True  

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            mock_memory_controller.read.return_value = 0x22
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = OpCode.execute(0xA0, registers, mock_memory_controller)
            self.assertEqual(count, 2)
            mock_memory_controller.read.assert_called_with(1)
            self.assertTrue(registers.y_index == 0x22)
            self.assertEqual(registers.pc, 2)
            self.assertFalse(registers.zero_flag)
            self.assertFalse(registers.negative_flag)

    def test_execute_ldy_immediate_zero(self):

        registers = Registers()
        registers.zero_flag = False
        registers.negative_flag = True  

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            mock_memory_controller.read.return_value = 0x0
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = OpCode.execute(0xA0, registers, mock_memory_controller)
            self.assertEqual(count, 2)
            mock_memory_controller.read.assert_called_with(1)
            self.assertTrue(registers.y_index == 0x0)
            self.assertEqual(registers.pc, 2)
            self.assertTrue(registers.zero_flag)
            self.assertFalse(registers.negative_flag)

    def test_execute_ldy_immediate_negative(self):

        registers = Registers()
        registers.zero_flag = True
        registers.negative_flag = False  

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            mock_memory_controller.read.return_value = -1
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = OpCode.execute(0xA0, registers, mock_memory_controller)
            self.assertEqual(count, 2)
            mock_memory_controller.read.assert_called_with(1)
            self.assertTrue(registers.y_index == -1)
            self.assertEqual(registers.pc, 2)
            self.assertFalse(registers.zero_flag)
            self.assertTrue(registers.negative_flag)

    def test_execute_lda_zeropage(self):

        registers = Registers()
        registers.zero_flag = True
        registers.negative_flag = True  

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # we're mocking 0xa5 0x21 and value at [0x0021] = 1
            mock_memory_controller.read.side_effect = [0x21, 1]
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = OpCode.execute(0xA5, registers, mock_memory_controller)
            self.assertEqual(count, 3)
            self.assertEqual(mock_memory_controller.read.call_count, 2)
            self.assertEqual(mock_memory_controller.read.call_args_list[1], unittest.mock.call(0x21))
            self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
            self.assertEqual(registers.pc, 2)
            self.assertEqual(registers.accumulator, 1)
            self.assertFalse(registers.zero_flag)
            self.assertFalse(registers.negative_flag)

    def test_execute_ldx_zeropage(self):

        registers = Registers()
        registers.zero_flag = True
        registers.negative_flag = True  

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # we're mocking 0xa5 0x21 and value at [0x0021] = 1
            mock_memory_controller.read.side_effect = [0x21, 1]
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = OpCode.execute(0xA6, registers, mock_memory_controller)
            self.assertEqual(count, 3)
            self.assertEqual(mock_memory_controller.read.call_count, 2)
            self.assertEqual(mock_memory_controller.read.call_args_list[1], unittest.mock.call(0x21))
            self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
            self.assertEqual(registers.pc, 2)
            self.assertEqual(registers.x_index, 1)
            self.assertFalse(registers.zero_flag)
            self.assertFalse(registers.negative_flag)

    def test_execute_ldy_zeropage(self):

        registers = Registers()
        registers.zero_flag = True
        registers.negative_flag = True  

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # we're mocking 0xa5 0x21 and value at [0x0021] = 1
            mock_memory_controller.read.side_effect = [0x21, 1]
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = OpCode.execute(0xA4, registers, mock_memory_controller)
            self.assertEqual(count, 3)
            self.assertEqual(mock_memory_controller.read.call_count, 2)
            self.assertEqual(mock_memory_controller.read.call_args_list[1], unittest.mock.call(0x21))
            self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
            self.assertEqual(registers.pc, 2)
            self.assertEqual(registers.y_index, 1)
            self.assertFalse(registers.zero_flag)
            self.assertFalse(registers.negative_flag)

    def test_execute_lda_absolute(self):

        registers = Registers()
        registers.zero_flag = True
        registers.negative_flag = True  

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # we're mocking 0xa5 0x21 and value at [0x0021] = 1
            mock_memory_controller.read.side_effect = [0x21, 0x22, 1]
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = OpCode.execute(0xAD, registers, mock_memory_controller)
            self.assertEqual(count, 4)

            # these are checked more thoroughly in addressing_modes_tests
            self.assertEqual(mock_memory_controller.read.call_count, 3)
            self.assertEqual(registers.pc, 3)
            self.assertEqual(registers.accumulator, 1)
            self.assertFalse(registers.zero_flag)
            self.assertFalse(registers.negative_flag)

    def test_execute_ldx_absolute(self):

        registers = Registers()
        registers.zero_flag = False
        registers.negative_flag = True  

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # we're mocking 0xa5 0x21 and value at [0x0021] = 1
            mock_memory_controller.read.side_effect = [0x21, 0x22, 0]
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = OpCode.execute(0xAE, registers, mock_memory_controller)
            self.assertEqual(count, 4)

            # these are checked more thoroughly in addressing_modes_tests
            self.assertEqual(mock_memory_controller.read.call_count, 3)
            self.assertEqual(registers.pc, 3)
            self.assertEqual(registers.x_index, 0)
            self.assertTrue(registers.zero_flag)
            self.assertFalse(registers.negative_flag)

    def test_execute_ldy_absolute(self):

        registers = Registers()
        registers.zero_flag = True
        registers.negative_flag = False  

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # we're mocking 0xa5 0x21 and value at [0x0021] = 1
            mock_memory_controller.read.side_effect = [0x21, 0x22, 0xf0]
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = OpCode.execute(0xAC, registers, mock_memory_controller)
            self.assertEqual(count, 4)

            # these are checked more thoroughly in addressing_modes_tests
            self.assertEqual(mock_memory_controller.read.call_count, 3)
            self.assertEqual(registers.pc, 3)
            self.assertEqual(registers.x_index, 0)
            self.assertFalse(registers.zero_flag)
            self.assertTrue(registers.negative_flag)

if __name__ == '__main__':
    unittest.main()