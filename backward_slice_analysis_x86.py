from idautils import *
from idaapi import *
import register

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
		
		preds


		
def getfunction(ins):
	return
	
def taint_reg(reg, bb, index):
	return
	
def main():
	#taint_reg()
	return
	
if __name__ == '__main__':
    main()