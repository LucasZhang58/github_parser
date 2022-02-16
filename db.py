from lib2to3.pytree import convert
import os
from pydoc import cram
import time
from inspect import currentframe, getframeinfo
import traceback

import utils

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
				self.__host = cfg.get("HOST", sec="Redis", default="localhost")
				self.__port = cfg.get("PORT", sec="Redis", default="6379")
				self.__db = cfg.get("DATABASE", sec="Redis", default="0")

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
			traceback.print_exc()
			raise Exception("Error dumping memory info: %s" % (str(e)))

	##################################################################
	# Database size
	##################################################################
	def size(self):
		assert self.__rc, "Failed to get DB size: DB not setup"
		try:
			return self.__rc.dbsize()
		except Exception as e:
			traceback.print_exc()
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
	# decode from bytes to str
	##################################################################
	def decode_redis(self, src):
		if isinstance(src, list) or isinstance(src, set):
			return [ item.decode('utf-8') for item in src ]
		if isinstance(src, dict):
			return { k.decode('utf-8'): v.decode('utf-8') for k,v in src.items() }
		return src
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
	# Add GitHub org data
	##################################################################
	def add_org(self, user_login, data_dict):
		try:
			key = 'org%' + user_login
			# print('key: ' + str(key))
			# print('data_dict: ' + str(data_dict))
			converted_data = self.convert_none_to_empty(data_dict)
			self.__rc.hmset(key, converted_data)
		except Exception as e:
			# print('user_login: ' + str(user_login) + ' is of type ' + str(type(user_login)))
			# print('data_dict: ' + str(data_dict) + ' is of type ' + str(type(data_dict)))
			# print('converted_data: ' + str(converted_data) + ' is of type ' + str(type(converted_data)))
			# print('key: ' + str(key) + ' is of type ' + str(type(key)))
			print('ERROR: ' + str(e))
			traceback.print_exc()
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)
			exit(1)

	##################################################################
	# Get repos
	##################################################################
	def get_all_repos(self):
		try:
			key_pattern = 'repo%*'

			for batch in self.__get_matching_batches(key_pattern):
				for idx, val in utils.for_each_item_int(list(batch)):
					if not val:
						continue
					val = val.decode('utf-8')
					if not val.startswith('repo%'):
						raise Exception('Invalid repo name %s!' % (val))
					yield val.replace('repo%','')
		except Exception as e:
			traceback.print_exc()
			raise Exception("Failed to get all repos from DB: %s!" % (str(e)))

	def get_repo(self, repo_fullname):
		try:
			val = self.__rc.hgetall('repo%' + repo_fullname)
			return self.decode_redis(val)
		except Exception as e:
			raise Exception('Failed to get repo %s: %s' % (repo_fullname, str(e)))

	def get_data(self, repo_fullname, data_type):
		try:
			key = repo_fullname + '%' + data_type
			val = self.__rc.smembers(key)
			return self.decode_redis(val)
		except Exception as e:
			raise Exception('Failed to get repo %s data on %s: %s' % \
				(repo_fullname, data_type, str(e)))

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
			if len(converted_data) == 0:
				converted_data = {'':''}
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
	# Add Member
	##################################################################

	def add_member(self, full_repo_name, m_dict):
		try:
			key = full_repo_name + '%'+ 'members'
			self.__rc.sadd(key, str(m_dict))
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
	#size = db.size()
	#print(size)

	for repo_fullname in db.get_all_repos():
	repo_data = db.get_repo(repo_fullname)
	print(repo_data)
	#for star in db.get_data(repo_fullname, 'stars'):
	#       print(star)
	#for fork in db.get_data(repo_fullname, 'forks'):
	#       print(fork)
	#for release in db.get_data(repo_fullname, 'releases'):
	#       print(release)

##################################################################
# Main
##################################################################
if __name__ == "__main__":
	test()
