import unittest

from unittest.mock import patch
from memory_controller import MemoryController
from registers import Registers
from opcodes import OpCode


class OpCodeTests(unittest.TestCase):
    
    def test_execute_nop(self):

        registers = Registers()

        with patch.object(MemoryController, 'read', return_value = None) as mock_memory_controller:
            count = OpCode.execute(0xEA, registers, mock_memory_controller)
            self.assertEqual(count, 2)
            mock_memory_controller.assert_not_called()
            self.assertTrue(registers == Registers())

    def test_execute_tax(self):

        registers = Registers()
        dummy_value = 0x7c # (positive, not zero)
        registers.accumulator =  dummy_value

        with patch.object(MemoryController, 'read', return_value = None) as mock_memory_controller:
            count = OpCode.execute(0xAA, registers, mock_memory_controller)
            self.assertEqual(count, 2)
            mock_memory_controller.assert_not_called()
            self.assertEqual(registers.accumulator, dummy_value)
            self.assertEqual(registers.accumulator, registers.x_index)
            self.assertFalse(registers.negative_flag)
            self.assertFalse(registers.zero_flag)

    def test_execute_tay(self):

        registers = Registers()
        dummy_value = 0x7c # (positive, not zero)
        registers.accumulator =  dummy_value

        with patch.object(MemoryController, 'read', return_value = None) as mock_memory_controller:
            count = OpCode.execute(0xA8, registers, mock_memory_controller)
            self.assertEqual(count, 2)
            mock_memory_controller.assert_not_called()
            self.assertEqual(registers.accumulator, dummy_value)
            self.assertEqual(registers.accumulator, registers.y_index)
            self.assertFalse(registers.negative_flag)
            self.assertFalse(registers.zero_flag)

    def test_execute_txa(self):

        registers = Registers()
        dummy_value = 0x7c # (positive, not zero)
        registers.x_index =  dummy_value

        with patch.object(MemoryController, 'read', return_value = None) as mock_memory_controller:
            count = OpCode.execute(0x8A, registers, mock_memory_controller)
            self.assertEqual(count, 2)
            mock_memory_controller.assert_not_called()
            self.assertEqual(registers.x_index, dummy_value)
            self.assertEqual(registers.accumulator, registers.x_index)
            self.assertFalse(registers.negative_flag)
            self.assertFalse(registers.zero_flag)

    def test_execute_tya(self):

        registers = Registers()
        dummy_value = 0x7c # (positive, not zero)
        registers.y_index =  dummy_value

        with patch.object(MemoryController, 'read', return_value = None) as mock_memory_controller:
            count = OpCode.execute(0x98, registers, mock_memory_controller)
            self.assertEqual(count, 2)
            mock_memory_controller.assert_not_called()
            self.assertEqual(registers.y_index, dummy_value)
            self.assertEqual(registers.accumulator, registers.y_index)
            self.assertFalse(registers.negative_flag)
            self.assertFalse(registers.zero_flag)

    def test_execute_tsx(self):

        registers = Registers() # leave sp with default
        old_sp = registers.sp

        with patch.object(MemoryController, 'read', return_value = None) as mock_memory_controller:
            count = OpCode.execute(0xBA, registers, mock_memory_controller)
            self.assertEqual(count, 2)
            mock_memory_controller.assert_not_called()
            self.assertEqual(registers.x_index, old_sp)
            self.assertEqual(registers.sp, old_sp)
            self.assertTrue(registers.negative_flag) # default sp should be $fd
            self.assertFalse(registers.zero_flag)

    def test_execute_txs(self):

        registers = Registers() 
        dummy_value = 0x7c # (positive, not zero)
        registers.x_index = dummy_value

        with patch.object(MemoryController, 'read', return_value = None) as mock_memory_controller:
            count = OpCode.execute(0x9A, registers, mock_memory_controller)
            self.assertEqual(count, 2)
            mock_memory_controller.assert_not_called()
            self.assertEqual(registers.x_index, dummy_value)
            self.assertEqual(registers.sp, dummy_value)
            self.assertFalse(registers.negative_flag) # default sp should be $fd
            self.assertFalse(registers.zero_flag)

if __name__ == '__main__':
    unittest.main()