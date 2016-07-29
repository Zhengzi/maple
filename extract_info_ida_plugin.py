from idautils import *
from idaapi import *
import networkx as nx
import time
import matplotlib.pyplot as plt
import pickle


#iteratively loop over every basic block to get cfg within one function, one basic block will be a node in the graph
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
						for succs_block in succs:
						
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
				path_new = path + GetFunctionName(func_ea) + ".gml"
				nx.write_gml(cfg, path_new)
				
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
	nodes = cfg.nodes()
	for node in nodes:
		ns = cfg.successors(node)
		if not ns:
			print hex(node)
	
	#print nx.connected_components(cfg)
	#nx.draw(cfg)
	#plt.show()
	#plt.savefig("graph.png", dpi=1000)
	'''	
	#testing
	print cfg.number_of_nodes()
	print cfg.number_of_edges()
	#print cfg.node()
	nodes = cfg.nodes()
	print
	for node in nodes:
		print "parent: "
		print hex(node)
		print "child: "
		ns = cfg.successors(node)
		for n in ns:
			print hex(n)
	#endtesting
	'''
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
		#print 'function: {0:50} out_degree: {1:4d} in_degree: {2:4d} ratio: {3:6f}'.format(func_name, out_degree, in_degree, ratio)
	return
	
#this func aims to find the number of indirect calls in the function, as well as find any particular calls in the function.
#it returns the count of the calls 	
def find_the_number_of_indirect_call():
	count = 0
	count_memcpy = 0
	
	for seg in Segments():	
		
		if SegName(seg) == ".text":
	
			functions = Functions(seg)		
			for func_ea in functions:	
				info = "" + GetFunctionName(func_ea) + "\n"
				#print GetFunctionName(func_ea)
				flag1 = False
				flag2 = False
				indiret_count = 0
				total_count = 0
				for bb in FlowChart(get_func(func_ea)):
					for head in Heads(bb.startEA,bb.endEA):
						if isCode(getFlags(head)):
							mnem = GetMnem(head)
							if mnem == "call":
								op = GetOpnd(head, 0)
								total_count = total_count + 1
								#if "[" in op:
								if "eax" in op or "ebx" in op or "ecx" in op or "edx" in op or "esi" in op or "edi" in op or "ebp" in op or "esp" in op:
								#if op == "eax" or op == "ebx" or op == "ecx" or op ==  "edx" or op == "esi" or op == "edi" or op == "esp" or op == "ebp":
									indiret_count = indiret_count + 1
									count += 1
									print GetFunctionName(func_ea)
								if "memcpy" in op:
									flag1 = True
								if "malloc" in op:								
									flag2 = True
				ratio = 0 if total_count==0 else (float)(indiret_count)/(float)(total_count)
				info += "indrect call: " + str(indiret_count) + " indrect call ration: " + str(ratio)
				#print info	
				if flag1 and flag2:
					count_memcpy += 1
					flag1 = False
					flag2 = False

	print count
	return
	
def count_in_out_edge_without_api(cfg, api_list):	
	#print "number of functions: " + str(cfg.number_of_nodes())
	#print "number of total call edges: " + str(cfg.number_of_edges())
	for node in cfg.nodes():
		func_name = GetFunctionName(node)

		out_degree = 0
		succs = cfg.successors(node)
		for item in succs:
			f_name = GetFunctionName(item)
			if f_name in api_list:
				continue
			out_degree += 1
		
		in_degree = 0
		preds  = cfg.predecessors(node)
		for item in preds:
			f_name = GetFunctionName(item)
			if f_name in api_list:
				continue
			in_degree += 1
					
		ratio = -1
		if in_degree + out_degree > 0:
			ratio = (float)(out_degree)/(float)(in_degree + out_degree)
		#manaully set the longest function name to 50 char, largest number of func call to 9999
		#print 'function: {0:50} out_degree: {1:4d} in_degree: {2:4d} ratio: {3:6f}'.format(func_name, out_degree, in_degree, ratio)
	return

#generate the function list from the given binary and store it in to a files
def _get_function_list():
	func_list = []
	for seg in Segments():	
		if SegName(seg) == ".text":
			functions = Functions(seg)		
			for func_ea in functions:	
				
				func_name = GetFunctionName(func_ea)
				func_list.append(func_name)		
	f = open('C:\\Users\\Xu Zhengzi\\Desktop\\func_list.txt','a')
	for item in func_list:
		f.write(item)
		f.write("\n")
	f.close
	return func_list

#load the fucntion list from the hhd, I have not uploaded the function list yet.	
def load_func_list():
	func_list = []
	f = open('C:\\Users\\Xu Zhengzi\\Desktop\\func_list.txt','r')
	lines = f.readlines()
	for item in lines:
		function_name = item[:-1]
		func_list.append(function_name)
	f.close
	
	#process the list item
	#hack replace the func name with .func name
	#it may not be corret all the time
	func_list_dot = []
	for item in func_list:
		func_dot_name = "." + item[1:]
		func_list_dot.append(item)
		func_list_dot.append(func_dot_name)
	return func_list_dot
	
def main():
	
	#wait until IDA finishing loading the project
	idaapi.autoWait()
	#extract_inter_function_cfg("C:\\Users\\Xu Zhengzi\\Desktop\\opensslh\\")
	extract_intra_function_cfg("C:\\Users\\Xu Zhengzi\\Desktop\\og\\")
	#func_cfg = extract_inter_function_cfg()
	#count_in_out_edge(func_cfg)
	#_get_function_list()
	#func_list = load_func_list()
	#t0 = time.time()
	#count_in_out_edge_without_api(func_cfg, func_list)
	#print time.time() - t0
	#find_the_number_of_indirect_call()
	print "Finish"
		
if __name__ == '__main__':
	t0 = time.time()
	main()
	print time.time() - t0