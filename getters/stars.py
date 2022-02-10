import html
from platform import release
import traceback
import json
import os
import sys
from inspect import currentframe, getframeinfo
from getters import repos, persons

##########################
# Watch Events
##########################
def get_WatchEvent(repo_name, created_at, json_payload, record_d, db):

	try:
		actor = json_payload['actor']
	except KeyError as ke:
		try:
			actor = record_d['actor']
		except KeyError as ke:
			actor = None
	except Exception as e:
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('WATCHEVENT_EXCEPTION: ' + str(e))
		exit(1)

	try:
		actor_gravatar = json_payload['actor_gravatar']
	except KeyError as ke:
		try:
			actor_gravatar = record_d['actor_attributes']['gravatar_id']
		except KeyError as ke:
			actor_gravatar = None
	except Exception as e:
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('WATCHEVENT_EXCEPTION: ' + str(e))
		exit(1)

	try:
		starred_at = created_at
	except KeyError as ke:
		starred_at = None
	except Exception as e:
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('WATCHEVENT_EXCEPTION: ' + str(e))
		exit(1)

	stars_dict = {'starred_at': starred_at}
	if actor:
		stars_dict['actor'] = actor
	
	if actor_gravatar:
		stars_dict['actor_gravatar'] = actor_gravatar

	# save in the database
	try:
		db.add_data(repo_name, created_at, 'stars', stars_dict)
	except Exception as e:
		print('repo_name: ' + str(repo_name))
		print('created_at: ' + str(created_at))
		print('json_payload: ' + str(json_payload))
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)    
		traceback.print_exc()
		print("Failed to save %s WatchEvent record at %s: %s" % \
				(repo_name, created_at, str(e)))

	
	# event_type = 'WatchEvent'
	# repos.get_Repo(repo_name, created_at, json_payload, record_d, db, event_type)
	# persons.get_Person(repo_name, created_at, json_payload, record_d, db, event_type)

