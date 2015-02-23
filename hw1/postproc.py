'''
	This program is used to postprocessing the output of Megam and SVMLight
	Usage:
		postproc.py [OPTION] [INPUT FILE] [OUTPUTFILE] -v(optional) [GROUNDTRUTH FILE](optional, with -v)
	Option:
		1 : input file is a file containing the predicted results of megam, the format is
			[predicted label]\t[param1] [param2] ...
			output is only one column containing predicted label
		2 : input file is a file containing the predicted results of svmLight...
		3 : generate a test file for megam. format:
			TEST [feature1] [feature2] ...
		4 : input file is a file containing the predicted results of svmLight, the format is
			[score]
	-v: optional. precision, recall and f-score will be calculated when -v and GOUNDTRUTH FILE is provided
'''
import sys

def model_eval(pred, grnd):
	prec_num = dict()
	prec_denom = dict()
	rec_num = dict()
	rec_denom = dict()
	classname = dict()
	for i in range(0, len(pred)):
		c_pred = pred[i]
		tag = grnd[i]
		if tag not in classname:
			classname[tag] = 1
		if c_pred not in classname:
			classname[c_pred] = 1
		if c_pred not in prec_denom:
			prec_denom[c_pred] = 0
		if tag not in rec_denom:
			rec_denom[tag] = 0
		if c_pred not in prec_num:
			prec_num[c_pred] = 0
		if tag not in rec_num:
			rec_num[tag] = 0
		prec_denom[c_pred] += 1
		rec_denom[tag]+=1
		if c_pred == tag:
			prec_num[c_pred]+=1
			rec_num[tag]+=1

	for c in classname:
		print('class '+c)
		prec = prec_num[c]/prec_denom[c]
		rec = rec_num[c]/rec_denom[c]
		f = 2*prec*rec/(prec+rec)
		print('Precision: '+str(prec)+' Recall: '+str(rec)+' F-score: '+str(f)+'\n', file = sys.stderr)

def refine_megam(path):
	pred_tag = list()
	handler = open(path, errors = 'ignore')
	while True:
		strline = handler.readline()
		if not strline:
			break
		tokens = strline.strip().split('\t')
		pred_tag.append(tokens[0])
	handler.close()
	return pred_tag

def test_megam(inpath, outpath):
	inhandler = open(inpath, errors = 'ignore')
	outhandler = open(outpath, 'w')
	while True:
		strline = inhandler.readline()
		if not strline:
			break
		outhandler.write('TEST '+strline)
	inhandler.close()
	outhandler.close()

def get_groudtruth(path):
	#used to get tag from a standard dev set file
	tag = list()
	handler = open(path, errors = 'ignore')
	while True:
		strline = handler.readline()
		if not strline:
			break
		tokens = strline.strip().split(' ')
		tag.append(tokens[0])
	handler.close()
	return tag

def refine_svmlight(path, map_table):
	pred_tag = list()
	handler = open(path)
	while True:
		strline = handler.readline()
		if not strline:
			break
		score = float(strline.strip('\n'))
		if score > -0.23093018:
			pred_tag.append(map_table['1'])
		else:
			pred_tag.append(map_table['-1'])
	handler.close()
	return pred_tag

def save(path, pred):
	handler = open(path, 'w')
	for e in pred:
		handler.write(e+'\n')
	handler.close()
	
def main():
	if len(sys.argv)<4:
		print('python3 '+sys.argv[0]+' [OPTION] [INPUT FILE] [OUTPUTFILE] -v(optional) [GROUNDTRUTH FILE](optional, with -v)', file = sys.stderr)
		return
	opt = int(sys.argv[1])
	input_path = sys.argv[2]
	output_path = sys.argv[3]
	truth_path = ''
	eval_flag = False
	if len(sys.argv) == 6:
		if sys.argv[4] == '-v':
			truth_path = sys.argv[5]
			eval_flag = True
		else:
			print('python3 '+sys.argv[0]+' [OPTION] [INPUT FILE] [OUTPUTFILE] -v(optional) [GROUNDTRUTH FILE](optional, with -v)', file = sys.stderr)
			return
	pred = list()
	tag = list()
	if opt == 1:
		pred = refine_megam(input_path)
		save(output_path, pred)
	elif opt == 2:
		pass
	elif opt == 3:
		test_megam(input_path, output_path)
	elif opt == 4:
		pred = refine_svmlight(input_path, {'1':'POS', '-1':'NEG'})
		save(output_path, pred)
	if eval_flag:
		tag = get_groudtruth(truth_path)
		model_eval(pred, tag)

if __name__ == '__main__':
	main()

