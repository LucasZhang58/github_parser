import html
from platform import release
import traceback
import json
import os
import sys
from inspect import currentframe, getframeinfo
from getters import persons, repos
import name
##########################
# Push Events
##########################
def get_PushEvent(repo_name, created_at, json_payload, record_d, db, commits, commit_past_repo_names):
	try:
		# author name
		try:
			if len(json_payload['commits']) != 0:
				try:
					if isinstance(json_payload['commits'], list):
						
						if isinstance(json_payload['commits'][0], dict):
							if isinstance(json_payload['commits'][0]['author'], dict):
								author_name = json_payload['commits'][0]['author']['name']
					
			else:
				author_name = None
		except KeyError as ke:
			author_name = None

		# author email
		try:
			if len(json_payload['commits']) != 0:
				author_email = json_payload['commits'][0]['author']['email']
			else:
				author_email = None
		except KeyError as ke:
			author_email = None

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
		traceback.print_exc()
		exit(1)

	commit = {'commited_at' : created_at}
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

	full_repo_name = name.get_full_repo_name(json_payload, record_d, repo_name)
  
	# save in the database
	try:
		db.add_data(full_repo_name, created_at, 'commits', commits_dict)
	except Exception as e:
		print("Failed to save %s PushEvent record at %s: %s" % \
				(full_repo_name, created_at, str(e)))
		traceback.print_exc()
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)
