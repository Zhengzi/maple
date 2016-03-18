from idautils import *
from idaapi import *
import register
import re
import networkx as nx

#This file aims to perform the static backward slicing on x86 instruction set
#TODO: add backward slcing functionality based on vex IR instead of x86

#NOTE: the function is not designed for 100% accurate backward slicing. 
#TODO: coperate it with the value set analysis and symbolic executionn

#given a Register name, the basic block, and the instruction location, the function will return the 
#currently, I only focus on the taint analysis within a function
#I simply ignore the effect of function calls in the basic blocks
#TODO: add in the concept of context sensitivity level in order to get more accurate the 
def back_slicing(bb, index):
	slice = []
	worklist = []
	worklist.append((bb, index))
	while worklist:
		ins = worklist[0]
		del worklist[0]
		if not ins in slice:
			slice.append(ins)
			worklist.append(preds(ins))
	return

#given an instruction, this function aims to determine which of the instruction in the function is tainted.
#currently we only consider context sesitivity 0. (within the function itself)
#we loop over all the instruction spatially sitting before the given instruction to look for the taint
#we ignore the loop, so that the instruction behind the given one will not be tainted
#we ignore the if branch, so that both of the branch will be taken 
#very time consuming implementation O(n^2), need to change later
def preds(ins):
	funcs = getfunction(ins)
	preds = []
	for new_ins in funcs:
		#hack: we loop until we reach the ins it self
		if new_ins == ins:
			break
		
		
def taint(lines):
	#get_s
	lines = [
	"15 | ------ IMark(0x80495b8, 2, 0) ------",
	"16 | t2 = GET:I8(eax)",
	"17 | t1 = GET:I8(eax)",
	"18 | t0 = And8(t2,t1)",
	"19 | PUT(cc_op) = 0x0000000d",
	"20 | t3 = 8Uto32(t0)",
	"21 | PUT(cc_dep1) = t3",
	"22 | PUT(cc_dep2) = 0x00000000",
	"23 | PUT(cc_ndep) = 0x00000000",
	"24 | PUT(eip) = 0x080495ba",
	"25 | ------ IMark(0x80495ba, 6, 0) ------",
	"26 | t5 = GET:I32(cc_op)",
	"27 | t6 = GET:I32(cc_dep1)",
	"28 | t7 = GET:I32(cc_dep2)",
	"29 | t8 = GET:I32(cc_ndep)",
	"30 | t9 = x86g_calculate_condition(0x00000004,t5,t6,t7,t8):Ity_I32",
	"31 | t4 = 32to1(t9)",
	"32 | if (t4) { PUT(eip) = 0x8049735L; Ijk_Boring }",
	"33 | PUT(eip) = 0x080495c0",
	"34 | t10 = GET:I32(eip)"
	]
	queue = []
	cfg = nx.DiGraph()
	for line in lines:
		
		if "if" in line:
			key = re.findall('t[0-9]+|cc_[a-z]+[0-9]?|eax|ebx|ecx|edx|esi|edi|esp|ebp', line)
		elif "=" in line:
			ls = line.split('=',1)		
			rhs = re.findall('t[0-9]+|cc_[a-z]+[0-9]?|eax|ebx|ecx|edx|esi|edi|esp|ebp', ls[0])
			lhs = re.findall('t[0-9]+|cc_[a-z]+[0-9]?|eax|ebx|ecx|edx|esi|edi|esp|ebp', ls[1])
		
			
			if rhs and lhs:
				r = rhs[0]
				#print lhs.captures(1)
				for item in lhs:
					cfg.add_edge(r, item)
				
	lst = list(nx.dfs_postorder_nodes(cfg, key))
	print lst

		
def getfunction(ins):
	return
	
def taint_reg(reg, bb, index):
	return
	
def main():
	#taint_reg()
	return
	
if __name__ == '__main__':
    #main()
	taint()