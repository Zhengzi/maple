import time
import re
from zss import simple_distance, Node
from operator import itemgetter
import os


def go_diff(path1,path2):
	l1 = []
	l2 = []
	total_count = 0
	count = 0
	
	for file in os.listdir(path1):
		if file.endswith(".txt"):
			l1.append(file)
			
	for file in os.listdir(path2):
		if file.endswith(".txt"):
			l2.append(file)
	
	for i in range(len(l1)):
		for j in range(len(l2)):
			if l1[i] == l2[j]:
				f = load(path1 +  l1[i] , path2 + l2[j] , l1[i])	
				total_count += 1
				#print total_count
				if f:
					count += 1
	print total_count
	print count
	
	
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

def print_result(name, result):				
	flag = True
	for item in result:
		if item[2] > 0:
			if flag:
				print name
				flag = False
			print item

def find_score(pair_score_list, item1, item2):	
	for item in pair_score_list:
		if item[0] == item1 and item[1] == item2:
			return item[2]
			
	return -1
				
			

def load(original_path, patched_path, name):
	#read in the function info
	original = open(original_path, 'r')
	patched = open(patched_path, 'r')
	
	#list of bbs
	original_list = []
	patched_list = []
	
	
	#replace jumps and remove "new line char"
	for line in original.readlines():
		line = re.sub('j[a-z]+','j',line)
		line = re.sub('\n','',line)
		original_list.append(line)
		
	for line in patched.readlines():
		line = re.sub('j[a-z]+','j',line)
		line = re.sub('\n','',line)
		patched_list.append(line)
	
	
	pair_score_list = []
	#calculate difference
	for i in range(len(original_list)):
		for j in range(len(patched_list)):
			b1 = original_list[i].split(' ')
			b2 = patched_list[j].split(' ')
			
			#calculate the difference basic on the meno
			d = tree_edit_distance(b1[1],b2[1])
			
			#add the pair similarity score based on the 
			tmp = [b1[0],b2[0],d]
			pair_score_list.append(tmp)
	
	final_score = []
	for i in range(len(original_list)):
		for j in range(len(patched_list)):
			b1 = original_list[i].split(' ')
			b2 = patched_list[j].split(' ')
			
			bp1 = []
			bp2 = []
			
			if len(b1) == 3:
				bp1 = b1[2].rstrip(',').split(',')
				
			if len(b2) == 3:
				bp2 = b2[2].rstrip(',').split(',')
			
			diff_in_num = abs(len(bp1) - len(bp2)) / 10.0
			
			min = 0
			if len(bp1) == 0 and len(bp2) == 0:
				pass
			else: 
				min = 1000
				for item1 in bp1:
					for item2 in bp2:
						score = find_score(pair_score_list, item1, item2)
						if score < min:
							min = score
				#min = min / 10000.0
			
			#print min
			#d = tree_edit_distance(b1[1],b2[1])
			#print d
			d = find_score(pair_score_list, b1[0],b2[0])
			#print d
			s = d + diff_in_num + min
			
			
			tmp = [b1[0],b2[0],s]
			final_score.append(tmp)

	
	final_score = sorted(final_score, key=itemgetter(2))
	#print pair_score_list
	
	
	original_r = {}
	patched_r = {}
	for i in range(len(original_list)):
		original_r[original_list[i].split(' ')[0]] = True
		#print original_list[i].split(' ')[0]
	for j in range(len(patched_list)):
		patched_r[patched_list[j].split(' ')[0]] = True
		#print patched_list[j].split(' ')[0]
		
	#print original
	
	result = []	
	for item in final_score:
		if original_r[item[0]] and patched_r[item[1]]:
			result.append(item)
			original_r[item[0]] = False
			patched_r[item[1]] = False
			
	for k, v in original_r.iteritems():
		if v:
			result.append([k,0,1000])
	for k, v in patched_r.iteritems():
		if v:
			result.append([0,k,1000])
	
	print_result(name, result)
	
	r1 = []
	r2 = []
	for item in result:
		if item[2] > 0:
			if not item[0] == 0:
				r1.append(item[0])
			if not item[1] == 0:
				r2.append(item[1])
	r3 = []
	r3.append(r1)
	r3.append(r2)
	return r3
	#return_result
	
	
def main():
	#original_path = "C:\\Users\\Xu Zhengzi\\Desktop\\opensslg\\dtls1_clear_queues.isra.0.txt"
	#patched_path = "C:\\Users\\Xu Zhengzi\\Desktop\\opensslh\\dtls1_clear_queues.isra.0.txt"
	#load(original_path, patched_path)
	#go_diff("C:\\Users\\Xu Zhengzi\\Desktop\\opensslg\\", "C:\\Users\\Xu Zhengzi\\Desktop\\opensslh\\")
	r = load("C:\\Users\\Xu Zhengzi\\Desktop\\opensslg\\EVP_DecodeUpdate.txt", "C:\\Users\\Xu Zhengzi\\Desktop\\opensslh\\EVP_DecodeUpdate.txt","dtls1_reassemble_fragment.txt")
	print r


if __name__ == '__main__':
	t0 = time.time()
	main()
	print time.time() - t0
	