'''
	An implementation of Naive Bayes Classifier
	Usage:
		python3 nblearn.py [TRAIN FILE] -h [MODEL FILE]
	Argument list:
		TRAIN FILE:
			A file containing training examples. One example per line.
		MODEL FILE:
			A file generated to save all the parameters
		-h (optional):
			It indicates a development set exists in the training file, start with a 'DEV' tag in a single line
'''

import sys
import math
from Utility import Utility
from NBClassifier import NBClassifier
from collections import defaultdict

def main():
	if len(sys.argv)<3:
		print('python3 '+sys.argv[0]+' [TRAIN FILE] -h(optional) [MODEL FILE]', file = sys.stderr)
		return
	train_file = '';mod_file = ''
	dev_flag = False
	if len(sys.argv) == 3:
		train_file = sys.argv[1]
		mod_file = sys.argv[2]
	elif len(sys.argv) == 4:
		train_file = sys.argv[1]
		mod_file = sys.argv[3]
		if sys.argv[2] == '-h':
			dev_flag = True
	util = Utility(train_file, mod_file, '')
	nbc = NBClassifier(True, False, dev_flag, util)
	nbc.train()
	util.save_mod((nbc.prior, nbc.model_param))
	if dev_flag:
		nbc.model_eval()

if __name__ == '__main__':
	main()

