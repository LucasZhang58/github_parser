from inspect import currentframe, getframeinfo
import traceback

import utils

class Database:

	##################################################################
	# Init
	##################################################################
	def __init__(self, dryrun=False):
		try:
			import config
			cfg = config.Config()
			db_type = cfg.get('Type', 'DB')
			if db_type == "redis":
				import redis
				self.__host = cfg.get("HOST", sec="Redis", default="localhost")
				self.__port = cfg.get("PORT", sec="Redis", default="6379")
				self.__db = cfg.get("DATABASE", sec="Redis", default="0")

				self.__dryrun = dryrun
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
	def add_actor(self, actor_login, actor_type, data_dict):
		try:
			assert self.__rc, "Failed to add actor %s: DB not setup" % (actor_type)
			if self.__dryrun:
				return
			key = actor_type + '%' + actor_login
			converted_data = self.convert_none_to_empty(data_dict)
			self.__rc.hmset(key, converted_data)
		except Exception as e:
			print('ERROR: ' + str(e))
			traceback.print_exc()
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)
			exit(1)


	##################################################################
	# Get actors
	##################################################################
	def get_all_actors(self, actor_type):
		try:
			key_pattern = actor_type + '%*'

			for batch in self.__get_matching_batches(key_pattern):
				for idx, val in utils.for_each_item_int(list(batch)):
					if not val:
						continue
					val = val.decode('utf-8')
					if not val.startswith(actor_type + '%'):
						raise Exception('Invalid %s name %s!' % (actor_type, val))
					yield val.replace(actor_type + '%','')
		except Exception as e:
			traceback.print_exc()
			raise Exception("Failed to get all %s from DB: %s!" % (actor_type, str(e)))


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

	def get_repo_or_actor(self, repo_fullname):
		try:
			val = self.__rc.hgetall('repo%' + repo_fullname)
		#	print('val: ' + str(val))
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

			assert self.__rc, "Failed to add repo %s: DB not setup" % (repo_fullname)
			if self.__dryrun:
				return
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

			assert self.__rc, "Failed to add data %s: DB not setup" % (repo_fullname)
			if self.__dryrun:
				return
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

	def add_member(self, full_repo_name, m_dict, actor_type):
		try:
			# NOTE: @repo_id is full repo name
			if '/' not in full_repo_name:
				print('repo_fullname: ' + str(full_repo_name))
				# example: 'foo/bar' where @foo is the GitHub user and @bar is the repo name
				raise Exception('db.add_repo accepts full repo name (e.g., foo/bar)')

			assert self.__rc, "Failed to add actor %s: DB not setup" % (actor_type)
			if self.__dryrun:
				return
			key = full_repo_name + '%'+ 'members'
			self.__rc.sadd(key, str(m_dict))
		except Exception as e:
			print('ERROR: ' + str(e))
			traceback.print_exc()
			frameinfo = getframeinfo(currentframe())
			print(frameinfo.filename, frameinfo.lineno)
			exit(1)


	##################################################################
	# Get Data From Redis
	##################################################################

	def get_out_data(self, repo_fullname, data_type):
		try:
			val = self.__rc.hgetall( data_type + '%' + repo_fullname)
			return self.decode_redis(val)
		except Exception as e:
			raise Exception('Failed to get repo %s: %s' % (repo_fullname, str(e)))

	def get_all_data_type(self, data_type):
		try:
			key_pattern = data_type + '%*'
			print(key_pattern)

			for batch in self.__get_matching_batches(key_pattern):
				for idx, val in utils.for_each_item_int(list(batch)):
					if not val:
						continue
					val = val.decode('utf-8')
					if not val.startswith(key_pattern):
						raise Exception('Invalid repo name %s!' % (val))
					yield val.replace(key_pattern,'')
		except Exception as e:
			traceback.print_exc()
			raise Exception("Failed to get all repos from DB: %s!" % (str(e)))

	def get_data_type_data(self, data_type_fullname):
		try:
			val = self.__rc.hgetall('repo%' + data_type_fullname)
			return self.decode_redis(val)
		except Exception as e:
			raise Exception('Failed to get repo %s: %s' % (data_type_fullname, str(e)))


	# def get_repo(self, repo_fullname):
	# 	try:
	# 		val = self.__rc.hgetall('repo%' + repo_fullname)
	# 		return self.decode_redis(val)
	# 	except Exception as e:
	# 		raise Exception('Failed to get repo %s: %s' % (repo_fullname, str(e)))

	# def get_all_stars(self):

	# 	try:

	# 		key_pattern = '*%star%*'
	
	# 		#print("self.__get_matching_batches(key_pattern): " + str(self.__get_matching_batches(key_pattern)))

	# 		for batch in self.__get_matching_batches(key_pattern):

	# 			for idx, val in utils.for_each_item_int(list(batch)):
	
	# 				if not val:
	# 					continue
	# 				val = val.decode('utf-8')
	
	# 				if not val.startswith('star%'):
	# 					raise Exception('Invalid star name %s!' % (val))
	# 				yield val.replace('%star%','')
		
					
	# 	except Exception as e:
	# 		traceback.print_exc()
	# 		raise Exception("Failed to get all stars from DB: %s!" % (str(e)))

	# def get_star(self, star_fullname):
	# 	try:
	# 		val = self.__rc.hgetall('%star%' + star_fullname)
	# 		return self.decode_redis(val)
	# 	except Exception as e:
	# 		raise Exception('Failed to get stars %s: %s' % (star_fullname, str(e)))

	# def get_fork(self, fork_fullname):
	# 	try:
	# 		val = self.__rc.hgetall('forks%' + fork_fullname)
	# 		return self.decode_redis(val)
	# 	except Exception as e:
	# 		raise Exception('Failed to get forks %s: %s' % (fork_fullname, str(e)))

	def get_all_stars(self):
		try:
			key_pattern = '%stars%'

			for batch in self.__get_matching_batches(key_pattern):
				for idx, val in utils.for_each_item_int(list(batch)):
					if not val:
						continue
					val = val.decode('utf-8')
					if not val.startswith('stars%'):
						raise Exception('Invalid repo name %s!' % (val))
					yield val.replace('repo%','')
		except Exception as e:
			traceback.print_exc()
			raise Exception("Failed to get all repos from DB: %s!" % (str(e)))

# 	def get_star(self, star_fullname):# returns the created_at
# 		try:
# 			#val = self.__rc.hgetall('repo%' + star_fullname)
# 			val = self.__rc.hgetall(star_fullname + '%stars%')
# 		#	print('val: ' + str(val))
# 			return self.decode_redis(val)
# 		except Exception as e:
# 			raise Exception('Failed to get repo %s: %s' % (star_fullname, str(e)))


	def get_value(self, repo_fullname, data_type, db, created_at):
		try:
			
			key = repo_fullname + '%stars%'
			#print(key)
			val = self.__rc.hgetall(repo_fullname + '%stars%' + created_at)
			#print('val: ' + str(val))
			return self.decode_redis(val)
		except Exception as e:
			raise Exception('Failed to get repo %s: %s' % (repo_fullname, str(e)))


# ##################################################################
# unit test
##################################################################
def test():
	db = Database()
#	print('*%star%*')
	# print(db)
	# size = db.size()
	# print(size)
	# for i in db.get_all_repos():
	# 	repo_data = db.get_repo(i)
	# 	print(repo_data)
	# print(db.get_all_stars())


	for repo_fullname in db.get_all_repos():
		repo_data = db.get_repo(repo_fullname)
		# print(repo_data)
		print(repo_fullname)
		repo_data[repo_fullname] = {}
		curr_dict = {repo_data : {}}

		for branch_created_at in db.get_data(repo_fullname, 'branches'):
			val = db.get_value(repo_fullname, 'branches', db, branch_created_at)
			print(val)

		for tag_created_at in db.get_data(repo_fullname, 'tags'):
			val = db.get_value(repo_fullname, 'tags', db, tag_created_at)
			print(val)

		for release_created_at in db.get_data(repo_fullname, 'releases'):
			val = db.get_value(repo_fullname, 'releases', db, release_created_at)
			print(val)


		for fork_created_at in db.get_data(repo_fullname, 'forks'):
			val = db.get_value(repo_fullname, 'forks', db, fork_created_at)
			print(val)


		for star_created_at in db.get_data(repo_fullname, 'stars'):
			val = db.get_value(repo_fullname, 'stars', db, star_created_at)
			repo_data[repo_fullname] = val
			print(val)

		for issue_created_at in db.get_data(repo_fullname, 'issues'):
			val = db.get_value(repo_fullname, 'issues', db, issue_created_at)
			repo_data[repo_fullname] = val
			print(val)



		for member_created_at in db.get_data(repo_fullname, 'members'):
			val = db.get_value(repo_fullname, 'members', db, member_created_at)
			repo_data[repo_fullname] = val
			print(val)

		for commit_created_at in db.get_data(repo_fullname, 'commits'):
			val = db.get_value(repo_fullname, 'commits', db, commit_created_at)
			repo_data[repo_fullname] = val
			print(val)



		print('####################################################################')



	# for repo_fullname in db.get_all_repos():
	# 	# repo_data = db.get_final_data(repo_fullname, 'stars', db)
	# 	# print(repo_data)





	# 	for repo_fullname in db.get_all_stars():
	# 		#print(repo_fullname)
	# 		data = db.get_star(repo_fullname)
	# 		print(data)

	# for star_fullname in db.get_all_stars():
	# 	print('UIIIIIIIIIII')
	# 	repo_data = db.get_star(star_fullname)
	# 	print('OOOOOOOOOOOO')
	# 	print(repo_data)

	#for star in db.get_data(repo_fullname, 'stars'):
	#       print(star)
	#for fork in db.get_data(repo_fullname, 'forks'):
	#       print(fork)
	#for release in db.get_data(repo_fullname, 'releases'):
	#       print(release)

	









	# for star in db.get_all_data_type('stars'):
 	# 	print(star)

	# for data_type_fullname in db.get_all_data_type('stars'):
	# 	star_data = db.get_data_type_data(data_type_fullname)
	# 	print(star_data)
		# for star in db.get_all_data_type('stars'):
		# 	print(star)




	# for star in db.get_data(repo_fullname, 'stars'):
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
