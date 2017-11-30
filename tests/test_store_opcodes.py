import unittest

from unittest.mock import patch, Mock
from emupy6502.memory_controller import MemoryController
from emupy6502.registers import Registers
from emupy6502.opcodes import OpCode


class OpCodeTestsStores(unittest.TestCase):

    def test_execute_sta_zeropage(self):

        opcode = OpCode()
        registers = Registers()
        registers.accumulator = 3

        mock_memory_controller = Mock()

        # we're mocking 0x85 0x21 
        mock_memory_controller.read.side_effect = [0x21]
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0x85, registers, mock_memory_controller)
        self.assertEqual(count, 3)
        self.assertEqual(mock_memory_controller.read.call_count, 1)
        self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
        mock_memory_controller.write.assert_called_with(0x21, 3)
        self.assertEqual(registers.pc, 2)

    def test_execute_stx_zeropage(self):

        opcode = OpCode()
        registers = Registers()
        registers.x_index = 4

        mock_memory_controller = Mock()

        # we're mocking 0x86 0x20 
        mock_memory_controller.read.side_effect = [0x20]
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0x86, registers, mock_memory_controller)
        self.assertEqual(count, 3)
        self.assertEqual(mock_memory_controller.read.call_count, 1)
        self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
        mock_memory_controller.write.assert_called_with(0x20, 4)
        self.assertEqual(registers.pc, 2)

    def test_execute_sty_zeropage(self):

        opcode = OpCode()
        registers = Registers()
        registers.y_index = 5

        mock_memory_controller = Mock()

        # we're mocking 0x84 0x30
        mock_memory_controller.read.side_effect = [0x30]
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0x84, registers, mock_memory_controller)
        self.assertEqual(count, 3)
        self.assertEqual(mock_memory_controller.read.call_count, 1)
        self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
        mock_memory_controller.write.assert_called_with(0x30, 5)
        self.assertEqual(registers.pc, 2)

    def test_execute_sta_zeropage_x(self):

        opcode = OpCode()
        registers = Registers()
        registers.accumulator = 0x20
        registers.x_index = 3

        mock_memory_controller = Mock()

        # we're mocking 0x95 0x21 so store to [0x0024]
        mock_memory_controller.read.side_effect = [0x21]
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0x95, registers, mock_memory_controller)
        self.assertEqual(count, 4)

        # these are checked more thoroughly in addressing_modes_tests
        self.assertEqual(mock_memory_controller.read.call_count, 1)
        self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
        mock_memory_controller.write.assert_called_with(0x24, 0x20)
        self.assertEqual(registers.pc, 2)

    def test_execute_sta_zeropage_x_wrap(self):

        opcode = OpCode()
        registers = Registers()
        registers.accumulator = 0x20
        registers.x_index = 3

        mock_memory_controller = Mock()

        # we're mocking 0x95 0x21 so store to [0x0024]
        mock_memory_controller.read.side_effect = [0xfe]
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0x95, registers, mock_memory_controller)
        self.assertEqual(count, 4)

        # these are checked more thoroughly in addressing_modes_tests
        self.assertEqual(mock_memory_controller.read.call_count, 1)
        self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
        mock_memory_controller.write.assert_called_with(0x01, 0x20)
        self.assertEqual(registers.pc, 2)

    def test_execute_sty_zeropage_x(self):

        opcode = OpCode()
        registers = Registers()
        registers.y_index = 0x20
        registers.x_index = 3

        mock_memory_controller = Mock()

        # we're mocking 0x94 0x21 so store to [0x0024]
        mock_memory_controller.read.side_effect = [0x21]
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0x94, registers, mock_memory_controller)
        self.assertEqual(count, 4)

        # these are checked more thoroughly in addressing_modes_tests
        self.assertEqual(mock_memory_controller.read.call_count, 1)
        self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
        mock_memory_controller.write.assert_called_with(0x24, 0x20)
        self.assertEqual(registers.pc, 2)

    def test_execute_sty_zeropage_x_wrap(self):

        opcode = OpCode()
        registers = Registers()
        registers.y_index = 0x20
        registers.x_index = 3

        mock_memory_controller = Mock()

        # we're mocking 0x94 0x21 so store to [0x0024]
        mock_memory_controller.read.side_effect = [0xfe]
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0x94, registers, mock_memory_controller)
        self.assertEqual(count, 4)

        # these are checked more thoroughly in addressing_modes_tests
        self.assertEqual(mock_memory_controller.read.call_count, 1)
        self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
        mock_memory_controller.write.assert_called_with(0x01, 0x20)
        self.assertEqual(registers.pc, 2)

    def test_execute_stx_zeropage_y(self):

        opcode = OpCode()
        registers = Registers()
        registers.x_index = 0x20
        registers.y_index = 3

        mock_memory_controller = Mock()

        # we're mocking 0x96 0x21 so store to [0x0024]
        mock_memory_controller.read.side_effect = [0x21]
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0x96, registers, mock_memory_controller)
        self.assertEqual(count, 4)

        # these are checked more thoroughly in addressing_modes_tests
        self.assertEqual(mock_memory_controller.read.call_count, 1)
        self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
        mock_memory_controller.write.assert_called_with(0x24, 0x20)
        self.assertEqual(registers.pc, 2)

    def test_execute_stx_zeropage_y_wrap(self):

        opcode = OpCode()
        registers = Registers()
        registers.x_index = 0x20
        registers.y_index = 3

        mock_memory_controller = Mock()

        # we're mocking 0x96 0x21 so store to [0x0024]
        mock_memory_controller.read.side_effect = [0xfe]
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0x96, registers, mock_memory_controller)
        self.assertEqual(count, 4)

        # these are checked more thoroughly in addressing_modes_tests
        self.assertEqual(mock_memory_controller.read.call_count, 1)
        self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
        mock_memory_controller.write.assert_called_with(0x01, 0x20)
        self.assertEqual(registers.pc, 2)

    def test_execute_sta_absolute(self):

        opcode = OpCode()
        registers = Registers()
        registers.accumulator = 0x20

        mock_memory_controller = Mock()

        # we're mocking 0x8D 0x21 so store to [0x0024]
        mock_memory_controller.read.side_effect = [0, 0x20]
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0x8D, registers, mock_memory_controller)
        self.assertEqual(count, 4)

        # these are checked more thoroughly in addressing_modes_tests
        self.assertEqual(mock_memory_controller.read.call_count, 2)
        self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
        mock_memory_controller.write.assert_called_with(0x2000, 0x20)
        self.assertEqual(registers.pc, 3)

    def test_execute_stx_absolute(self):

        opcode = OpCode()
        registers = Registers()
        registers.x_index = 0x20

        mock_memory_controller = Mock()

        # we're mocking 0x8E 0x21 so store to [0x0024]
        mock_memory_controller.read.side_effect = [0, 0x20]
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0x8E, registers, mock_memory_controller)
        self.assertEqual(count, 4)

        # these are checked more thoroughly in addressing_modes_tests
        self.assertEqual(mock_memory_controller.read.call_count, 2)
        self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
        mock_memory_controller.write.assert_called_with(0x2000, 0x20)
        self.assertEqual(registers.pc, 3)

    def test_execute_sty_absolute(self):

        opcode = OpCode()
        registers = Registers()
        registers.y_index = 0x20

        mock_memory_controller = Mock()

        # we're mocking 0x8C 0x21 so store to [0x0024]
        mock_memory_controller.read.side_effect = [0, 0x20]
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0x8C, registers, mock_memory_controller)
        self.assertEqual(count, 4)

        # these are checked more thoroughly in addressing_modes_tests
        self.assertEqual(mock_memory_controller.read.call_count, 2)
        self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
        mock_memory_controller.write.assert_called_with(0x2000, 0x20)
        self.assertEqual(registers.pc, 3)

    def test_execute_sta_absolute_x(self):

        opcode = OpCode()
        registers = Registers()
        registers.accumulator = 0x20
        registers.x_index = 3

        mock_memory_controller = Mock()

        # we're mocking 0x9D 0x2100 so write is to [0x2103]
        mock_memory_controller.read.side_effect = [0, 0x21]
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0x9D, registers, mock_memory_controller)
        self.assertEqual(count, 5)

        # these are checked more thoroughly in addressing_modes_tests
        self.assertEqual(mock_memory_controller.read.call_count, 2)
        mock_memory_controller.write.assert_called_with(0x2103, 0x20)
        self.assertEqual(registers.pc, 3)

    def test_execute_sta_absolute_y(self):

        opcode = OpCode()
        registers = Registers()
        registers.accumulator = 0x20
        registers.y_index = 3

        mock_memory_controller = Mock()

        # we're mocking 0x99 0x2100 so write is to [0x2103]
        mock_memory_controller.read.side_effect = [0, 0x21]
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(0x99, registers, mock_memory_controller)
        self.assertEqual(count, 5)

        # these are checked more thoroughly in addressing_modes_tests
        self.assertEqual(mock_memory_controller.read.call_count, 2)
        mock_memory_controller.write.assert_called_with(0x2103, 0x20)
        self.assertEqual(registers.pc, 3)

if __name__ == '__main__':
    unittest.main()