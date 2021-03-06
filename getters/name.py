import traceback
import json
import os
import sys
from inspect import currentframe, getframeinfo
from getters import repos, actors

def get_actor_login_string(json_payload, record_d, full_repo_name):
	actor_name_string = None
	repo_name = None

	if '/' in full_repo_name:
		actor_name_string, repo_name = full_repo_name.split('/')
		return actor_name_string
	else:
		actor_name_string = None
	try:
		if isinstance(record_d['actor'], str):
			return record_d['actor']

		elif isinstance(record_d['actor'], dict):
			return record_d['actor']['login']

		elif isinstance(record_d['actor_attributes'], dict):
			return record_d['actor_attributes']['login']
		
		else:
			print('USER_NAME_STRING IS NOT FOUND!!!!!!!!')
			print('record_d: ' + str(record_d))
			exit(1)

	except KeyError as ke:
		try:
			if isinstance(json_payload['actor'], str):
				return json_payload['actor']
		except KeyError as ke:
			print('USER_NAME_STRING IS NOT FOUND!!!!!!!!')
			print('record_d: ' + str(record_d))
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('KEYERROR GET_USER_NAME_STRING_EXCEPTION: ' + str(ke))
			exit(1)

	except Exception as e:

		print('record_d: ' + str(record_d))
		print('ERROR: ' + str(e))
		traceback.print_exc()
		actor_name_string = None
		exit(1)

def url_to_name(repo_url):
	if repo_url.startswith('https://api.github.dev/repos/'):
		full_repo_name = repo_url.replace('https://api.github.dev/repos/', '')
		return full_repo_name

	elif repo_url.startswith('https://api.github.com/repos/'):
		full_repo_name = repo_url.replace('https://api.github.com/repos/', '')
		return full_repo_name
	
	elif repo_url.startswith('https://github.com/'):
		full_repo_name = repo_url.replace('https://github.com/', '')
		return full_repo_name

	elif repo_url.startswith('https://cache-default-email.review-lab.github.com/api/v3/repos/'):
		full_repo_name = repo_url.replace('https://cache-default-email.review-lab.github.com/api/v3/repos/', '')
		return full_repo_name

	elif repo_url.startswith('https://mg-author-re-request.review-lab.github.com/api/v3/repos/'):
		full_repo_name = repo_url.replace('https://mg-author-re-request.review-lab.github.com/api/v3/repos/', '')
		return full_repo_name
	else:
		traceback.print_exc()
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('NEW url_to_name URL CASE. repo_url: ' + str(repo_url))
		exit(1)

def get_full_repo_name_helper(record_d, r):

	# use 'name' first
	full_repo_name = record_d[r]['name']
	if '/' in full_repo_name:
		return full_repo_name

	# rely on 'url'
	repo_url = record_d[r]['url']
	full_repo_name = url_to_name(repo_url)
	if '/' in full_repo_name:
		return full_repo_name

	raise Exception('get_full_repo_name_helper PROBLEM: ' + str(full_repo_name))

def get_full_repo_name(json_payload, record_d, repo_name):
	# check for repo and repository in a record
	if ('repo' in record_d) and ('repository' in record_d):
		raise Exception('REPO_and_REPOSITORY_in_the_same_record_EXCEPTION')
	if '/' in repo_name:
		return repo_name

	if 'repo' in record_d:
		return get_full_repo_name_helper(record_d, 'repo')

	if 'repository' in record_d:
		return get_full_repo_name_helper(record_d, 'repository')

	raise Exception('get_full_repo_name PROBLEM: ' + str(record_d))
