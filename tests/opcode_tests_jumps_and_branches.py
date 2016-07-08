import unittest

from unittest.mock import patch
from memory_controller import MemoryController
from registers import Registers
from opcodes import OpCode


class OpCodeTestsJumpsAndBranches(unittest.TestCase):

    def test_execute_jmp_absolute(self):

        registers = Registers()

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            mock_memory_controller.read.side_effect = [0x00, 0xc0]
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = OpCode.execute(0x4C, registers, mock_memory_controller)
            self.assertEqual(count, 3)

            # Tested more thoroughly in addressing_modes_tests
            self.assertEqual(mock_memory_controller.read.call_count, 2)
            self.assertEqual(registers.pc, 0xc000)
    
    def test_execute_jmp_indirect(self):

        registers = Registers()

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            mock_memory_controller.read.side_effect = [0x00, 0xc0, 0x34, 0x12]
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = OpCode.execute(0x6C, registers, mock_memory_controller)
            self.assertEqual(count, 5)

            # Tested more thoroughly in addressing_modes_tests
            self.assertEqual(mock_memory_controller.read.call_count, 4)
            self.assertEqual(registers.pc, 0x1234)

if __name__ == '__main__':
    unittest.main()