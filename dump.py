from inspect import currentframe, getframeinfo
import traceback
from db import Database
import config
import utils
import os
import sys




# ##################################################################
# Dump repo schema data from Redis to files
####################################################################
def get_repo_schema():
	db = Database()

	for repo_fullname in db.get_all_repos():
		repo_data = db.get_repo(repo_fullname)
		# print(repo_data)
		print(repo_fullname)
		repo_data[repo_fullname] = {}
		curr_dict = {repo_data : {}}

		for branch_created_at in db.get_data(repo_fullname, 'branches'):
			val = db.get_value(repo_fullname, 'branches', db, branch_created_at)
			print(val)

		for tag_created_at in db.get_data(repo_fullname, 'tags'):
			val = db.get_value(repo_fullname, 'tags', db, tag_created_at)
			print(val)

		for release_created_at in db.get_data(repo_fullname, 'releases'):
			val = db.get_value(repo_fullname, 'releases', db, release_created_at)
			print(val)


		for fork_created_at in db.get_data(repo_fullname, 'forks'):
			val = db.get_value(repo_fullname, 'forks', db, fork_created_at)
			print(val)


		for star_created_at in db.get_data(repo_fullname, 'stars'):
			val = db.get_value(repo_fullname, 'stars', db, star_created_at)
			repo_data[repo_fullname] = val
			print(val)

		for issue_created_at in db.get_data(repo_fullname, 'issues'):
			val = db.get_value(repo_fullname, 'issues', db, issue_created_at)
			repo_data[repo_fullname] = val
			print(val)



		for member_created_at in db.get_data(repo_fullname, 'members'):
			val = db.get_value(repo_fullname, 'members', db, member_created_at)
			repo_data[repo_fullname] = val
			print(val)

		for commit_created_at in db.get_data(repo_fullname, 'commits'):
			val = db.get_value(repo_fullname, 'commits', db, commit_created_at)
			repo_data[repo_fullname] = val
			print(val)



		print('####################################################################')


# ##################################################################
# Dump user/org schema data from Redis to files
####################################################################
def get_actor_schema():
	db = Database()
	for actor_login in db.get_all_actors():
		for user_created_at in db.get_data(actor_login, 'user'):
			val = db.get_value(actor_login, 'user', db, user_created_at)
			print(val)

		for org_created_at in db.get_data(actor_login, 'org'):
			val = db.get_value(actor_login, 'org', db, org_created_at)
			print(val)


