import html
from http.client import InvalidURL
from platform import release
import traceback
import json
import os
import sys
from inspect import currentframe, getframeinfo
import getters.name as name

##########################
# REPO
##########################
def get_Repo(repo_name, created_at, json_payload, record_d, in_dict, db):
	repo_name = None
	repo_url = None
	repo_created_at = None
	repo_description = None
	repo_homepage = None
	size = None
	language = None
	owner = None
	is_forked = None
	try:
		try:
			repo_name = in_dict['name']
		except KeyError as ke:
			repo_name = None

		try:
			repo_url = in_dict['url']
		except KeyError as ke:
			repo_url = None

		try:
			repo_created_at = in_dict['created_at']
		except KeyError as ke:
			repo_created_at = None

		try:
			pushed_at = in_dict['pushed_at']
		except KeyError as ke:
			pushed_at = None

		try:
			repo_description = in_dict['description']
		except KeyError as ke:
			repo_description = None

		try:
			repo_homepage = in_dict['homepage']
		except KeyError as ke:
			repo_homepage = None

		try:
			size = in_dict['size']
		except KeyError as ke:
			size = None

		try:
			language = in_dict['language']
		except KeyError as ke:
			language = None

		try:
			if isinstance(in_dict['owner'], dict):
				owner = in_dict['owner']['login']
			else:
				raise KeyError
		except KeyError as ke:
			owner = None

		try:
			is_forked = in_dict['fork']
		except KeyError as ke:
			is_forked = None

		try:
			id = in_dict['id']
		except KeyError as ke:
			id = None

		try:
			private = in_dict['private']
		except KeyError as ke:
			private = None

		try:
			has_issues = in_dict['has_issues']
		except KeyError as ke:
			has_issues = None

		try:
			has_downloads = in_dict['has_downloads']
		except KeyError as ke:
			has_downloads = None

		try:
			has_wiki = in_dict['has_wiki']
		except KeyError as ke:
			has_wiki = None
	except Exception as e:
		print('record_d: ' + str(record_d) + ' is of type ' + str(type(record_d)))
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)		
		print('GET_REPO_EXCEPTION: ' + str(e))
		exit(1)

	if repo_url == None:
		return

	repo_dict = {}
	if repo_name:
		repo_dict['repo_name'] = repo_name	

	if repo_url:
		repo_dict['repo_url'] = repo_url 

	if repo_created_at:
		repo_dict['repo_created_at'] = repo_created_at

	if pushed_at:
		repo_dict['pushed_at'] = pushed_at			 

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

	if 'repo' in record_d and 'repository' in record_d:
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('REPO_and_REPOSITORY_in_the_same_record_EXCEPTION')
		exit(1)

	full_repo_name = name.get_full_repo_name(json_payload, record_d, repo_name)		   
	if not full_repo_name:
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('full_repo_name is None')
		exit(1)

	# save in the database
	try:
		db.add_repo(full_repo_name, repo_dict)
	except Exception as e:
		print("Failed to save %s repo data at %s: %s" % \
				(repo_name, created_at, str(e)))
		traceback.print_exc()
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)
