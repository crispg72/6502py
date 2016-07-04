import unittest
from opcodes import OpCode


class OpCodeTests(unittest.TestCase):
    
    def test_execute_nop(self):

        count = OpCode.execute(0xEA, None, None)
        self.assertEqual(count, 2)

if __name__ == '__main__':
    unittest.main()