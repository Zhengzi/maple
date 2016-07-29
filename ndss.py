from idautils import *
from idaapi import *
import networkx as nx
import time
import matplotlib.pyplot as plt

def remove_loop(cfg, address):
	
	nodes = cfg.nodes()
	new_cfg = nx.DiGraph()
	
	
	visited = []
	queue = []
	
	for node in nodes:
		if node.startEA == address:
			new_cfg.add_node(node)
			visited.append(node)
			queue.append(node)
			
			while queue:
				na = queue[0]
				del queue[0]
				ns = cfg.successors(na)
				
				for n in ns:
					if n not in visited:
						visited.append(n)
						queue.append(n)
						new_cfg.add_edge(na, n)
			break
	return new_cfg

def extract_trace(cfg, length):
	nodes = cfg.nodes()
	for node in nodes:
		print "root: "
		print hex(node.startEA)
		print "result: "
		x = extract_trace2(cfg, node, length)
		for items in x:
			print "t:"
			for item in items:
				print hex(item.startEA)
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
		




def extract_intra_function_cfg(length):
	#loop over every segments
	#seg: the starting address for each segments
	for seg in Segments():	
		#we only focus on the basic block in the text section
		#TODO: add support to determine the sections, which contains the useful basic blocks 
		if SegName(seg) == ".text":
			#functions = Functions(seg)		
			#for func_ea in functions:		
			func_ea = here()
			print hex(func_ea)
			
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
				
				cfg.add_node(bb)
				
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
												
						cfg.add_edge(preds_block, bb)
						
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
							
						cfg.add_edge(bb, succs_block)
						
			new_cfg = remove_loop(cfg, func_ea)		
			print new_cfg.number_of_nodes()
			print new_cfg.number_of_edges()
			#extract_trace(new_cfg, length)
			break
	return


def main():
	idaapi.autoWait()
	extract_intra_function_cfg(3)
	print "Finish"
	
	
	
	
if __name__ == '__main__':
	t0 = time.time()
	main()
	print time.time() - t0