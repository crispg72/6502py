import unittest

from unittest.mock import patch
from memory_controller import MemoryController
from registers import Registers
from opcodes import OpCode


class OpCodeTestsArithmetic(unittest.TestCase):
    
    def execute_adc_carry_clear(self, opcode, expected_clocks):

        registers = Registers()
        registers.accumulator = 5
        registers.zero_flag = True
        registers.negative_flag = True  

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            mock_memory_controller.read.return_value = 0x22
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = OpCode.execute(opcode, registers, mock_memory_controller)
            self.assertEqual(count, expected_clocks)
            self.assertTrue(registers.accumulator == 0x27)
            self.assertFalse(registers.zero_flag)
            self.assertFalse(registers.negative_flag)
            self.assertFalse(registers.carry_flag)

    def execute_adc_carry_set(self, opcode, expected_clocks):

        registers = Registers()
        registers.accumulator = 5
        registers.zero_flag = True
        registers.negative_flag = True  
        registers.carry_flag = True  

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            mock_memory_controller.read.return_value = 0x22
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = OpCode.execute(opcode, registers, mock_memory_controller)
            self.assertEqual(count, expected_clocks)
            self.assertTrue(registers.accumulator == 0x28)
            self.assertFalse(registers.zero_flag)
            self.assertFalse(registers.negative_flag)
            self.assertFalse(registers.carry_flag)

    def execute_adc_should_set_carry(self, opcode, expected_clocks):

        registers = Registers()
        registers.accumulator = 1
        registers.zero_flag = False
        registers.negative_flag = True    

        with patch.object(MemoryController, 'read') as mock_memory_controller:

            mock_memory_controller.read.return_value = 0xff
            registers.pc += 1 #need to fake the cpu reading the opcode
            count = OpCode.execute(opcode, registers, mock_memory_controller)
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


if __name__ == '__main__':
    unittest.main()