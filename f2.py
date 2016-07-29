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
	l1 = []
	l2 = []
	total_count = 0
	count = 0
	
	for file in os.listdir(path1):
		if file.endswith(".gml"):
			l1.append(file)
			
	for file in os.listdir(path2):
		if file.endswith(".gml"):
			l2.append(file)
	
	for i in range(len(l1)):
		for j in range(len(l2)):
			if l1[i] == l2[j]:
				x = load_3(path1 +  l1[i] , path2 + l2[j] , l1[i])	
				count += x
				total_count += 1
				print '{}/{}'.format(count, total_count)
				#print count
				#print total_count
				#if f:
				#	count += 1
	#print total_count
	#print count


def find_root(nodes,g):
	l = 0
	r = None
	for item in nodes:
		text = g.node[item]["text"]
		length = len(text.split(','))
		if length > l:
			l = length
			r = item
			
	return r
	

def t(g):
	roots = [n for n,d in g.in_degree().items() if d==0]
	root = find_root(roots,g)
	
	result = []
	
	tmp = []
	tmp.append(root)
	tmp.append(g.node[root]["text"])
	
	result.append(tmp)
	
	visited = []
	visited.append(root)
	
	current = []
	current.extend(g.successors(root))
	
	while current:
		new = []
		for item in current:
			if item not in visited:
				tmp = []
				tmp.append(item)
				tmp.append(g.node[item]["text"])
				result.append(tmp)
				visited.append(item)
				new.extend(g.successors(item))
				
		current = new
	return result
	
	
def tree_edit_distance_wrapper(s1,s2):	
	score = tree_edit_distance(s1,s2)
	#print s1,s2
	#print score * 2 / float(len(s1.split(',')) +len(s2.split(',')))
	#if score * 2 / float(len(s1.split(',')) +len(s2.split(','))) > 0.2:
	

	if score > 0:
	#if score > 2:
		return 1
	return 0

def tree_edit_distance(s1,s2):	
	l1 = s1.split(',')
	l2 = s2.split(',')	
	
	#ave_len = (len(l1) + len(l2)) / 2
	
	n1 = Node("")
	for item in l1:
		#print item
		n1.addkid(Node(item))
		
	n2 = Node("")
	for item in l2:
		#print item
		n2.addkid(Node(item))
	
	return simple_distance(n1, n2)


def process_successor(succs, g):
	if not succs:
		return succs
		
	if len(succs) == 1:
		return succs
	
	if len(succs) == 2:	
		result = []
		l1 = g.node[succs[0]]["text"]
		l2 = g.node[succs[1]]["text"]
		if l1.count(',') > l2.count(','):
			result.append(succs[1])
			result.append(succs[0])
			return result
		elif l1.count(',') < l2.count(','):
			return succs
		else:
			if l1 > l2:
				result.append(succs[1])
				result.append(succs[0])
				return result
			return succs			
	else:
		return succs
	
def qucik_hash(g):
	roots = [n for n,d in g.in_degree().items() if d==0]
	if not roots:
		return 0
	
	root = find_root(roots,g)
	

	#root = root[0]
	result = []
	
	hash_value = 0
	
	tmp = []
	tmp.append(root)
	tmp.append(g.node[root]["text"])
	
	result.append(tmp)
	hash_object = hashlib.md5(g.node[root]["text"])
	hash_value += int(hash_object.hexdigest(),base=16)
	
	visited = []
	visited.append(root)
	
	current = []
	tt = process_successor(g.successors(root),g)
	current.extend(tt)
	
	while current:
		new = []
		for item in current:
			if item not in visited:
				tmp = []
				tmp.append(item)
				tmp.append(g.node[item]["text"])
				result.append(tmp)
				hash_object = hashlib.md5(g.node[item]["text"])
				hash_value += int(hash_object.hexdigest(),base=16)
				visited.append(item)
				tt = process_successor(g.successors(item),g)
				new.extend(tt)
				
		current = new
	return [result, hash_value]
	
def load_3(gml1,gml2,name):
	g1 = nx.read_gml(gml1)			
	g2 = nx.read_gml(gml2)
	
	q1 = qucik_hash(g1)
	q2 = qucik_hash(g2)
	
	if not q1:
		return 0
		
	if not q2:
		return 0
	
	v1 = q1[1]
	v2 = q2[1]
	s1 = q1[0]
	s2 = q2[0]
	
	if v1 == v2:
		#print "skip"
		return 0
	#print s1	
	#print s2
	
	to_write = []

	to_write.append(name)
	
	with open("result_openssl.txt", "a") as myfile:
		for item in to_write:
			myfile.write(item)
			myfile.write("\n")
	return 1
	
def load_2(gml1,gml2,name):
	g1 = nx.read_gml(gml1)			
	g2 = nx.read_gml(gml2)
	
	q1 = qucik_hash(g1)
	q2 = qucik_hash(g2)
	
	v1 = q1[1]
	v2 = q2[1]
	s1 = q1[0]
	s2 = q2[0]
	
	if v1 == v2:
		print "skip"
		return 0
	print s1	
	print s2
	
	to_write = []

	to_write.append(name)
	
	m = lcs(s1,s2)
	
	index = find_index(m)
	
	
	match1 = []
	match2 = []
	
	for item in index:
		to_write.append(hex(s1[item[0]][0]) + " " + hex(s2[item[1]][0]))
	
		#print hex(s1[item[0]][0]) + " " + hex(s2[item[1]][0])
		match1.append(s1[item[0]][0])
		match2.append(s2[item[1]][0])
		
	flag = False	
	to_write.append("o")	
	for item in s1:
		if item[0] not in match1:
			#print hex(item[0])
			flag = True
			to_write.append(hex(item[0]))

			
	to_write.append("p")
	
	for item in s2:
		if item[0] not in match2:
			#print hex(item[0])
			flag = True
			to_write.append(hex(item[0]))
			
	#if flag:
		#with open("result_2.txt", "a") as myfile:
	with open("result_3.txt", "a") as myfile:
		for item in to_write:
			myfile.write(item)
			myfile.write("\n")
	return 1
	#return 0	
	
def load(gml1,gml2,name):
	g1 = nx.read_gml(gml1)			
	g2 = nx.read_gml(gml2)	
	s1 = t(g1)
	s2 = t(g2)
	#print s1	
	#print s2
	
	with open("result.txt", "a") as myfile:
		myfile.write(name)
		myfile.write("\n") 
		
		m = lcs(s1,s2)
		
		index = find_index(m)
		
		
		match1 = []
		match2 = []
		
		for item in index:
		
			myfile.write(hex(s1[item[0]][0]) + " " + hex(s2[item[1]][0]))
			myfile.write("\n") 
		
			#print hex(s1[item[0]][0]) + " " + hex(s2[item[1]][0])
			match1.append(s1[item[0]][0])
			match2.append(s2[item[1]][0])
			
		myfile.write("o")
		myfile.write("\n") 	
		
		for item in s1:
			if item[0] not in match1:
				#print hex(item[0])
				myfile.write(hex(item[0]))
				myfile.write("\n") 
				
		myfile.write("p")
		myfile.write("\n") 
		
		for item in s2:
			if item[0] not in match2:
				#print hex(item[0])
				myfile.write(hex(item[0]))
				myfile.write("\n") 
				
		#print 	
	return 0
	
	
def find_index(m):
	s = m.shape
	r = s[0] - 1
	c = s[1] - 1
	v = m[r][c]
	
	index = []
	while r > 0 and c > 0:
		if m[r-1][c] == v:
			r = r-1
		elif m[r][c-1] == v:
			c = c-1
		else:
			index.append([r,c])
			r = r-1
			c = c-1
			v = v-1

	if v > 0:
		index.append([r,c])
	return index
	
def lcs(s1,s2):
	if not s1:
		return 0
	if not s2:
		return 0
		
	matrix = numpy.zeros((len(s1),len(s2)))
	matrix_r = numpy.zeros((len(s1),len(s2)))
	
	flag = False
	for i in range(len(s1)):
		if flag:
			matrix[i][0] = 1 
		if tree_edit_distance_wrapper(s1[i][1], s2[0][1]) == 0:
			matrix[i][0] = 1 
			matrix_r[i][0] = 1 
			flag = True
			
	flag = False
	for i in range(len(s2)):
		if flag:
			matrix[0][i] = 1 
		if tree_edit_distance_wrapper(s1[0][1], s2[i][1]) == 0:
			matrix[0][i] = 1 
			matrix_r[0][i] = 1 
			flag = True

	for i in range(1,len( s1)):
		for j in range(1,len(s2)):
			a = matrix[i-1][j]
			b = matrix[i][j-1]
			c = matrix[i-1][j-1]
			if tree_edit_distance_wrapper(s1[i][1], s2[j][1]) == 0:
				c = c + 1	
				
			'''
				if i == 3 and j ==4:
					print s1[i][1], s2[j][1], 'equals'
					raw_input()
			
			else:
				if i == 3 and j ==4:
					print s1[i][1], s2[j][1], 'inequals'
					raw_input()
			''' 
				
				
			if c > a and c > b:
				matrix_r[i][j] = 1
				
			matrix[i][j] = max(a,b,c)
			
	#print matrix	
	#print matrix_r	
	return matrix


def test():
	a = [1,2,3]
	print a[-1]
	
def main():
	#load_2("C:\Users\Xu Zhengzi\Desktop\og\ssl3_do_change_cipher_spec.gml","C:\Users\Xu Zhengzi\Desktop\oh\ssl3_do_change_cipher_spec.gml","")
	#print tree_edit_distance('mov,mov,mov,mov,mov,call,test,jnz','mov,mov,mov,mov,mov,call,add,xor,pop,pop,retn')
	#print tree_edit_distance_wrapper('mov,mov,mov,mov,mov,call,test,jnz','mov,mov,mov,mov,mov,call,add,xor,pop,pop,retn')
	#test()
	#go_diff("C:\\Users\\Xu Zhengzi\\Desktop\\linux316\\" , "C:\\Users\\Xu Zhengzi\\Desktop\\linux317\\")
	#go_diff("C:\\Users\\Xu Zhengzi\\Desktop\\glc2\\" , "C:\\Users\\Xu Zhengzi\\Desktop\\glc3\\")
	#go_diff("C:\\Users\\Xu Zhengzi\\Desktop\\l3162\\" , "C:\\Users\\Xu Zhengzi\\Desktop\\l3163\\")
	#load_2("C:\Users\Xu Zhengzi\Desktop\linux316\\acpi_device_hotplug.gml","C:\Users\Xu Zhengzi\Desktop\linux317\\acpi_device_hotplug.gml","acpi_device_hotplug")
	#load_2("C:\Users\Xu Zhengzi\Desktop\l3162\\aac_init_adapter.gml","C:\Users\Xu Zhengzi\Desktop\l3163\\aac_init_adapter.gml","aac_init_adapter")
	#load_2("C:\Users\Xu Zhengzi\Desktop\\aac_init_adapter.gml","C:\Users\Xu Zhengzi\Desktop\l3162\\aac_init_adapter.gml","aac_init_adapter")
	#go_diff("C:\\Users\\Xu Zhengzi\\Desktop\\l3162_new\\" , "C:\\Users\\Xu Zhengzi\\Desktop\\l3163_new\\")
	#load_2("C:\Users\Xu Zhengzi\Desktop\l3162\\rfcomm_process_rx.gml","C:\Users\Xu Zhengzi\Desktop\l3163\\rfcomm_process_rx.gml","rfcomm_process_rx")
	go_diff("C:\\Users\\Xu Zhengzi\\Desktop\\og\\" , "C:\\Users\\Xu Zhengzi\\Desktop\\oh\\")
	print "Finish"
		
if __name__ == '__main__':
	t0 = time.time()
	main()
	print time.time() - t0