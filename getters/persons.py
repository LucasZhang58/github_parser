import html
from platform import release
import traceback
import json
import os
import sys
from inspect import currentframe, getframeinfo
from getters import persons, repos

##########################
# Person
##########################

def get_Person(repo_name, created_at, json_payload, record_d, db, event_type):
	login = None
	id = None
	avatar_url = None
	type = None
	gravatar_id = None
	url = None

	# RELEASE EVENT
	if event_type == 'ReleaseEvent':
		try:
			login = json_payload['release']['author']['login']
		except KeyError as ke:
			#print(str(ke))
			login = None
		except Exception as e:

			login = None
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('PERSONEVENT_EXCEPTION: ' + str(e))
			exit(1)

		try:
			id = json_payload['release']['author']['id']
		except KeyError as ke:
			#print(str(ke))
			id = None
		except Exception as e:
			id = None
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('PERSONEVENT_EXCEPTION: ' + str(e))
			exit(1)

		try:
			avatar_url = json_payload['release']['author']['avatar_url']
		except KeyError as ke:
			#print(str(ke))
			avatar_url = None
		except Exception as e:
			print(str(e))
			avatar_url = None
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('PERSONEVENT_EXCEPTION: ' + str(e))
			exit(1)
			
		type = 'author'

		try:
			gravatar_id = json_payload['release']['author']['gravatar_id']
		except KeyError as ke:
			#print(str(ke))
			gravatar_id = None
		except Exception as e:
			gravatar_id = None
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('PERSONEVENT_EXCEPTION: ' + str(e))
			exit(1)
			
		try:
			url = json_payload['release']['author']['url']
		except KeyError as ke:
			#print(str(ke))
			url = None
		except Exception as e:
			url = None
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('PERSONEVENT_EXCEPTION: ' + str(e))
			exit(1)
			
	# FORK EVENT
	if event_type == 'ForkEvent' and isinstance(record_d['forkee'], dict):
		try:
			login = json_payload['forkee']['owner']['login']
		except KeyError as ke:
			#print(str(ke))
			login = None
		except Exception as e:
			login = None
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('PERSONEVENT_EXCEPTION: ' + str(e))
			exit(1)

		try:
			id = json_payload['forkee']['owner']['id']
		except KeyError as ke:
			#print(str(ke))
			id = None
		except Exception as e:
			id = None
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('PERSONEVENT_EXCEPTION: ' + str(e))
			exit(1)

		try:
			avatar_url = json_payload['forkee']['owner']['avatar_url']
		except KeyError as ke:
			#print(str(ke))
			avatar_url = None
		except Exception as e:
			avatar_url = None
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('PERSONEVENT_EXCEPTION: ' + str(e))
			exit(1)
			
		type = 'owner'

			
		try:
			gravatar_id = json_payload['forkee']['owner']['gravatar_id']
		except KeyError as ke:
			#print(str(ke))
			gravatar_id = None
		except Exception as e:
			gravatar_id = None
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('PERSONEVENT_EXCEPTION: ' + str(e))
			exit(1)
			
		try:
			url = json_payload['forkee']['owner']['url']
		except KeyError as ke:
			#print(str(ke))
			url = None
		except Exception as e:
			url = None
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('PERSONEVENT_EXCEPTION: ' + str(e))
			exit(1)

		# MEMBER EVENT
		if event_type == 'MemberEvent':
			try:
				login = json_payload['member']['login']
			except KeyError as ke:
				#print(str(ke))
				login = None
			except Exception as e:
				login = None
				frameinfo = getframeinfo(currentframe())
				print(frameinfo.filename, frameinfo.lineno)	
				print('PERSONEVENT_EXCEPTION: ' + str(e))
				exit(1)

			try:
				id = json_payload['member']['id']
			except KeyError as ke:
				#print(str(ke))
				id = None
			except Exception as e:
				id = None
				frameinfo = getframeinfo(currentframe())
				print(frameinfo.filename, frameinfo.lineno)	
				print('PERSONEVENT_EXCEPTION: ' + str(e))
				exit(1)

			try:
				avatar_url = json_payload['member']['avatar_url']
			except KeyError as ke:
				#print(str(ke))
				avatar_url = None
			except Exception as e:
				avatar_url = None
				frameinfo = getframeinfo(currentframe())
				print(frameinfo.filename, frameinfo.lineno)	
				print('PERSONEVENT_EXCEPTION: ' + str(e))
				exit(1)
				
			type = 'member'

				
			try:
				gravatar_id = json_payload['member']['gravatar_id']
			except KeyError as ke:
				#print(str(ke))
				gravatar_id = None
			except Exception as e:
				gravatar_id = None
				frameinfo = getframeinfo(currentframe())
				print(frameinfo.filename, frameinfo.lineno)	
				print('PERSONEVENT_EXCEPTION: ' + str(e))
				exit(1)
				
			try:
				url = json_payload['member']['url']
			except KeyError as ke:
				#print(str(ke))
				url = None
			except Exception as e:
				url = None
				frameinfo = getframeinfo(currentframe())
				print(frameinfo.filename, frameinfo.lineno)	
				print('PERSONEVENT_EXCEPTION: ' + str(e))
				exit(1)

		# ISSUE EVENT
		if event_type == 'IssuesEvent':
			if isinstance(json_payload['issue'], dict):
				try:
					login = json_payload['issue']['user']['login']
				except KeyError as ke:
					#print(str(ke))
					login = None
				except Exception as e:
					login = None
					frameinfo = getframeinfo(currentframe())
					print(frameinfo.filename, frameinfo.lineno)	
					print('PERSONEVENT_EXCEPTION: ' + str(e))
					exit(1)

				try:
					id = json_payload['issue']['user']['id']
				except KeyError as ke:
					#print(str(ke))
					id = None
				except Exception as e:
					id = None
					frameinfo = getframeinfo(currentframe())
					print(frameinfo.filename, frameinfo.lineno)	
					print('PERSONEVENT_EXCEPTION: ' + str(e))
					exit(1)

				try:
					avatar_url = json_payload['issue']['user']['avatar_url']
				except KeyError as ke:
					#print(str(ke))
					avatar_url = None
				except Exception as e:
					avatar_url = None
					frameinfo = getframeinfo(currentframe())
					print(frameinfo.filename, frameinfo.lineno)	
					print('PERSONEVENT_EXCEPTION: ' + str(e))
					exit(1)
					
				type = 'user'

					
				try:
					gravatar_id = json_payload['issue']['user']['gravatar_id']
				except KeyError as ke:
					#print(str(ke))
					gravatar_id = None
				except Exception as e:
					gravatar_id = None
					frameinfo = getframeinfo(currentframe())
					print(frameinfo.filename, frameinfo.lineno)	
					print('PERSONEVENT_EXCEPTION: ' + str(e))
					exit(1)
					
				try:
					url = json_payload['issue']['user']['url']
				except KeyError as ke:
					#print(str(ke))
					url = None
				except Exception as e:
					url = None
					frameinfo = getframeinfo(currentframe())
					print(frameinfo.filename, frameinfo.lineno)	
					print('PERSONEVENT_EXCEPTION: ' + str(e))
					exit(1)
			else:
				return
					
			person_dict = {
				'login' : login,
				'id' : id,
				'avatar_url' : avatar_url,
				'type' : type,
				'gravatar_id' : gravatar_id,
				'url' : url
			}

	# save in the database
	try:
		db.add_data(repo_name, created_at, 'person', person_dict)
	except Exception as e:
		print("Failed to save %s person data at %s: %s" % \
				(repo_name, created_at, str(e)))
		traceback.print_exc()
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)

