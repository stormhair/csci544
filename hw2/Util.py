'''
	Module for Utility
'''
import sys
from collections import defaultdict

class Util(object):
	def tokenize(self, text):
		return text.strip('\n').split(' ')
		
	def load_feats(self, path):
		feats = list()
		handler = open(path, errors = 'ignore')
		while True:
			text = handler.readline()
			if not text:
				break
			f = list()
			tks = self.tokenize(text)
			tag = tks[0]
			for i in range(1, len(tks)):
				f.append(tks[i])
			feats.append((tag, f))			
		handler.close()
		return feats
		
	def load_test(self, path):
		feats = list()
		handler = open(path, errors = 'ignore')
		while True:
			text = handler.readline()
			if not text:
				break
			f = list()
			tks = self.tokenize(text)
			for i in range(1, len(tks)):
				f.append(tks[i])
			feats.append(f)
		handler.close()
		return feats
	
	def load_model(self, path):
		handler = open(path, errors = 'ignore')
		tags = dict()
		feats = dict()
		param_w = defaultdict(dict)
		#load tags
		text = handler.readline() 
		tks = self.tokenize(text)
		for t in tks:
			tags[t] = 1
			param_w[t] = dict()
		#load feature name
		text = handler.readline() 
		tks = self.tokenize(text)
		for t in tks:
			feats[t] = 1
		#load weights
		while True:
			text = handler.readline()
			if not text:
				break
			tks = self.tokenize(text)
			tag = tks[0]
			i = 1
			while i<len(tks)-1:
				param_w[tks[i]] = float(tks[i+1])
				i+=2
		handler.close()
		return tags, feats, param_w
	
	def save_model(self, path, model):
		handler = open(path, 'w')
		tags = model[0]
		feats = model[1]
		param_w = model[2]
		#save tags
		handler.write(' '.join(tags)+'\n')
		#save feature name
		handler.write(' '.join(feats)+'\n')
		#save weights
		for c in param_w:
			handler.write(c)
			for n in param_w[c]:
				handler.write(' '+n+' '+str(param_w[c][n]))
			handler.write('\n')
		handler.close()

