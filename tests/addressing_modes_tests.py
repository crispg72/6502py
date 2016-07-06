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

if __name__ == '__main__':
    unittest.main()