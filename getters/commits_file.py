import html
from platform import release
import traceback
import json
import os
import sys
from inspect import currentframe, getframeinfo
from getters import actors, repos
import name
##########################
# Push Events
##########################
# def shas_helper(repo_name, created_at, json_payload, record_d, db, commits, commit_past_repo_names, type_name, element):
#         commited_at = created_at
#         author_name = None
#         author_email = None
#         message = None
#         commit_id = None
#         try:
#                 commit_id = element[0]

#                 author_email = element[1]

#                 message = element[2]

#                 author_name = element[3]
#         except KeyError as ke:
#                 frameinfo = getframeinfo(currentframe())
#                 print(frameinfo.filename, frameinfo.lineno)	
#                 print('ERROR PUSHEVENT_EXCEPTION: ' + str(ke))
#                 traceback.print_exc()
#         except Exception as e:
#                 frameinfo = getframeinfo(currentframe())
#                 print(frameinfo.filename, frameinfo.lineno)	
#                 print('ERROR PUSHEVENT_EXCEPTION: ' + str(e))
#                 traceback.print_exc()
#                 exit(1)
#         add_to_db(repo_name, created_at, json_payload, record_d, db, commits, commit_past_repo_names, author_name, author_email, message, commit_id)

# def commits_helper(repo_name, created_at, json_payload, record_d, db, commits, commit_past_repo_names, type_name, element):
#         commited_at = created_at
#         author_name = None
#         author_email = None
#         message = None
#         commit_id = None
#         try:
#                 commit_id = element['sha']

#                 author_email = element['author']['email']

#                 message = element['message']

#                 author_name = element['author']['name']
#         except KeyError as ke:
#                 frameinfo = getframeinfo(currentframe())
#                 print(frameinfo.filename, frameinfo.lineno)	
#                 print('ERROR PUSHEVENT_EXCEPTION: ' + str(ke))
#                 traceback.print_exc()
#         except Exception as e:
#                 frameinfo = getframeinfo(currentframe())
#                 print(frameinfo.filename, frameinfo.lineno)	
#                 print('ERROR PUSHEVENT_EXCEPTION: ' + str(e))
#                 traceback.print_exc()
#                 exit(1)
#         add_to_db(repo_name, created_at, json_payload, record_d, db, commits, commit_past_repo_names, author_name, author_email, message, commit_id)

def get_PushEvent(repo_name, created_at, json_payload, record_d, db, commits, commit_past_repo_names):

        # if 'shas' in json_payload:
        #         type_name = 'shas'
        #         if json_payload['shas']:
        #                 for i in json_payload['shas']:
        #                         shas_helper(repo_name, created_at, json_payload, record_d, db, commits, commit_past_repo_names, type_name, i)
                
        # elif 'commits' in json_payload:
        #         type_name = 'commits'
        #         if json_payload['commits']:
        #                 for i in json_payload['commits']:
        #                         commits_helper(repo_name, created_at, json_payload, record_d, db, commits, commit_past_repo_names, type_name, i)
        # else:
        #         frameinfo = getframeinfo(currentframe())
        #         print(frameinfo.filename, frameinfo.lineno)	
        #         print("Neither shas not commits is in json_payload!!!!!")
        #         print('record_d: ' + str(record_d))

        #testing purpose only!!!!!
        add_to_db(repo_name, created_at, json_payload, record_d, db)
        

# def  add_to_db(repo_name, created_at, json_payload, record_d, db, commits, commit_past_repo_names, author_name, author_email, message, commit_id):
def  add_to_db(repo_name, created_at, json_payload, record_d, db):

        # commit = {'commited_at' : created_at}

        # if author_name:
        #         commit['author_name'] = author_name

        # if author_email:
        #         commit['author_email'] = author_email

        # if message:
        #         commit['message'] =  message

        # if commit_id:
        #         commit['commit_id'] =  commit_id

        # commits.append(commit)

        # commits_dict = {
        #         'commits' : commits
        # }

        full_repo_name = name.get_full_repo_name(json_payload, record_d, repo_name)

        # if repo_name not in commit_past_repo_names:
        #         commits_dict[full_repo_name] = [commit]
        # else:
        #         commits_dict[full_repo_name].append(commit)

        # # save in the database
        # try:
        #         db.add_data(full_repo_name, created_at, 'commits', commits_dict)
        # except Exception as e:
        #         print("Failed to save %s PushEvent record at %s: %s" % \
        #                         (full_repo_name, created_at, str(e)))
        #         traceback.print_exc()
        #         frameinfo = getframeinfo(currentframe())
        #         print(frameinfo.filename, frameinfo.lineno)

        # check for repo and actor_attributes in a record
        if '"repo":' in str(record_d) and '"repository":' in str(record_d):
                frameinfo = getframeinfo(currentframe())
                print(frameinfo.filename, frameinfo.lineno)	
                print('REPO_and_REPOSITORY_in_the_same_record_EXCEPTION: ' + str(e))
                exit(1)

        # try:
        #         r_dict = record_d['repo']
        # except KeyError as ke:
        #         try:
        #                 r_dict = record_d['repository']
        #         except KeyError as ke:
        #                 frameinfo = getframeinfo(currentframe())
        #                 print(frameinfo.filename, frameinfo.lineno)	
        #                 print('KEYERROR PUSHEVENT_EXCEPTION: ' + str(ke))
        #                 exit(1)

        # except Exception as e:
        #         frameinfo = getframeinfo(currentframe())
        #         print(frameinfo.filename, frameinfo.lineno)	
        #         print('ERROR PUSHEVENT_EXCEPTION: ' + str(e))
        #         traceback.print_exc()
        #         exit(1)

        #testing purpose only!!!!!
        r_dict = full_repo_name #TESTING ONLY

        if isinstance(r_dict, str):
                repos.get_Repo(full_repo_name, created_at, json_payload, record_d, r_dict, db)
        else:
                raise Exception("'r_dict' not a str!")

        # if isinstance(r_dict, dict):
        #         repos.get_Repo(full_repo_name, created_at, json_payload, record_d, r_dict, db)
        # else:
        #         raise Exception("'r_dict' (%s) is not a dict!\n%s" % (r_dict, record_d))

        # # actor making the releasing
        # try:
        #         if isinstance(record_d['actor'], dict):
        #                 actor_dict = record_d['actor']
        #                 actors.get_Actor(full_repo_name, actor_dict, record_d, db, created_at)
        #         elif isinstance(record_d['actor'], str):
        #                 actor_dict = {'login' : record_d['actor']}
        #                 actors.get_Actor(full_repo_name, actor_dict, record_d, db, created_at)
        #         elif isinstance(record_d['actor_attributes'], dict):
        #                         actor_dict = record_d['actor_attributes']
        #                         actors.get_Actor(full_repo_name, actor_dict, record_d, db, created_at)
        #         else:
        #                 print("record_d: " + str(record_d))
        #                 print("HAVEN'T FOUND P_DICT")
        # except KeyError as ke:
        #         actor_dict = None
        #         print('actor_dict: ' + str(actor_dict))
        #         frameinfo = getframeinfo(currentframe())
        #         print(frameinfo.filename, frameinfo.lineno)	
        #         print('record_d: ' + str(record_d))
        #         print('KEYERROR PUSHEVENT_EXCEPTION: ' + str(ke))
        #         exit(1)
        # except Exception as e:
        #         frameinfo = getframeinfo(currentframe())
        #         print(frameinfo.filename, frameinfo.lineno)	
        #         print('ERROR PUSHEVENT_EXCEPTION: ' + str(e))
        #         traceback.print_exc()
        #         exit(1)

        # # actor owning the repo
        # if isinstance(actor_dict, dict):
        #         actors.get_Actor(full_repo_name, actor_dict, record_d, db, created_at)
        # else:
        #         raise Exception("'actor_dict' (%s) is not a dict!\n%s" % (actor_dict, record_d))