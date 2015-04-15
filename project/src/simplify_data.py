'''
keep first name, last name, pid, and rComments only
format
	pid\tfirst name\tlast name\t#comment
	rComments1
	rComments2
	...
	pid\tfirst name\tlast name\t#comment
	...
By Wenqiang Wang
'''
import json

def main():
	input_path = '../data/usc.prof.ratings.json'
	inhandler = open(input_path)
	output_path = '../data/usc.prof.comments'
	outhandler = open(output_path, 'w')
	while True:
		text = inhandler.readline()
		if not text:
			break
		text = text.strip()
		data = json.loads(text)
		outhandler.write(str(data['pid'])+'\t'+data['first_name']+'\t'+data['last_name']+'\t'+str(len(data['ratings']))+'\n')
		for i in range(0, len(data['ratings'])):
			outhandler.write(data['ratings'][i]['rComments']+'\n')
	inhandler.close()
	outhandler.close()

if __name__ == '__main__':
	main()