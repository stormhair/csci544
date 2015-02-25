'''
	Averaged perceptron
	python perceplearn.py [TRAININGFILE] [MODELFILE] -i [#iteration]
'''
import sys
import AvgPerceptron
import Util

def main():
	if len(sys.argv)<3:
		print('python3 '+sys.argv[0]+' [TRAININGFILE] [MODELFILE] -i [#iteration] (optional)', file = sys.stderr)
		return
	inpath = sys.argv[1]
	outpath = sys.argv[2]
	n_iter = 10
	if len(sys.argv) == 5:
		if sys.argv[3] == '-i':
			n_iter  = int(sys.argv[4])
	
	util = Util.Util()
	avg_percep = AvgPerceptron.AvgPerceptron(n_iter)
	print('loading training set...', file = sys.stderr)
	avg_percep.load_train(inpath, util)
	print('training...', file = sys.stderr)
	#avg_percep.train_on_file(inpath, util)
	avg_percep.train_with_shuflle()
	print('training over', file = sys.stderr)
	avg_percep.save_model(outpath, util)
	
if __name__ == '__main__':
	main()
