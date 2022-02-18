import traceback
from getters import repos, actors, name, helpers
from inspect import currentframe, getframeinfo

##########################
# Watch Events
##########################

def get_WatchEvent(repo_name, created_at, json_payload, record_d, db):
	actor = None
	starred_at = None
	actor_gravatar = None

	try:
		actor, actor_dict = helpers.get_actor_and_actor_dict(json_payload, record_d)
		starred_at = created_at

		# actor_gravatar
		try:
			if isinstance(record_d['actor'], dict):
				actor_gravatar = record_d['actor']['actor_gravatar']
			elif isinstance(record_d['actor_attributes'], dict):
				actor_gravatar = record_d['actor_attributes']['actor_gravatar']
			else:
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

	# output dict
	stars_dict = {}
	if starred_at:
		stars_dict['starred_at'] = starred_at
	if actor:
		stars_dict['actor'] = actor
	if actor_gravatar:
		stars_dict['actor_gravatar'] = actor_gravatar

	# full repo name
	try:
		full_repo_name = name.get_full_repo_name(json_payload, record_d, repo_name)
		if not full_repo_name:
			raise Exception('full_repo_name is None')
	except Exception as e:
		print("%s\n%s" % (str(e), record_d))
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
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
		# if 'owner' not in r_dict or not r_dict['owner']:
		# 	raise Exception('No owner')
		repos.get_Repo(full_repo_name, created_at, json_payload, record_d, r_dict, db)
	else:
		raise Exception("'r_dict' (%s) is not a dict!\n%s" % (r_dict, record_d))

	if isinstance(actor_dict, dict):
		actors.get_Actor(full_repo_name, actor_dict, record_d, db, created_at)
	else:
		raise Exception("'actor_dict' (%s) is not a dict!\n%s" % (actor_dict, record_d))
