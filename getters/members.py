import html
from platform import release
import traceback
import json
import os
import sys
from inspect import currentframe, getframeinfo
from getters import persons, repos
import getters.name as name

##########################
# Member Events
##########################

def get_MemberEvent(repo_name, created_at, json_payload, record_d, db, member_past_repo_names, members_dict):
	full_repo_name = name.get_full_repo_name(json_payload, record_d, repo_name)

	if full_repo_name not in member_past_repo_names:
		members_dict[full_repo_name] = [record_d]
	else:
		members_dict[full_repo_name].append(record_d)
	member_past_repo_names.add(full_repo_name)



	# save in the database
	try:
		db.add_member(full_repo_name, login, 'members', members_dict[full_repo_name])
	except Exception as e:
		print("Failed to save %s MemberEvent record at %s: %s" % \
				(full_repo_name, created_at, str(e)))
		traceback.print_exc()
	

