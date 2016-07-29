from idautils import *
from idaapi import *
import networkx as nx
import time
import matplotlib.pyplot as plt
import pickle

def extract_intra_function_cfg(path):
	
	#loop over every segments
	#seg: the starting address for each segments
	for seg in Segments():	

		#we only focus on the basic block in the text section
		#TODO: add support to determine the sections, which contains the useful basic blocks 
		if SegName(seg) == ".text":
	
			functions = Functions(seg)		
			for func_ea in functions:		
			#func_ea = here()
			
				#initialized a directed graph to store cfg
				cfg = nx.DiGraph()
				
				#hack
				#In IDA same basic block will be created serveral times. When adding basic block into the networkx graph,
				#duplicated node will be added. In order to solve this, I use a array to store only one copy of basic block.
				#The same basic block will have the same starting address
				#TODO: use the start address of baisc block to replace the hack
				tmp_bbs = []
				
				#flag FC_PREDS is to get the backward info 
				for bb in FlowChart(get_func(func_ea), flags=FC_PREDS):

					#check if we have already met this bb
					flag = True
					for tmp_bb in tmp_bbs:
						if tmp_bb.startEA == bb.startEA:
							bb = tmp_bb
							flag = False
					if flag:
						tmp_bbs.append(bb)
						
					#TODO: use own basicblock class to wrap the ida pro basic block class
					
					
					list = []
					for head in Heads(bb.startEA,bb.endEA):
							if isCode(getFlags(head)):
								mnem = GetMnem(head)
								list.append(mnem)
					
					cfg.add_node(bb.startEA)
					nx.set_node_attributes(cfg, 'text', {bb.startEA:','.join(list)})
					#cfg.node[bb]['text'] = ','.join(list)
					
					preds = bb.preds()
					succs = bb.succs()
					
					if preds:
						for preds_block in preds:
						
							#check if we have already met this bb
							flag = True
							for tmp_bb in tmp_bbs:
								if tmp_bb.startEA == preds_block.startEA:
									preds_block = tmp_bb
									flag = False
							if flag:
								tmp_bbs.append(preds_block)
								
								
							cfg.add_edge(preds_block.startEA, bb.startEA)

							list = []
							for head in Heads(preds_block.startEA,preds_block.endEA):
									if isCode(getFlags(head)):
										mnem = GetMnem(head)
										list.append(mnem)
							nx.set_node_attributes(cfg, 'text', {preds_block.startEA:','.join(list)})
							#cfg.node[preds_block]['name'] = ','.join(list)
										
							
							
					if succs:
						for succs_block in preds:
						
							#check if we have already met this bb
							flag = True
							for tmp_bb in tmp_bbs:
								if tmp_bb.startEA == succs_block.startEA:
									succs_block = tmp_bb
									flag = False
							if flag:
								tmp_bbs.append(succs_block)
								
							cfg.add_edge(bb.startEA, succs_block.startEA)
							
							list = []
							for head in Heads(succs_block.startEA,succs_block.endEA):
									if isCode(getFlags(head)):
										mnem = GetMnem(head)
										list.append(mnem)
										
							nx.set_node_attributes(cfg, 'text', {succs_block.startEA:','.join(list)})
							#cfg.node[succs_block]['name'] = ','.join(list)
							
				path_new = path + GetFunctionName(func_ea) + ".gml"
				nx.write_gml(cfg, path_new)			
	return
	
def main():
	idaapi.autoWait()
	extract_intra_function_cfg("C:\\Users\\Xu Zhengzi\\Desktop\\linux317\\")
	print "Finish"
		
if __name__ == '__main__':
	t0 = time.time()
	main()
	print time.time() - t0