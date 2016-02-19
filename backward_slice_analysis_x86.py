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
def taint_reg(reg, bb, index):
	return
	
def main():
	#taint_reg()
	return
	
if __name__ == '__main__':
    main()