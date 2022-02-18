import traceback
from inspect import currentframe, getframeinfo
from getters import actors, repos, helpers, name

##########################
# Member Events
##########################

def get_m_dict(json_payload, record_d):
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
	return m_dict
	

def get_MemberEvent(repo_name, created_at, json_payload, record_d, db, member_past_repo_names, members_dict):
	full_repo_name = name.get_full_repo_name(json_payload, record_d, repo_name)
	user_name_string = name.get_actor_login_string(json_payload, record_d, full_repo_name)

	if full_repo_name not in member_past_repo_names:
		members_dict[full_repo_name] = [record_d]
	else:
		members_dict[full_repo_name].append(record_d)
	member_past_repo_names.add(full_repo_name)

	m_dict = get_m_dict(json_payload, record_d)

	# get actor_type
	try:
		if isinstance(record_d['actor'], dict):
			actor_type = helpers.get_actor_type_from_url(record_d['actor']['url'])
		elif isinstance(record_d['url'], str):
			actor_type = helpers.get_actor_type_from_url(record_d['url'])
		else: 
			print('record_d is not a dict and record_d is ' + str(record_d))
	except KeyError as ke:
		print('KEYERROR: ' + ' actor not in record_d ' + str(ke))
	except Exception as e:
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('KEYERROR: ' + print(str(ke)))
		print('record_d: ' + str(record_d))

	actor_type = helpers.get_actor_type_from_url(record_d['actor'])

	# save in the database
	try:
		try:
			# pass
			db.add_member(full_repo_name, m_dict, actor_type)
		except KeyError as ke:
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('KEYERROR: ' + str(ke))
			print('record_d: ' + str(record_d))
		try:
			if isinstance(m_dict, dict):
				actors.get_Actor(full_repo_name, m_dict, record_d, db, created_at)			
			elif isinstance(m_dict, str):
				m_dict = {'login' : m_dict}
				actors.get_Actor(full_repo_name, m_dict, record_d, db, created_at)
			else:
				print('m_dict is not a dict or a str!')
		
		except KeyError as ke:
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('KEYERROR: ' + str(ke))
			print('record_d: ' + str(record_d))
		try:
			actor, actor_dict = helpers.get_actor_and_actor_dict(json_payload, record_d)
			actors.get_Actor(full_repo_name, actor_dict, record_d, db, created_at)

		except KeyError as ke:
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('KEYERROR: ' + str(ke))
			print('record_d: ' + str(record_d))
			# pass

	except Exception as e:
		db.add_member(full_repo_name, m_dict, actor_type)
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('EXCEPTION MEMBEREVENT_EXCEPTION: ' + str(e))
		traceback.print_exc()
		exit(1)



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
		print('EXCEPTION MEMBEREVENT_EXCEPTION: ' + str(e))
		traceback.print_exc()
		exit(1)

	if isinstance(r_dict, dict):
		repos.get_Repo(full_repo_name, created_at, json_payload, record_d, r_dict, db)
	else:
		print('r_dict: ' + str(r_dict))
		print('R_DICT IS NOT A DICT!!!!!!!!!!!!!!!!')

