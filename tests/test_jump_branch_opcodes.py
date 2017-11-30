import unittest

from unittest.mock import patch
from emupy6502.memory_controller import MemoryController
from emupy6502.registers import Registers
from emupy6502.opcodes import OpCode


class OpCodeTestsJumpsAndBranches(unittest.TestCase):

    def test_execute_jmp_absolute(self):

        opcode = OpCode()
        registers = Registers()

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            mock_memory_controller.read.side_effect = [0x00, 0xc0]
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = opcode.execute(0x4C, registers, mock_memory_controller)
            self.assertEqual(count, 3)

            # Tested more thoroughly in addressing_modes_tests
            self.assertEqual(mock_memory_controller.read.call_count, 2)
            self.assertEqual(registers.pc, 0xc000)

    def test_execute_jmp_indirect(self):

        opcode = OpCode()
        registers = Registers()

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            mock_memory_controller.read.side_effect = [0x00, 0xc0, 0x34, 0x12]
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = opcode.execute(0x6C, registers, mock_memory_controller)
            self.assertEqual(count, 5)

            # Tested more thoroughly in addressing_modes_tests
            self.assertEqual(mock_memory_controller.read.call_count, 4)
            self.assertEqual(registers.pc, 0x1234)

    def test_execute_bpl_branch_not_taken(self):

        opcode = OpCode()
        registers = Registers()
        registers.negative_flag = True
        registers.pc = 0xc000

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            mock_memory_controller.read.side_effect = [0x02]
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = opcode.execute(0x10, registers, mock_memory_controller)
            self.assertEqual(count, 2)

            # Tested more thoroughly in addressing_modes_tests
            self.assertEqual(mock_memory_controller.read.call_count, 1)
            self.assertEqual(registers.pc, 0xc002)

    def test_execute_bpl_branch_taken_forward_no_page_boundary(self):

        opcode = OpCode()
        registers = Registers()
        registers.negative_flag = False
        registers.pc = 0xc000

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            mock_memory_controller.read.side_effect = [0x03]
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = opcode.execute(0x10, registers, mock_memory_controller)
            self.assertEqual(count, 3)

            # Tested more thoroughly in addressing_modes_tests
            self.assertEqual(mock_memory_controller.read.call_count, 1)
            self.assertEqual(registers.pc, 0xc005)

    def test_execute_bpl_branch_taken_backward_no_page_boundary(self):

        opcode = OpCode()
        registers = Registers()
        registers.negative_flag = False
        registers.pc = 0xc000

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            mock_memory_controller.read.side_effect = [0xfe]
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = opcode.execute(0x10, registers, mock_memory_controller)
            self.assertEqual(count, 3)

            # Tested more thoroughly in addressing_modes_tests
            self.assertEqual(mock_memory_controller.read.call_count, 1)
            self.assertEqual(registers.pc, 0xc000)

    def test_execute_bmi_branch_not_taken(self):

        opcode = OpCode()
        registers = Registers()
        registers.negative_flag = False
        registers.pc = 0xc000

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            mock_memory_controller.read.side_effect = [0x02]
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = opcode.execute(0x30, registers, mock_memory_controller)
            self.assertEqual(count, 2)

            # Tested more thoroughly in addressing_modes_tests
            self.assertEqual(mock_memory_controller.read.call_count, 1)
            self.assertEqual(registers.pc, 0xc002)

    def test_execute_bmi_branch_taken(self):

        opcode = OpCode()
        registers = Registers()
        registers.negative_flag = True
        registers.pc = 0xc000

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            mock_memory_controller.read.side_effect = [0xfe]
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = opcode.execute(0x30, registers, mock_memory_controller)
            self.assertEqual(count, 3)

            # Tested more thoroughly in addressing_modes_tests
            self.assertEqual(mock_memory_controller.read.call_count, 1)
            self.assertEqual(registers.pc, 0xc000)

    def test_execute_bvc_branch_not_taken(self):

        opcode = OpCode()
        registers = Registers()
        registers.overflow_flag = True
        registers.pc = 0xc000

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            mock_memory_controller.read.side_effect = [0x02]
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = opcode.execute(0x50, registers, mock_memory_controller)
            self.assertEqual(count, 2)

            # Tested more thoroughly in addressing_modes_tests
            self.assertEqual(mock_memory_controller.read.call_count, 1)
            self.assertEqual(registers.pc, 0xc002)

    def test_execute_bvc_branch_taken(self):

        opcode = OpCode()
        registers = Registers()
        registers.overflow_flag = False
        registers.pc = 0xc000

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            mock_memory_controller.read.side_effect = [0xfe]
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = opcode.execute(0x50, registers, mock_memory_controller)
            self.assertEqual(count, 3)

            # Tested more thoroughly in addressing_modes_tests
            self.assertEqual(mock_memory_controller.read.call_count, 1)
            self.assertEqual(registers.pc, 0xc000)

    def test_execute_bvs_branch_not_taken(self):

        opcode = OpCode()
        registers = Registers()
        registers.overflow_flag = False
        registers.pc = 0xc000

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            mock_memory_controller.read.side_effect = [0x02]
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = opcode.execute(0x70, registers, mock_memory_controller)
            self.assertEqual(count, 2)

            # Tested more thoroughly in addressing_modes_tests
            self.assertEqual(mock_memory_controller.read.call_count, 1)
            self.assertEqual(registers.pc, 0xc002)

    def test_execute_bvs_branch_taken(self):

        opcode = OpCode()
        registers = Registers()
        registers.overflow_flag = True
        registers.pc = 0xc000

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            mock_memory_controller.read.side_effect = [0xfe]
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = opcode.execute(0x70, registers, mock_memory_controller)
            self.assertEqual(count, 3)

            # Tested more thoroughly in addressing_modes_tests
            self.assertEqual(mock_memory_controller.read.call_count, 1)
            self.assertEqual(registers.pc, 0xc000)

    def test_execute_bcc_branch_not_taken(self):

        opcode = OpCode()
        registers = Registers()
        registers.carry_flag = True
        registers.pc = 0xc000

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            mock_memory_controller.read.side_effect = [0x02]
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = opcode.execute(0x90, registers, mock_memory_controller)
            self.assertEqual(count, 2)

            # Tested more thoroughly in addressing_modes_tests
            self.assertEqual(mock_memory_controller.read.call_count, 1)
            self.assertEqual(registers.pc, 0xc002)

    def test_execute_bcc_branch_taken(self):

        opcode = OpCode()
        registers = Registers()
        registers.carry_flag = False
        registers.pc = 0xc000

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            mock_memory_controller.read.side_effect = [0xfe]
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = opcode.execute(0x90, registers, mock_memory_controller)
            self.assertEqual(count, 3)

            # Tested more thoroughly in addressing_modes_tests
            self.assertEqual(mock_memory_controller.read.call_count, 1)
            self.assertEqual(registers.pc, 0xc000)

    def test_execute_bcs_branch_not_taken(self):

        opcode = OpCode()
        registers = Registers()
        registers.carry_flag = False
        registers.pc = 0xc000

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            mock_memory_controller.read.side_effect = [0x02]
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = opcode.execute(0xb0, registers, mock_memory_controller)
            self.assertEqual(count, 2)

            # Tested more thoroughly in addressing_modes_tests
            self.assertEqual(mock_memory_controller.read.call_count, 1)
            self.assertEqual(registers.pc, 0xc002)

    def test_execute_bcs_branch_taken(self):

        opcode = OpCode()
        registers = Registers()
        registers.carry_flag = True
        registers.pc = 0xc000

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            mock_memory_controller.read.side_effect = [0xfe]
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = opcode.execute(0xb0, registers, mock_memory_controller)
            self.assertEqual(count, 3)

            # Tested more thoroughly in addressing_modes_tests
            self.assertEqual(mock_memory_controller.read.call_count, 1)
            self.assertEqual(registers.pc, 0xc000)

    def test_execute_bne_branch_not_taken(self):

        opcode = OpCode()
        registers = Registers()
        registers.zero_flag = True
        registers.pc = 0xc000

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            mock_memory_controller.read.side_effect = [0x02]
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = opcode.execute(0xd0, registers, mock_memory_controller)
            self.assertEqual(count, 2)

            # Tested more thoroughly in addressing_modes_tests
            self.assertEqual(mock_memory_controller.read.call_count, 1)
            self.assertEqual(registers.pc, 0xc002)

    def test_execute_bne_branch_taken(self):

        opcode = OpCode()
        registers = Registers()
        registers.zero_flag = False
        registers.pc = 0xc000

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            mock_memory_controller.read.side_effect = [0xfe]
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = opcode.execute(0xd0, registers, mock_memory_controller)
            self.assertEqual(count, 3)

            # Tested more thoroughly in addressing_modes_tests
            self.assertEqual(mock_memory_controller.read.call_count, 1)
            self.assertEqual(registers.pc, 0xc000)

    def test_execute_beq_branch_not_taken(self):

        opcode = OpCode()
        registers = Registers()
        registers.zero_flag = False
        registers.pc = 0xc000

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            mock_memory_controller.read.side_effect = [0x02]
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = opcode.execute(0xf0, registers, mock_memory_controller)
            self.assertEqual(count, 2)

            # Tested more thoroughly in addressing_modes_tests
            self.assertEqual(mock_memory_controller.read.call_count, 1)
            self.assertEqual(registers.pc, 0xc002)

    def test_execute_beq_branch_taken(self):

        opcode = OpCode()
        registers = Registers()
        registers.zero_flag = True
        registers.pc = 0xc000

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            mock_memory_controller.read.side_effect = [0xfe]
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = opcode.execute(0xf0, registers, mock_memory_controller)
            self.assertEqual(count, 3)

            # Tested more thoroughly in addressing_modes_tests
            self.assertEqual(mock_memory_controller.read.call_count, 1)
            self.assertEqual(registers.pc, 0xc000)

if __name__ == '__main__':
    unittest.main()
