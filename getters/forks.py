import html
from platform import release
import traceback
import json
import os
import sys
from inspect import currentframe, getframeinfo
from getters import repos, persons
##########################
# Fork Events
##########################

def get_ForkEvent(repo_name, created_at, json_payload, record_d, db):

	# forkee
	try:
		if isinstance(json_payload['forkee'], int):
			forkee = json_payload['forkee']
		else:
			forkee = json_payload['forkee']['id']
	except KeyError as ke:
		try:
			forkee = record_d['actor']
		except KeyError as ke:
			print('GET_FORKEVENT_KEYERROR: ' + str(ke))
			forkee = None
		except Exception as e:
			print('record_d: ' + str(record_d) + ' is of type ' + str(type(record_d)))
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('FORKEVENT_EXCEPTION: ' + str(e))
			exit(1)

	# 
	try:
		forked_at = record_d['created_at']
	except KeyError as ke:
		try:
			if isinstance(json_payload['forkee'], int):
				forked_at = created_at 
			else:
				forked_at = json_payload['forkee']['created_at']
		except KeyError as ke:
			forked_at = created_at
		except Exception as e:
			print('record_d: ' + str(record_d) + ' is of type ' + str(type(record_d)))
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('FORKEVENT_EXCEPTION: ' + str(e))
			exit(1)
	except Exception as e:
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('FORKEVENT_EXCEPTION: ' + str(e))
		exit(1)

	#
	try:
		size = record_d['repository']['size']
	except KeyError as ke:
		if isinstance(json_payload['forkee'], dict):
			size = json_payload['forkee']['size']
		else:
			size = None
	except Exception as e:
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('FORKEVENT_EXCEPTION: ' + str(e))
		exit(1)
 
	forks_dict = { 'created_at' : forked_at}
	if forkee:
		forks_dict['forkee'] = forkee
	if size:
		forks_dict['size'] = size
   
	# save in the database
	try:
		db.add_data(repo_name, created_at, 'forks', forks_dict)
	except Exception as e:
		print("Failed to save %s ForkEvent record at %s: %s" % \
				(repo_name, created_at, str(e)))
		traceback.print_exc()
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)

	# event_type = 'ForkEvent'
	# persons.get_Person(repo_name, created_at, json_payload, record_d, db, event_type)
	# repos.get_Repo(repo_name, created_at, json_payload, record_d, db, event_type)
