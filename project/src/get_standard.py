'''
	get standard and save them in seperate files
	By Wenqiang Wang
'''
import sys
import json
def main():
	infile = '../data/usc.prof.ratings.json'
	outdir = '../data/standard/'
	path = '../data/standard.list.txt'
	handler = open(path)
	pid = dict()
	while True:
		text = handler.readline()
		if not text:
			break
		token = text.strip().split('\t')
		pid[int(token[0])] = True
	handler.close()

	handler = open(infile)
	while True:
		text = handler.readline()
		if not text:
			break
		text = text.strip()
		data = json.loads(text)
		if data['pid'] in pid:
			output_path = outdir+str(data['pid'])
			outhandler = open(output_path, 'w')
			for r in data['ratings']:
				outhandler.write(r['rComments']+'\n')
			outhandler.close()
	handler.close()

if __name__ == '__main__':
	main()