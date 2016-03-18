import re
import networkx as nx
from zss import simple_distance, Node
from operator import itemgetter

#from idautils import *
#from idaapi import *

def taint():
	#get_s
	lines = [
	"15 | ------ IMark(0x80495b8, 2, 0) ------",
	"16 | t2 = GET:I8(eax)",
	"17 | t1 = GET:I8(eax)",
	"18 | t0 = And8(t2,t1)",
	"19 | PUT(cc_op) = 0x0000000d",
	"20 | t3 = 8Uto32(t0)",
	"21 | PUT(cc_dep1) = t3",
	"22 | PUT(cc_dep2) = 0x00000000",
	"23 | PUT(cc_ndep) = 0x00000000",
	"24 | PUT(eip) = 0x080495ba",
	"25 | ------ IMark(0x80495ba, 6, 0) ------",
	"26 | t5 = GET:I32(cc_op)",
	"27 | t6 = GET:I32(cc_dep1)",
	"28 | t7 = GET:I32(cc_dep2)",
	"29 | t8 = GET:I32(cc_ndep)",
	"30 | t9 = x86g_calculate_condition(0x00000004,t5,t6,t7,t8):Ity_I32",
	"31 | t4 = 32to1(t9)",
	"32 | if (t4) { PUT(eip) = 0x8049735L; Ijk_Boring }",
	"33 | PUT(eip) = 0x080495c0",
	"34 | t10 = GET:I32(eip)"
	]
	queue = []
	cfg = nx.DiGraph()
	for line in lines:
		
		if "if" in line:
			pass
		elif "=" in line:
			ls = line.split('=',1)		
			rhs = re.findall('t[0-9]+|cc_[a-z]+[0-9]?|eax|ebx|ecx|edx|esi|edi|esp|ebp', ls[0])
			lhs = re.findall('t[0-9]+|cc_[a-z]+[0-9]?|eax|ebx|ecx|edx|esi|edi|esp|ebp', ls[1])
		
			
			if rhs and lhs:
				r = rhs[0]
				#print lhs.captures(1)
				for item in lhs:
					cfg.add_edge(r, item)
				
	lst = list(nx.dfs_postorder_nodes(cfg, "t4"))
	print lst

def extract_intra_function_cfg(name):
	for seg in Segments():	
		if SegName(seg) == ".text":
	
			#functions = Functions(seg)		
			#for func_ea in functions:		
			func_ea = here()
			
			cfg = nx.DiGraph()
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
				
				cfg.add_node(bb.startEA)
				
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
	nx.write_gml(cfg, "C:\\Users\\Xu Zhengzi\\Desktop\\tt\\second.gml")
	return cfg	
	
def load():
	f = open("C:\\Users\\Xu Zhengzi\\Desktop\\tt\\f.txt", 'r')
	s = open("C:\\Users\\Xu Zhengzi\\Desktop\\tt\\s.txt", 'r')
	#cfg1 = nx.read_gml("C:\\Users\\Xu Zhengzi\\Desktop\\tt\\fisrt.gml")
	#cfg2 = nx.read_gml("C:\\Users\\Xu Zhengzi\\Desktop\\tt\\second.gml")
	f_list = []
	s_list = []
	
	for line in f.readlines():
		line = re.sub('j[a-z]+','j',line)
		line = re.sub('\n','',line)
		f_list.append(line)
		
	for line in s.readlines():
		line = re.sub('j[a-z]+','j',line)
		line = re.sub('\n','',line)
		s_list.append(line)
		
	for i in range(len(f_list)):
		for j in range(len(s_list)):
			if f_list[i] == s_list[j]:
				f_list[i] = ""
				s_list[j] = ""

	f_list = filter(None, f_list)
	s_list = filter(None, s_list)
	
	lll = []
	for i in range(len(f_list)):
		for j in range(len(s_list)):
			d = tree_edit_distance(f_list[i],s_list[j])
			l = [i,j,d]
			lll.append(l)
			
	lll = sorted(lll, key=itemgetter(2))
	
	f1 = []
	s1 = []
	for i in range(len(f_list)):
		f1.append(True)
	for j in range(len(s_list)):
		s1.append(True)
		
	result = []	
	for item in lll:
		if f1[int(item[0])] and s1[int(item[1])]:
			result.append(item)
			f1[int(item[0])] = False
			s1[int(item[1])] = False
			
	for i in range(len(f1)):
		if f1[i]:
			result.append([i,-1,-1])
	for j in range(len(s1)):
		if s1[j]:
			result.append([-1,j,-1])
			
	#print result
	aa = []
	ff = []
	ss = []
	for item in result:
		if item[0] == -1:
			#print s_list[int(item[1])]
			ss.append(s_list[int(item[1])])
			continue
		if item[1] == -1:
			#print f_list[int(item[0])]
			ff.append(f_list[int(item[0])])
			continue
		
		p = crazy(f_list[int(item[0])],s_list[int(item[1])])
		aa.append(p)
	
	l11 = []
	l22 = []
	for item in aa:
		if item[0]:
			l11.append(item[0])
		if item[1]:
			l22.append(item[1])
			
	for i in range(len(l11)):
		for j in range(len(l22)):
			if l11[i] == l22[j]:
				l11[i] = ""
				l22[j] = ""

	l11 = filter(None, l11)
	l22 = filter(None, l22)
	
	res_f = []
	res_s = []
	for item in l11:
		tmp = [x for x in item if x != "nop"]
		if tmp:
			res_f.append(','.join(tmp))
		
	for item in l22:
		tmp = [x for x in item if x != "nop"]
		if tmp:
			res_s.append(','.join(tmp))
		#res.append(','.join(tmp))
	
	#l11.extend(l22)
	#l11 = [x for x in l11 if x != "nop"]
	#res = [item for sublist in l11 for item in sublist]
	#res = [x for x in res if x != "nop"]
	print "**********"
	print res_f
	print ff
	print "**********"
	print res_s
	print ss
	print "**********"
	#print l22
		#p = [x for x in p if not x == "nop"]
		#if p:
		#	print p
	#tree_edit_distance(f_list[10],s_list[6])
	#some ridiculous steps, haha
	'''
	print f_list[2]
	print s_list[2]
	print f_list
	print s_list
	'''
	f.close()
	s.close()
	
def crazy(s1,s2):	
	l1 = s1.split(',')
	l2 = s2.split(',')
	#print l1
	#print l2
	for i in range(len(l1)):
		for j in range(len(l2)):
			if l1[i] == l2[j]:
				l1[i] = ""
				l2[j] = ""

	l1 = filter(None, l1)
	l2 = filter(None, l2)
	#print l1
	#print l2
	ll = [l1,l2]
	#print res
	return ll

def tree_edit_distance(s1,s2):	
	l1 = s1.split(',')
	l2 = s2.split(',')	
	n1 = Node("")
	for item in l1:
		#print item
		n1.addkid(Node(item))
		
	n2 = Node("")
	for item in l2:
		#print item
		n2.addkid(Node(item))
	
	return simple_distance(n1, n2)
	
def Ndss_imp():
	func_ea = here()
	f = open("C:\\Users\\Xu Zhengzi\\Desktop\\tt\\x.txt", 'w')
	for bb in FlowChart(get_func(func_ea), flags=FC_PREDS):
		list = []
		for head in Heads(bb.startEA,bb.endEA):
			if isCode(getFlags(head)):
				mnem = GetMnem(head)
				list.append(mnem)
				
		f.write(','.join(list))
		f.write('\n')
	f.close()
			
if __name__ == '__main__':
	#extract_intra_function_cfg("first")
	#extract_intra_function_cfg("second")
	#Ndss_imp()
	load()
	#tree_edit_distance()