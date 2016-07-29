from idautils import *
from idaapi import *
import networkx as nx
import time
import matplotlib.pyplot as plt
import pickle
def main2():
	with open("gan.txt" , 'w') as f:
		for seg in Segments():	
		
			#we only focus on the basic block in the text section
			#TODO: add support to determine the sections, which contains the useful basic blocks 
			if SegName(seg) == ".text":
		
				functions = Functions(seg)		
				for func_ea in functions:		
				#func_ea = here()
					if not get_func(func_ea).does_return():
						print GetFunctionName(func_ea)
						f.write(GetFunctionName(func_ea))
						f.write("\n")

						
def main3():
	func_ea = here()
	for bb in FlowChart(get_func(func_ea), flags=FC_PREDS):
		for head in Heads(bb.startEA,bb.endEA):
			print hex(head) + str(isCode(getFlags(head)))

def main4():
	with open("fail_hack.txt" , 'w') as f:
		for seg in Segments():	
			if SegName(seg) == ".text":
				functions = Functions(seg)	
				#func_ea = here() ##
				#print hex(func_ea)
				for func_ea in functions:
					flag_retn = False
					
					for bb in FlowChart(get_func(func_ea), flags=FC_PREDS):
						
						succs = bb.succs()

						if succs:
							if len(list(succs)) != 0:
								continue
						print hex(bb.startEA)
						print hex(bb.endEA)
						
						for head in Heads(bb.startEA,bb.endEA):
							if isCode(getFlags(head)):
								mnem = GetMnem(head)
								#print mnem
								if mnem == "retn":
									flag_retn = True
						li = list(Heads(bb.startEA,bb.endEA))	
						if li:							
							mnem = GetMnem(li[-1])
						#print mnem
						if mnem == "jmp":
							flag_retn = True
									
					if not flag_retn:
						name = GetFunctionName(func_ea)				
						f.write(name) 
						f.write("\n")
						
					#break
def main():
	#idaapi.autoWait()
	count = 0
	with open("no_return.txt" , 'w') as f:
		for seg in Segments():	
			if SegName(seg) == ".text":
				functions = Functions(seg)	
				for func_ea in functions:		
					#func_ea = here()
					func = idaapi.get_func(func_ea)
					#func = func_ea
					flags = idc.GetFunctionFlags(func_ea)
					name = GetFunctionName(func_ea)					
					if flags & FUNC_NORET:
						f.write(name) 
						f.write("\n")
						count += 1
					'''
					if flags & FUNC_FAR:
						f.write("FUNC_FAR") 
						#print hex(func), "FUNC_FAR"
					if flags & FUNC_LIB:
						f.write("FUNC_LIB") 
						#print hex(func), "FUNC_LIB"
					if flags & FUNC_STATIC:
						f.write("FUNC_STATIC") 
						#print hex(func), "FUNC_STATIC"
					if flags & FUNC_FRAME:
						f.write("FUNC_FRAME") 
						#print hex(func), "FUNC_FRAME"
					if flags & FUNC_USERFAR:
						f.write("FUNC_USERFAR") 
						#print hex(func), "FUNC_USERFAR"
					if flags & FUNC_HIDDEN:
						f.write("FUNC_HIDDEN") 
						#print hex(func), "FUNC_HIDDEN"
					if flags & FUNC_THUNK:
						f.write("FUNC_THUNK") 
						#print hex(func), "FUNC_THUNK"
					if flags & FUNC_LIB:
						f.write("FUNC_LIB") 
						#print hex(func), "FUNC_BOTTOMBP"
						
					if flags & FUNC_SP_READY:
						f.write("FUNC_SP_READY") 
					'''
					
					#color = get_func_cmt(func,True)
					#cmt = RptCmt(ea)
					#cmt = idc.GetCommentEx(0x080AC500, True)
					#cmt = GetCommentEx(0xC53B5CAD,1)
					
					#cmt = idautils.get_any_indented_cmt(0xC53B5F77,"red")
					#print cmt
					#print color
					#f.write(str(cmt))
					#f.write(type(color))
					#f.write(color)


					#print flags
					#print hex(func_ea)
		
		
	print "Finish"
	print count
		
if __name__ == '__main__':
	t0 = time.time()
	main4()
	print time.time() - t0