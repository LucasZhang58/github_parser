import html
from platform import release
import traceback
import json
import os
import sys
from inspect import currentframe, getframeinfo
from getters import repos, persons, orgs
import getters.name as name

##########################
# Watch Events
##########################

def get_actor_from_p_dict(p_dict):
	actor = None
	if 'login' in p_dict:
		actor = p_dict['login']
	elif 'url' in p_dict:
		actor = name.url2actor(p_dict['url'])
	return actor

# gets 'p_dict', but prioritizes dict over str
def get_actor_and_p_dict(json_payload, record_d):

	p_dict = None
	actor = None

	if 'actor' in json_payload:
		if isinstance(json_payload['actor'], str):
			actor = json_payload['actor']
		elif isinstance(json_payload['actor'], dict):
			p_dict = json_payload['actor']
			actor = get_actor_from_p_dict(p_dict)
		else:
			raise Exception("json_payload['actor'] is not a str or dict")

	if (not actor or not p_dict or not isinstance(p_dict, dict)) and 'actor_attributes' in record_d and isinstance(record_d['actor_attributes'], dict):
		if not actor:
			actor = get_actor_from_p_dict(record_d['actor_attributes'])
		else:
			p_dict = record_d['actor_attributes']

	if (not actor or not p_dict or not isinstance(p_dict, dict)) and 'actor' in record_d:
		if not actor:
			if isinstance(record_d['actor'], str):
				actor = record_d['actor']
			elif isinstance(record_d['actor'], dict):
				actor = get_actor_from_p_dict(record_d['actor'])
			else:
				raise Exception("record_d['actor'] is not a str or dict")
		
		elif isinstance(record_d['actor'], dict):
			p_dict = record_d['actor']

	if not actor:
		raise Exception("no actor")
	if not p_dict:
		if actor:
			p_dict = {'login' : actor}
		else:
			raise Exception("no p_dict")

	return actor, p_dict

def get_WatchEvent(repo_name, created_at, json_payload, record_d, db):
	actor = None
	starred_at = None
	actor_gravatar = None

	try:
		actor, p_dict = get_actor_and_p_dict(json_payload, record_d)
		starred_at = created_at

		# actor_gravatar
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
		print('record_d: ' + str(record_d))
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
		if 'repo' in record_d and isinstance(record_d['repo'], dict):
			r_dict = record_d['repo']
		elif 'repository' in record_d and isinstance(record_d['repository'], dict):
			r_dict = record_d['repository']
		else:
			raise Exception("'repository' or 'repo' not found in record_d!")

	except Exception as e:
		print('record_d: ' + str(record_d))
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		traceback.print_exc()
		exit(1)

	if isinstance(r_dict, dict):
		repos.get_Repo(full_repo_name, created_at, json_payload, record_d, r_dict, db)
	else:
		raise Exception("'r_dict' (%s) is not a dict!\n%s" % (r_dict, record_d))

	if isinstance(p_dict, dict):
		persons.get_Person(full_repo_name, created_at, json_payload, record_d, p_dict, db)
	else:
		raise Exception("'p_dict' (%s) is not a dict!\n%s" % (p_dict, record_d))

	if 'org' in record_d:
		if isinstance(record_d['org'], dict):
			orgs.get_Org(full_repo_name, created_at, json_payload, record_d, record_d['org'], db)
		else:
			raise Exception("'org' (%s) is not a dict!\n%s" % (record_d['org'], record_d))

		


