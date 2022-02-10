import html
from platform import release
import traceback
import json
import os
import sys
from inspect import currentframe, getframeinfo
from getters import persons, repos

##########################
# Issues Events
##########################

def get_IssuesEvent(repo_name, created_at, json_payload, db):
	issue_id = None	   
	try:
		if isinstance(json_payload['issue'], int):
			issue_id = json_payload['issue']
		else:
			issue_id = json_payload['issue']['issue_id']
	except KeyError as ke:
		issue_id = None
	except Exception as e:
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('ISSUEEVENT_EXCEPTION: ' + str(e))
		exit(1)

	try:
		if json_payload['action'] == 'opened' and isinstance(json_payload['issue'], dict):
			issue_created_at = json_payload['issue']['created_at']
		else:
			issue_created_at = created_at
	except KeyError as ke:
		issue_created_at = None
	except Exception as e:
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('ISSUEEVENT_EXCEPTION: ' + str(e))
		exit(1)

	try:
		if json_payload['action'] == 'closed' and isinstance(json_payload['issue'], dict):
			closed_at = json_payload['issue']['created_at']
	except KeyError as ke:
		closed_at = None
	except Exception as e:
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('ISSUEEVENT_EXCEPTION: ' + str(e))
		exit(1)

	description = None
	try:
		description = json_payload['body']
	except KeyError as ke:

		description = None
	except Exception as e:
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('ISSUEEVENT_EXCEPTION: ' + str(e))
		exit(1)
	
	user = None
	try:
		if 'user' in str(json_payload):
			user = json_payload['user']['issue_id']
		else:
			user = None
	except KeyError as ke:
		try:
			if isinstance(json_payload['issue'], dict):
				user = json_payload['issue']['user']['issue_id']

		except KeyError as ke:
			print('json_payload: ' + str(json_payload))

			user = None
	except Exception as e:
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('ISSUEEVENT_EXCEPTION: ' + str(e))
		exit(1)
	

	assignee = None
	try:
		if 'assignee' in str(json_payload):
			assignee = json_payload['assignee']
		else:
			assignee = None
	except KeyError as ke:
		try:
			assignee = json_payload['issue']['assignee']
		except KeyError as ke:
			assignee = None
	except Exception as e:
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('ISSUEEVENT_EXCEPTION: ' + str(e))
		exit(1)

	title = None
	try:
		 if isinstance(json_payload['issue'], dict):
			 title = json_payload['issue']['title']
	except KeyError as ke:
		try:
			if 'title' in str(json_payload):
				title = json_payload['title']
			else:
				title = None
		except KeyError as ke:
			title = None
	except Exception as e:
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('ISSUEEVENT_EXCEPTION: ' + str(e))
		exit(1)
	
	issues_dict = {'created_at' : issue_created_at}
	if issue_id:
		issues_dict['ID'] = issue_id

	if closed_at:
		issues_dict['closed_at'] = closed_at

	if description:
		issues_dict['description'] = description

	if user:
		issues_dict['user'] = user

	if assignee:
		issues_dict['assignee'] = assignee

	if title:
		issues_dict['title'] = title
	# save in the database
	try:
		db.add_data(repo_name, created_at, 'issues', issues_dict)
	except Exception as e:
		print("Failed to save %s IssuesEvent record at %s: %s" % \
				(repo_name, created_at, str(e)))

	# event_type = 'IssuesEvent'
	# repos.get_Repo(repo_name, created_at, json_payload, record_d, db, event_type)
	# persons.get_Person(repo_name, created_at, json_payload, record_d, db, event_type)
