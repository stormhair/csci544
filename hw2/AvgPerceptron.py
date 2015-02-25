'''
	Module for Averaged Perceptron
'''

from collections import defaultdict
import random
import Util
import sys

class AvgPerceptron(object):
	train = list()
	dev = list()
	test = list()
	max_iter = 10
	#----------------model parameters----------------
	tags = dict()
	feats = dict()
	param_w = defaultdict(dict)
	#------------------------------------------------

	def __init__(self, m_iter):
		self.max_iter = m_iter
		
	def load_train(self, path, util):
		self.train = util.load_feats(path)
		
	def load_dev(self, path, util):
		self.dev = util.load_feats(path)

	def load_test(self, path, util):
		self.test = util.load_test(path)

	def load_model(self, path, util):
		self.tags, self.feats, self.param_w = util.load_model(path)

	def save_model(self, path, util):
		#------debug-------
		#print(str(self.tags))
		#c = input()
		#------------------
		util.save_model(path,(self.tags, self.feats, self.param_w))

	def vec_dot_prod(self, x, y):
		if len(x) == 0 or len(y) == 0:
			return 0
		score = 0
		if len(x)<len(y):
			for d in x:
				if d in y:
					#------debug-------
					#print(str(x[d]))
					#c = input()
					#------------------
					score+=x[d]*y[d]
		else:
			for d in y:
				if d in x:
					score+=x[d]*y[d]
					#------debug-------
					#print(str(y[d]))
					#c = input()
					#------------------
		#------debug-------
		#print(str(x)+' x '+str(y)+' = '+str(score))
		#c = input()
		#------------------
		return score

	def vec_plus(self, x, y):
		s = dict()
		for d in x:
			s[d] = x[d]
		for d in y:
			if d not in s:
				s[d] = y[d]
			else:
				s[d] += y[d]
		#------debug-------
		#print(str(x)+' + '+str(y)+' = '+str(s))
		#c = input()
		#------------------
		return s

	def vec_minus(self, x, y):
		s = dict()
		for d in y:
			y[d] = -y[d]
		s = self.vec_plus(x, y)
		return s

	def train_with_shuflle(self):
		#initialize tags and feats
		for example in self.train:
			if example[0] not in self.tags:
				self.tags[example[0]] = 1
			for elem in example[1]:
				if elem not in self.feats:
					self.feats[elem] = 1
		
		seq = list()
		for i in range(0, len(self.train)):
			seq.append(i)
		for i in range(0, self.max_iter):
			print('it '+str(i+1)+'...', file = sys.stderr)
			avg_param_w = self.param_w
			random.shuffle(seq)
			for idx in seq:
				c = self.train[idx][0]
				f = self.train[idx][1]
				#generate fx
				fx = dict()
				for w in f:
					if w not in fx:
						fx[w] = 0
					fx[w]+=1
				#argmax
				pred_c = ''
				cur_max_score = float('-inf')
				for cn in self.param_w:
					pred_score = self.vec_dot_prod(fx, self.param_w[cn])
					if pred_score>cur_max_score:
						cur_max_score = pred_score
						pred_c = cn
				#updating
				if pred_c!=c:
					self.param_w[pred_c] = self.vec_minus(self.param_w[pred_c], fx)
					self.param_w[c] = self.vec_plus(self.param_w[c], fx)
				#averaging
				#for cn in avg_param_w:
				#	avg_param_w[cn] = self.vec_plus(avg_param_w[cn], self.param_w[cn])
			#for c in avg_param_w:
			#	for n in avg_param_w[c]:
			#		avg_param_w[c][n]/=len(self.train)
			#self.param_w = avg_param_w
	
	def train_on_file(self, path, util):
		#open file once to get tags, feature names
		n_train = 0
		handler = open(path, errors = 'ignore')
		while True:
			text = handler.readline()
			if not text:
				break
			n_train+=1
			tks = util.tokenize(text)
			tag = tks[0]
			f = tks[1:]
			if tag not in self.tags:
				self.tags[tag] = 1
			if tag not in self.param_w:
				self.param_w[tag] = dict()
			for elem in f:
				if elem not in self.feats:
					self.feats[elem] = 1
		handler.close()
		#read file max_iter times to train the perceptron
		for i in range(0, self.max_iter):
			handler = open(path, errors = 'ignore')
			print('it '+str(i+1)+'...', file = sys.stderr)
			avg_param_w = self.param_w
			while True:
				text = handler.readline()
				if not text:
					break
				tks = util.tokenize(text)
				c = tks[0]
				f = tks[1:]
				#generate fx
				fx = dict()
				for w in f:
					if w not in fx:
						fx[w] = 0
					fx[w]+=1
				#------debug-------
				#print(fx)
				#------------------
				#argmax
				pred_c = ''
				cur_max_score = float('-inf')
				for cn in self.param_w:
					pred_score = self.vec_dot_prod(fx, self.param_w[cn])
					#------debug-------
					#print(str(pred_score))
					#------------------
					if pred_score>cur_max_score:
						cur_max_score = pred_score
						pred_c = cn
				#updating
				if pred_c!=c:
					self.param_w[pred_c] = self.vec_plus(self.param_w[pred_c], fx)
					self.param_w[c] = self.vec_minus(self.param_w[c], fx)
				#averaging
				for cn in avg_param_w:
					avg_param_w[cn] = self.vec_plus(avg_param_w[cn], self.param_w[cn])
			handler.close()
			for c in avg_param_w:
				for n in avg_param_w[c]:
					avg_param_w[c][n]/=n_train
				#------debug-------
				#print(avg_param_w[c])
				#tmp = input()
				#------------------
			self.param_w = avg_param_w
		
	def predict(self, example_tokens):
		#generate fx
		fx = dict()
		for w in example_tokens:
			if w not in fx:
				fx[w] = 0
			fx[w]+=1
		#argmax
		pred_c = ''
		cur_max_score = float('-inf')
		for cn in self.param_w:
			print(self.param_w[cn], file = sys.stderr)
			pred_score = self.vec_dot_prod(fx, self.param_w[cn])
			if pred_score>cur_max_score:
				cur_max_score = pred_score
				pred_c = cn
		return pred_c

	def eval_model(self):
		pass

