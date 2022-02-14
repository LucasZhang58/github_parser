import html
from platform import release
import traceback
import json
import os
import sys
from inspect import currentframe, getframeinfo
from getters import repos, persons
import getters.name as name

##########################
# Watch Events
##########################
def get_WatchEvent(repo_name, created_at, json_payload, record_d, db):
	actor = None
	starred_at = None
	actor_gravatar = None

	try:
		try:
			if isinstance(json_payload['actor'], str):
				actor = json_payload['actor']
			elif isinstance(json_payload['actor'], dict):
				actor = json_payload['actor']['login']
			else:
				# print('record_d: ' + str(record_d))
				raise KeyError("KEYERROR: json_payload['actor'] is not a str or dict")
		except KeyError:
				if isinstance(record_d['actor'], str):
					actor = record_d['actor']
				elif isinstance(record_d['actor'], dict):
					actor = record_d['actor']['login']
				elif isinstance(record_d['actor_attributes'], dict):
					actor = record_d['actor_attributes']['login']
				else:
					# print('record_d: ' + str(record_d))
					raise Exception("Exception: json_payload['actor'] is not a str or dict")
		# acttor_gravatar
		starred_at = created_at
		try:
			if isinstance(record_d['actor'], dict):
				actor_gravatar = record_d['actor']['actor_gravatar']
			elif isinstance(record_d['actor_attributes'], dict):
				actor_gravatar = record_d['actor_attributes']['actor_gravatar']
			else:
				# print('record_d: ' + str(record_d))
				raise KeyError("KEYERROR: record_d['actor'] and record_d['actor'] are not dicts")
		except KeyError:
			actor_gravatar = None
	except Exception as e:
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)
		print('WATCHEVENT_EXCEPTION: %s\njson_payload: %s\nrecord_d: %s' % \
			(str(e), json_payload, record_d))
		print('record_d: ' + str(record_d))
		traceback.print_exc()
		exit(1)

	stars_dict = {}
	if starred_at:
		stars_dict['starred_at'] = starred_at
	if actor:
		stars_dict['actor'] = actor
	if actor_gravatar:
		stars_dict['actor_gravatar'] = actor_gravatar
	
	full_repo_name = name.get_full_repo_name(json_payload, record_d, repo_name)
	if not full_repo_name:
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('full_repo_name is None')
		exit(1)

	# save in the database
	try:
		db.add_data(full_repo_name, created_at, 'stars', stars_dict)
	except Exception as e:
		print('full_repo_name: ' + str(full_repo_name))
		print('created_at: ' + str(created_at))
		print('json_payload: ' + str(json_payload))
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)    
		traceback.print_exc()
		print("Failed to save %s WatchEvent record at %s: %s" % \
				(full_repo_name, created_at, str(e)))

	# check for repo and actor_attributes in a record
	if 'repo' in record_d and 'repository' in record_d:
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('REPO_and_REPOSITORY_in_the_same_record_EXCEPTION: ' + str(e))
		exit(1)

	try:
		r_dict = record_d['repo']
	except KeyError as ke:
		try:
			r_dict = record_d['repository']
		except KeyError as ke:
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('WATCHEVENT_EXCEPTION: ' + str(ke))
			exit(1)
	except Exception as e:
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('WATCHEVENT_EXCEPTION: ' + str(e))
		exit(1)

	if isinstance(r_dict, dict):
		repos.get_Repo(full_repo_name, created_at, json_payload, record_d, r_dict, db)

	try:
		p_dict = record_d['actor']
	except KeyError as ke:
		try:
			p_dict = record_d['actor_attributes']
		except KeyError as ke:
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('WATCHEVENT_EXCEPTION: ' + str(ke))
			exit(1)
	except Exception as e:
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		exit(1)

	if isinstance(p_dict, dict):
		persons.get_Person(full_repo_name, created_at, json_payload, record_d, p_dict, db)
