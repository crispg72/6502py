import unittest

from unittest.mock import patch
from memory_controller import MemoryController
from registers import Registers
from opcodes import OpCode


class RegistersTests(unittest.TestCase):
    
    def test_set_NZ_non_zero_positive(self):

        registers = Registers()
        registers.set_NZ(1)
        self.assertFalse(registers.negative_flag)
        self.assertFalse(registers.zero_flag)

    def test_set_NZ_zero_positive(self):

        registers = Registers()
        registers.set_NZ(0)
        self.assertFalse(registers.negative_flag)
        self.assertTrue(registers.zero_flag)

    def test_set_NZ_non_zero_negative(self):

        registers = Registers()
        registers.set_NZ(-3)
        self.assertTrue(registers.negative_flag)
        self.assertFalse(registers.zero_flag)

    def test_set_NZV_non_zero_negative_no_overflow(self):

        registers = Registers()
        registers.accumulator = 4
        registers.set_NZV(-3, 1)
        self.assertFalse(registers.negative_flag)
        self.assertFalse(registers.zero_flag)
        self.assertFalse(registers.overflow_flag)

    def test_set_NZV_non_zero_not_negative_overflow(self):

        registers = Registers()
        registers.accumulator = 0x80
        # Here we act as if we have done -128 + -1
        registers.set_NZV(0xff, 0x7f)
        self.assertFalse(registers.negative_flag)
        self.assertFalse(registers.zero_flag)
        self.assertTrue(registers.overflow_flag)

    def test_set_NZV_non_zero_negative_overflow(self):

        registers = Registers()
        registers.accumulator = 0x7f
        # Here we act as if we have done 127 + 1
        registers.set_NZV(1, 0x80)
        self.assertTrue(registers.negative_flag)
        self.assertFalse(registers.zero_flag)
        self.assertTrue(registers.overflow_flag)

if __name__ == '__main__':
    unittest.main()