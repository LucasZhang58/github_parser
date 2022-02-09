import gzip
import json
import gzip_github_parser as ghp
import os
import sys
import re
#import multiprocess as mp
import gzip_github_parser as ghp

from db import Database
import multiprocess as mp

input_path = r'/opt/GHArchive'

##############################
# main function
##############################
def main():

	# get db manager
	try:
		db = Database()
	except Exception as e:
		print("Failed to get dbing manager: %s. Exiting!" % (str(e)))
		exit(1)

	# collect the records
	gzip_file_list = []
	for gzip_file in os.listdir(input_path):
		gzip_file_list.append(gzip_file)

	print("Collected %d gzipped files" % (len(gzip_file_list)))
	args = [input_path, db]
	mp.start_parallel_workers(gzip_file_list, ghp.parse_gzip_file, args)

##############################
# call the main function
##############################
if __name__ == "__main__":
	main()
