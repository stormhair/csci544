'''
	POS tagging, generate all possible NN,JJ pairs in each sentence
	by Wenqiang Wang
'''
import sys
import nltk
import argparse
import json
import string

def tokenize(text):
	tokens = text.split(' ')
	new_tokens = list()
	exclude = set(string.punctuation)
	for i in range(0, len(tokens)):
		s = tokens[i].strip()
		s = ''.join(ch for ch in s if ch not in exclude)
		t = s.lower()
		if len(t)>0:
			new_tokens.append(t)
	return new_tokens

def generate_baseline(pos):
	res = list()
	for i in range(0, len(pos)-1):
		if pos[i][1] in ['NN', 'NNP', 'NNPS', 'NNS']:
			for j in range(i+1, len(pos)):
				if pos[j][1] in ['JJ', 'JJR', 'JJS']:
					res.append((pos[i][0],pos[j][0]))
	return res

def main():
	parser = argparse.ArgumentParser(description='Generate baselines')
	parser.add_argument('-u', help='path of the file containing the target instance', type = str)
	parser.add_argument('-t', help='path of the file containing training data', type = str)
	args = parser.parse_args()
	target = open(args.u)
	users = dict()
	while True:
		text = target.readline()
		if not text:
			break
		text = text.strip().split('\t')
		users[int(text[0])] = True
	target.close()
	train = open(args.t)
	while True:
		text = train.readline()
		if not text:
			break
		text = text.strip()
		data = json.loads(text)
		if data['pid'] in users:
			handler = open('../data/baseline/'+str(data['pid'])+'.txt', 'w')
			for rate in data['ratings']:
				reviews = rate['rComments']
				tokens = tokenize(reviews)
				results = nltk.pos_tag(tokens)
				baseline = generate_baseline(results)
				for elem in baseline:
					handler.write(elem[0]+','+elem[1]+'\n')
			handler.close()
if __name__ == '__main__':
	main()