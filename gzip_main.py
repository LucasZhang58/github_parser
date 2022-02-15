import os
import sys
import gzip_github_parser as ghp
import traceback
from db import Database
import multiprocess as mp

import config

##############################
# main function
##############################
def main():

	# validate number of inputs
	if len(sys.argv) != 2:
		print("USAGE: python3 %s <path-to-dir-containing-gharchive-gzip-files>" % (sys.argv[0]))
		exit(1)

	# validate input path
	input_path = sys.argv[1]
	if not os.path.exists(input_path) or not os.path.isdir(input_path):
		print("%s does not exist. Exiting!" % (input_path))
		exit(1)

	# get db manager
	try:
		db = Database()
	except Exception as e:
		print("Failed to get dbing manager: %s. Exiting!" % (str(e)))
		traceback.print_exc()
		exit(1)

	# collect the records
	gzip_file_list = []
	for root_dir, dirs, files in os.walk(input_path, topdown=False):
		for file_name in files:
			gzip_file_list.append(os.path.join(root_dir, file_name))

	print("Collected %d gzipped files" % (len(gzip_file_list)))

	cfg = config.Config()
	mode = 'ProcessPool' #cfg.get("QUEUING", "Infrastructure")

	args = [input_path, db]
	if mode == "ProcessPool":
		mp.start_parallel_workers(gzip_file_list, ghp.parse_gzip_file, args)
	else:
		for f in gzip_file_list:
			ghp.parse_gzip_file(f, args, None)

##############################
# call the main function
##############################
if __name__ == "__main__":
	main()
