'''
	Given predicted results and the groud truth, calculate precision, recall and f-score for each name entity tag
	Usage:
		python3 nerEval.py PREDICTEDFILE GROUNDTRUTHFILE
	
'''
import sys

NETAG = ['LOC', 'ORG', 'PER', 'MISC']

def tokenize(text):
	return text.strip().split(' ')

def split_tag_and_word(tokens):
	tags = list()
	words = list()
	for token in tokens:
		elem = token.split('/')
		end = len(elem)
		t = elem[end-1]
		w = '/'.join(elem[0:end-1])
		tags.append(t)
		words.append(w)
	return tags, words

def check(tags, words, tags0, words0, prec_numer, prec_denom, rec_numer, rec_denom):
	i = 0
	# check precision
	while i < len(tags):
		if tags[i][0] == 'B':
			net = tags[i][2:]
			prec_denom[net]+=1
			if tags0[i] == tags[i]:
				i+=1
				flag = True
				while tags0[i][0] == 'I':
					if tags[i] != tags0[i]:
						flag = False
						break
					i+=1
				if flag:
					prec_numer[net]+=1
				i-=1
		i+=1
	# check recall
	i = 0
	while i < len(tags0):
		if tags0[i][0] == 'B':
			net = tags0[i][2:]
			rec_denom[net]+=1
			if tags[i] == tags0[i]:
				i+=1
				flag = True
				while tags0[i][0] == 'I':
					if tags[i] != tags0[i]:
						flag = False
						break
					i+=1
				if flag:
					rec_numer[net]+=1
				i-=1
		i+=1

def main():
	if len(sys.argv)!=3:
		print('Given predicted results and the groud truth, calculate precision, recall and f-score for each name entity tag\nUsage\n\tpython3 '+sys.argv[0]+' PREDICTEDFILE GROUNDTRUTHFILE', file = sys.stderr)
		return

	global NETAG
	prec_numer = dict()
	prec_denom = dict()
	rec_numer = dict()
	rec_denom = dict()

	for t in NETAG:
		prec_numer[t] = 0
		prec_denom[t] = 0
		rec_numer[t] = 0
		rec_denom[t] = 0
	
	pfile = sys.argv[1]
	gfile = sys.argv[2]
	
	phandler = open(pfile, errors = 'ignore')
	ghandler = open(gfile, errors = 'ignore')
	
	while True:
		text = phandler.readline()
		if not text:
			break
		tks1 = tokenize(text)

		text = ghandler.readline()
		if not text:
			print('Fatal error: the predicted file has more lines than the groud truth file!', file = sys.stderr)
			break
		
		tks0 = tokenize(text)
		
		if len(tks1)!=len(tks0):
			print('Fatal error: the two sentence cannot be aligned!', file = sys.stderr)
			continue	

		ne_tag1, words1 = split_tag_and_word(tks1)
		ne_tag0, words0 = split_tag_and_word(tks0)

		check(ne_tag1, words1, ne_tag0, words0, prec_numer, prec_denom, rec_numer, rec_denom)
	
	print('Tag\tPrecision\tRecall\tF-score\t')
	pn = 0;pd = 0;rn = 0;rd = 0
	for t in NETAG:
		pn+=prec_numer[t]
		pd+=prec_denom[t]
		rn+=rec_numer[t]
		rd+=rec_denom[t]
		print(t, end='')
		n = prec_numer[t]
		d = prec_denom[t]
		p = float('-inf')
		r = float('-inf')
		if d == 0:
			print('\tN/A', end = '')
		else:
			p = n/d
			print('\t'+str(p), end='')
		n = rec_numer[t]
		d = rec_denom[t]
		if d == 0:
			print('\tN/A', end = '')
		else:
			r = n/d
			print('\t'+str(r), end='')
		if p>0 and r>0:
			print('\t'+str(2*p*r/(p+r)))
		else:
			print('\tN/A')
	o_p = pn/pd;o_r = rn/rd
	print('Overall F-score: '+str(2*o_p*o_r/(o_p+o_r)))

if __name__ == '__main__':
	main()
