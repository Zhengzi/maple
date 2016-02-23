#import pyvex
#import archinfo
from idautils import *
from idaapi import *

def tanslate(bb):
	for head in Heads(bb.startEA,bb.endEA):
		if isCode(getFlags(head)):
			#I give up now, so I use a very silly way to do this.
			#find a starting address 
			#find a ending address
			#then find all the byte from them
			instr = ""
			for ea in range(ItemHead(head), ItemEnd(head)):
				instr += format_instr(Byte(ea))
			
			#Get the vex representation of the x86 code
			#need linux enviroment to install pyvex pacakage			
			#irsb = pyvex.IRSB(instr, 0x400000, archinfo.ArchX86())
			print instr
			
	#irsb = pyvex.IRSB(bb, archinfo.VexArchX86)

#format the instr convert "0x4" to "\x04"	
def format_instr(byte):
	s = str(hex(byte))
	if len(s) == 3:
		s = s[:2] + '0' + s[2:]
	s = '\\' + s[1:]
	return s
	
def main():
	func_ea = here()
	print GetFunctionName(func_ea)
	for bb in FlowChart(get_func(func_ea)):
		tanslate(bb)
	return


if __name__ == '__main__':
    main()