import pyvex
import archinfo
from entity_class_def import BasicBlock as bb_class
import os
import pickle

#For I cannot install the pyvex on Window, so I need to use this script to convert x86 to vex on linux system. Then I can do analysis on it

#future: we need to be able to convert all assembly to vex using this function
#directly modify the bb class
def convert_x86_to_vex(bb):
	instructions = ""
	for ins in bb.instr:
		instructions += ins
		
	irsb = pyvex.IRSB(instructions, bb.startEA, archinfo.ArchX86())
	bb.vex = irsb
	
	#testing
	print irsb.pp()
	#endtest
	
	return
	
	
def load_basic_block(filename):
	bb_ins = pickle.load(file(filename))
	return bb_ins
	
def main():
	#hard code the dir which stores the data 
	dir = ""
	#
	for file in os.listdir(dir):
		if file.endswith(".pickle"):
			bb_ins = load_basic_block(file)
			convert_x86_to_vex(bb_ins)
	return

if __name__ == '__main__':
    main()