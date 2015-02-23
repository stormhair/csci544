'''
	preprocessing datasets
	python3 preproc.py [OPTION] [INPUTPATH] [OUTPUTPATH] -m (optional) [map file]
	OPTION LIST
		1 : provide directory containing TRAINING examples (or dev) for spam detection, the program will generate a single file containing all the valid training examples(or dev), one example per line
		2 : provide directory containing TRAINING examples (or dev) for sentiment analysis, the program will generate a single file containing all the valid training examples(or dev), one example per line
		3 : provide file containing training examples (or dev) for spam detection in the format of SVMLight, the program will generate a single file containing all the valid training examples(or dev), one example per line.
		4 : provide file containing training examples (or dev) for sentiment analysis in the format of SVMLight, the program will generate a single file containing all the valid training examples(or dev), one example per line
		5 : provide directory containing TEST examples for spam detection, the program will generate a single file conatining all the valid test examples, one example per line
		6 : provide directory containing TEST examples for sentiment analysis, the program will generate a single file conatining all the valid test examples, one example per line
		7 : split the given dataset into training set and development set (10% as dev set)
		8 : given a single feature file, the program will generate a sample. the fraction is 10%
		9 : provide the path of TEST examples for spam detection or sentiment analysis, the program will generate a single file conatining all the valid test examples, one example per line, in svmlight format. -m is required
'''

import os
import sys
import string
import re
import random

#data structures
stop_words = {'the':1, 'of':1, 'and':1, 'to':1, 'a':1, 'an':1, 'for':1, 'is':1, 'on':1, 'be':1, 'are':1, 'will':1, 'that':1, 'it':1, 'with':1, 'or':1, 'as':1, 'by':1, 'at':1, 'in':1, 'which':1, 'any':1, 'also':1}
nonsense_words = {'Subject:':1, 'subject:':1}
del_char = ''
del_map = dict()

#functions
def tokenize_spam(text):
	tokens = text.strip().split(' ')
	i = len(tokens)-1
	while i>=0:
		tokens[i] = tokens[i].lower()
		if tokens[i] in string.punctuation:
			del tokens[i]
		elif tokens[i] in stop_words:
			del tokens[i]
		elif tokens[i] in nonsense_words:
			del tokens[i]
		elif tokens[i].isdigit():
			y = int(tokens[i])
			if y<=2100 and y>=1000:
				tokens[i] = '/year'
			else:
				tokens[i] = '/digit'
		i-=1
	return tokens

def tokenize_sent(text):
	global del_map
	tokens = text.strip().split(' ')
	i = len(tokens)-1
	trans = str.maketrans(del_map)
	while i>=0:
		tokens[i] = tokens[i].translate(trans)
		if len(tokens[i]) == 0 or tokens[i] == ' ':
			del tokens[i]
			i-=1
			continue
		tokens[i] = tokens[i].lower()
		if tokens[i] in stop_words:
			del tokens[i]
		elif tokens[i].isdigit():
			y = int(tokens[i])
			if y<=2100 and y>=1000:
				tokens[i] = '/year'
			else:
				tokens[i] = '/digit'
		i-=1
	return tokens

def toss(f):
	if random.random() < f:
		return True
	else:
		return False

def main():
	if len(sys.argv)<4:
		print('python3 '+sys.argv[0]+' [OPTION] [INPUTPATH] [OUTPUTPATH] -m (optional) [map file]', file = sys.stderr)
		return
	opt = int(sys.argv[1])
		
	file_dir = sys.argv[2]
	output_path = sys.argv[3]
	n_item = 0
	
	#initialize del_map
	global del_char
	global del_map
	del_char = string.punctuation+' '+'\t'
	for i in range(0, len(del_char)):
		del_map[del_char[i]] = None
	
	#fracation of development set for sentiment data set
	f_sample = 0.1

	#
	word_table = dict()
	n_word = dict()
	feats = list()
	class_name = list()
	word_flag = False
	word_file = ''
	if len(sys.argv) == 6:
		if sys.argv[4] == '-m':
			word_flag = True
			word_file = sys.argv[5]
			f = open(word_file, errors = 'ignore')
			while True:
				strline = f.readline()
				if not strline:
					break
				tokens = strline.rstrip('\n').split()
				if len(tokens)!=2:
					continue
				word_table[tokens[0]] = int(tokens[1])
			f.close()

	map_table = dict()
	if opt == 3:
		map_table = {'SPAM':'1', 'HAM':'-1'}
	if opt == 4:
		map_table = {'POS':'1', 'NEG':'-1'}
	
	if opt == 3 or opt == 4:
		idx = 1
		input_path = file_dir
		inhandler = open(input_path, errors = 'ignore')
		while True:
			wc = dict()
			strline = inhandler.readline()
			if not strline:
				break
			tokens = strline.strip().split(' ')
			class_name.append(map_table[tokens[0]])
			for i in range(1, len(tokens)):
				if word_flag == False:
					if tokens[i] not in word_table:
						word_table[tokens[i]] = idx
						idx+=1
				if tokens[i] not in word_table:
					continue
				if tokens[i] not in n_word:
					n_word[tokens[i]] = 0
				if tokens[i] not in wc:
					wc[tokens[i]] = 0
				n_word[tokens[i]]+=1
				wc[tokens[i]]+=1
			feats.append(wc)
		inhandler.close()

		#save word table
		if word_flag == False:
			word_path = ''
			if opt == 3:
				word_path = 'spam.word'
			elif opt == 4:
				word_path = 'sentiment.word'
			outhandler = open(word_path, 'w')
			for w in word_table:
				outhandler.write(w+' '+str(word_table[w])+'\n')
			outhandler.close()
		
		#save features
		outhandler = open(output_path, 'w')
		for i in range(0, len(feats)):
			sl = list()
			for w in feats[i]:
				feats[i][w] = feats[i][w]/n_word[w] #update: normalization
				sl.append((word_table[w], w))
			sl = sorted(sl, key = lambda x:x[0])
			outhandler.write(class_name[i])
			for elem in sl:
				outhandler.write(' '+str(elem[0])+':'+str(feats[i][elem[1]]))
			outhandler.write('\n')
		outhandler.close()
		return

	if opt == 7:
		n_train = 0;n_dev = 0
		handler = open(sys.argv[2], errors = 'ignore')
		train = open(sys.argv[3]+'/sentiment.train', 'w')
		dev = open(sys.argv[3]+'/sentiment.dev', 'w')
		while True:
			strline = handler.readline()
			if not strline:
				break			
			if toss(f_sample):
				dev.write(strline)
				n_dev+=1
			else:
				train.write(strline)
				n_train+=1
		handler.close()
		train.close()
		dev.close()
		print('#Train: '+str(n_train)+' #Dev: '+str(n_dev))
		return

	if opt == 8:
		n_sample = 0
		inhandler = open(sys.argv[2], errors = 'ignore')
		outhandler = open(sys.argv[3], 'w')
		while True:
			strline = inhandler.readline()
			if not strline:
				break			
			if toss(f_sample):
				outhandler.write(strline)
				n_sample+=1
		inhandler.close()
		outhandler.close()
		return

	if opt == 9:
		if len(sys.argv)!=6:
			print('python3 '+sys.argv[0]+' [OPTION] [INPUTPATH] [OUTPUTPATH] -m (optional) [map file]', file = sys.stderr)
			return
		inpath = sys.argv[2]
		outpath = sys.argv[3]
		wordpath = sys.argv[5]
		#load word table
		inhandler = open(wordpath, errors = 'ignore')
		while True:
			strline = inhandler.readline()
			if not strline:
				break
			tokens = strline.rstrip('\n').split(' ')
			if len(tokens)!=2:
				continue
			word_table[tokens[0]] = int(tokens[1])
		inhandler.close()
		#generate features
		inhandler = open(inpath, errors = 'ignore')
		while True:
			wc = dict()
			strline = inhandler.readline()
			if not strline:
				break
			tokens = strline.strip().split(' ')
			for i in range(1, len(tokens)):
				if tokens[i] not in word_table:
					continue
				if tokens[i] not in n_word:
					n_word[tokens[i]] = 0
				if tokens[i] not in wc:
					wc[tokens[i]] = 0
				n_word[tokens[i]]+=1
				wc[tokens[i]]+=1
			feats.append(wc)
		inhandler.close()
		#save features
		outhandler = open(outpath, 'w')
		for i in range(0, len(feats)):
			sl = list()
			for w in feats[i]:
				feats[i][w] = feats[i][w]/n_word[w] #update: normalization
				sl.append((word_table[w], w))
			sl = sorted(sl, key = lambda x:x[0])
			outhandler.write('1')
			for elem in sl:
				outhandler.write(' '+str(elem[0])+':'+str(feats[i][elem[1]]))
			outhandler.write('\n')
		outhandler.close()		
		return

	files = os.listdir(file_dir)
	output_handle = open(output_path, 'w')
	for f in files:
		tag = ''
		tokens = []
		if opt == 1:
			if f.find("HAM"):
				tag = 'HAM'
			else:
				tag = 'SPAM'
		elif opt == 2:
			if f.find("POS"):
				tag = 'POS'
			else:
				tag = 'NEG'
		#read the file
		path = file_dir+"/"+f
		input_file = open(path, errors = 'ignore');
		while True:
			strline = input_file.readline()
			if not strline:
				break
			if opt == 1 or opt == 5:
				tokens = tokens + tokenize_spam(strline)
			elif opt == 2 or opt == 6:
				tokens = tokens + tokenize_sent(strline)
		input_file.close()
		if len(tokens)>0:
			if opt == 1 or opt == 2:
				output_handle.write(tag+' '+' '.join(tokens)+'\n')
			elif opt == 5 or opt == 6:
				output_handle.write(' '.join(tokens)+'\n')
			n_item+=1
	output_handle.close()
	print('# of valid examples: '+str(n_item), file = sys.stderr)
	
if __name__ == '__main__':
	main()

