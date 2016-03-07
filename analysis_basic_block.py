from idautils import *
from idaapi import *
import register


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
	
#this is the ndss paper's feature of a function
#this is for experiment purpose, will not use it in practice
'''
data_transfer = ['movsx','movss', 'movzx','cmov','cmova','cmovae','cmovb','cmovbe','cmovc','cmove','cmovg','cmovge','cmovl','cmovle','cmovna','cmovnae','cmovnb','cmovnbe','cmovnc','cmovne','cmovng','cmovnge','cmovnl','cmovnle','cmovno','cmovnp','cmovns','cmovnz','cmovo','cmovp','cmovpe','cmovpo','cmovs','cmovz','set','seta','setae','setb','setbe','setc','sete','setg','setge','setl','setle','setna','setnae','setnb','setnbe','setnc','setne','setng','setnge','setnl','setnle','setno','setnp','setns','setnz','seto','setp','setpe','setpo','sets','setz','xchg','cmpxchg']
arithmetic = ['add','adc','sub','sbb','mul','imul','div','neg', 'idiv', 'inc', 'dec']
stack = ['pusha', 'pushf', 'popa', 'popf']
logical = ['and','or','not']
shift_rotate = ['shr','shl','sal','sar','rol','ror','rcl','rcr']
control_transfer = ['jno','jnp','jns','jo','jp','jpe','jpo','js','jecxz','jcxz']
loop = ['loop','loopne','loopnz','loope','loopz']
string = ['cmps','cmpsb','cmpsw','cmpsd','cmpsq','lods','lodsb','lodsw','lodsd','lodsq','movs','movsb','movsw','movsd','movsq','scas','scasb','scasw','scasd','scasq','stos','stosb','stosw','stosd','stosq','rep']
flag = ['cld','clc','stc','std', 'cmc', 'sti', 'cli']
sign = ['cbw', 'cwd', 'cwde', 'cdq', 'csq']
misc =['hlt', 'retn', 'retf']
fpu = ['fld', 'fstp']
port = ['in', 'out']
common = ['mov', 'jmp', 'cmp', 'lea', 'jz', 'jnz', 'jmp', 'jl', 'jle', 'jb', 'jbe']

call_tags = ['mem', 'str', 'cpy', 'cat', 'move', 'host', 'reg', 'set', 'get', 'open', 'write', 'read', 'close', 'error', 'len', 'alloc', 'brk', 'fork', 'io', 'heap', 'name', 'crypt', 'net', 'socket', 'sys', 'file', 'load', 'lib', 'cache', 'mutex', 'proc', 'thread', 'process', 'sleep', 'chk', 'free', 'put', 'print']
'''


def Ndss_imp():
	t0 = time.time()
	t_count = 0
	for seg in Segments():	
	
		if SegName(seg) == ".text" or SegName(seg) == ".plt":
	
			#functions = Functions(seg)
			#for func_ea in functions:				
				bb_count = 0
				instr_count = 0
				func_ea = here()
				
				print FuncItems(func_ea)
				#getStack(func_ea)
				var_count = getStack(func_ea)
				#print len(list(CodeRefsTo(func_ea, 1)))
				#print hex(func_ea)
				redirection_count = 0
				incoming_call_count = len(list(CodeRefsTo(func_ea, 1)))
				outcoming_call_count = 0
				transfer_instr_count = 0
				logic_instr_count = 0
				logical = ['and','or','not','xor']
				misc =['hlt', 'retn', 'retf']
				edges_count = 0
				for bb in FlowChart(get_func(func_ea)):
					bb_count += 1
					t_count += 1
					#print hex(bb.startEA)
					for head in Heads(bb.startEA,bb.endEA):
						if isCode(getFlags(head)):
							instr_count += 1
							mnem = GetMnem(head)
							if mnem == "call":
								outcoming_call_count  += 1
								redirection_count += 1
							elif "j" in mnem:
								transfer_instr_count += 1
								edges_count += 2
								redirection_count += 1
							if mnem == "jmp":
								edges_count -= 1
							if mnem in logical:
								logic_instr_count += 1
							if mnem in misc:
								redirection_count += 1
								
								
	print t_count
	print time.time() - t0	
	
	print "bb_count: " + str(bb_count)
	print "incoming_call_count: " + str(incoming_call_count)
	print "instr_count: " + str(instr_count)
	print "outcoming_call_count: " + str(outcoming_call_count)
	print "transfer_instr_count: " + str(transfer_instr_count)
	print "edges_count: " + str(edges_count)
	print "logic_instr_count: " + str(logic_instr_count)
	print "var_count: " + str(var_count)
	print "redirection_count: " + str(redirection_count)

	
def getStack(address):
	'gets variables used on the stack'
	# Related reads and/or pointers on stacks in IDA
	# http://zairon.wordpress.com/2008/02/15/idc-script-and-stack-frame-variables-length/
	# https://github.com/moloch--/IDA-Python/blob/master/Stack_Calculator.py
	stackFrame = GetFrame(address)
	lastEntry = GetLastMember(stackFrame)
	count = 0
	c = 0
	#stack = []
	while count <= lastEntry:
			localName = GetMemberName(stackFrame,count)
			size = GetMemberSize(stackFrame, count)
			flag = GetMemberFlag(stackFrame, count)
			if localName == None or size == None or flag == -1:
					count += 1
					continue 
			#stack.append((localName, size, hex(flag)))
			count += size
			c += 1
	# returns stack variable list[tuple(localName, size, hex(flags))]
	return c	
	
def t():
	func_ea = here()
	print len(list(CodeRefsTo(func_ea, 1)))
	
def main():
	func_ea = here()
	print GetFunctionName(func_ea)
	for bb in FlowChart(get_func(func_ea)):
		info = get_bb_basic_info(bb)	
		print info
	
if __name__ == '__main__':
    #main()
	Ndss_imp()

	#t()