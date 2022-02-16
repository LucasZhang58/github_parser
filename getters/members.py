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
	user_name_string = name.get_user_name_string(json_payload, record_d, full_repo_name)

	if full_repo_name not in member_past_repo_names:
		members_dict[full_repo_name] = [record_d]
	else:
		members_dict[full_repo_name].append(record_d)
	member_past_repo_names.add(full_repo_name)

	try:
		m_dict = record_d['member']
	except KeyError as ke:
		m_dict = json_payload['member']
	except Exception as e:
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('No member dict in this MEMBEREVENT record')
		print('KEYERROR MEMBEREVENT_EXCEPTION: ' + str(e))
		traceback.print_exc()
		exit(1)



	# # save in the database
	# try:
	# 	db.add_member(full_repo_name, m_dict)
	# 	try:
	# 		if m_dict['type'] == 'User':
	# 			persons.get_Person(full_repo_name, created_at, json_payload, record_d, m_dict, db)
	# except Exception as e:
	# 	db.add_member(full_repo_name, m_dict)
	# 	print('record_d: ' + str(record_d))
	# 	print("Failed to save %s MemberEvent record at %s: %s" % \
	# 			(full_repo_name, created_at, str(e)))
	# 	traceback.print_exc()




	# check for repo and actor_attributes in a record
	if '"repo":' in str(record_d) and '"repository":' in str(record_d):
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('REPO_and_REPOSITORY_in_the_same_record_EXCEPTION: ' + str(e))
		exit(1)

	#Call the get_Repo() function
	try:
		r_dict = record_d['repo']
	except KeyError as ke:
		try:
			r_dict = record_d['repository']
		except KeyError as ke:
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('KEYERROR MEMBEREVENT_EXCEPTION: ' + str(ke))
			exit(1)

	except Exception as e:
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('KEYERROR MEMBEREVENT_EXCEPTION: ' + str(e))
		traceback.print_exc()
		exit(1)

	if isinstance(r_dict, dict):
		repos.get_Repo(full_repo_name, created_at, json_payload, record_d, r_dict, db)
	else:
		print('r_dict: ' + str(r_dict))
		print('R_DICT IS NOT A DICT!!!!!!!!!!!!!!!!')






	#If memeber is of type user,call the get_Person function

	try:

		try:
			if isinstance(record_d['actor_attributes'], dict):
				p_dict = record_d['actor_attributes']
				persons.get_Person(full_repo_name, created_at, json_payload, record_d, p_dict, db)
			else:
				print("record_d: " + str(record_d))
				print("HAVEN'T FOUND P_DICT")
		except KeyError as ke:
			if isinstance(json_payload[record_d['actor_attributes']], dict):
				p_dict = json_payload[record_d['actor_attributes']]
				persons.get_Person(full_repo_name, created_at, json_payload, record_d, p_dict, db)
			else:
				print("json_payload: " + str(json_payload))
				print("HAVEN'T FOUND P_DICT")
			try:
				if isinstance(record_d['actor'], dict):
					p_dict = record_d['actor']
					persons.get_Person(full_repo_name, created_at, json_payload, record_d, p_dict, db)
				else:
					print("record_d: " + str(record_d))
					print("HAVEN'T FOUND P_DICT")
			except KeyError as ke:
				try:
					if isinstance(json_payload['actor'], dict):
						p_dict = json_payload['actor']
						persons.get_Person(full_repo_name, created_at, json_payload, record_d, p_dict, db)
					else:
						print("json_payload: " + str(json_payload))
						print("HAVEN'T FOUND P_DICT")

				except KeyError as ke:
					pass
	except KeyError as ke:
		pass

	except Exception as e:
		pass
