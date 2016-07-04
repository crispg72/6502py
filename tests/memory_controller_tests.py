import unittest
from memory_controller import MemoryController


class MemoryControllerTests(unittest.TestCase):
    
    def test_read_with_no_buffer_raises(self):

        controller = MemoryController()

        with self.assertRaises(TypeError):
        	value = controller.read(0)

    def test_write_with_no_buffer_raises(self):

        controller = MemoryController()

        with self.assertRaises(TypeError):
        	controller.write(0, 0)

    def test_read_from_invalid_address_raises(self):

        controller = MemoryController(10)

        with self.assertRaises(IndexError):
        	value = controller.read(11)

if __name__ == '__main__':
    unittest.main()