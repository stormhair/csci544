'''
	Crawl the required data
	by Wenqiang Wang
'''
import argparse
import urllib.request
import json
import sys
import time
import random

def wait_time(min_t):
	return min_t+random.randint(1,7)

def get_professors_list(path):
	'''
	@param
		path type:string desc:the path containing professor id in the target university
	@return
		ret_list type:list of string desc:all professors' url in the university
	'''
	ret_list = list()
	jstr = str()
	handle = open(path)
	jstr = handle.readline().strip()
	data = json.loads(jstr)
	prof_list = data['response']['docs']
	for i in range(0, len(prof_list)):
		if int(prof_list[i]['total_number_of_ratings_i'])>0:
			tmp_dict = {'pid':'', 'first_name':'', 'last_name':''}
			tmp_dict['pid'] = prof_list[i]['pk_id']
			tmp_dict['first_name'] = prof_list[i]['teacherfirstname_t']
			tmp_dict['last_name'] = prof_list[i]['teacherlastname_t']
			ret_list.append(tmp_dict)
	return ret_list

def get_professor_data(prof_id):
	'''
	@param
		prof_id type:string desc:the id of the professor
	@return
		data type:string desc:containing meta html
	NEED EXCEPTION PROCESSING
	'''
	prof_profile = dict()
	print('downloading '+str(prof_id)+'...', file = sys.stderr)
	i = 1
	while True:
		url = 'http://www.ratemyprofessors.com/paginate/professors/ratings?tid='+str(prof_id)+'&page='+str(i)
		print('requesting page '+str(i)+' ...', file = sys.stderr)
		data = urllib.request.urlopen(url).read()
		data = data.decode('utf8')
		data = json.loads(data)
		print('requested!', file = sys.stderr)
		if len(data['ratings']) == 0:
			break
		if len(prof_profile) == 0:
			prof_profile = data
		else:
			prof_profile['ratings'].append(data['ratings'])
		i+=1
		time.sleep(wait_time(2))
	return prof_profile

def main():
	parser = argparse.ArgumentParser(description='This module scrapes reviews about professors from USC from www.ratemyprofessor.com.')
	#parser.add_argument('-id', type = str, metavar = 'UniversityID', default = '1381', help='the id of the target university', required = True)
	parser.add_argument('-i', type = str, metavar = 'INPUT', help='the path of the list of all professors in the target university', required = True)
	parser.add_argument('-o', type = str, metavar = 'OUTPUT', help='the path of the output file', required = True)

	args = parser.parse_args()
	argVars= vars(args)

	#uid = argVars['id'];
	#url_list = get_professors_url_list(uid)

	input_path = argVars['i']

	ret_list = get_professors_list(input_path)
	print('#professors: '+str(len(ret_list)), file = sys.stderr)

	output_path = argVars['o']
	output_handler = open(output_path, 'a')
	#
	#cont = False
	for elem in ret_list:
		#if elem['pid'] == 1506578:
		#	cont = True
		#if cont == False:
		#	continue
		profile = get_professor_data(elem['pid'])
		data = elem
		if 'ratings' in profile:
			data['ratings'] = profile['ratings']
		else:
			data['ratings'] = list()
		encodedjson = json.dumps(data)
		output_handler.write(encodedjson+'\n')
	output_handler.close()
	
if __name__ == '__main__':
	main()
