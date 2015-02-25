'''
	Use megam.opt to tag
		netag.py [MODEL]
	take test examples from STDIN and output the tags on STDOUT
'''

import io
import os
import sys
import codecs
import random

def tokenize(text):
	return text.split(' ')

def str2words(strline):
	return strline.split(' ')

def str2example_dev(strline):
	ret = ''
	tokens = strline.split(' ')
	tokens.append('EOS/EOS/O')
	tokens.insert(0, 'BOS/BOS/O')
	words = []
	pos_tags = []
	ner_tags = []
	for token in tokens:
		token = token.split('/')
		e = len(token)
		pos_tags.append(token[e-2])
		ner_tags.append(token[e-1])
		if e>3:
			words.append('/'.join(token[0:e-2]))
		else:
			words.append(token[0])
	for i in range(1, len(words)-1):
		ret+=(ner_tags[i]+' w:'+words[i]+' w_prev:'+words[i-1]+' w_next:'+words[i+1]+' pos:'+pos_tags[i]+' pos_prev:'+pos_tags[i-1]+' pos_next:'+pos_tags[i+1]+'\n')
	return ret

def str2example_test(strline):
	ret = ''
	tokens = strline.split(' ')
	tokens.append('EOS/EOS')
	tokens.insert(0, 'BOS/BOS')
	words = list()
	pos_tags = list()
	for token in tokens:
		token = token.split('/')
		e = len(token)
		if e == 2:
			words.append(token[0])
		else:
			words.append('/'.join(token[0:e-1]))
		pos_tags.append(token[e-1])
	for i in range(1, len(words)-1):
		ret+=('TEST w:'+words[i]+' w_prev:'+words[i-1]+' w_next:'+words[i+1]+' pos:'+pos_tags[i]+' pos_prev:'+pos_tags[i-1]+' pos_next:'+pos_tags[i+1]+'\n')
	return ret

def main():
	if len(sys.argv)<2:
		print(sys.argv[0]+' [MODEL(input)] -dev (optional)', file=sys.stderr)
		return
	dev_mode = False
	mod_path = sys.argv[1]
	if len(sys.argv) == 3:
		if sys.argv[2] == '-dev':
			dev_mode = True
		else:
			print(sys.argv[0]+' [MODEL(input)] -dev (optional)', file=sys.stderr)
			return
	print('Reading examples...', file = sys.stderr)
	if dev_mode:
		print('dev mode', file = sys.stderr)

	tmp_path = 'netag.test.tmp'+str(random.randint(100000, 999999))+'~'
	tmp_handle = open(tmp_path, 'w')
	sentence = list()

	input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='latin_1')

	#while True:
	for strline in input_stream:
		strline = strline.strip()

		tks = tokenize(strline)
		tks_dev = list()
		if dev_mode:
			for tk in tks:
				tmp_tks = tk.split('/')
				tk = '/'.join(tmp_tks[0:len(tmp_tks)-1])
				tks_dev.append(tk)
		if dev_mode:
			sentence.append(tks_dev)
		else:
			sentence.append(tks)

		if dev_mode:
			tmp_handle.write(str2example_dev(strline))
		else:
			tmp_handle.write(str2example_test(strline))

	tmp_handle.close()
	print('#sentence: '+str(len(sentence))+'\ntagging', file = sys.stderr)	

	#call megam.opt to label
	ret = os.popen('/home/stephen/csci544/tools/megam_i686.opt -quiet -nc -predict '+mod_path+' multitron '+tmp_path).read()
	os.system('rm '+tmp_path)
	
	ne_tags = list()
	for r in ret.split('\n'):
		token = r.split('\t')
		ne_tags.append(token[0])

	offset = 0
	for i in range(0, len(sentence)):
		output_str = list()
		for j in range(0, len(sentence[i])):
			output_str.append(sentence[i][j]+'/'+ne_tags[offset+j])
		print(' '.join(output_str))
		offset+=len(sentence[i])
	
if __name__ == '__main__':
	main()

