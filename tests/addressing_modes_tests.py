import unittest

from unittest.mock import patch
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

if __name__ == '__main__':
    unittest.main()