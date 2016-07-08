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

    def test_relative_loads_next_value_from_pc(self):

        registers = Registers()

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            mock_memory_controller.read.return_value = 0x22
            # 'BPL' 0x10 opcode is relative address mode
            value = AddressingModes.handle(0x10, registers, mock_memory_controller)
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

    def test_absolute_jmp_calls_read_correctly(self):

        registers = Registers()
        registers.pc = 1 #fake loading of opcode

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # we're mocking 0xa5 0x22 and value at [0x0022] = 1
            mock_memory_controller.read.side_effect = [0x22, 0x23, 1]
            # 'JMP' 0x4c opcode is absolute address mode
            value = AddressingModes.handle(0x4C, registers, mock_memory_controller)
            self.assertEqual(mock_memory_controller.read.call_count, 2)
            self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
            self.assertEqual(mock_memory_controller.read.call_args_list[1], unittest.mock.call(2))
            self.assertEqual(registers.pc, 3)
            self.assertEqual(value, 0x2322)

    def test_absolute_calls_read_correctly(self):

        registers = Registers()
        registers.pc = 1 #fake loading of opcode

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # we're mocking 0xa5 0x22 and value at [0x0022] = 1
            mock_memory_controller.read.side_effect = [0x22, 0x23, 1]
            # 'LDA' 0xad opcode is absolute address mode
            value = AddressingModes.handle(0xAD, registers, mock_memory_controller)
            self.assertEqual(mock_memory_controller.read.call_count, 3)
            self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
            self.assertEqual(mock_memory_controller.read.call_args_list[1], unittest.mock.call(2))
            self.assertEqual(mock_memory_controller.read.call_args_list[2], unittest.mock.call(0x2322))
            self.assertEqual(registers.pc, 3)
            self.assertEqual(value, 1)

    def test_zero_page_x_index_calls_read_correctly(self):

        registers = Registers()
        registers.pc = 1 #fake loading of opcode
        registers.x_index = 3

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # we're mocking 0xB5 0x03 and value at [0x06] = 1
            mock_memory_controller.read.side_effect = [3, 1]
            # 'LDA' 0xB5 opcode is zero page x indexed address mode
            value = AddressingModes.handle(0xB5, registers, mock_memory_controller)
            self.assertEqual(mock_memory_controller.read.call_count, 2)
            self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
            self.assertEqual(mock_memory_controller.read.call_args_list[1], unittest.mock.call(6))
            self.assertEqual(registers.pc, 2)
            self.assertEqual(value, 1)

    def test_zero_page_x_index_deals_with_wraparound(self):

        registers = Registers()
        registers.pc = 1 #fake loading of opcode
        registers.x_index = 0xff

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # we're mocking 0xB5 0x03 and value at [0x02] = 1
            mock_memory_controller.read.side_effect = [3, 1]
            # 'LDA' 0xB5 opcode is zero page x indexed address mode
            value = AddressingModes.handle(0xB5, registers, mock_memory_controller)
            self.assertEqual(mock_memory_controller.read.call_count, 2)
            self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
            self.assertEqual(mock_memory_controller.read.call_args_list[1], unittest.mock.call(2))
            self.assertEqual(registers.pc, 2)
            self.assertEqual(value, 1)

    def test_zero_page_y_index_calls_read_correctly(self):

        registers = Registers()
        registers.pc = 1 #fake loading of opcode
        registers.y_index = 3

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # we're mocking 0xB6 0x03 and value at [0x06] = 1
            mock_memory_controller.read.side_effect = [3, 1]
            # 'LDX' 0xB6 opcode is zero page x indexed address mode
            value = AddressingModes.handle(0xB6, registers, mock_memory_controller)
            self.assertEqual(mock_memory_controller.read.call_count, 2)
            self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
            self.assertEqual(mock_memory_controller.read.call_args_list[1], unittest.mock.call(6))
            self.assertEqual(registers.pc, 2)
            self.assertEqual(value, 1)

    def test_zero_page_y_index_deals_with_wraparound(self):

        registers = Registers()
        registers.pc = 1 #fake loading of opcode
        registers.y_index = 0xff

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # we're mocking 0xB6 0x03 and value at [0x02] = 1
            mock_memory_controller.read.side_effect = [3, 1]
            # 'LDX 0xB6 opcode is zero page x indexed address mode
            value = AddressingModes.handle(0xB6, registers, mock_memory_controller)
            self.assertEqual(mock_memory_controller.read.call_count, 2)
            self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
            self.assertEqual(mock_memory_controller.read.call_args_list[1], unittest.mock.call(2))
            self.assertEqual(registers.pc, 2)
            self.assertEqual(value, 1)

    def test_indirect(self):

        registers = Registers()
        registers.pc = 1 #fake loading of opcode
        registers.y_index = 0xff

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # we're mocking 0x6C 0x03 0xf0 and value at [0xf003] = 0x1234
            mock_memory_controller.read.side_effect = [3, 0xf0, 0x34, 0x12]
            # 'JMP' 0x6C opcode uses indirect addressing
            value = AddressingModes.handle(0x6C, registers, mock_memory_controller)
            self.assertEqual(mock_memory_controller.read.call_count, 4)
            self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
            self.assertEqual(mock_memory_controller.read.call_args_list[1], unittest.mock.call(2))
            self.assertEqual(mock_memory_controller.read.call_args_list[2], unittest.mock.call(0xf003))
            self.assertEqual(mock_memory_controller.read.call_args_list[3], unittest.mock.call(0xf004))
            self.assertEqual(registers.pc, 3)
            self.assertEqual(value, 0x1234)

    def test_zp_index_indirect_x(self):

        registers = Registers()
        registers.pc = 1 #fake loading of opcode
        registers.x_index = 0x3

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # we're mocking 0xA1 0x03 and value at [0x06] = 0x1234
            mock_memory_controller.read.side_effect = [3, 0x34, 0x12]
            # 'LDA' 0xA1 opcode uses indirect addressing
            value = AddressingModes.handle(0xA1, registers, mock_memory_controller)
            self.assertEqual(mock_memory_controller.read.call_count, 3)
            self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
            self.assertEqual(mock_memory_controller.read.call_args_list[1], unittest.mock.call(6))
            self.assertEqual(mock_memory_controller.read.call_args_list[2], unittest.mock.call(7))
            self.assertEqual(registers.pc, 2)
            self.assertEqual(value, 0x1234)

    def test_zp_index_indirect_x_wraparound_1(self):

        registers = Registers()
        registers.pc = 1 #fake loading of opcode
        registers.x_index = 0xff

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # we're mocking 0xA1 0x03 and value at [0xff] = 0x12, [0x00] = 0x34
            mock_memory_controller.read.side_effect = [3, 0x34, 0x12]
            # 'LDA' 0xA1 opcode uses indirect addressing
            value = AddressingModes.handle(0xA1, registers, mock_memory_controller)
            self.assertEqual(mock_memory_controller.read.call_count, 3)
            self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
            self.assertEqual(mock_memory_controller.read.call_args_list[1], unittest.mock.call(2))
            self.assertEqual(mock_memory_controller.read.call_args_list[2], unittest.mock.call(3))
            self.assertEqual(registers.pc, 2)
            self.assertEqual(value, 0x1234)

    def test_zp_index_indirect_x_wraparound_2(self):

        registers = Registers()
        registers.pc = 1 #fake loading of opcode
        registers.x_index = 0xfe

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # we're mocking 0xA1 0x03 and value at [0xff] = 0x12, [0x00] = 0x34
            mock_memory_controller.read.side_effect = [1, 0x34, 0x12]
            # 'LDA' 0xA1 opcode uses indirect addressing
            value = AddressingModes.handle(0xA1, registers, mock_memory_controller)
            self.assertEqual(mock_memory_controller.read.call_count, 3)
            self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
            self.assertEqual(mock_memory_controller.read.call_args_list[1], unittest.mock.call(0xff))
            self.assertEqual(mock_memory_controller.read.call_args_list[2], unittest.mock.call(0))
            self.assertEqual(registers.pc, 2)
            self.assertEqual(value, 0x1234)

    def test_absolute_x(self):

        registers = Registers()
        registers.pc = 1 #fake loading of opcode
        registers.x_index = 0x3
        AddressingModes.cycle_count = 0

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # we're mocking 0xBD 0xc000 
            mock_memory_controller.read.side_effect = [0, 0xc0]
            # 'LDA' 0xBD opcode uses indirect addressing
            value = AddressingModes.handle(0xBD, registers, mock_memory_controller)
            self.assertEqual(mock_memory_controller.read.call_count, 2)
            self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
            self.assertEqual(mock_memory_controller.read.call_args_list[1], unittest.mock.call(2))
            self.assertEqual(registers.pc, 3)
            self.assertEqual(value, 0xc003)
            self.assertEqual(AddressingModes.cycle_count, 0)

    def test_absolute_x_page_boundary(self):

        registers = Registers()
        registers.pc = 1 #fake loading of opcode
        registers.x_index = 0x3
        AddressingModes.cycle_count = 0

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # we're mocking 0xBD 0xc000 
            mock_memory_controller.read.side_effect = [0xfe, 0xc0]
            # 'LDA' 0xBD opcode uses indirect addressing
            value = AddressingModes.handle(0xBD, registers, mock_memory_controller)
            self.assertEqual(mock_memory_controller.read.call_count, 2)
            self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
            self.assertEqual(mock_memory_controller.read.call_args_list[1], unittest.mock.call(2))
            self.assertEqual(registers.pc, 3)
            self.assertEqual(value, 0xc101)
            self.assertEqual(AddressingModes.cycle_count, 1)

    def test_absolute_y(self):

        registers = Registers()
        registers.pc = 1 #fake loading of opcode
        registers.y_index = 0x3
        AddressingModes.cycle_count = 0

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # we're mocking 0xB9 0xc000 
            mock_memory_controller.read.side_effect = [0, 0xc0]
            # 'LDA' 0xB9 opcode uses indirect addressing
            value = AddressingModes.handle(0xB9, registers, mock_memory_controller)
            self.assertEqual(mock_memory_controller.read.call_count, 2)
            self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
            self.assertEqual(mock_memory_controller.read.call_args_list[1], unittest.mock.call(2))
            self.assertEqual(registers.pc, 3)
            self.assertEqual(value, 0xc003)
            self.assertEqual(AddressingModes.cycle_count, 0)

    def test_absolute_y_page_boundary(self):

        registers = Registers()
        registers.pc = 1 #fake loading of opcode
        registers.y_index = 0x3
        AddressingModes.cycle_count = 0

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # we're mocking 0xB9 0xc000 
            mock_memory_controller.read.side_effect = [0xfe, 0xc0]
            # 'LDA' 0xB9 opcode uses indirect addressing
            value = AddressingModes.handle(0xB9, registers, mock_memory_controller)
            self.assertEqual(mock_memory_controller.read.call_count, 2)
            self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
            self.assertEqual(mock_memory_controller.read.call_args_list[1], unittest.mock.call(2))
            self.assertEqual(registers.pc, 3)
            self.assertEqual(value, 0xc101)
            self.assertEqual(AddressingModes.cycle_count, 1)

    def test_indirect_indexed_y(self):

        registers = Registers()
        registers.pc = 1 #fake loading of opcode
        registers.y_index = 0x3
        AddressingModes.cycle_count = 0

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # we're mocking 0xB1 0x2a  memory at 0x2a = [0x28, 0x40]
            mock_memory_controller.read.side_effect = [0x2a, 0x28, 0x40]
            # 'LDA' 0xB9 opcode uses indirect addressing
            value = AddressingModes.handle(0xB1, registers, mock_memory_controller)
            self.assertEqual(mock_memory_controller.read.call_count, 3)
            self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
            self.assertEqual(mock_memory_controller.read.call_args_list[1], unittest.mock.call(0x2a))
            self.assertEqual(mock_memory_controller.read.call_args_list[2], unittest.mock.call(0x2b))
            self.assertEqual(registers.pc, 2)
            self.assertEqual(value, 0x402b)
            self.assertEqual(AddressingModes.cycle_count, 0)

    def test_indirect_indexed_y_zp_boundary(self):

        registers = Registers()
        registers.pc = 1 #fake loading of opcode
        registers.y_index = 0x3
        AddressingModes.cycle_count = 0

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # we're mocking 0xB1 0xff  memory at 0xff = [0x28, 0x40]
            mock_memory_controller.read.side_effect = [0xff, 0x28, 0x40]
            # 'LDA' 0xB9 opcode uses indirect addressing
            value = AddressingModes.handle(0xB1, registers, mock_memory_controller)
            self.assertEqual(mock_memory_controller.read.call_count, 3)
            self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
            self.assertEqual(mock_memory_controller.read.call_args_list[1], unittest.mock.call(0xff))
            self.assertEqual(mock_memory_controller.read.call_args_list[2], unittest.mock.call(0x00))
            self.assertEqual(registers.pc, 2)
            self.assertEqual(value, 0x402b)
            self.assertEqual(AddressingModes.cycle_count, 0)

    def test_indirect_indexed_y_page_boundary(self):

        registers = Registers()
        registers.pc = 1 #fake loading of opcode
        registers.y_index = 0x3
        AddressingModes.cycle_count = 0

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # we're mocking 0xB1 0x2a  memory at 0x2a = [0xfe, 0x40]
            mock_memory_controller.read.side_effect = [0x2a, 0xfe, 0x40]
            # 'LDA' 0xB9 opcode uses indirect addressing
            value = AddressingModes.handle(0xB1, registers, mock_memory_controller)
            self.assertEqual(mock_memory_controller.read.call_count, 3)
            self.assertEqual(mock_memory_controller.read.call_args_list[0], unittest.mock.call(1))
            self.assertEqual(mock_memory_controller.read.call_args_list[1], unittest.mock.call(0x2a))
            self.assertEqual(mock_memory_controller.read.call_args_list[2], unittest.mock.call(0x2b))
            self.assertEqual(registers.pc, 2)
            self.assertEqual(value, 0x4101)
            self.assertEqual(AddressingModes.cycle_count, 1)

if __name__ == '__main__':
    unittest.main()