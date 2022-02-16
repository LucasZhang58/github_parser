import html
from platform import release
import traceback
import json
import os
import sys
from inspect import currentframe, getframeinfo
from getters import persons, repos, orgs
import getters.name as name


def get_user_type_from_url(in_dict):
	if '/users/' in in_dict['url']:
		return 'user'
	elif '/orgs/' in in_dict['url']:
		return 'org'
	else:
		frameinfo = getframeinfo(currentframe())
		print(frameinfo.filename, frameinfo.lineno)
		print('Actor is not a dict!')
		print('in_dict: ' + str(in_dict))