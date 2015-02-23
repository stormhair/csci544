'''
	An implementation of Naive Bayes Classifier
	Usage:
		python3 nbclassify.py [MODEL FILE] [TEST FILE]
	Argument list:
		MODEL FILE:
			A file containing all the parameters
		TEST FILE:
			A file containing test set
'''

import sys
import math
from Utility import Utility
from NBClassifier import NBClassifier
from collections import defaultdict

def main():
	if len(sys.argv)!=3:
		print('python3 '+sys.argv[0]+' [MODEL FILE] [TEST FILE]', file = sys.stderr)
		return
	mod_path = sys.argv[1]
	test_path = sys.argv[2]
	util = Utility('', mod_path, test_path)
	nbc = NBClassifier(False, True, False, util)
	nbc.classify()

if __name__ == '__main__':
	main()

