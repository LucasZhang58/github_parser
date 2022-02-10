import html
from platform import release
import traceback
import json
import os
import sys
from inspect import currentframe, getframeinfo
from getters import persons, repos

##########################
# Release Events
##########################

def get_ReleaseEvent(repo_name, created_at, json_payload, record_d, db):

	# release name
	try:
		tag_name = json_payload['release']['tag_name']
	except KeyError as ke:
		tag_name  = None
	except Exception as e:
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('RELEASEEVENT_EXCEPTION: ' + str(e))
		exit(1)

	# release timestamp
	try:
		released_at = json_payload['release']['created_at']
	except KeyError as ke:
		released_at = None
	except Exception as e:
		released_at = None
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('RELEASEEVENT_EXCEPTION: ' + str(e))
		exit(1)

	# release published date
	try:
		published_at = json_payload['release']['published_at']
	except KeyError as ke:
		published_at = None
	except Exception as e:
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('RELEASEEVENT_EXCEPTION: ' + str(e))
		exit(1)

	# release html url
	try:
		html_url = json_payload['release']['html_url']
	except KeyError as ke:
		html_url = None
	except Exception as e:
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('RELEASEEVENT_EXCEPTION: ' + str(e))
		exit(1)

	# release body
	try:
		body = json_payload['release']['body']
	except KeyError as ke:
		body = None
	except Exception as e:
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('RELEASEEVENT_EXCEPTION: ' + str(e))
		exit(1)

	try:
		author = json_payload['release']['author']['id']
	except KeyError as ke:
		author = None
	except Exception as e:
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('RELEASEEVENT_EXCEPTION: ' + str(e))
		exit(1)

	try:
		assets_in = json_payload['release']['assets']
	except KeyError as ke:
		assets_in = None
	except Exception as e:
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('RELEASEEVENT_EXCEPTION: ' + str(e))
		exit(1)

	# all assets
	assets_out = []
	for asset in assets_in:
		try:
			uploader_id = asset['uploader']['id']
		except KeyError as ke:
			uploader_id = None
		except Exception as e:
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('RELEASEEVENT_EXCEPTION: ' + str(e))
			exit(1)

		try:
			content_type = asset['content_type']
		except KeyError as ke:
			content_type = None
		except Exception as e:
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('RELEASEEVENT_EXCEPTION: ' + str(e))
			exit(1)
				
		try:
			size = asset['size']
		except KeyError as ke:
			size = None
		except Exception as e:
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)	
			print('RELEASEEVENT_EXCEPTION: ' + str(e))
			exit(1)
		
		try:
				download_count = asset['download_count']
		except KeyError as ke:

				download_count = None
		except Exception as e:
				frameinfo = getframeinfo(currentframe())
				print(frameinfo.filename, frameinfo.lineno)	
				print('RELEASEEVENT_EXCEPTION: ' + str(e))
				exit(1)
		
		try:
				asset_created_at = asset['created_at']
		except KeyError as ke:
				asset_created_at = None
		except Exception as e:
				frameinfo = getframeinfo(currentframe())
				print(frameinfo.filename, frameinfo.lineno)	
				print('RELEASEEVENT_EXCEPTION: ' + str(e))
				exit(1)
		
		try:
				updated_at = asset['updated_at']
		except KeyError as ke:
				updated_at = None
		except Exception as e:
				frameinfo = getframeinfo(currentframe())
				print(frameinfo.filename, frameinfo.lineno)	
				print('RELEASEEVENT_EXCEPTION: ' + str(e))
				exit(1)
		
		try:
				browser_download_url = asset['browser_download_url']
		except KeyError as ke:
				browser_download_url = None
		except Exception as e:
				frameinfo = getframeinfo(currentframe())
				print(frameinfo.filename, frameinfo.lineno)	
				print('RELEASEEVENT_EXCEPTION: ' + str(e))
				exit(1)

		asset_out = {'asset_created_at' : asset_created_at}
		if uploader_id:
			asset_out['uploader_id'] = uploader_id

		if content_type:
			asset_out['content_type'] = content_type

		if size:
			asset_out['size'] = size

		if download_count:
			asset_out['download_count'] = download_count

		if updated_at:
			asset_out['updated_at'] = updated_at

		if browser_download_url:
			asset_out['browser_download_url'] = browser_download_url

		assets_out.append(asset_out)

	try:
		prerelease = json_payload['release']['prerelease']
	except KeyError as ke:
		browser_download_url = None
	except Exception as e:
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('RELEASEEVENT_EXCEPTION: ' + str(e))
		exit(1)

	try:
		draft = json_payload['release']['draft']
	except KeyError as ke:
		browser_download_url = None
	except Exception as e:
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('RELEASEEVENT_EXCEPTION: ' + str(e))
		exit(1)

	try:
		target_commitish = json_payload['release']['target_commitish']
	except KeyError as ke:
		target_commitish = None
	except Exception as e:
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		print('RELEASEEVENT_EXCEPTION: ' + str(e))
		exit(1)
	
	releases_dict = {'created_at' : created_at}

	if released_at:
		releases_dict['released_at'] = released_at

	if tag_name:
		releases_dict['tag_name'] = tag_name

	if published_at:
		releases_dict['published_at'] = published_at

	if html_url:
		releases_dict['html_url'] = html_url

	if body:
		releases_dict['body'] = body

	if author:
		releases_dict['author'] = author

	if assets_out:
		releases_dict['assets'] = assets_out

	if prerelease:
		releases_dict['prerelease'] = prerelease

	if draft:
		releases_dict['draft'] = draft

	if target_commitish:
		releases_dict['target_commitish'] = target_commitish

	# save in the database		
	try:
		db.add_data(repo_name, created_at, 'releases', releases_dict)
	except Exception as e:
		traceback.print_exc()
		print("Failed to save %s ReleaseEvent record at %s: %s" % (repo_name, created_at, str(e)))

	event_type = 'ReleaseEvent'
	# repos.get_Repo(repo_name, created_at, json_payload, record_d, db, event_type)
	# persons.get_Person(repo_name, created_at, json_payload, record_d, db, event_type)
