import unittest

from unittest.mock import patch
from memory_controller import MemoryController
from registers import Registers
from opcodes import OpCode


class OpCodeTests(unittest.TestCase):
    
    def test_execute_lda_immediate(self):

        registers = Registers()

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            mock_memory_controller.read.return_value = 0x22
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = OpCode.execute(0xA9, registers, mock_memory_controller)
            self.assertEqual(count, 2)
            mock_memory_controller.read.assert_called_with(1)
            self.assertTrue(registers.accumulator == 0x22)
            self.assertEqual(registers.pc, 2)


if __name__ == '__main__':
    unittest.main()