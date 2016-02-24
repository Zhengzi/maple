class BasicBlock:
	def __init__(self):
		self.start_address = None
		self.end_address = None
		self.instr = None
		self.func = None
		#self.program = None
		self.vex = None
		
	def write_to_file(self):
		return
	def load_from_file(self):
		return
		

class Function:
	def __init__(self, start_address):
		self.start_address = start_address
		self.end_address = None
		self.bb_list = []
		self.in_funcs = None
		self.out_funcs = None
		self.program = None