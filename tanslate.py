#import pyvex
#import archinfo
from idautils import *
from idaapi import *
from entity_class_def import BasicBlock as bb_class
import pickle
import struct


def create_bb_instance(bb, func_name):
	bb_ins = bb_class()
	bb_ins.start_address = bb.startEA
	bb_ins.end_address = bb.endEA		
	bb_ins.instr = tanslate(bb)
	
	#tmp_dic = tanslate_strict(bb)
	#for key,value in 
	#bb_ins.instr_hex = tanslate_hex(bb)
	bb_ins.func = func_name
	
	#hard code the address for testing purpose
	pickle.dump(bb_ins, file("C:\\Users\\Xu Zhengzi\\Desktop\\test\\" + str(hex(bb.startEA))+".pickle",'w'))
	#bb.program = None
	
#this define the strict basic blocks
#asumption is that the basic block only is divided by the "call", in fact there is others.
#FIX: add other seperater support
def create_strict_bb_instances(bb, func_name):
	tmp_dic = tanslate_strict(bb)
	for key, value in tmp_dic.iteritems():
		bb_ins = bb_class()
		bb_ins.start_address = key
		#bb_ins.end_address = bb.endEA		
		bb_ins.instr = value
		bb_ins.func = func_name
		pickle.dump(bb_ins, file("C:\\Users\\Xu Zhengzi\\Desktop\\test\\" + str(hex(key))+".pickle",'w'))
	
def tanslate_strict(bb):
	instructions = {}
	tmp = []
	flag = True
	startadd = ""
	for head in Heads(bb.startEA,bb.endEA):
		if isCode(getFlags(head)):						
			if flag:
				startadd = head
				flag = False
			
			instr = ""
			for ea in range(ItemHead(head), ItemEnd(head)):
				instr += format_instr(Byte(ea))
			tmp.append(instr)
			
			mnem = GetMnem(head)
			if mnem == "call":
				instructions[startadd] = tmp
				tmp = []
				flag = True
	if tmp:
		instructions[startadd] = tmp
	return 	instructions							
	
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
			#print instr
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
						#create_bb_instance(bb, GetFunctionName(func_ea))
						create_strict_bb_instances(bb, GetFunctionName(func_ea))
	return


if __name__ == '__main__':
    main()
	#ss()