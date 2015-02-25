'''
	Use megam.opt to tag
	Usage:
		postrain.py [MODEL] -dev (optional)
		take test examples from STDIN and output the tags on STDOUT
		-dev dev mode 
'''

import os
import sys
import random

def tokenize(text):
	return text.split(' ')

def str2words(strline):
	ret=[]
	tokens = strline.split(' ')
	for token in tokens:
		token = token.split('/')
		ret.append(token[0])
	return ret

def str2example_dev(strline):
	ret = ''
	tokens = strline.split(' ')
	tokens.append('EOS/EOS')
	tokens.insert(0, 'BOS/BOS')
	words = list()
	pos_tags = list()
	for token in tokens:
		token = token.split('/')
		words.append(token[0])
		pos_tags.append(token[1])
	for i in range(1, len(words)-1):
		ret+=(pos_tags[i]+' w:'+words[i]+' w_prev:'+words[i-1]+' w_next:'+words[i+1]+'\n')
	return ret

def str2example_test(strline):
	ret = ''
	tokens = strline.split(' ')
	tokens.append('EOS')
	tokens.insert(0, 'BOS')
	words = list()
	pos_tags = list()
	for token in tokens:
		words.append(token)
	for i in range(1, len(words)-1):
		ret+=('TEST w:'+words[i]+' w_prev:'+words[i-1]+' w_next:'+words[i+1]+'\n')
	return ret

def main():
	if len(sys.argv)<2:
		print(sys.argv[0]+' [MODEL(input)] -dev (optional)', file=sys.stderr)
		return
	mod_path = sys.argv[1]
	dev_mode = False
	if len(sys.argv) == 3:
		if sys.argv[2] == '-dev':
			dev_mode = True
		else:
			print(sys.argv[0]+' [MODEL(input)] -dev (optional)', file=sys.stderr)
			return

	sentence = list()
	
	if dev_mode:
		print('dev mode', file = sys.stderr)

	print('Reading examples...', file = sys.stderr)
	tmp_path = 'postag.test.tmp'+str(random.randint(100000, 999999))+'~'
	tmp_handle = open(tmp_path, 'w')
	while True:
		#get test examples from STDIN
		try:
			strline = input()
			strline = strline.rstrip()

			tks = tokenize(strline)
			tks_dev = list()
			if dev_mode:
				tks = tokenize(strline)
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
		except(EOFError):
			tmp_handle.close()
			break

	print('#sentence: '+str(len(sentence))+'\ntagging', file = sys.stderr)

	#call megam.opt to label
	ret = os.popen('/home/stephen/csci544/tools/megam_i686.opt -quiet -nc -predict '+mod_path+' multitron '+tmp_path).read()
	os.system('rm '+tmp_path)

	#----debug-----
	#print(str(len(ret.split('\n'))), file = sys.stderr)
	#out = open('return.txt', 'w')
	#out.write(ret)
	#--------------

	tags = list()
	for r in ret.split('\n'):
		token = r.split('\t')
		tags.append(token[0])

	#----debug-----
	nw = 0
	print('#tags '+str(len(tags)), file = sys.stderr)
	for s in sentence:
		nw+=len(s)
	print('#words '+str(nw), file = sys.stderr)
	#--------------
	
	offset = 0
	for i in range(0, len(sentence)):
		output_str = list()
		for j in range(0, len(sentence[i])):
			output_str.append(sentence[i][j]+'/'+tags[offset+j])
		print(' '.join(output_str))
		offset+=len(sentence[i])
	
if __name__ == '__main__':
	main()

