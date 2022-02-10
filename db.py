from lib2to3.pytree import convert
import os
from pydoc import cram
import time
import redis
from inspect import currentframe, getframeinfo
import traceback

class Database:

	##################################################################
	# Init
	##################################################################
	def __init__(self):
		try:
			self.__r = redis.StrictRedis()
		except Exception as e:
			raise Exception("Error initializing Redis: %s" % (str(e)))

	##################################################################
	# Memory used
	##################################################################
	def memused(self):
		assert self.__r, "Failed to get DB memused: DB not setup"
		try:
			return self.__r.info()['used_memory']
		except Exception as e:
			raise Exception("Error dumping memory info: %s" % (str(e)))

	##################################################################
	# Database size
	##################################################################
	def size(self):
		assert self.__r, "Failed to get DB size: DB not setup"
		try:
			return self.__r.dbsize()
		except Exception as e:
			raise Exception("Error dumping index size: %s" % (str(e)))

	##################################################################
	# convert None to ''
	##################################################################
	def convert_none_to_empty(self, data_dict):
		converted_data = {}
		for k, v in data_dict.items():
			if v == None:
				v = ''
			else:
				v = str(v)
			converted_data[k] = v
		return converted_data

	##################################################################
	# Add GitHub user data
	##################################################################
	def add_user(self, user_id, data_dict):
		try:
			key = 'user%' + user_id
			converted_data = self.convert_none_to_empty(data_dict)
			self.__r.hmset(key, converted_data)
		except Exception as e:
			print('ERROR: ' + str(e))
			traceback.print_exc()
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)
			exit(1)

	##################################################################
	# Add GitHub repo data
	##################################################################
	def add_repo(self, repo_id, data_dict):
		try:
			# NOTE: @repo_id is full repo name
			if '/' not in repo_id:
				# example: 'foo/bar' where @foo is the GitHub user and @bar is the repo name
				raise Exception('db.add_repo accepts full repo name (e.g., foo/bar)')

			key = 'repo%' + repo_id
			converted_data = self.convert_none_to_empty(data_dict)
			self.__r.hmset(key, converted_data)
		except Exception as e:
			print('ERROR: ' + str(e))
			traceback.print_exc()
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)
			exit(1)

	##################################################################
	# Add event data for a repo
	##################################################################
	def add_data(self, repo_id, created_at, data_type, data_dict):
		try:
			# NOTE: @repo_id is full repo name
			if '/' not in repo_id:
				# example: 'foo/bar' where @foo is the GitHub user and @bar is the repo name
				raise Exception('db.add_repo accepts full repo name (e.g., foo/bar)')

			converted_data = self.convert_none_to_empty(data_dict)
			key = repo_id + '%' + data_type + '%' + created_at
			self.__r.hmset(key, converted_data)
			key = repo_id + '%' + data_type
			self.__r.sadd(key, created_at)
		except Exception as e:
			print('ERROR: ' + str(e))
			traceback.print_exc()
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)
			exit(1)

##################################################################
# unit test
##################################################################
def test():
	db = Database()
	size = db.size()
	print(size)

##################################################################
# Main
##################################################################
if __name__ == "__main__":
	test()
