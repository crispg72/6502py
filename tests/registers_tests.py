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


if __name__ == '__main__':
    unittest.main()