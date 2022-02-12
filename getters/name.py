import html
from lib2to3.pgen2.token import SLASH
from nturl2path import url2pathname
from platform import release
import traceback
import json
import os
import sys
from inspect import currentframe, getframeinfo
from getters import repos, persons

def get_user_name_string(json_payload, record_d):
	user_name_string = None
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
		user_name_string = None
		exit(1)

def url_to_name(repo_url):
	try:
		if repo_url.startswith('https://api.github.dev/repos/'):
			full_repo_name = repo_url.replace('https://api.github.dev/repos/', '')
			return full_repo_name

		elif repo_url.startswith('https://api.github.com/repos/'):
			full_repo_name = repo_url.replace('https://api.github.com/repos/', '')
			return full_repo_name
		
		elif repo_url.startswith('https://github.com/'):
			full_repo_name = repo_url.replace('https://github.com/', '')
			return full_repo_name

		else:
			raise Exception("Failed to detect repo_url startswith!")
	except Exception as e:
		traceback.print_exc()
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('NEW url_to_name URL CASE. repo_url %s: %s' % (str(repo_url), str(e)))
		exit(1)

def get_full_repo_name_helper(record_d, r):
	try:
		full_repo_name = record_d[r]['name']
		if '/' in full_repo_name:
			return full_repo_name

		repo_url = record_d[r]['url']
		full_repo_name = url_to_name(repo_url)
		if '/' in full_repo_name:
			return full_repo_name

		else:
			raise Exception("Failed to find full_repo_name!")
	except Exception as e:
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('get_full_repo_name_helper PROBLEM %s: %s' % (str(full_repo_name), str(e)))
		exit(1)

def get_full_repo_name(json_payload, record_d, repo_name):

	try:
		# check for repo and repository in a record
		if ('repo' in record_d) and ('repository' in record_d):
			raise Exception('REPO_and_REPOSITORY_in_the_same_record_EXCEPTION')

		elif '/' in repo_name:
			return repo_name

		elif 'repo' in record_d:
			full_repo_name = get_full_repo_name_helper(record_d, 'repo')
			return full_repo_name              

		elif 'repository' in record_d:
			full_repo_name = get_full_repo_name_helper(record_d, 'repository')
			return full_repo_name

		else:
			raise Exception("Failed to detect 'repo' and 'repository' in record_d!")

	except Exception as e:
		print(record_d)
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('get_full_repo_name PROBLEM %s: %s' % (str(full_repo_name), str(e)))
		exit(1)
