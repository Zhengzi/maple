import networkx as nx
import time
import matplotlib.pyplot as plt
import pickle
from zss import simple_distance, Node
import numpy
import re
from operator import itemgetter
import os
import hashlib

def go_diff(path1,path2):
	count = 0
	
	for file in os.listdir(path1):
		if file.endswith(".gml"):
			number = merge_node(path1+file, path2+file)
			count += number
			#print count
			
	print count

def remove_last_jump(text):
	new_text = text.split(',')
	if not new_text:
		return text
	if "j" in new_text[-1]:
		new_text = new_text[:-1]
	return ",".join(new_text)
	
def merge_node(path,new_path):
	g = nx.read_gml(path)
	nodes = [n for n,d in g.out_degree().items() if d==1]
	for node in nodes:
		if not node in g.nodes():
			continue
			
		if g.in_degree(node) != 1:
			continue	
		p = g.successors(node)
		#print p
		#dict = g.in_degree(p)
		#print dict[p]
		#print g.in_degree(p)[p[0]]
		if g.in_degree(p)[p[0]] == 1:
			text1 = g.node[node]["text"]
			text1 = remove_last_jump(text1)
			text2 = g.node[p[0]]["text"]
			
			#print text1
			#print text2
			
			new_text = text1 + ',' + text2
			#print new_text
			
			nns = g.successors(p[0])
			g.node[node]["text"] = new_text
			
			for n in nns:
				g.add_edge(node, n)
			g.remove_node(p[0])
	nx.write_gml(g, new_path)
	return nx.number_of_nodes(g)
	
go_diff("C:\\Users\\Xu Zhengzi\\Desktop\\l3162\\", "C:\\Users\\Xu Zhengzi\\Desktop\\l3162_new\\")
go_diff("C:\\Users\\Xu Zhengzi\\Desktop\\l3163\\", "C:\\Users\\Xu Zhengzi\\Desktop\\l3163_new\\")
#g1 = nx.read_gml("C:\Users\Xu Zhengzi\Desktop\l3163\\aac_init_adapter.gml")
#merge_node(g1)

#print remove_last_jump("a,a,a,a,a,a,jmp")