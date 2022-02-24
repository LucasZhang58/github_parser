from inspect import currentframe, getframeinfo
import traceback

import gzip
import json
import sys
import os

sys.path.append('getters')
import stars 
import releases
import forks
import issues
import members
import refs
import commits_file
  
######################
# Parse Events
######################
def parse_event(repo_name:str, created_at:str, json_payload:str, record_d:dict, db, member_past_repo_names, member_dict, commits, commit_past_repo_names, ref_past_repo_names):

        # if 'WatchEvent' == record_d['type']:
        #         stars.get_WatchEvent(repo_name, created_at, json_payload, record_d, db)

        if 'ReleaseEvent' == record_d['type']:
                releases.get_ReleaseEvent(repo_name, created_at, json_payload, record_d, db)

        # elif 'ForkEvent' == record_d['type']:
        #        forks.get_ForkEvent(repo_name, created_at, json_payload, record_d, db)

        # elif 'CreateEvent' == record_d['type']:
        #         refs.get_CreateEvent(repo_name, created_at, json_payload, record_d, db, ref_past_repo_names)

        # if 'IssuesEvent' == record_d['type']:
        #         #pass
        #         # TODO enable this
        #         issues.get_IssuesEvent(repo_name, created_at, json_payload, record_d, db)

        # if 'PushEvent' == record_d['type']:
                # #pass
                # # TODO enable this
                # commits_file.get_PushEvent(repo_name, created_at, json_payload, record_d, db, commits, commit_past_repo_names)

        # elif 'MemberEvent' == record_d['type']:
        #         members.get_MemberEvent(repo_name, created_at, json_payload, record_d, db, member_past_repo_names, member_dict)

        # # skip these events
        # elif record_d['type'] in ['IssueCommentEvent', 'PullRequestEvent', 'PullRequestReviewCommentEvent', 'GollumEvent', 'CommitCommentEvent']:
        # 	pass

        # else:
        # 	# TODO enable this
        # 	print("Ignoring %s events" % (record_d['type']))

######################
# Parse Record
######################
def parse_gzip_file(gzip_file:str, args:list, worker_id:int):
        input_path = args[0]
        db = args[1]
        repo_list = args[2]
 #       print(repo_list)


        member_past_repo_names = set()
        commit_past_repo_names = set()
        ref_past_repo_names = {}
        member_dict = {}
        commits = []

        # read input file
        completeName = os.path.join(input_path, str(gzip_file))

        with gzip.open(completeName,'rb') as f:
                for idx, content in enumerate(f):
                        try:
                                try:
                                        record_d = json.loads(content)
                                except Exception as e:
                                        print("Failed to parse record at line %d in %s" % (idx + 1, completeName))
                                        traceback.print_exc()
                                        continue

                                # repo_name
                                try:
                                        repo_name = record_d['repo']['name']
                                except KeyError as ke:
                                        try:
                                                repo_name = record_d['repository']['name']
                                        except KeyError as ke:
                                                continue
                             #   print(repo_name)
                                if repo_name not in repo_list:
                                        continue

                                print(repo_name)

                                # created_at
                                try:
                                        created_at = record_d['created_at']
                                except KeyError as ke:
                                        created_at = None

                                # json_payload
                                try:
                                        json_payload = record_d['payload']
                                except KeyError as ke:
                                        json_payload = None

                                # parse records
                                if repo_name != "test":
                                        parse_event(repo_name, created_at, json_payload, record_d, db,	member_past_repo_names, member_dict, commits, commit_past_repo_names, ref_past_repo_names)
                                
                        except Exception as e:
                                print('parse_event EXCEPTION: ' +  (str(e)))
                                print('record_d: ' + str(record_d))
                                frameinfo = getframeinfo(currentframe())
                                traceback.print_exc()
                                print(frameinfo.filename, frameinfo.lineno)
                                exit(1)
