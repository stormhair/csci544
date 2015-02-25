'''
	Use megam.opt to train
		postrain.py [TRAININGFILE] [MODEL]
'''
import os
import sys
import random

def str2example(strline):
	ret = ''
	tokens = strline.split(' ')
	tokens.append('EOS/EOS')
	tokens.insert(0, 'BOS/BOS')
	words = []
	tags = []
	for token in tokens:
		token = token.split('/')
		e = len(token)
		if e == 2:
			words.append(token[0])
		else:
			words.append('/'.join(token[0:e-1]))
		tags.append(token[e-1])
	for i in range(1, len(words)-1):
		ret+=(tags[i]+' w:'+words[i]+' w_prev:'+words[i-1]+' w_next:'+words[i+1]+'\n')
	return ret

def main():
	if len(sys.argv)!=3:
		print(sys.argv[0]+' [TRAININGFILE(input)] [MODEL(output)]', file = sys.stderr)
		return
	handle1 = open(sys.argv[1])
	tmp_file = 'postag'+str(random.randint(100000,999999))+'.train~'
	handle2 = open(tmp_file, 'w')
	while True:
		strline = handle1.readline()
		if not strline:
			break
		strline = strline.strip()
		handle2.write(str2example(strline))
	handle1.close()
	handle2.close()
	#system call megam.opt
	os.system('/home/stephen/csci544/tools/megam_i686.opt -nc -quiet multitron '+tmp_file+' > '+sys.argv[2])
	#system call to remove the temporary file
	os.system('rm '+tmp_file)

if __name__ == '__main__':
	main()

