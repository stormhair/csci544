import sys
from collections import defaultdict

class Utility(object):
	def __init__(self, path1, path2, path3):
		self.path1 = path1 #file path for training examples
		self.path2 = path2 #file path for model
		self.path3 = path3 #file path for test set

	def tokenize(self, text):
		tokens = text.strip().split(' ')
		return tokens

	def load_examples(self):
		handle = open(self.path1, errors = 'ignore')
		examples = list()
		dev = list()
		dev_flag = False
		while True:
			strline = handle.readline()
			if not strline:
				break
			tokens = self.tokenize(strline)
			if tokens[0] == 'DEV':
				dev_flag = True
				continue
			if dev_flag:
				dev.append((tokens[0], tokens[1:]))
			else:
				examples.append((tokens[0], tokens[1:]))
		handle.close()
		if dev_flag:
			return examples, dev
		else:
			return examples

	def load_test(self):
		handler = open(self.path3, errors = 'ignore')
		test = list()
		while True:
			strline = handler.readline()
			if not strline:
				break
			tokens = self.tokenize(strline)
			test.append(tokens)
		handler.close()
		return test

	def load_mod(self):
		#data structure for model
		prior = dict();params = defaultdict(dict)
		handler = open(self.path2, errors = 'ignore')
		idx2c = list()
		#load class names
		strline = handler.readline()
		tokens = self.tokenize(strline)
		for t in tokens:
			idx2c.append(t)
		#load priors
		strline = handler.readline()
		tokens = self.tokenize(strline)
		for i in range(0, len(tokens)):
			prior[idx2c[i]] = float(tokens[i])
		#load other parameters
		#n_line = 2
		while True:
			#n_line+=1
			strline = handler.readline()
			if not strline:
				break
			tokens = self.tokenize(strline)
			'''
			#-----------------------DEBUG--------------------------	
			if len(tokens)!=3:
				print('Fatal error at line '+str(n_line)+': '+str(tokens), file = sys.stderr)
			#-----------------------DEBUG--------------------------
			'''
			params[tokens[0]] = dict()
			for i in range(1, len(tokens)):
				params[tokens[0]][idx2c[i-1]] = float(tokens[i])
		handler.close()
		return prior, params

	def save_mod(self, param):
		handler = open(self.path2, 'w')
		prior = param[0]
		p = param[1]
		c2idx = dict()
		idx = 0
		tags = list()
		for c in prior:
			c2idx[c] = idx
			tags.append(c)
			idx+=1
		handler.write(' '.join(tags)+'\n')
		tmp = [0]*idx
		for c in prior:
			tmp[c2idx[c]] = prior[c]
		handler.write(str(tmp[0]))
		for i in range(1, len(tmp)):
			handler.write(' '+str(tmp[i]))
		handler.write('\n')
		for w in p:
			handler.write(w)
			tmp = [0]*idx
			for c in p[w]:
				tmp[c2idx[c]] = p[w][c]
			for i in range(0, len(tmp)):
				handler.write(' '+str(tmp[i]))
			handler.write('\n')
		handler.close()

