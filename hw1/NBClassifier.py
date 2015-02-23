import sys
import math
from Utility import Utility
from collections import defaultdict
 
class NBClassifier(object):
	train_set = list() #training set. element: (tag, [feats])
	dev_set = list() #develoment set. might be empty
	test_set = list() #test set. used to classify
	#------------------------model parameters----------------------------
	#p(c)
	prior = defaultdict()
	#model parameters. probability of different words given each class with add-one smoothing
	model_param = defaultdict(dict)
	#average of p(w|c) in terms of c
	avg_param = dict()
	#--------------------------------------------------------------------
	
	def __init__(self, learn, pred, dev, utility):
		self.learn = learn
		self.pred = pred
		if self.learn:
			if dev:
				self.train_set, self.dev_set = utility.load_examples()
			else:
				self.train_set = utility.load_examples()
		elif self.pred:
			self.prior, self.model_param = utility.load_mod()
			self.test_set = utility.load_test()
			#averaging
			denom = len(self.model_param)
			for c in self.prior:
				s = 0
				for w in self.model_param:
					s += self.model_param[w][c]
				self.avg_param[c] = s/denom
		print('Train set: '+str(len(self.train_set))+' Dev set: '+str(len(self.dev_set))+' Test set: '+str(len(self.test_set)), file = sys.stderr)
		
	def train(self):
		tags = dict() #count of each class
		n_words = dict() #number of words in documents in each class
		vacabulary = defaultdict(dict) #size of vacabulary of each class
		n_train = 0 # == len(train_set)
		if self.learn!=True:
			print('Invalid initialization!\nThis instance is used to classify!', file = sys.stderr)
			return
		n_train = len(self.train_set)
		print('Training...\n', file = sys.stderr)
		for i in range(0, n_train):
			tag = self.train_set[i][0]
			feats = self.train_set[i][1]
			#n_c
			if tag not in tags:
				tags[tag] = 0
			tags[tag]+=1
			#k
			if tag not in vacabulary:
				vacabulary[tag] = dict()
			#N
			if tag not in n_words:
				n_words[tag] = 0
			n_words[tag] += len(feats)
			#n
			for elem in feats:
				if elem not in self.model_param:
					self.model_param[elem] = dict()
				if tag not in self.model_param[elem]:
					self.model_param[elem][tag] = 0
				self.model_param[elem][tag]+=1
				if elem not in vacabulary[tag]:
					vacabulary[tag][elem] = 1
		print('Frequency of each tag')
		print(tags, file = sys.stderr)
		print('')
		#parameters calculation
		#p(c)
		s = 0
		for key in tags:
			s += tags[key]
		for key in tags:
			self.prior[key] = math.log10(tags[key])-math.log10(s)
		#p(w|c) with add-one smoothing
		for w in self.model_param:
			for c in tags:
				if c in self.model_param[w]:
					self.model_param[w][c] = math.log10(self.model_param[w][c]+1)-math.log10(n_words[c]+len(vacabulary[c]))
				else:
					self.model_param[w][c] = -math.log10(n_words[c]+len(vacabulary[c]))
		#averaging
		denom = len(self.model_param)
		for c in tags:
			s = 0
			for w in self.model_param:
				s += self.model_param[w][c]
			self.avg_param[c] = s/denom
			
	def posterior(self, feats, c):
		likelihood = self.prior[c]
		for w in feats:
			if w in self.model_param:
				likelihood += self.model_param[w][c]
			else:
				likelihood += self.avg_param[c]
		return likelihood
	
	def predict(self, feats):
		ml = float('-inf')
		mc = ''
		for c in self.prior:
			p = self.posterior(feats, c)
			if p > ml:
				ml = p
				mc = c
		return mc

	def classify(self):
		if self.pred!=True:
			print('Invalid initialization!\nThis instance is used to train!', file = sys.stderr)
			return
		n_test = len(self.test_set)
		for i in range(0, n_test):
			#output the predicted class name on STDOUT
			print(self.predict(self.test_set[i]))

	def model_eval(self):
		n_dev = len(self.dev_set)
		if len(self.dev_set) == 0:
			return
		prec_num = dict()
		prec_denom = dict()
		rec_num = dict()
		rec_denom = dict()
		for i in range(0, n_dev):
			tag = self.dev_set[i][0]
			feats = self.dev_set[i][1]
			c_pred = self.predict(feats)
			if c_pred not in prec_denom:
				prec_denom[c_pred] = 0
			if tag not in rec_denom:
				rec_denom[tag] = 0
			if c_pred not in prec_num:
				prec_num[c_pred] = 0
			if tag not in rec_num:
				rec_num[tag] = 0
			prec_denom[c_pred] += 1
			rec_denom[tag]+=1
			if c_pred == tag:
				prec_num[c_pred]+=1
				rec_num[tag]+=1
		for c in self.prior:
			print('class '+c)
			prec = prec_num[c]/prec_denom[c]
			rec = rec_num[c]/rec_denom[c]
			f = 2*prec*rec/(prec+rec)
			print('Precision: '+str(prec)+' Recall: '+str(rec)+' F-score: '+str(f)+'\n', file = sys.stderr)
	

