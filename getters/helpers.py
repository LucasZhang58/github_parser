##########################
# Helpers
##########################

def get_actor_login_from_url(actor_url):
	actor = None
	if actor_url.startswith('https://api.github.dev/users/') and \
		len(actor_url) > len('https://api.github.dev/users/'):
		actor = actor_url.replace('https://api.github.dev/users/')
	return actor


def get_actor_type_from_url(actor_url):
	if '/users/' in actor_url:
		return 'User'
	elif '/orgs/' in actor_url:
		return 'Organization'
	return None

def get_actor_from_actor_dict(actor_dict):
	actor = None
	if 'login' in actor_dict:
		actor = actor_dict['login']
	elif 'url' in actor_dict:
		actor = get_actor_login_from_url(actor_dict['url'])
	return actor

# gets 'actor_dict', but prioritizes dict over str
def get_actor_and_actor_dict(json_payload, record_d):

	actor_dict = None
	actor = None

	if 'actor' in json_payload:
		if isinstance(json_payload['actor'], str):
			actor = json_payload['actor']
		elif isinstance(json_payload['actor'], dict):
			actor_dict = json_payload['actor']
			actor = get_actor_from_actor_dict(actor_dict)
		else:
			raise Exception("json_payload['actor'] is not a str or dict")

	if 'actor_attributes' in record_d and isinstance(record_d['actor_attributes'], dict):
		new_actor = get_actor_from_actor_dict(record_d['actor_attributes'])
		new_actor_dict = record_d['actor_attributes']
		if not actor and new_actor:
			actor = new_actor 
		if not actor_dict or not isinstance(actor_dict, dict) and new_actor_dict and len(new_actor_dict) > len(actor_dict):
			actor_dict = new_actor_dict
		else:
			raise Exception("EXCEPTION: if 'actor_attributes' in record_d and isinstance(record_d['actor_attributes'], dict):")


	if 'actor_attributes' in json_payload and isinstance(json_payload['actor_attributes'], dict):
		new_actor = get_actor_from_actor_dict(json_payload['actor_attributes'])
		new_actor_dict = json_payload['actor_attributes']
		if not actor and new_actor:
			actor = new_actor 
		if not actor_dict or not isinstance(actor_dict, dict) and new_actor_dict and len(new_actor_dict) > len(actor_dict):
			actor_dict = new_actor_dict
		else:
			raise Exception("EXCEPTION: if 'actor_attributes' in json_payload and isinstance(json_payload['actor_attributes'], dict'")

	if 'actor' in record_d:
		new_actor = None
		new_actor_dict = None
		if isinstance(record_d['actor'], str):
			new_actor = record_d['actor']
		elif isinstance(record_d['actor'], dict):
			new_actor_dict = record_d['actor']
			new_actor = get_actor_from_actor_dict(record_d['actor'])
		else:
			raise Exception("record_d['actor'] is not a str or dict")
		
		if not actor and new_actor:
			actor = new_actor 
		if not actor_dict or not isinstance(actor_dict, dict) and new_actor_dict and len(new_actor_dict) > len(actor_dict):
			actor_dict = new_actor_dict

	if not actor:
		raise Exception("no actor")
	if not actor_dict:
		if actor:
			actor_dict = {'login' : actor}
		else:
			raise Exception("no actor_dict")

	return actor, actor_dict
