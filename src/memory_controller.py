class MemoryController(object):

	def __init__(self, buffer_size = None):

		if buffer_size:
			self.buffer = bytearray(buffer_size)
		else:
			self.buffer = None

	def read(self, address):

		return self.buffer[address]

	def write(self, address, value):

		self.buffer[address] = value