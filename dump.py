from inspect import currentframe, getframeinfo
import traceback
from db import Database
import config
import utils
import os
import sys
import json





def write_data(repo_name, value, output_path, type_name):

        if '/' in repo_name:
                user_id, repo_name = repo_name.split('/')
        else:
                repo_name = repo_name
                user_id = None

        # check if user dir exist
        if user_id != None:
                user_dir_path = os.path.join(output_path, user_id)
        else:
                user_dir_path = output_path
        if not os.path.exists(user_dir_path):
                os.mkdir(user_dir_path)

        repo_dir_path = os.path.join(user_dir_path, repo_name)
        if not os.path.exists(repo_dir_path):
                os.mkdir(repo_dir_path)

        completeName = os.path.join(repo_dir_path, type_name + ".json")

	########
        # if file exists, load prev data		
        if os.path.exists(completeName):
                try:
                        with open(completeName, 'r') as f:
                                d = f.read()
                                data = json.loads(d)
                except Exception as e:
                        frameinfo = getframeinfo(currentframe())
                        print(frameinfo.filename, frameinfo.lineno)     
                        print(repr(d))
                        print(sys.exc_info())
                        print(str(e))
                        print('def write_data: Exit')
                        exit(1)

                # update with new data
                try:
                        data[type_name].append(value)
                except KeyError:
                        data[type_name] = [value]
        else:
                data = {
                "repo_name" : repo_name,
                type_name: [
                        value
                ]
                }

        # save updated data
        output_file_data = json.dumps(data)
        with open(completeName, 'w+') as f:
                f.write(output_file_data)




# ##################################################################
# Dump repo schema data from Redis to files
####################################################################
def get_repo_schema(output_path):
	db = Database()

	for repo_fullname in db.get_all_repos():
		repo_data = db.get_repo_or_actor(repo_fullname, 'repo')
		write_data(repo_fullname, repo_data, output_path, 'repos')
	

		# for branch_created_at in db.get_data(repo_fullname, 'branches'):
		# 	#print(branch_created_at)
		# 	val = db.get_value(repo_fullname, 'branches', db, branch_created_at)
		# 	print(val)

		# for tag_created_at in db.get_data(repo_fullname, 'tags'):
		# 	val = db.get_value(repo_fullname, 'tags', db, tag_created_at)
		# 	print(val)

		for release_created_at in db.get_data(repo_fullname, 'releases'):
			val = db.get_value(repo_fullname, 'releases', db, release_created_at)
			write_data(repo_fullname, val, output_path, 'releases')
		
			

	
		for fork_created_at in db.get_data(repo_fullname, 'forks'):
			val = db.get_value(repo_fullname, 'forks', db, fork_created_at)
			write_data(repo_fullname, val, output_path, 'forks')


		for star_created_at in db.get_data(repo_fullname, 'stars'):
			val = db.get_value(repo_fullname, 'stars', db, star_created_at)
			write_data(repo_fullname, val, output_path, 'stars')


		for issue_created_at in db.get_data(repo_fullname, 'issues'):
			val = db.get_value(repo_fullname, 'issues', db, issue_created_at)
			write_data(repo_fullname, val, output_path, 'issues')




		for member in db.get_data(repo_fullname, 'members'):
			write_data(repo_fullname, member, output_path, 'members')


		for commit_created_at in db.get_data(repo_fullname, 'commits'):
			val = db.get_value(repo_fullname, 'commits', db, commit_created_at)
			write_data(repo_fullname, val, output_path, 'commits')







# ##################################################################
# Dump user/org schema data from Redis to files
####################################################################
def get_user_schema(output_path):
	db = Database()
	for actor_login in db.get_all_data_type('user'):
		user_data = db.get_repo_or_actor(actor_login, 'user')
		write_data(actor_login, user_data, output_path, 'users')






def get_org_schema(output_path):
	db = Database()
	for actor_login in db.get_all_data_type('org'):
		org_data =  db.get_repo_or_actor(actor_login, 'org')
		write_data(actor_login, org_data, output_path, 'users')



##################################################################
# Main
##################################################################
if __name__ == "__main__":#
	get_repo_schema('/opt/lucas/red_output')
#	get_user_schema()
#	get_org_schema()
#
	