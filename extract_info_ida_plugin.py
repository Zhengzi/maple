from idautils import *
from idaapi import *
import networkx as nx

#iteratively loop over every basic block to get info
def extract_intra_function_cfg():

	#wait until IDA finishing loading the project
	idaapi.autoWait()
	
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
					
				#TODO use own basicblock class to wrap the ida pro basic block class
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
						
			#testing
			print cfg.number_of_nodes()
			print cfg.number_of_edges()
			nodes = cfg.nodes()
			for node in nodes:
				print node.startEA			
			#endtest
			
	return
	
def extract_inter_function_cfg():
	return
	
def main():
	extract_intra_function_cfg()
	extract_inter_function_cfg()
	print "Finish"
		
if __name__ == '__main__':
    main()