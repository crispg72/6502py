import pytest
from emupy6502.memory_controller import MemoryController


def test_read_with_no_buffer_raises():

    controller = MemoryController()

    with pytest.raises(TypeError):
        controller.read(0)

def test_write_with_no_buffer_raises():

    controller = MemoryController()

    with pytest.raises(TypeError):
        controller.write(0, 0)

def test_read_from_invalid_address_raises():

    controller = MemoryController(10)

    with pytest.raises(IndexError):
        controller.read(11)
