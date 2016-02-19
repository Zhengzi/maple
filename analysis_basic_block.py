from enum import Enum
from idautils import *
from idaapi import *

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

#TODO: get a full list of critical APIs	
api_list_gl = ["memcpy"]

#given a basic block, return the basic info of the bb. The info is then used for machine learning
def get_bb_basic_info(bb):
	
	#initialize the info of bb
	info = "bb: " + str(hex(bb.startEA)) + "\n"
	
	#get_no_of_instructions
	count = 0 
	for head in Heads(bb.startEA,bb.endEA):
		if isCode(getFlags(head)):
			count += 1
			
	format_str = "ints: " + str(count) + "\n"
	info += format_str
	
	#get_no_of_registers
	count = [0,0,0,0,0,0,0,0]
	for head in Heads(bb.startEA,bb.endEA):
		if isCode(getFlags(head)):
			for i in range(8):
				if Register(i).name in idc.GetDisasm(head):
					count[i] += 1		
					
	format_str = "reg: " + str(count) + "\n"
	info += format_str
	
	#TODO: implement this functionnality
	'''
	#get_apis_in_patch
	api_list = []
	for line in text:
		for api in api_list_gl:
			if api in line:
				api_list.append(api)
				
	format_str = "reg: " + str(api_list) + "\n"
	info += format_str
	'''
	
	#get_apis_in_func
	calls = []
	for head in Heads(bb.startEA,bb.endEA):
		if isCode(getFlags(head)):
			mnem = GetMnem(head)
			if mnem == "call":
				calls.append(GetOpnd(head, 0))
	format_str = "calls: " + str(calls) + "\n"
	info += format_str
	
	#get_no_of_check
	count = 0 
	for head in Heads(bb.startEA,bb.endEA):
		if isCode(getFlags(head)):
			mnem = GetMnem(head)
			if mnem == "test" or mnem == "cmp":
				count += 1
	format_str = "check: " + str(count) + "\n"
	info += format_str
	
	#get_no_of_memory_access
	count = 0 
	for head in Heads(bb.startEA,bb.endEA):
		if isCode(getFlags(head)):
			op_first = GetOpType(head, 0)			
			if op_first == 2 or op_first == 3 or op_first == 4:
				count += 1
				
			op_second = GetOpType(head, 1)
			if op_second == 2 or op_second == 3 or op_second == 4:
				count += 1
				
	format_str = "mem: " + str(count) + "\n"
	info += format_str
	
	#get_bb_sig
	sig = []
	for head in Heads(bb.startEA,bb.endEA):
		if isCode(getFlags(head)):
			mnem = GetMnem(head)
			sig.append(mnem)
	format_str = "signature: " + str(sig) + "\n"
	info += format_str
	
	#TODO: use a info class to store the info getted, or to store it in the bb wrapper class
	return info
	
def main():
	func_ea = here()
	print GetFunctionName(func_ea)
	for bb in FlowChart(get_func(func_ea)):
		info = get_bb_basic_info(bb)	
		print info
	
if __name__ == '__main__':
    main()