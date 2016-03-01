from idautils import *
from idaapi import *
import networkx as nx

#iteratively loop over every basic block to get cfg within one function, one basic block will be a node in the graph
def extract_intra_function_cfg():
	
	#loop over every segments
	#seg: the starting address for each segments
	for seg in Segments():	

		#we only focus on the basic block in the text section
		#TODO: add support to determine the sections, which contains the useful basic blocks 
		if SegName(seg) == ".text":
	
			#functions = Functions(seg)		
			#for func_ea in functions:		
			func_ea = here()
			
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
			'''			
			#testing
			print cfg.number_of_nodes()
			print cfg.number_of_edges()
			nodes = cfg.nodes()
			for node in nodes:
				print node.startEA			
			#endtest
			'''
	return

#get the function call cfg, in which a function starting address is a cfg node	
def extract_inter_function_cfg():
	
	#loop over every segments
	#seg: the starting address for each segments
	
	#initialized a directed graph to store cfg
	cfg = nx.DiGraph()
	
	for seg in Segments():	
	
		if SegName(seg) == ".text" or SegName(seg) == ".plt":
			
			functions = Functions(seg)		
			for func_ea in functions:	
				
				#It will add some isolated node into the graph
				cfg.add_node(func_ea)
				
				for ref in CodeRefsTo(func_ea, 1):				
					calling_func = get_func(ref)
					if not calling_func:
						continue
					calling_func_startEA = calling_func.startEA
					cfg.add_edge(calling_func_startEA, func_ea)
			
			#for ref in CodeRefsFrom(func_ea, 1):
			#	print "  calling %s(0x%x)" % (GetFunctionName(ref), ref)
			
	#testing
	#print cfg.number_of_nodes()
	#print cfg.number_of_edges()
	#nodes = cfg.nodes()
	#for node in nodes:
	#	print node
	#endtesting
	
	return cfg

def count_in_out_edge(cfg):	
	print "number of functions: " + str(cfg.number_of_nodes())
	print "number of total call edges: " + str(cfg.number_of_edges())
	for node in cfg.nodes():
		func_name = GetFunctionName(node)
		#print "function: " + func_name + " out_degree: " + str(cfg.out_degree(node)) + " in_degree: " + str(cfg.in_degree(node))
		out_degree = cfg.out_degree(node)
		in_degree  = cfg.in_degree(node)
		ratio = -1
		if in_degree + out_degree > 0:
			ratio = (float)(out_degree)/(float)(in_degree + out_degree)
		#manaully set the longest function name to 50 char, largest number of func call to 9999
		print 'function: {0:50} out_degree: {1:4d} in_degree: {2:4d} ratio: {3:6f}'.format(func_name, out_degree, in_degree, ratio)
	return
	
def main():
	
	#wait until IDA finishing loading the project
	idaapi.autoWait()
	
	extract_intra_function_cfg()
	func_cfg = extract_inter_function_cfg()
	count_in_out_edge(func_cfg)
	print "Finish"
		
if __name__ == '__main__':
    main()