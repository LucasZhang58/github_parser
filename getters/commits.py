import html
from platform import release
import traceback
import json
import os
import sys
from inspect import currentframe, getframeinfo
from getters import persons, repos

##########################
# Push Events
##########################

def get_PushEvent(repo_name, created_at, json_payload, db, commits, commit_past_repo_names):

	# author name
	try:
		if len(json_payload['commits']) != 0:
			author_name = json_payload['commits'][0]['author']['name']
		else:
			author_name = None
	except KeyError as ke:
		author_name = None
	except Exception as e:
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('PUSHEVENT_EXCEPTION: ' + str(e))
		exit(1)

	# author email
	try:
		if len(json_payload['commits']) != 0:
			author_email = json_payload['commits'][0]['author']['email']
		else:
			author_email = None
	except KeyError as ke:
		author_email = None
	except Exception as e:
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('PUSHEVENT_EXCEPTION: ' + str(e))
		exit(1)

	# commit message
	message = None
	try:
		message = json_payload['message']
	except KeyError as ke:
		message = None
	except Exception as e:
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('PUSHEVENT_EXCEPTION: ' + str(e))
		exit(1)

	commit = {'created_at' : created_at}
	if author_name:
		commit['author_name'] = author_name
	if author_email:
		commit['author_email'] = author_email
	if message:
		commit['message'] =  message

	commits.append(commit)
	commits_dict = {
		'repo_name' : repo_name,
		'commits' : commits
	}

	if repo_name not in commit_past_repo_names:
		commits_dict['{}'.format(repo_name)] = [commit]
	else:
		commits_dict['{}'.format(repo_name)].append(commit)
  
	# save in the database
	try:
		db.add_data(repo_name, created_at, 'commits', commits_dict)
	except Exception as e:
		print("Failed to save %s PushEvent record at %s: %s" % \
				(repo_name, created_at, str(e)))
		traceback.print_exc()
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)

	# event_type = 'PushEvent'

	# repos.get_Repo(repo_name, created_at, json_payload, record_d, db, event_type)
	# persons.get_Person(repo_name, created_at, json_payload, record_d, db, event_type)
