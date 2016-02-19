from enum import Enum
#TODO: use vex IR to replace the x86 registers
class Register(Enum):
	eax = 0
	ebx = 1
	ecx = 2
	edx = 3
	esi = 4
	edi = 5
	esp = 6
	ebp = 7