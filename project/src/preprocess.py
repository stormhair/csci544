'''
get basic statitcs of the data
By Wenqiang Wang
'''
import sys
import json

def main():
	input_path = '../data/usc_prof_ratings.json'
	inhandler = open(input_path)
	output_path = '../data/usc.prof.ratings.json'
	outhandler = open(output_path, 'w')
	while True:
		text = inhandler.readline()
		if not text:
			break
		text = text.strip()
		data = json.loads(text)
		new_data = data.copy()
		new_data['ratings'] = list()
		for item in data['ratings']:
			if type(item) == type(dict()):
				new_data['ratings'].append(item)
			elif type(item) == type(list()):
				for item2 in item:
					new_data['ratings'].append(item2)
		print(len(new_data['ratings']))
		outhandler.write(json.dumps(new_data)+'\n')
	inhandler.close()

if __name__ == '__main__':
	main()