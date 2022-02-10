import html
from http.client import InvalidURL
from platform import release
import traceback
import json
import os
import sys
from inspect import currentframe, getframeinfo
##########################
# REPO
##########################

def get_Repo(repo_name, created_at, json_payload, record_d, db, event_type):

	repo_name = repo_name
	repo_url = None

	created_at = None

	repo_description = None
	repo_homepage = None
	size = None
	language = None
	  #  license = None

	owner = None
	is_forked = None

	if '"repo":' in str(record_d):

		try:
			repo_name = record_d['repo']['name']
		except KeyError as ke:
			#print('GET_REPO_KEYERROR: ' + str(ke))
			repo_name = repo_name
		except Exception as e:
			print('record_d: ' + str(record_d) + ' is of type ' + str(type(record_d)))
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('GET_REPO_EXCEPTION: ' + str(e))
			exit(1)

		try:
			repo_url = record_d['repo']['url']
		except KeyError as ke:
			#print('GET_REPO_KEYERROR: ' + str(ke))
			repo_url = None
		except Exception as e:
			print('record_d: ' + str(record_d) + ' is of type ' + str(type(record_d)))
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('GET_REPO_EXCEPTION: ' + str(e))
			exit(1)

		try:
			id = record_d['repo']['id']
		except KeyError as ke:
			#print('GET_REPO_KEYERROR: ' + str(ke))
			id = None
		except Exception as e:
			print('record_d: ' + str(record_d) + ' is of type ' + str(type(record_d)))
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('GET_REPO_EXCEPTION: ' + str(e))
			exit(1)

	if event_type == 'ForkEvent' and isinstance(record_d['forkee'], dict):
		try:
			repo_name = record_d['forkee']['name']
		except KeyError as ke:
			repo_name = None
		except Exception as e:
			print('record_d: ' + str(record_d) + ' is of type ' + str(type(record_d)))
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('GET_REPO_EXCEPTION: ' + str(e))
			exit(1)
		
		try:
			repo_url = record_d['forkee']['url']
				
		except KeyError as ke:
			repo_url = None
		except Exception as e:
			print('record_d: ' + str(record_d) + ' is of type ' + str(type(record_d)))
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('GET_REPO_EXCEPTION: ' + str(e))
			exit(1)
		try:
			created_at = record_d['forkee']['created_at']
				
		except KeyError as ke:
			created_at = created_at
		except Exception as e:
			print('record_d: ' + str(record_d) + ' is of type ' + str(type(record_d)))
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('GET_REPO_EXCEPTION: ' + str(e))
			exit(1)

		try:
			pushed_at = record_d['forkee']['pushed_at']
		except KeyError as ke:
			pushed_at = None
		except Exception as e:
			print('record_d: ' + str(record_d) + ' is of type ' + str(type(record_d)))
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('GET_REPO_EXCEPTION: ' + str(e))
			exit(1)

		try:
			repo_description = record_d['forkee']['description']
		except KeyError as ke:
			repo_description = None
		except Exception as e:
			print('record_d: ' + str(record_d) + ' is of type ' + str(type(record_d)))
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('GET_REPO_EXCEPTION: ' + str(e))
			exit(1)

		try:
			repo_homepage = record_d['forkee']['homepage']
		except KeyError as ke:
			repo_homepage = None
		except Exception as e:
			print('record_d: ' + str(record_d) + ' is of type ' + str(type(record_d)))
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('GET_REPO_EXCEPTION: ' + str(e))
			exit(1)
		

	

		try:
			size = record_d['forkee']['size']
				
		except KeyError as ke:
			#print('GET_REPO_KEYERROR: ' + str(ke))
			size = None
		except Exception as e:
			print('record_d: ' + str(record_d) + ' is of type ' + str(type(record_d)))
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('GET_REPO_EXCEPTION: ' + str(e))
			exit(1)
		
		try:
			language = record_d['forkee']['language']
				
		except KeyError as ke:
			#print('GET_REPO_KEYERROR: ' + str(ke))
			language = None
		except Exception as e:
			print('record_d: ' + str(record_d) + ' is of type ' + str(type(record_d)))
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('GET_REPO_EXCEPTION: ' + str(e))
			exit(1)
		try:
			owner = record_d['forkee']['owne']
				
		except KeyError as ke:
			#print('GET_REPO_KEYERROR: ' + str(ke))
			owner = None
		except Exception as e:
			print('record_d: ' + str(record_d) + ' is of type ' + str(type(record_d)))
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('GET_REPO_EXCEPTION: ' + str(e))
			exit(1)

		
		try:
			is_forked = record_d['forkee']['fork']
				
		except KeyError as ke:
			#print('GET_REPO_KEYERROR: ' + str(ke))
			is_forked = None
		except Exception as e:
			print('record_d: ' + str(record_d) + ' is of type ' + str(type(record_d)))
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('GET_REPO_EXCEPTION: ' + str(e))
			exit(1)
		try:
			id = record_d['forkee']['id']
				
		except KeyError as ke:
			#print('GET_REPO_KEYERROR: ' + str(ke))
			id = None
		except Exception as e:
			print('record_d: ' + str(record_d) + ' is of type ' + str(type(record_d)))
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('GET_REPO_EXCEPTION: ' + str(e))
			exit(1)
		try:
			private = record_d['forkee']['private']
				
		except KeyError as ke:
			#print('GET_REPO_KEYERROR: ' + str(ke))
			private = None
		except Exception as e:
			print('record_d: ' + str(record_d) + ' is of type ' + str(type(record_d)))
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('GET_REPO_EXCEPTION: ' + str(e))
			exit(1)
		
		try:
			has_issues = record_d['forkee']['has_issues']
				
		except KeyError as ke:
			#print('GET_REPO_KEYERROR: ' + str(ke))
			has_issues = None
		except Exception as e:
			print('record_d: ' + str(record_d) + ' is of type ' + str(type(record_d)))
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('GET_REPO_EXCEPTION: ' + str(e))
			exit(1)
		

	

		try:
			has_downloads = record_d['forkee']['has_downloads']
				
		except KeyError as ke:
			#print('GET_REPO_KEYERROR: ' + str(ke))
			has_downloads = None
		except Exception as e:
			print('record_d: ' + str(record_d) + ' is of type ' + str(type(record_d)))
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('GET_REPO_EXCEPTION: ' + str(e))
			exit(1)
		

		try:
			has_wiki = record_d['forkee']['has_wiki']
				
		except KeyError as ke:
			#print('GET_REPO_KEYERROR: ' + str(ke))
			has_wiki = None
		except Exception as e:
			print('record_d: ' + str(record_d) + ' is of type ' + str(type(record_d)))
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('GET_REPO_EXCEPTION: ' + str(e))
			exit(1)

	if '"repository":' in str(record_d):
		try:
			repo_name = record_d['repository']['name']
		except KeyError as ke:
			#print('GET_REPO_KEYERROR: ' + str(ke))
			repo_name = None
		except Exception as e:
			print('record_d: ' + str(record_d) + ' is of type ' + str(type(record_d)))
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('GET_REPO_EXCEPTION: ' + str(e))
			exit(1)
		
		try:
			repo_url = record_d['repository']['url']
		except KeyError as ke:
			#print('GET_REPO_KEYERROR: ' + str(ke))
			repo_url = None
		except Exception as e:
			print('record_d: ' + str(record_d) + ' is of type ' + str(type(record_d)))
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('GET_REPO_EXCEPTION: ' + str(e))
			exit(1)
		try:
			created_at = record_d['repository']['created_at']
				
		except KeyError as ke:
			#print('GET_REPO_KEYERROR: ' + str(ke))
			created_at = created_at
		except Exception as e:
			print('record_d: ' + str(record_d) + ' is of type ' + str(type(record_d)))
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('GET_REPO_EXCEPTION: ' + str(e))
			exit(1)
		try:
			pushed_at = record_d['repository']['pushed_at']
				
		except KeyError as ke:
			#print('GET_REPO_KEYERROR: ' + str(ke))
			pushed_at = None
		except Exception as e:
			print('record_d: ' + str(record_d) + ' is of type ' + str(type(record_d)))
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('GET_REPO_EXCEPTION: ' + str(e))
			exit(1)
		try:
			repo_description = record_d['repository']['description']
				
		except KeyError as ke:
			#print('GET_REPO_KEYERROR: ' + str(ke))
			repo_description = None
		except Exception as e:
			print('record_d: ' + str(record_d) + ' is of type ' + str(type(record_d)))
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('GET_REPO_EXCEPTION: ' + str(e))
			exit(1)

		try:
			repo_homepage = record_d['repository']['homepage']
		except KeyError as ke:
			#print('GET_REPO_KEYERROR: ' + str(ke))
			repo_homepage = None
		except Exception as e:
			print('record_d: ' + str(record_d) + ' is of type ' + str(type(record_d)))
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('GET_REPO_EXCEPTION: ' + str(e))
			exit(1)

		try:
			size = record_d['repository']['size']
		except KeyError as ke:
			size = None
		except Exception as e:
			print('record_d: ' + str(record_d) + ' is of type ' + str(type(record_d)))
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('GET_REPO_EXCEPTION: ' + str(e))
			exit(1)
		
		try:
			language = record_d['repository']['language']
				
		except KeyError as ke:
			language = None
		except Exception as e:
			print('record_d: ' + str(record_d) + ' is of type ' + str(type(record_d)))
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('GET_REPO_EXCEPTION: ' + str(e))
			exit(1)

		try:
			owner = record_d['repository']['owne']
		except KeyError as ke:
			owner = None
		except Exception as e:
			print('record_d: ' + str(record_d) + ' is of type ' + str(type(record_d)))
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('GET_REPO_EXCEPTION: ' + str(e))
			exit(1)

		try:
			is_forked = record_d['repository']['fork']
		except KeyError as ke:
			is_forked = None
		except Exception as e:
			print('record_d: ' + str(record_d) + ' is of type ' + str(type(record_d)))
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('GET_REPO_EXCEPTION: ' + str(e))
			exit(1)

		try:
			id = record_d['repository']['id']
		except KeyError as ke:
			id = None
		except Exception as e:
			print('record_d: ' + str(record_d) + ' is of type ' + str(type(record_d)))
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('GET_REPO_EXCEPTION: ' + str(e))
			exit(1)

		try:
			private = record_d['repository']['private']
				
		except KeyError as ke:
			#print('GET_REPO_KEYERROR: ' + str(ke))
			private = None
		except Exception as e:
			print('record_d: ' + str(record_d) + ' is of type ' + str(type(record_d)))
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('GET_REPO_EXCEPTION: ' + str(e))
			exit(1)
		
		try:
			has_issues = record_d['repository']['has_issues']
		except KeyError as ke:
			has_issues = None
		except Exception as e:
			print('record_d: ' + str(record_d) + ' is of type ' + str(type(record_d)))
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('GET_REPO_EXCEPTION: ' + str(e))
			exit(1)

		try:
			has_downloads = record_d['repository']['has_downloads']
		except KeyError as ke:
			has_downloads = None
		except Exception as e:
			print('record_d: ' + str(record_d) + ' is of type ' + str(type(record_d)))
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('GET_REPO_EXCEPTION: ' + str(e))
			exit(1)

		try:
			has_wiki = record_d['repository']['has_wiki']
		except KeyError as ke:
			has_wiki = None
		except Exception as e:
			print('record_d: ' + str(record_d) + ' is of type ' + str(type(record_d)))
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('GET_REPO_EXCEPTION: ' + str(e))
			exit(1)

	repo_dict = {}
	if repo_name:
		repo_dict['repo_name'] = repo_name
	
	if repo_url:
		repo_dict['repo_url'] = repo_url

	if created_at:
		repo_dict['created_at'] = created_at

	if pushed_at:
		repo_dict['pushed-at'] = pushed_at

	if repo_description:
		repo_dict['repo_description'] = repo_description

	if repo_homepage:
		repo_dict['repo_homepage'] = repo_homepage

	if size:
		repo_dict['size'] = size

	if language:
		repo_dict['language'] = language

	if owner:
		repo_dict['owner'] = owner

	if is_forked:
		repo_dict['is_forked'] = is_forked

	if id:
		repo_dict['id'] = id

	if private:
		repo_dict['private'] = private

	if has_issues:
		repo_dict['has_issues'] = has_issues

	if has_downloads:
		repo_dict['has_downloads'] = has_downloads

	if has_wiki:
		repo_dict['has_wiki'] = has_wiki
  
	# save in the database
	try:
		db.add_data(repo_name, created_at, 'repos', repo_dict)
	except Exception as e:
		print("Failed to save %s repo data at %s: %s" % \
				(repo_name, created_at, str(e)))
		traceback.print_exc()
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)
