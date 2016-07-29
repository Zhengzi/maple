from idautils import *
from idaapi import *
import networkx as nx
import time
import matplotlib.pyplot as plt


def extract_trace(cfg, length, nodes):
	#nodes = cfg.nodes()
	for node in nodes:
		print "root: "
		print hex(node)
		print "result: "
		x = extract_trace2(cfg, node, length)
		for items in x:
			print "t:"
			for item in items:
				print hex(item)
			print
		#break

def extract_trace2(cfg, node, length):
	if length == 1:
		return [[node]]
	else:
		ns = cfg.predecessors(node)
		tmp = []
		for n in ns:
			
			rs = extract_trace2(cfg, n, length-1)
			for r in rs:
				tmp2 = []
				tmp2.extend(r)
				tmp2.append(node)
				tmp.append(tmp2)
				
				
		return tmp


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
					
					cfg.add_node(hex(bb.startEA))
					
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
													
							cfg.add_edge(hex(preds_block.startEA), hex(bb.startEA))
							
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
								
							cfg.add_edge(hex(bb.startEA), hex(succs_block.startEA))
				'''			
				#testing
				print cfg.number_of_nodes()
				print cfg.number_of_edges()
				nodes = cfg.nodes()
				for node in nodes:
					print node.startEA			
				#endtest
				'''
				path_new = path + GetFunctionName(func_ea) + ".gml"
				nx.write_gml(cfg, path_new)
				
	return
	
def main():	
	#wait until IDA finishing loading the project
	idaapi.autoWait()
	#extract_intra_function_cfg("C:\\Users\\Xu Zhengzi\\Desktop\\oh\\")
	cfg1 = nx.read_gml("C:\\Users\\Xu Zhengzi\\Desktop\\og\\dtls1_reassemble_fragment.gml")
	cfg2 = nx.read_gml("C:\\Users\\Xu Zhengzi\\Desktop\\oh\\dtls1_reassemble_fragment.gml")
	nodes1 = ['0x80c0b14', '0x80c0b9a', '0x80c0c3c', '0x80c0c57', '0x80c0c5d', '0x80c0c8c', '0x80c0ccc', '0x80c0d0a', '0x80c0d2c', '0x80c0e83', '0x80c0fb4', '0x80c0eb6', '0x80c0f53', '0x80c0b97', '0x80c0d88', '0x80c0de1', '0x80c0db5', '0x80c0fac', '0x80c0f73', '0x80c0dd9']
	extract_trace(cfg1, 3, nodes1)

	print "Finish"
		
if __name__ == '__main__':
	t0 = time.time()
	main()
	print time.time() - t0