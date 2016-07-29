from idautils import *
from idaapi import *

def save(path):
	for seg in Segments():			
		if SegName(seg) == ".text":
			functions = Functions(seg)
			for func_ea in functions:	
				#func_ea = here()
				name = GetFunctionName(func_ea)
				#print name[0:3]
				if name[0:3] == "sub":
					path_new = path + GetFunctionName(func_ea) + ".txt"
					f = open(path_new, 'w')
					for bb in FlowChart(get_func(func_ea), flags=FC_PREDS):
						list = []
						
						for head in Heads(bb.startEA,bb.endEA):
							if isCode(getFlags(head)):
								mnem = GetMnem(head)
								list.append(mnem)
						
						
						#preds = bb.preds()

				
						
						#f.write(str(hex(bb.startEA)))	
						#f.write(" ")
						f.write(','.join(list))
						'''
						if preds:
							f.write(" ")
							for preds_block in preds:	
								f.write(str(hex(preds_block.startEA)))
								f.write(",")
								
						'''
						f.write('\n')
					f.close()
	
if __name__ == '__main__':
	save("C:\\Users\\Xu Zhengzi\\Desktop\\adobe_ro\\")
