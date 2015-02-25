'''
	Averaged perceptron
	This is a program used to classify
	INPUT:
		test instances from STDIN and model file
	OUTPUT:
		results of classification
'''
import sys
import Util
import AvgPerceptron

def main():
	if len(sys.argv)!=2:
		print('Feeds one example to be classified through STDIN\nUsage\n\tpython3 '+sys.argv[0]+' [MODEL FILE]', file = sys.stderr)
		return
	inpath = sys.argv[1]
	util = Util.Util()
	avg_percep = AvgPerceptron.AvgPerceptron(10)
	print('loading model...', file = sys.stderr)
	avg_percep.load_model(inpath, util)
	print('model loaded!', file = sys.stderr)
	text = input()
	feats = util.tokenize(text)
	print(avg_percep.predict(feats))
	sys.stdout.flush()
if __name__ == '__main__':
	main()
