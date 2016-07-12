import unittest

from unittest.mock import patch, Mock
from memory_controller import MemoryController
from registers import Registers
from opcodes import OpCode


class OpCodeTestsStores(unittest.TestCase):

    def test_execute_sta_zeropage(self):

        registers = Registers()
        registers.accumulator = 3

        mock_memory_controller = Mock()

        # we're mocking 0x85 0x21 
        mock_memory_controller.read.side_effect = [0x21]
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = OpCode.execute(0x85, registers, mock_memory_controller)
        self.assertEqual(count, 3)
        self.assertEqual(mock_memory_controller.read.call_count, 1)
        self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
        mock_memory_controller.write.called_with(0x21, 3)
        self.assertEqual(registers.pc, 2)

    def test_execute_stx_zeropage(self):

        registers = Registers()
        registers.x_index = 4

        mock_memory_controller = Mock()

        # we're mocking 0x86 0x20 
        mock_memory_controller.read.side_effect = [0x20]
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = OpCode.execute(0x86, registers, mock_memory_controller)
        self.assertEqual(count, 3)
        self.assertEqual(mock_memory_controller.read.call_count, 1)
        self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
        mock_memory_controller.write.called_with(0x20, 4)
        self.assertEqual(registers.pc, 2)

    def test_execute_sty_zeropage(self):

        registers = Registers()
        registers.y_index = 5

        mock_memory_controller = Mock()

        # we're mocking 0x84 0x30
        mock_memory_controller.read.side_effect = [0x30]
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = OpCode.execute(0x84, registers, mock_memory_controller)
        self.assertEqual(count, 3)
        self.assertEqual(mock_memory_controller.read.call_count, 1)
        self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
        mock_memory_controller.write.called_with(0x30, 5)
        self.assertEqual(registers.pc, 2)


if __name__ == '__main__':
    unittest.main()