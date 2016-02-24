#import pyvex
#import archinfo
from idautils import *
from idaapi import *
from entity_class_def import BasicBlock as bb_class
import pickle


def creat_bb_instance(bb, func_name):
	bb_ins = bb_class(5)
	bb_ins.start_address = bb.startEA
	bb_ins.end_address = bb.endEA		
	bb_ins.instr = tanslate(bb)
	bb_ins.func = func_name
	
	#hard code the address for testing purpose
	pickle.dump(bb_ins, file("C:\\Users\\user1\\Desktop\\test\\" + str(hex(bb.startEA))+".pickle",'w'))
	#bb.program = None
	
	
def tanslate(bb):
	instruction = []
	for head in Heads(bb.startEA,bb.endEA):
		if isCode(getFlags(head)):
			#I give up now, so I use a very silly way to do this.
			#find a starting address 
			#find a ending address
			#then find all the bytes between them
			instr = ""
			for ea in range(ItemHead(head), ItemEnd(head)):
				instr += format_instr(Byte(ea))
			
			#Get the vex representation of the x86 code
			#need linux enviroment to install pyvex pacakage			
			#irsb = pyvex.IRSB(instr, 0x400000, archinfo.ArchX86())
			print instr
			instruction.append(instr)
			
	return 	instruction	
	#irsb = pyvex.IRSB(bb, archinfo.VexArchX86)

#format the instr convert "0x4" to "\x04"	
def format_instr(byte):
	s = str(hex(byte))
	if len(s) == 3:
		s = s[:2] + '0' + s[2:]
	s = '\\' + s[1:]
	return s
	
def main():
	for seg in Segments():		
		if SegName(seg) == ".text":
			functions = Functions(seg)					
			for func_ea in functions:	
				
				#fix: the Functions method will return functions fall outside the ".text" segment
				#we need to check the Segname again to remove the "extern" part of functions
				if SegName(func_ea) == ".text":		
					print GetFunctionName(func_ea)
					for bb in FlowChart(get_func(func_ea)):
					#tanslate(bb)
						creat_bb_instance(bb, GetFunctionName(func_ea))
	return


if __name__ == '__main__':
    main()