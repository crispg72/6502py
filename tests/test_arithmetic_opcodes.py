import unittest

from unittest.mock import patch, Mock
from emupy6502.memory_controller import MemoryController
from emupy6502.registers import Registers
from emupy6502.opcodes import OpCode


class OpCodeTestsArithmetic(unittest.TestCase):
    
    def execute_adc_carry_clear(self, actual_opcode, expected_clocks):

        opcode = OpCode()
        registers = Registers()
        registers.accumulator = 5
        registers.zero_flag = True
        registers.negative_flag = True  

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            mock_memory_controller.read.return_value = 0x22
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = opcode.execute(actual_opcode, registers, mock_memory_controller)
            self.assertEqual(count, expected_clocks)
            self.assertTrue(registers.accumulator == 0x27)
            self.assertFalse(registers.zero_flag)
            self.assertFalse(registers.negative_flag)
            self.assertFalse(registers.carry_flag)

    def execute_adc_carry_set(self, actual_opcode, expected_clocks):

        opcode = OpCode()
        registers = Registers() 
        registers.accumulator = 5
        registers.zero_flag = True
        registers.negative_flag = True  
        registers.carry_flag = True  

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            mock_memory_controller.read.return_value = 0x22
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = opcode.execute(actual_opcode, registers, mock_memory_controller)
            self.assertEqual(count, expected_clocks)
            self.assertTrue(registers.accumulator == 0x28)
            self.assertFalse(registers.zero_flag)
            self.assertFalse(registers.negative_flag)
            self.assertFalse(registers.carry_flag)

    def execute_adc_should_set_carry(self, actual_opcode, expected_clocks):

        opcode = OpCode()
        registers = Registers()
        registers.accumulator = 1
        registers.zero_flag = False
        registers.negative_flag = True    

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            mock_memory_controller.read.return_value = 0xff
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = opcode.execute(actual_opcode, registers, mock_memory_controller)
            self.assertEqual(count, expected_clocks)
            self.assertTrue(registers.accumulator == 0)
            self.assertTrue(registers.zero_flag)
            self.assertFalse(registers.negative_flag)
            self.assertTrue(registers.carry_flag)

    def test_execute_adc_immediate_carry_clear(self):

        self.execute_adc_carry_clear(0x69, 2)

    def test_execute_adc_immediate_carry_set(self):

        self.execute_adc_carry_set(0x69, 2)

    def test_execute_adc_immediate_should_set_carry(self):

        self.execute_adc_should_set_carry(0x69, 2)

    def test_execute_adc_zeropage_carry_clear(self):

        self.execute_adc_carry_clear(0x65, 3)

    def test_execute_adc_zeropage_carry_set(self):

        self.execute_adc_carry_set(0x65, 3)

    def test_execute_adc_zeropage_should_set_carry(self):

        self.execute_adc_should_set_carry(0x65, 3)

    # No need to test all combinations of carry, uses same code as
    # other immediate addressing modes
    def test_execute_adc_immediate_zp_x(self):

        opcode = OpCode()
        registers = Registers()
        registers.accumulator = 5
        registers.x_index = 3
        registers.zero_flag = True
        registers.negative_flag = True  

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # we're mocking 0xb5 0x21 and value at [0x0024] = 1
            mock_memory_controller.read.side_effect = [0x21, 1]

            registers.pc += 1 #need to fake the cpu reading the opcode
            count = opcode.execute(0x75, registers, mock_memory_controller)
            self.assertEqual(count, 4)
            self.assertTrue(registers.accumulator == 6)
            self.assertFalse(registers.zero_flag)
            self.assertFalse(registers.negative_flag)
            self.assertFalse(registers.carry_flag)

    # No need to test all combinations of carry, uses same code as
    # other immediate addressing modes
    def test_execute_adc_absolute(self):

        opcode = OpCode()
        registers = Registers()
        registers.accumulator = 5
        registers.zero_flag = True
        registers.negative_flag = True  

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # we're mocking 0xb5 0x21 0x22 and value at [0x2221] = 1
            mock_memory_controller.read.side_effect = [0x21, 0x22, 1]

            registers.pc += 1 #need to fake the cpu reading the opcode
            count = opcode.execute(0x6D, registers, mock_memory_controller)
            self.assertEqual(count, 4)
            self.assertTrue(registers.accumulator == 6)
            self.assertFalse(registers.zero_flag)
            self.assertFalse(registers.negative_flag)
            self.assertFalse(registers.carry_flag)

    def test_execute_adc_absolute_x(self):

        opcode = OpCode()
        registers = Registers()
        registers.accumulator = 5
        registers.x_index = 3
        registers.zero_flag = True
        registers.negative_flag = True  

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # we're mocking 0xBD 0x2100 and value at [0x2103] = 1
            mock_memory_controller.read.side_effect = [0, 0x21, 1]

            registers.pc += 1 #need to fake the cpu reading the opcode
            count = opcode.execute(0x7D, registers, mock_memory_controller)
            self.assertEqual(count, 4)
            self.assertTrue(registers.accumulator == 6)
            self.assertFalse(registers.zero_flag)
            self.assertFalse(registers.negative_flag)
            self.assertFalse(registers.carry_flag)

    def test_execute_adc_absolute_x_page_boundary(self):

        opcode = OpCode()
        registers = Registers()
        registers.accumulator = 5
        registers.x_index = 3
        registers.zero_flag = True
        registers.negative_flag = True  

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # we're mocking 0xBD 0x2100 and value at [0x2202] = 1
            mock_memory_controller.read.side_effect = [0xff, 0x21, 1]

            registers.pc += 1 #need to fake the cpu reading the opcode
            count = opcode.execute(0x7D, registers, mock_memory_controller)
            self.assertEqual(count, 5)
            self.assertTrue(registers.accumulator == 6)
            self.assertFalse(registers.zero_flag)
            self.assertFalse(registers.negative_flag)
            self.assertFalse(registers.carry_flag)

    def test_execute_adc_absolute_y(self):

        opcode = OpCode()
        registers = Registers()
        registers.accumulator = 5
        registers.y_index = 3
        registers.zero_flag = True
        registers.negative_flag = True  

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # we're mocking 0xBD 0x2100 and value at [0x2103] = 1
            mock_memory_controller.read.side_effect = [0, 0x21, 1]

            registers.pc += 1 #need to fake the cpu reading the opcode
            count = opcode.execute(0x79, registers, mock_memory_controller)
            self.assertEqual(count, 4)
            self.assertTrue(registers.accumulator == 6)
            self.assertFalse(registers.zero_flag)
            self.assertFalse(registers.negative_flag)
            self.assertFalse(registers.carry_flag)

    def test_execute_adc_absolute_y_page_boundary(self):

        opcode = OpCode()
        registers = Registers()
        registers.accumulator = 5
        registers.y_index = 3
        registers.zero_flag = True
        registers.negative_flag = True  

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # we're mocking 0xBD 0x2100 and value at [0x2202] = 1
            mock_memory_controller.read.side_effect = [0xff, 0x21, 1]

            registers.pc += 1 #need to fake the cpu reading the opcode
            count = opcode.execute(0x79, registers, mock_memory_controller)
            self.assertEqual(count, 5)
            self.assertTrue(registers.accumulator == 6)
            self.assertFalse(registers.zero_flag)
            self.assertFalse(registers.negative_flag)
            self.assertFalse(registers.carry_flag)

    def test_execute_adc_indexed_indirect_x(self):

        opcode = OpCode()
        registers = Registers()
        registers.accumulator = 5
        registers.x_index = 3
        registers.zero_flag = True
        registers.negative_flag = True  

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # we're mocking 0x61 0x03 and value at [0x06] = 0x1234, [0x1234] = 3
            mock_memory_controller.read.side_effect = [3, 0x34, 0x12, 3]

            registers.pc += 1 #need to fake the cpu reading the opcode
            count = opcode.execute(0x61, registers, mock_memory_controller)
            self.assertEqual(count, 6)
            self.assertEqual(mock_memory_controller.read.call_count, 4)            
            self.assertTrue(registers.accumulator == 8)
            self.assertFalse(registers.zero_flag)
            self.assertFalse(registers.negative_flag)
            self.assertFalse(registers.carry_flag)

    def test_execute_adc_indirect_indexed_y(self):

        opcode = OpCode()
        registers = Registers()
        registers.accumulator = 5
        registers.y_index = 3
        registers.zero_flag = True
        registers.negative_flag = True  

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # we're mocking 0x71 0x2a  memory at 0x2a = [0x28, 0x40], [0x402B] = 3
            mock_memory_controller.read.side_effect = [0x2a, 0x28, 0x40, 3]

            registers.pc += 1 #need to fake the cpu reading the opcode
            count = opcode.execute(0x71, registers, mock_memory_controller)
            self.assertEqual(count, 5)
            self.assertEqual(mock_memory_controller.read.call_count, 4)            
            self.assertTrue(registers.accumulator == 8)
            self.assertFalse(registers.zero_flag)
            self.assertFalse(registers.negative_flag)
            self.assertFalse(registers.carry_flag)

    def test_execute_adc_indirect_indexed_y_page_boundary(self):

        opcode = OpCode()
        registers = Registers()
        registers.accumulator = 5
        registers.y_index = 3
        registers.zero_flag = True
        registers.negative_flag = True  

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # we're mocking 0x71 0x2a  memory at 0x2a = [0x28, 0x40], [0x4101] = 3
            mock_memory_controller.read.side_effect = [0x2a, 0xfe, 0x40, 3]

            registers.pc += 1 #need to fake the cpu reading the opcode
            count = opcode.execute(0x71, registers, mock_memory_controller)
            self.assertEqual(count, 6)
            self.assertEqual(mock_memory_controller.read.call_count, 4)
            self.assertTrue(registers.accumulator == 8)
            self.assertFalse(registers.zero_flag)
            self.assertFalse(registers.negative_flag)
            self.assertFalse(registers.carry_flag)

    def execute_sbc_borrow_in_borrow_out_no_overflow_positive_result(self, actual_opcode, expected_clocks, mock_memory_controller, **kwargs):

        opcode = OpCode()
        registers = Registers()
        setattr(registers,'accumulator',0x50)

        if kwargs:
            for arg in kwargs:
                setattr(registers, arg, kwargs[arg])

        # Mocking 0x150 - 0xf0 (borrow 'in')
        registers.pc += 1 #need to fake the cpu reading the opcode
        count = opcode.execute(actual_opcode, registers, mock_memory_controller)
        self.assertEqual(count, expected_clocks)
        self.assertEqual(registers.accumulator, 0x5f)
        self.assertFalse(registers.zero_flag)
        self.assertFalse(registers.negative_flag)
        self.assertFalse(registers.carry_flag)
        self.assertFalse(registers.overflow_flag)

    def test_execute_sbc_immediate_borrow_in_borrow_out_no_overflow_positive_result(self):

        mock_memory_controller = Mock()
        mock_memory_controller.read.return_value = 0xf0

        self.execute_sbc_borrow_in_borrow_out_no_overflow_positive_result(0xE9, 2, mock_memory_controller)
        self.assertEqual(mock_memory_controller.read.call_count, 1)

    def test_execute_sbc_zeropage_borrow_in_borrow_out_no_overflow_positive_result(self):

        mock_memory_controller = Mock()
        # we're mocking 0xE5 0x20 and [0x20] = 0xf0
        mock_memory_controller.read.side_effect = [0x20, 0xf0]

        self.execute_sbc_borrow_in_borrow_out_no_overflow_positive_result(0xE5, 3, mock_memory_controller)
        self.assertEqual(mock_memory_controller.read.call_count, 2)

    def test_execute_sbc_zeropageX_borrow_in_borrow_out_no_overflow_positive_result(self):

        mock_memory_controller = Mock()
        # we're mocking 0xF5 0x20 and [0x23] = 0xf0
        mock_memory_controller.read.side_effect = [0x20, 0xf0]

        self.execute_sbc_borrow_in_borrow_out_no_overflow_positive_result(0xF5, 4, mock_memory_controller, x_index = 3)
        self.assertEqual(mock_memory_controller.read.call_count, 2)

    def test_execute_sbc_absolute_borrow_in_borrow_out_no_overflow_positive_result(self):

        mock_memory_controller = Mock()
        # we're mocking 0xED 0x0 0x20 and [0x2000] = 0xf0
        mock_memory_controller.read.side_effect = [0, 0x20, 0xf0]

        self.execute_sbc_borrow_in_borrow_out_no_overflow_positive_result(0xED, 4, mock_memory_controller)
        self.assertEqual(mock_memory_controller.read.call_count, 3)

    def test_execute_sbc_absoluteX_borrow_in_borrow_out_no_overflow_positive_result(self):

        mock_memory_controller = Mock()
        # we're mocking 0xFD 0x00 0x20 and [0x2003] = 0xf0
        mock_memory_controller.read.side_effect = [0x00, 0x20, 0xf0]

        self.execute_sbc_borrow_in_borrow_out_no_overflow_positive_result(0xFD, 4, mock_memory_controller, x_index = 3)
        self.assertEqual(mock_memory_controller.read.call_count, 3)

    def test_execute_sbc_absoluteX_borrow_in_borrow_out_no_overflow_positive_result_extra_cycle(self):

        mock_memory_controller = Mock()
        # we're mocking 0xFD 0xfe 0x20 and [0x2101] = 0xf0
        mock_memory_controller.read.side_effect = [0xfe, 0x20, 0xf0]

        self.execute_sbc_borrow_in_borrow_out_no_overflow_positive_result(0xFD, 5, mock_memory_controller, x_index = 3)
        self.assertEqual(mock_memory_controller.read.call_count, 3)

    def test_execute_sbc_absoluteY_borrow_in_borrow_out_no_overflow_positive_result(self):

        mock_memory_controller = Mock()
        # we're mocking 0xF9 0x00 0x20 and [0x2003] = 0xf0
        mock_memory_controller.read.side_effect = [0x00, 0x20, 0xf0]

        self.execute_sbc_borrow_in_borrow_out_no_overflow_positive_result(0xF9, 4, mock_memory_controller, y_index = 3)
        self.assertEqual(mock_memory_controller.read.call_count, 3)

    def test_execute_sbc_absoluteY_borrow_in_borrow_out_no_overflow_positive_result_extra_cycle(self):

        mock_memory_controller = Mock()
        # we're mocking 0xF9 0xfe 0x20 and [0x2101] = 0xf0
        mock_memory_controller.read.side_effect = [0xfe, 0x20, 0xf0]

        self.execute_sbc_borrow_in_borrow_out_no_overflow_positive_result(0xF9, 5, mock_memory_controller, y_index = 3)
        self.assertEqual(mock_memory_controller.read.call_count, 3)

    def test_execute_sbc_indirectX_borrow_in_borrow_out_no_overflow_positive_result(self):

        mock_memory_controller = Mock()
        # we're mocking 0xE1 0x20 and [0x23] = 0x1234 [0x1234] = 0xf0
        mock_memory_controller.read.side_effect = [0x20, 0x34, 0x12, 0xf0]

        self.execute_sbc_borrow_in_borrow_out_no_overflow_positive_result(0xE1, 6, mock_memory_controller, x_index = 3)
        self.assertEqual(mock_memory_controller.read.call_count, 4)

    def test_execute_sbc_indirectY_borrow_in_borrow_out_no_overflow_positive_result(self):

        mock_memory_controller = Mock()
        # we're mocking 0xF1 0x20 and [0x20] = 0x1234 [0x1237] = 0xf0
        mock_memory_controller.read.side_effect = [0x44, 0x34, 0x12, 0xf0]

        self.execute_sbc_borrow_in_borrow_out_no_overflow_positive_result(0xF1, 5, mock_memory_controller, y_index = 3)
        self.assertEqual(mock_memory_controller.read.call_count, 4)

    def test_execute_sbc_indirectY_borrow_in_borrow_out_no_overflow_positive_result_extra_cycle(self):

        mock_memory_controller = Mock()
        # we're mocking 0xF1 0x20 and [0x20] = 0x1234 [0x1301] = 0xf0
        mock_memory_controller.read.side_effect = [0x44, 0xfe, 0x12, 0xf0]

        self.execute_sbc_borrow_in_borrow_out_no_overflow_positive_result(0xF1, 6, mock_memory_controller, y_index = 3)
        self.assertEqual(mock_memory_controller.read.call_count, 4)

    def test_execute_sbc_immediate_no_borrow_in_borrow_out_overflow_negative_result(self):

        opcode = OpCode()
        registers = Registers()
        registers.accumulator = 0x50
        registers.carry_flag = True

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # Mocking 0xE9 0xb0 so subtracting 0x50 - 0xb0 (80 - -80)
            mock_memory_controller.read.return_value = 0xb0
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = opcode.execute(0xE9, registers, mock_memory_controller)
            self.assertEqual(count, 2)
            self.assertTrue(registers.accumulator == 0xa0)
            self.assertFalse(registers.zero_flag)
            self.assertTrue(registers.negative_flag)
            self.assertFalse(registers.carry_flag)
            self.assertTrue(registers.overflow_flag)

    def test_execute_sbc_immediate_borrow_in_borrow_out_no_overflow_negative_result(self):

        opcode = OpCode()
        registers = Registers()
        registers.accumulator = 0x50

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # Mocking 0xE9 0x70 so subtracting 0x150 - 0x70 (borrow 'in')
            mock_memory_controller.read.return_value = 0x70
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = opcode.execute(0xE9, registers, mock_memory_controller)
            self.assertEqual(count, 2)
            self.assertEqual(registers.accumulator, 0xdf)
            self.assertFalse(registers.zero_flag)
            self.assertTrue(registers.negative_flag)
            self.assertFalse(registers.carry_flag)
            self.assertFalse(registers.overflow_flag)

    def test_execute_sbc_immediate_no_borrow_in_no_borrow_out_no_overflow_positive_result(self):

        opcode = OpCode()
        registers = Registers()
        registers.accumulator = 0x50
        registers.carry_flag = True

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # Mocking 0xE9 0x70 so subtracting 0x50 - 0x30 (80-48 = 32)
            mock_memory_controller.read.return_value = 0x30
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = opcode.execute(0xE9, registers, mock_memory_controller)
            self.assertEqual(count, 2)
            self.assertTrue(registers.accumulator == 0x20)
            self.assertFalse(registers.zero_flag)
            self.assertFalse(registers.negative_flag)
            self.assertTrue(registers.carry_flag)
            self.assertFalse(registers.overflow_flag)

    def test_execute_sbc_immediate_borrow_in_borrow_out_no_overflow_negative_result_2(self):

        opcode = OpCode()
        registers = Registers()
        registers.accumulator = 0xd0 #start with negative acc this time

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # Mocking 0xE9 0x70 so subtracting 0xd0 - 0xf0 (-48 - -16 = -32)
            mock_memory_controller.read.return_value = 0xf0
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = opcode.execute(0xE9, registers, mock_memory_controller)
            self.assertEqual(count, 2)
            self.assertEqual(registers.accumulator, 0xdf)
            self.assertFalse(registers.zero_flag)
            self.assertTrue(registers.negative_flag)
            self.assertFalse(registers.carry_flag)
            self.assertFalse(registers.overflow_flag)

    def test_execute_sbc_immediate_no_borrow_in_no_borrow_out_no_overflow_positive_result_2(self):

        opcode = OpCode()
        registers = Registers()
        registers.accumulator = 0xd0 #start with negative acc this time
        registers.carry_flag = True

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # Mocking 0xE9 0x70 so subtracting 0xd0 - 0xb0 (-48 - -80 = 32)
            mock_memory_controller.read.return_value = 0xb0
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = opcode.execute(0xE9, registers, mock_memory_controller)
            self.assertEqual(count, 2)
            self.assertTrue(registers.accumulator == 0x20)
            self.assertFalse(registers.zero_flag)
            self.assertFalse(registers.negative_flag)
            self.assertTrue(registers.carry_flag)
            self.assertFalse(registers.overflow_flag)

    def test_execute_sbc_immediate_borrow_in_no_borrow_out_overflow_positive_result(self):

        opcode = OpCode()
        registers = Registers()
        registers.accumulator = 0xd0 #start with negative acc this time

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # Mocking 0xE9 0x70 so subtracting 0xd0 - 0x70 (-48 - 112 = 96 (overflow))
            mock_memory_controller.read.return_value = 0x70
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = opcode.execute(0xE9, registers, mock_memory_controller)
            self.assertEqual(count, 2)
            self.assertEqual(registers.accumulator, 0x5f)
            self.assertFalse(registers.zero_flag)
            self.assertFalse(registers.negative_flag)
            self.assertTrue(registers.carry_flag)
            self.assertTrue(registers.overflow_flag)

    def test_execute_sbc_immediate_no_borrow_in_no_borrow_out_no_overflow_negative_result(self):

        opcode = OpCode()
        registers = Registers()
        registers.accumulator = 0xd0 #start with negative acc this time
        registers.carry_flag = True

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # Mocking 0xE9 0x30 so subtracting 0xd0 - 0x30 (-48 - 48 = -96)
            mock_memory_controller.read.return_value = 0x30
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = opcode.execute(0xE9, registers, mock_memory_controller)
            self.assertEqual(count, 2)
            self.assertTrue(registers.accumulator == 0xa0)
            self.assertFalse(registers.zero_flag)
            self.assertTrue(registers.negative_flag)
            self.assertTrue(registers.carry_flag)
            self.assertFalse(registers.overflow_flag)

if __name__ == '__main__':
    unittest.main()