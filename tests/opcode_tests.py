import unittest

from unittest.mock import patch
from memory_controller import MemoryController
from registers import Registers
from opcodes import OpCode


class OpCodeTests(unittest.TestCase):
    
    def test_execute_nop(self):

        registers = Registers()

        with patch.object(MemoryController, 'read', return_value = None) as mock_memory_controller:
            # 'NOP' opcode is 0xEA
            count = OpCode.execute(0xEA, registers, mock_memory_controller)
            self.assertEqual(count, 2)
            mock_memory_controller.assert_not_called()
            self.assertTrue(registers == Registers())

    def test_execute_tax(self):

        registers = Registers()
        dummy_value = 0x7c # (positive, not zero)
        registers.accumulator =  dummy_value

        with patch.object(MemoryController, 'read', return_value = None) as mock_memory_controller:
            # 'NOP' opcode is 0xEA
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
            # 'NOP' opcode is 0xEA
            count = OpCode.execute(0xA8, registers, mock_memory_controller)
            self.assertEqual(count, 2)
            mock_memory_controller.assert_not_called()
            self.assertEqual(registers.accumulator, dummy_value)
            self.assertEqual(registers.accumulator, registers.y_index)
            self.assertFalse(registers.negative_flag)
            self.assertFalse(registers.zero_flag)


if __name__ == '__main__':
    unittest.main()