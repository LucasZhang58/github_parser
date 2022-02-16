from inspect import currentframe, getframeinfo
import traceback

from getters import helpers

##########################
# Actor (User or Organization)
##########################

def get_Actor(full_repo_name, actor_dict, record_d, db):
	try:

		# String ID
		try:
			actor_login = actor_dict['login']
		except KeyError:
			if 'url' in actor_dict:
				actor_login = helpers.get_actor_login_from_url(actor_dict['url'])

		# validation: absolutely mandatory field
		if not actor_login:
			#raise Exception("Actor ('login') info not available!")
			return

		# Type: can be either 'User' or 'Organization'
		try:
			actor_type = actor_dict['type']
		except KeyError:
			try:
				actor_type = helpers.get_actor_type_from_url(actor_dict['url'])
			except KeyError as ke:
				actor_type = 'User'
				#print(record_d)

		# validation
		if actor_type == "User":
			actor_type = "user"
		elif actor_type == "Organization":
			actor_type = "org"
		else:
			raise Exception("Invalid actor_type: %s" % (actor_type))

		# Integer ID
		try:
			actor_id = actor_dict['id']
		except KeyError:
			actor_id = None

		# Name
		try:
			actor_name = actor_dict['name']
		except KeyError:
			actor_name = None

		# Email
		try:
			actor_email = actor_dict['email']
		except KeyError:
			actor_email = None

		# Company
		try:
			actor_company = actor_dict['company']
		except KeyError:
			actor_company = None

		# Location
		try:
			actor_location = actor_dict['location']
		except KeyError:
			actor_location = None

		# Avatar URL
		try:
			avatar_url = actor_dict['avatar_url']
		except KeyError:
			avatar_url = None

		# Gravatar ID
		try:
			gravatar_id = actor_dict['gravatar_id']
		except KeyError:
			gravatar_id = None

		# URL
		try:
			actor_url = actor_dict['url']
		except KeyError:
			actor_url = None

		# Blog
		try:
			actor_blog = actor_dict['blog']
		except KeyError:
			actor_blog = None

	except Exception as e:
		print("Error: %s\n%s\n%s" % (str(e), actor_dict, record_d))
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)	
		traceback.print_exc()
		exit(1)

	# construct output dict			
	actor_dict = {
		'login'	: actor_login,
	}
	if actor_type:
		actor_dict['type'] = actor_type,
	if actor_id:
		actor_dict['id'] =  actor_id
	if avatar_url:
		actor_dict['avatar_url'] = avatar_url
	if gravatar_id:
		actor_dict['gravatar_id'] = gravatar_id
	if actor_url:
		actor_dict['url'] = actor_url
	if actor_company:
		actor_dict['company'] = actor_company
	if actor_blog:
		actor_dict['blog'] = actor_blog
	if actor_name:
		actor_dict['name'] = actor_name
	if actor_location:
		actor_dict['location'] = actor_location
	if actor_email:
		actor_dict['email'] = actor_email

	# save in the database
	try:
		db.add_actor(actor_login, actor_type, actor_dict)
	except Exception as e:
		print("Failed to save %s actor data at %s: %s" % \
				(full_repo_name, created_at, str(e)))
		traceback.print_exc()
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)
		exit(1)
