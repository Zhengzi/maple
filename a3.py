import networkx as nx
import time
import matplotlib.pyplot as plt

def extract_trace(cfg, length, nodes):
	#nodes = cfg.nodes()
	#nodes_all = cfg.nodes()
	#print nodes_all
	for node in nodes:
		print "root: "
		#print type(node)
		node = int(node, 16)
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
		
def main():
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