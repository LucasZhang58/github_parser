from lib2to3.pytree import convert
import os
from pydoc import cram
import time
from inspect import currentframe, getframeinfo
import traceback

class Database:

	##################################################################
	# Init
	##################################################################
	def __init__(self):
		try:
			import config
			cfg = config.Config()
			db_type = cfg.get('Type', 'DB')
			if db_type == "redis":
				import redis
				self.__host = cfg.get("HOST", "Redis")
				self.__port = cfg.get("PORT", "Redis")
				self.__db = cfg.get("DATABASE", 0)
				self.__rc = redis.StrictRedis(host=self.__host, port=self.__port, db=self.__db)
			elif db_type == "rediscluster":
				import json
				from rediscluster import StrictRedisCluster
				nodes = json.loads(cfg.get("NODES", "RedisCluster"))
				self.__rc = StrictRedisCluster(startup_nodes=nodes, decode_responses=True, readonly_mode=readonly)

		except Exception as e:
			raise Exception("Error initializing Redis: %s" % (str(e)))

	##################################################################
	# Memory used
	##################################################################
	def memused(self):
		assert self.__rc, "Failed to get DB memused: DB not setup"
		try:
			return self.__rc.info()['used_memory']
		except Exception as e:
			raise Exception("Error dumping memory info: %s" % (str(e)))

	##################################################################
	# Database size
	##################################################################
	def size(self):
		assert self.__rc, "Failed to get DB size: DB not setup"
		try:
			return self.__rc.dbsize()
		except Exception as e:
			raise Exception("Error dumping index size: %s" % (str(e)))

	##################################################################
	# Batching
	##################################################################
	# iterate a list in batches of size n
	# source: https://stackoverflow.com/questions/22255589/get-all-keys-in-redis-database-with-python
	def __batcher(self, iterable, n):
		try:
			# Python 3
			from itertools import zip_longest
		except ImportError:
			# Python 2
			from itertools import izip_longest as zip_longest
		args = [iter(iterable)] * n
		return zip_longest(*args)

	# in batches of 500
	def __get_matching_batches(self, key_pattern, batch_size=500):
		return self.__batcher(self.__rc.scan_iter(key_pattern), batch_size)

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
	def add_user(self, user_name_string, data_dict):
		try:
			key = 'user%' + user_name_string
			# print('key: ' + str(key))
			# print('data_dict: ' + str(data_dict))
			converted_data = self.convert_none_to_empty(data_dict)
			self.__rc.hmset(key, converted_data)
		except Exception as e:
			print('ERROR: ' + str(e))
			traceback.print_exc()
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)
			exit(1)

	##################################################################
	# Get all repos
	##################################################################
	def get_repos(self):
		try:
			key_pattern = 'repo%*'

			for batch in self.__get_matching_batches(key_pattern):
				for idx, val in utils.for_each_item_int(list(batch)):
					print(val)
		except Exception as e:
			raise Exception("Failed to get all repos from DB: %s!" % (str(e)))
		
	##################################################################
	# Add GitHub repo data
	##################################################################
	def add_repo(self, repo_fullname, data_dict):
		try:
			# NOTE: @repo_id is full repo name
			if '/' not in repo_fullname:
				# example: 'foo/bar' where @foo is the GitHub user and @bar is the repo name
				raise Exception('db.add_repo accepts full repo name (e.g., foo/bar)')

			key = 'repo%' + repo_fullname
			converted_data = self.convert_none_to_empty(data_dict)
			self.__rc.hmset(key, converted_data)
		except Exception as e:
			print('full repo name: ' + str(repo_fullname))
			print('ERROR: ' + str(e))
			traceback.print_exc()
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)
			exit(1)

	##################################################################
	# Add event data for a repo
	##################################################################
	def add_data(self, repo_fullname, created_at, data_type, data_dict):
		try:
			# NOTE: @repo_id is full repo name
			if '/' not in repo_fullname:
				print('repo_fullname: ' + str(repo_fullname))
				# example: 'foo/bar' where @foo is the GitHub user and @bar is the repo name
				raise Exception('db.add_repo accepts full repo name (e.g., foo/bar)')

			converted_data = self.convert_none_to_empty(data_dict)
			key = repo_fullname + '%' + data_type + '%' + created_at
			self.__rc.hmset(key, converted_data)
			key = repo_fullname + '%' + data_type
			self.__rc.sadd(key, created_at)
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

	db.get_repos()

##################################################################
# Main
##################################################################
if __name__ == "__main__":
	test()
