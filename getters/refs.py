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

def get_CreateEvent(repo_name, created_at, json_payload, db, record_d, ref_past_repo_names):
	if json_payload['ref_type'] == 'branch' or record_d['ref_type'] == 'branch':
		try:
			try:
				branch_name = json_payload['ref']
			except KeyError as ke:
				try:
					branch_name = record_d['ref']
				except KeyError as ke:
					print('GET_CREATEEVENT_KEYERROR: ' + str(ke))
					branch_name = None
			try:
				record_created_at = json_payload['created_at']
			except KeyError as ke:
				record_created_at = created_at
		except Exception as e:
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('CREATEEVENT_EXCEPTION: ' + str(e))
			traceback.print_exc()
			exit(1)

		ref_helper(repo_name, created_at, record_d, json_payload, db, branch_name, tag_name, record_created_at, ref_past_repo_names)

	elif json_payload['ref_type'] == 'tag' or record_d['ref_type'] == 'tag':
		try:
			try:
				tag_name = json_payload['ref']
				
			except KeyError as ke:
				try:
					tag_name = record_d['ref']
				except KeyError as ke:
					print('GET_CREATEVENT_KEYERROR: ' + str(ke))
					tag_name = None
			try:
				record_created_at = json_payload['created_at']
			except KeyError as ke:
				record_created_at = None
		except Exception as e:
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('CREATEEVENT_EXCEPTION: ' + str(e))
			traceback.print_exc()
			exit(1)
		ref_helper(repo_name, created_at, record_d, json_payload, db, branch_name, tag_name, record_created_at, ref_past_repo_names)
	else:
		print('NEW REF TYPE!: ' + str(json_payload['ref_type']))
		print('NEW REF TYPE!: ' + str(record_d['ref_type']))
		print('record_d: ' + str(record_d))

def get_branch_or_tag_name():
	pass

def ref_helper(repo_name, created_at, record_d, json_payload, db, branch_name, tag_name, record_created_at, ref_past_repo_names):

	branch_dict = {}
	if record_created_at:
		branch_dict['record_created_at'] = record_created_at
	
	if branch_name:
		branch_dict['branch_name'] = branch_name
	
	tag_dict = {}
	if record_created_at:
		tag_dict['record_created_at'] = record_created_at
	
	if tag_name:
		tag_dict['tag_name'] = tag_name
	if branch_name:
		if branch_name not in str(ref_past_repo_names['{}'.format(repo_name)]['branches']) and not ref_past_repo_names['{}'.format(repo_name)]['branches']:
			ref_past_repo_names['{}'.format(repo_name)]['branches'] = [branch_dict]
		else:
			ref_past_repo_names['{}'.format(repo_name)]['branches'].append(branch_dict)
	if tag_name:
		if tag_name not in str(ref_past_repo_names['{}'.format(repo_name)]['tag']) and not ref_past_repo_names['{}'.format(repo_name)]['branches']:
			ref_past_repo_names['{}'.format(repo_name)]['tag'] = [tag_dict]
		else:
			ref_past_repo_names['{}'.format(repo_name)]['tag'].append(tag_dict)

	full_repo_name = name.get_full_repo_name(json_payload, record_d, repo_name)
	if not full_repo_name:
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('full_repo_name is None')
		exit(1)

	# save in the database
	try:
		db.add_data(full_repo_name, created_at, 'refs', ref_past_repo_names['{}'.format(repo_name)])
	except Exception as e:
		print("Failed to save %s ref output at %s: %s" % \
				(full_repo_name, created_at, str(e)))
		traceback.print_exc()

	# check for repo and actor_attributes in a record

	if 'repo'in record_d and 'repository'in record_d:
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('REPO_and_REPOSITORY_in_the_same_record_EXCEPTION: ' + str(e))
		exit(1)

	try:
		r_dict = record_d['repo']
	except KeyError as ke:
		try:
			r_dict = record_d['repository']
		except Exception as ee:
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('CREATEEVENT_EXCEPTION: ' + str(ee))
			exit(1)
	except Exception as e:
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('CREATEEVENT_EXCEPTION: ' + str(e))
		exit(1)

	if isinstance(r_dict, dict):
		repos.get_Repo(full_repo_name, created_at, json_payload, record_d, r_dict, db)

	#add actor into the dictionary?
	try:
		p_dict = record_d['actor']
	except KeyError as ke:
		try:
			p_dict = record_d['actor_attributes']
		except Exception as ee:
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('CREATEEVENT_EXCEPTION: ' + str(ee))
			exit(1)
	except Exception as e:
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('CREATEEVENT_EXCEPTION: ' + str(e))
		exit(1)

	user_name_string = name.get_user_name_string(json_payload, record_d)

	if isinstance(p_dict, dict):
		persons.get_Person(user_name_string, created_at, json_payload, record_d, p_dict, db)
