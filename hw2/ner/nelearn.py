'''
	Use megam.opt to train
		nelearn.py [TRAININGFILE] [MODEL]
'''
import os
import sys
import random

def str2example(strline):
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

def main():
	if len(sys.argv)!=3:
		print(sys.argv[0]+' [TRAININGFILE(input)] [MODEL(output)]', file = sys.stderr)
		return
	handle1 = open(sys.argv[1], errors = 'ignore')
	tmp_file = 'ner.train.'+str(random.randint(100000,999999))+'~'
	handle2 = open(tmp_file, 'w')
	while True:
		strline = handle1.readline()
		if not strline:
			break
		strline = strline.rstrip()
		handle2.write(str2example(strline))
	handle1.close()
	handle2.close()
	#system call megam.opt
	os.system('/home/stephen/csci544/tools/megam_i686.opt -nc -quiet multitron '+tmp_file+' > '+sys.argv[2])
	#system call to remove the temporary file
	os.system('rm '+tmp_file)

if __name__ == '__main__':
	main()

