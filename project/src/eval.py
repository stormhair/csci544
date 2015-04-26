'''
	Calculate precision and recall wrt the golden standard
	By Wenqiang Wang
'''
import sys
import argparse

def main():
	parser = argparse.ArgumentParser(description='Precision and Recall')
	parser.add_argument('-b', help='path of the file containing golden standard', type = str)
	parser.add_argument('-t', help='path of the file containing results', type = str)
	args = parser.parse_args()
	#read prediction
	pred = dict()
	n_pred = 0
	handler = open(args.t)
	while True:
		text = handler.readline()
		if not text:
			break
		tokens = text.strip().split(',')
		n_pred+=1
		if tokens[0] not in pred:
			pred[tokens[0]] = dict()
		if tokens[1] not in pred[tokens[0]]:
			pred[tokens[0]][tokens[1]] = 0
		pred[tokens[0]][tokens[1]]+=1
	handler.close()

	#read golden standard
	gold = dict()
	n_gold = 0
	handler = open(args.b)
	while True:
		text = handler.readline()
		if not text:
			break
		tokens = text.strip().split(',')
		n_gold+=1
		if tokens[0] not in gold:
			gold[tokens[0]] = dict()
		if tokens[1] not in gold[tokens[0]]:
			gold[tokens[0]][tokens[1]] = 0
		gold[tokens[0]][tokens[1]]+=1
	handler.close()

	#calc precision and recall
	n_acc = 0
	for key1 in pred:
		for key2 in pred[key1]:
			if key1 in gold:
				if key2 in gold[key1]:
					if gold[key1][key2]>0:
						gold[key1][key2]-=1
						n_acc+=1
	print('Precision: '+str(n_acc/n_pred)+'\tRecall: '+str(n_acc/n_gold))

if __name__ == '__main__':
	main()