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
# Person
##########################

def get_Person(repo_name, created_at, json_payload, record_d, in_dict, db):
	login = None
	id = None
	avatar_url = None
	type = None
	gravatar_id = None
	url = None
	try:
		try:
			login = in_dict['login']
		except KeyError as ke:
			login = None
		try:
			id = in_dict['id']
		except KeyError as ke:
			id = None
		try:
			avatar_url = in_dict['avatar_url']
		except KeyError as ke:
			avatar_url = None
		try:
			type = in_dict['type']
		except KeyError as ke:
			try:
				type = list(in_dict.keys())[0]
			except KeyError as ke:
				type = None
		try:
			gravatar_id = in_dict['gravatar_id']
		except KeyError as ke:
			gravatar_id = None
		try:
			url = in_dict['url']
		except KeyError as ke:
			url = None
	except Exception as e:
		url = None
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('PERSONEVENT_EXCEPTION: ' + str(e))
		traceback.print_exc()
		exit(1)
				
	person_dict = {
		'login' : login,
		'id' : id,
		'avatar_url' : avatar_url,
		'type' : type,
		'gravatar_id' : gravatar_id,
		'url' : url
	}

	user_name_string = name.get_user_name_string(json_payload, record_d)
	# save in the database
	try:
		db.add_user(user_name_string, person_dict)
	except Exception as e:
		print("Failed to save %s person data at %s: %s" % \
				(repo_name, created_at, str(e)))
		traceback.print_exc()
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)

