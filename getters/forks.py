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
import getters.name as name

##########################
# Fork Events
##########################
def get_repo_from_forkee(forkee):

	if 'name' in forkee:
		forked_repo_name = forkee['name']
		if '/' in forked_repo_name:
			return forked_repo_name

	if 'url' in forkee:
		fork_url = forkee['url']
		return name.url_to_name(fork_url)

	raise Exception("'/' is not in forked_repo_name, and 'url' is not in record_d['forkee']")	

def use_full_repo_name(json_payload, record_d, repo_name):
	user_name_string , repo_name_string = (name.get_full_repo_name(json_payload, record_d, repo_name)).split('/')

	if 'actor' in json_payload:
		if isinstance(json_payload['actor'], str):
			return json_payload['actor'] + '/' + repo_name_string
		elif isinstance(json_payload['actor'], dict):
			return json_payload['actor']['login'] + '/' + repo_name_string
		print('record_d: ' + str(record_d) + ' is of type ' + str(type(record_d)))
		raise Exception("'actor' is in json_payload, but is not a string")

	if 'actor' in record_d:
		if isinstance(record_d['actor'], str):
			return record_d['actor'] + '/' + repo_name_string
		elif isinstance(record_d['actor'], dict):
			return record_d['actor']['login'] + '/' + repo_name_string
		print('record_d: ' + str(record_d) + ' is of type ' + str(type(record_d)))
		raise Exception("'actor' is in record_d, but is not a string")

	raise Exception("'forkee' not in record_d or json_payload")

def parse_forkee(forkee, json_payload, record_d, repo_name):
	if isinstance(forkee, dict):
		return get_repo_from_forkee(forkee)
	elif isinstance(forkee, int):
		return use_full_repo_name(json_payload, record_d, repo_name)
		#raise Exception("'forkee' is of type int!")
	else:
		raise Exception("'forkee' is not a dict or int!")	

def get_forked_repo_name(json_payload, record_d, repo_name):
	try:
		if 'forkee' in record_d:
			return parse_forkee(record_d['forkee'], json_payload, record_d, repo_name)
		elif 'forkee' in json_payload:
			return parse_forkee(json_payload['forkee'], json_payload, record_d, repo_name)
		else:
			return use_full_repo_name(json_payload, record_d, repo_name)
	except Exception as e:
		print('record_d: ' + str(record_d))
		traceback.print_exc()
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('ERROR get_forked_repo_name() EXCEPTION: ' + str(e))
		exit(1)
		
def get_ForkEvent(repo_name, created_at, json_payload, record_d, db):
	forkee_actor_name = None
	forked_at = None
	forked_repo_name = None
	forked_repo_id = None
	size = None

	try:
		try:
			if isinstance(json_payload['forkee'], str): 
				forkee_actor_name = json_payload['actor']

			elif isinstance(json_payload['actor'], dict):
				forkee_actor_name = json_payload['actor']['login']

			elif isinstance(record_d['actor'], dict):
				forkee_actor_name = record_d['actor']['login']
			else:
				raise Exception("if forkee is in json_payload, forkee is not a str. If actor is in record_d, record_d['actor'] isn't  a dict. If 'actor' is in record_d, record_d['actor'] is not a dict")

		except KeyError as ke:
			try:
				if isinstance(record_d['actor'], str):
					forkee_actor_name = record_d['actor']
			except KeyError as ke:
				raise Exception('KEYERROR: forkee actor name not found')

		# fork timestamp
		try:
			forked_at = record_d['created_at']
		except KeyError as ke:
			try:
				if isinstance(json_payload['forkee'], int):
					forked_at = created_at
				elif isinstance(json_payload['forkee'], dict):
					forked_at = json_payload['forkee']['created_at']
				else:
					forked_at = created_at
			except KeyError as ke:
				forked_at = created_at

		# name of the repo that will be forked
		forked_repo_name = get_forked_repo_name(json_payload, record_d, repo_name)

		# ID of the repo that will be forked
		try:
			forked_repo_id = record_d['repo']['id']
		except KeyError as ke:
			try:
				forked_repo_id = record_d['repository']['id']
			except KeyError as ke:
				forked_repo_id = None

		# size of the repo that will be forked
		try:
			size = record_d['repository']['size']
		except KeyError as ke:
			try:
				if isinstance(json_payload['forkee'], dict):
					size = json_payload['forkee']['size']
				else:
					size = None
			except KeyError as ke:
				size = None

	except Exception as e:
		print('record: ' + str(record_d))
		print('FORKEVENT_EXCEPTION: ' + str(e))
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		traceback.print_exc()
		exit(1)
 
	forks_dict = {}

	if forkee_actor_name:
		forks_dict['forkee_actor_name'] = forkee_actor_name

	if forked_at:
		forks_dict['forked_at'] = forked_at

	if forked_repo_name:
		forks_dict['forked_repo_name'] = forked_repo_name

	if forked_repo_id:
		forks_dict['forked_repo_id'] = forked_repo_id

	if size:
		forks_dict['size'] = size

	full_repo_name = name.get_full_repo_name(json_payload, record_d, repo_name)
	if not full_repo_name:
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('full_repo_name is None')
		exit(1)
   
	# save in the database
	try:
		db.add_data(full_repo_name, created_at, 'forks', forks_dict)
	except Exception as e:
		print("Failed to save %s ForkEvent record at %s: %s" % \
				(full_repo_name, created_at, str(e)))
		traceback.print_exc()
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)

	# check for repo and repository in a record
	if 'repo' in record_d and 'repository' in record_d:
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('REPO_and_REPOSITORY_in_the_same_record_EXCEPTION: ' + str(e))
		exit(1)

	try:
		r_dict = record_d['forkee']

	except KeyError as ke:
		try:
			r_dict = json_payload['forkee']
		except KeyError as ke:
			try:
				r_dict = record_d['repository']
			except KeyError as ke:
				r_dict = record_d['repo']
	except Exception as e:
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('FORKEVENT_EXCEPTION: ' + str(e))
		traceback.print_exc()
		exit(1)

	if isinstance(r_dict, dict):
		repos.get_Repo(full_repo_name, created_at, json_payload, record_d, r_dict, db)

	# get the person who is forking the repo
	try:
		if 'forkee' in record_d:
			if isinstance(record_d['forkee'], dict):
				p_dict = record_d['forkee']['owner']
			elif isinstance(record_d['forkee'], int):
				# 'forkee' is the ID of the repo being created, no info here
				return
			else:
				raise Exception("'forkee' of type %s" % (type(record_d['forkee'])))

		elif 'actor_attributes' in record_d:
			if isinstance(record_d['actor_attributes'], dict):
				p_dict = record_d['actor_attributes']
			else:
				raise Exception("'actor_attributes' of type %s" % (type(record_d['actor_attributes'])))

		elif 'actor' in record_d:
			p_dict = record_d['actor']

			if isinstance(record_d['actor'], dict):
				p_dict = record_d['actor']
			elif isinstance(record_d['actor'], str):
				p_dict = {
					'login'	: record_d['actor'],
				}
			else:
				raise Exception("'actor' of type %s" % (type(record_d['actor'])))
		else:
			raise Exception("No person info in record_d: %s" % (record_d))

	except Exception as e:
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('ERROR FORKEVENT_EXCEPTION: ' + str(e))
		traceback.print_exc()
		exit(1)

	# add to the db
	persons.get_Person(full_repo_name, created_at, json_payload, record_d, p_dict, db)
