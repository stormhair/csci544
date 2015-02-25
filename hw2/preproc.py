'''
	Preprocessing and generating features
	Usage:
		python3 preproc.py [option] [input] [output]
		option
			1 : for POS tagging train. and dev. set
			2 : for POS tagging test set
			3 : for NER train. and dev. set
			4 : for NER test set
'''
import sys

n_token = 0
tag = dict()

def tokenize(text):
	return text.strip().split(' ')

def gen_feats_pos(tokens):
	global tag
	feats = list()
	words = list()
	pos_tags = list()
	tokens.append('EOS/EOS')
	tokens.insert(0, 'BOS/BOS')
	for tk in tokens:
		tk = tk.split('/')
		e = len(tk)
		if e == 2:
			words.append(tk[0])
		else:
			words.append('/'.join(tk[0:e-1]))
		pos_tags.append(tk[e-1])
		if tk[e-1] not in tag:
			tag[tk[e-1]] = 1
	for i in range(1, len(words)-1):
		feats.append(pos_tags[i]+' w:'+words[i]+' w_prev:'+words[i-1]+' w_next:'+words[i+1]+'\n')
	return feats

def gen_feats_pos_test(tokens):
	feats = list()
	words = list()
	tokens.append('EOS')
	tokens.insert(0, 'BOS')
	for tk in tokens:
		words.append(tk)
	for i in range(1, len(words)-1):
		feats.append('w:'+words[i]+' w_prev:'+words[i-1]+' w_next:'+words[i+1]+'\n')
	return feats

def gen_feats_ner(tokens):
	global tag
	feats = list()
	words = list()
	pos_tags = list()
	ne_tags = list()
	tokens.append('EOS/EOS/O')
	tokens.insert(0, 'BOS/BOS/O')
	for tk in tokens:
		tk = tk.split('/')
		e = len(tk)
		if e == 3:
			words.append(tk[0])
		else:
			words.append('/'.join(tk[0:e-2]))
		pos_tags.append(tk[e-2])
		ne_tags.append(tk[e-1])
		if tk[e-1] not in tag:
			tag[tk[e-1]] = 1
	for i in range(1, len(words)-1):
		feats.append(ne_tags[i]+' w:'+words[i]+' w_prev:'+words[i-1]+' w_next:'+words[i+1]+' pos:'+pos_tags[i]+' pos_prev:'+pos_tags[i-1]+' pos_next:'+pos_tags[i+1]+'\n')
	return feats

def gen_feats_ner_test(tokens):
	feats = list()
	words = list()
	pos_tags = list()
	tokens.append('EOS/EOS')
	tokens.insert(0, 'BOS/BOS')
	for tk in tokens:
		tk = tk.split('/')
		e = len(tk)
		if e == 2:
			words.append(tk[0])
		else:
			words.append('/'.join(tk[0:e-1]))
		pos_tags.append(tk[e-1])
	for i in range(1, len(words)-1):
		feats.append('w:'+words[i]+' w_prev:'+words[i-1]+' w_next:'+words[i+1]+' pos:'+pos_tags[i]+' pos_prev:'+pos_tags[i-1]+' pos_next:'+pos_tags[i+1]+'\n')
	return feats

def main():
	if len(sys.argv)<3:
		print('Preprocessing and generating features\nUsage\n\tpython3 '+sys.argv[0]+' [option] [input] [output]\noption\n\t1 : for POS tagging train. and dev. set\n\t2 : for POS tagging test set\n\t3 : for NER train. and dev. set\n\t4 : for NER test set', file = sys.stderr)
		return
	opt = int(sys.argv[1])
	inpath = sys.argv[2]
	outpath = sys.argv[3]
	global n_token
	global tag

	inhandler = open(inpath, errors = 'ignore')
	outhandler = open(outpath, 'w')
	
	while True:
		text = inhandler.readline()
		if not text:
			break
		tks = tokenize(text)
		n_token+=len(tks)
		feats = list()
		if opt == 1:
			feats = gen_feats_pos(tks)
		elif opt == 2:
			feats = gen_feats_pos_test(tks)
		elif opt == 3:
			feats = gen_feats_ner(tks)
		elif opt == 4:
			feats = gen_feats_ner_test(tks)
		for f in feats:
			outhandler.write(f)

	inhandler.close()
	outhandler.close()
	
	print('Summary\n#tokens: '+str(n_token)+' #tag: '+str(len(tag))+'\nTags: '+str(tag), file = sys.stderr)
	
if __name__ == '__main__':
	main()
