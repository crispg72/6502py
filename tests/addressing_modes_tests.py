import unittest

from unittest.mock import patch
from unittest.mock import Mock
from memory_controller import MemoryController
from registers import Registers
from addressing_modes import AddressingModes


class AdressingModesTests(unittest.TestCase):
    
    def test_implied_has_no_effect(self):

        registers = Registers()

        with patch.object(MemoryController, 'read', return_value = None) as mock_memory_controller:
            # 'RTS' opcode is implied address mode
            count = AddressingModes.handle(0x60, registers, mock_memory_controller)
            self.assertEqual(count, None)
            mock_memory_controller.assert_not_called()
            self.assertTrue(registers == Registers())

    def test_immediate_loads_next_value_from_pc(self):

        registers = Registers()

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            mock_memory_controller.read.return_value = 0x22
            # 'LDA' 0xA9 opcode is immediate address mode
            value = AddressingModes.handle(0xA9, registers, mock_memory_controller)
            mock_memory_controller.read.assert_called_with(0)
            self.assertEqual(registers.pc, 1)
            self.assertEqual(value, 0x22)

    def test_zero_page_calls_read_correctly(self):

        registers = Registers()
        registers.pc = 1 #fake loading of opcode

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # we're mocking 0xa5 0x22 and value at [0x0022] = 1
            mock_memory_controller.read.side_effect = [0x22, 1]
            # 'LDA' 0xA5 opcode is zero page address mode
            value = AddressingModes.handle(0xA5, registers, mock_memory_controller)
            self.assertEqual(mock_memory_controller.read.call_count, 2)
            self.assertEqual(mock_memory_controller.read.call_args_list[1], unittest.mock.call(0x22))
            self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
            self.assertEqual(registers.pc, 2)
            self.assertEqual(value, 1)

    def test_absolute_calls_read_correctly(self):

        registers = Registers()
        registers.pc = 1 #fake loading of opcode

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # we're mocking 0xa5 0x22 and value at [0x0022] = 1
            mock_memory_controller.read.side_effect = [0x22, 0x23, 1]
            # 'JMP' 0x4c opcode is absolute address mode
            value = AddressingModes.handle(0x4C, registers, mock_memory_controller)
            self.assertEqual(mock_memory_controller.read.call_count, 3)
            self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
            self.assertEqual(mock_memory_controller.read.call_args_list[1], unittest.mock.call(2))
            self.assertEqual(mock_memory_controller.read.call_args_list[2], unittest.mock.call(0x2322))
            self.assertEqual(registers.pc, 3)
            self.assertEqual(value, 1)

if __name__ == '__main__':
    unittest.main()