import unittest

from unittest.mock import patch
from memory_controller import MemoryController
from registers import Registers
from opcodes import OpCode


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

    def test_execute_sbc_immediate_carry_clear_result_positive(self):

        opcode = OpCode()
        registers = Registers()
        registers.accumulator = 5
        registers.zero_flag = True
        registers.negative_flag = True  

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # Mocking 0xE9 0x04
            mock_memory_controller.read.return_value = 3
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = opcode.execute(0xE9, registers, mock_memory_controller)
            self.assertEqual(count, 2)
            self.assertTrue(registers.accumulator == 1)
            self.assertFalse(registers.zero_flag)
            self.assertFalse(registers.negative_flag)
            self.assertFalse(registers.carry_flag)

    def test_execute_sbc_immediate_carry_clear_result_zero(self):

        opcode = OpCode()
        registers = Registers()
        registers.accumulator = 5
        registers.negative_flag = True  

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # Mocking 0xE9 0x05
            mock_memory_controller.read.return_value = 4
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = opcode.execute(0xE9, registers, mock_memory_controller)
            self.assertEqual(count, 2)
            self.assertTrue(registers.accumulator == 0)
            self.assertTrue(registers.zero_flag)
            self.assertFalse(registers.negative_flag)
            self.assertFalse(registers.carry_flag)

    def test_execute_sbc_immediate_carry_clear_result_negative(self):

        opcode = OpCode()
        registers = Registers()
        registers.accumulator = 5

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # Mocking 0xE9 0x06
            mock_memory_controller.read.return_value = 5
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = opcode.execute(0xE9, registers, mock_memory_controller)
            self.assertEqual(count, 2)
            self.assertTrue(registers.accumulator == 0xff)
            self.assertFalse(registers.zero_flag)
            self.assertTrue(registers.negative_flag)
            self.assertFalse(registers.carry_flag)

    def test_execute_sbc_immediate_carry_set_result_positive(self):

        opcode = OpCode()
        registers = Registers()
        registers.accumulator = 6
        registers.carry_flag = True
        registers.zero_flag = True
        registers.negative_flag = True  

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # Mocking 0xE9 0x04
            mock_memory_controller.read.return_value = 4
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = opcode.execute(0xE9, registers, mock_memory_controller)
            self.assertEqual(count, 2)
            self.assertTrue(registers.accumulator == 2)
            self.assertFalse(registers.zero_flag)
            self.assertFalse(registers.negative_flag)
            self.assertFalse(registers.carry_flag)

    def test_execute_sbc_immediate_carry_set_result_zero(self):

        opcode = OpCode()
        registers = Registers()
        registers.accumulator = 4
        registers.carry_flag = True        
        registers.negative_flag = True  

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # Mocking 0xE9 0x05
            mock_memory_controller.read.return_value = 4
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = opcode.execute(0xE9, registers, mock_memory_controller)
            self.assertEqual(count, 2)
            self.assertTrue(registers.accumulator == 0)
            self.assertTrue(registers.zero_flag)
            self.assertFalse(registers.negative_flag)
            self.assertFalse(registers.carry_flag)

    def test_execute_sbc_immediate_carry_set_result_negative(self):

        opcode = OpCode()
        registers = Registers()
        registers.accumulator = 5
        registers.carry_flag = True

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            # Mocking 0xE9 0x06
            mock_memory_controller.read.return_value = 6
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = opcode.execute(0xE9, registers, mock_memory_controller)
            self.assertEqual(count, 2)
            self.assertTrue(registers.accumulator == 0xff)
            self.assertFalse(registers.zero_flag)
            self.assertTrue(registers.negative_flag)
            self.assertFalse(registers.carry_flag)

if __name__ == '__main__':
    unittest.main()