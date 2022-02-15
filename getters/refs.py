from platform import release
import traceback
import json
import os
import sys
from inspect import currentframe, getframeinfo
from getters import repos, persons
import getters.name as name

##########################
# Create Events
##########################
def get_attributes(attr, json_payload, record_d, created_at):
	try:
		try:
			type_name = json_payload[attr]
		except KeyError as ke:
			try:
				type_name = record_d[attr]
			except KeyError as ke:
				raise Exception("attr %s not found!" % (attr))

		return type_name, created_at

	except Exception as e:
		print('record_d: ' + str(record_d))
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('get_attributes CREATEEVENT_EXCEPTION: ' + str(e))
		traceback.print_exc()
		exit(1)

def parse_ref_type(attr, ref_type, repo_name, created_at, json_payload, record_d, db, ref_past_repo_names):

	if ref_type in ['branch', 'object', 'repository']:
		branch_name, record_created_at = get_attributes(attr, json_payload, record_d, created_at)
		if ref_type == 'repository':
			if not branch_name:
				branch_name = 'master'
			ref_type = 'branch'
		ref_helper(repo_name, created_at, record_d, json_payload, db, branch_name, record_created_at, ref_past_repo_names, ref_type)

	elif ref_type == 'tag':
		tag_name, record_created_at = get_attributes(attr, json_payload, record_d, created_at)
		ref_helper(repo_name, created_at, record_d, json_payload, db, tag_name, record_created_at, ref_past_repo_names, ref_type)

	else:
		raise Exception("Unkown %s in json_payload: %s" % (ref_type))

def get_CreateEvent(repo_name, created_at, json_payload, record_d, db, ref_past_repo_names):
	try:
		if 'ref_type' in json_payload:
			parse_ref_type('ref', json_payload['ref_type'], repo_name, created_at, json_payload, record_d, db, ref_past_repo_names)
		elif 'ref_type' in record_d:
			parse_ref_type('ref', record_d['ref_type'], repo_name, created_at, json_payload, record_d, db, ref_past_repo_names)
		elif 'object' in json_payload:
			parse_ref_type('object_name', json_payload['object'], repo_name, created_at, json_payload, record_d, db, ref_past_repo_names)
		else:
			raise Exception('ref_type or object not found!')

	except Exception as e:
		print('record_d: ' + str(record_d) + ' is of type ' + str(record_d))
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('get_CreateEvent CREATEEVENT_EXCEPTION: ' + str(e))
		traceback.print_exc()
		exit(1)

def ref_helper(repo_name, created_at, record_d, json_payload, db, type_name, record_created_at, ref_past_repo_names, ref_type):
	try:
		full_repo_name = name.get_full_repo_name(json_payload, record_d, repo_name)

		#create type_dict to append to the branches, tag, or repository key-value pair
		type_dict = {}
		if record_created_at:
			type_dict['record_created_at'] = record_created_at
		if type_name:
			try:
				type_dict['{}_name'.format(ref_type)] = type_name
			except KeyError as ke:
				print('re_helper, type_name Error: ' + str(ke))

		ref_type_plural = ''
		if ref_type == 'branch':
			ref_type_plural = 'branches'
		elif ref_type == 'tag':
			ref_type_plural = 'tags'
		else:
			raise Exception("Unknown ref_type %s" % (ref_type))

		#try:
		#	if  full_repo_name not in  ref_past_repo_names:
		#		ref_past_repo_names[full_repo_name] = {ref_type_plural : [type_dict]}
		#		#print(ref_past_repo_names['{}'.format(full_repo_name)])
		#	else:
		#		if ref_type_plural not in ref_past_repo_names[full_repo_name]:
		#			ref_past_repo_names[full_repo_name][ref_type_plural] = [type_dict]
		#		else:
		#			ref_past_repo_names[full_repo_name][ref_type_plural].append(type_dict)
		#except KeyError as ke:
		#	print('KEYERROR re_helper, if full_repo_name not in ref_past_repo_names["{}".format(full_repo_name)] and not ref_past_repo_names["{}".format(full_repo_name)]: ' + str(ke))
		#	traceback.print_exc()

		# save in the database
		db.add_data(full_repo_name, created_at, ref_type_plural, type_dict)

		# save repo informtion
		try:
			r_dict = record_d['repo']
		except KeyError as ke:
			try:
				r_dict = record_d['repository']
			except KeyError as ke:
				raise Exception("'repo' or 'repository' not found")

		if isinstance(r_dict, dict):
			repos.get_Repo(full_repo_name, created_at, json_payload, record_d, r_dict, db)
		else:
			raise Exception("'r_dict' not a dict!")

		# save person information
		try:
			if isinstance(record_d['actor'], dict):
				p_dict = record_d['actor']
				persons.get_Person(full_repo_name, created_at, json_payload, record_d, p_dict, db)
			elif isinstance(record_d['actor_attributes'], dict):
					p_dict = record_d['actor_attributes']
					persons.get_Person(full_repo_name, created_at, json_payload, record_d, p_dict, db)
			else:
				raise Exception("HAVEN'T FOUND P_DICT")

		except KeyError as ke:
			if 'actor' in record_d:
				p_dict = {
					'login' : record_d['actor']
				}
			else:
				raise Exception('KEYERROR: ' + str(ke))

		full_repo_name = name.get_full_repo_name(json_payload, record_d, repo_name)

		if isinstance(p_dict, dict):
			persons.get_Person(full_repo_name, created_at, json_payload, record_d, p_dict, db)
		else:
			raise Exception('P_DICT (%s) IS NOT A DICT!' % (str(p_dict)))

	except Exception as e:
		print('record_d (%s): %s' % (type(record_d), str(record_d)))
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('ref_helper CREATEEVENT_EXCEPTION: ' + str(e))
		traceback.print_exc()
		exit(1)
