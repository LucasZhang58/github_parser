#########################################
#####	 MULTIPROCESS.PY
import multiprocessing
import traceback
import os
import re
import sys

import utils

###########################################################
# Multiprocessing
###########################################################
def worker(inq, work_func, args:list):
	process = multiprocessing.current_process()
	worker_id = process._identity
	print("Starting worker %s [%s]" % (process.name, worker_id))

	while True:
		try:

			# retrieve work item
			req = inq.get(block=True, timeout=5)

			idx, work_item = req

			# end of queue
			if not work_item:
				return

			# perform actual work
			ret = work_func(work_item, args, worker_id)

		except Exception as e:
			raise Exception("Worker %s [%s] failed to do work: %s" % \
					(process.name, process._identity, str(e)))

def start_parallel_workers(work_item_list:list, work_func, args:list=None):
	try:
		# register signal handler
		signal = utils.Signal()
		signal.install([utils.Signal.SIGINT, utils.Signal.SIGTERM])

		# multiprocessing
		manager = multiprocessing.Manager()

		inq = manager.Queue()

		work_args = (inq, work_func, args)

		cpu_count = multiprocessing.cpu_count()

		pool = multiprocessing.Pool(cpu_count, worker, work_args)

		# work with each item
		for idx, work_item in enumerate(work_item_list):

			# check for interruption
			if signal.caught():
				break

			inq.put((idx, work_item))

		for i in range(cpu_count):
			inq.put((None, None))

		# wait for them to exit
		pool.close()
		pool.join()

	except Exception as e:
                
		raise Exception("Failed to start workers: %s" % (str(e)))
                



