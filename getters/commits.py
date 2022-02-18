import html
from platform import release
import traceback
import json
import os
import sys
from inspect import currentframe, getframeinfo
from getters import persons, repos
import name

##########################
# Push Events
##########################
def get_PushEvent(repo_name, created_at, json_payload, record_d, db, commits, commit_past_repo_names):
        try:
                # author name
                try:
                        if len(json_payload['commits']) != 0:
                                if isinstance(json_payload['commits'], list):
                                        
                                        if isinstance(json_payload['commits'][0], dict):
                                                if isinstance(json_payload['commits'][0]['author'], dict):
                                                        author_name = json_payload['commits'][0]['author']['name']
                                        
                        else:
                                author_name = None
                except KeyError as ke:
                        author_name = None

                # author email
                try:
                        if len(json_payload['commits']) != 0:
                                author_email = json_payload['commits'][0]['author']['email']
                        else:
                                author_email = None
                except KeyError as ke:
                        author_email = None

                # commit message
                message = None
                try:
                        message = json_payload['message']
                except KeyError as ke:
                        message = None
        except Exception as e:
                frameinfo = getframeinfo(currentframe())
                print(frameinfo.filename, frameinfo.lineno)	
                print('PUSHEVENT_EXCEPTION: ' + str(e))
                traceback.print_exc()
                exit(1)

        commit = {'commited_at' : created_at}
        if author_name:
                commit['author_name'] = author_name
        if author_email:
                commit['author_email'] = author_email
        if message:
                commit['message'] =  message

        commits.append(commit)
        commits_dict = {
                'repo_name' : repo_name,
                'commits' : commits
        }

        if repo_name not in commit_past_repo_names:
                commits_dict['{}'.format(repo_name)] = [commit]
        else:
                commits_dict['{}'.format(repo_name)].append(commit)

        full_repo_name = name.get_full_repo_name(json_payload, record_d, repo_name)
  
        # save in the database
        try:
                db.add_data(full_repo_name, created_at, 'commits', commits_dict)
        except Exception as e:
                print("Failed to save %s PushEvent record at %s: %s" % \
                                (full_repo_name, created_at, str(e)))
                traceback.print_exc()
                frameinfo = getframeinfo(currentframe())
                print(frameinfo.filename, frameinfo.lineno)


        # check for repo and actor_attributes in a record
        if '"repo":' in str(record_d) and '"repository":' in str(record_d):
                frameinfo = getframeinfo(currentframe())
                print(frameinfo.filename, frameinfo.lineno)	
                print('REPO_and_REPOSITORY_in_the_same_record_EXCEPTION: ' + str(e))
                exit(1)

        try:
                r_dict = record_d['repo']
        except KeyError as ke:
                try:
                        r_dict = record_d['repository']
                except KeyError as ke:
                        frameinfo = getframeinfo(currentframe())
                        print(frameinfo.filename, frameinfo.lineno)	
                        print('KEYERROR RELEASEEVENT_EXCEPTION: ' + str(ke))
                        exit(1)

        except Exception as e:
                frameinfo = getframeinfo(currentframe())
                print(frameinfo.filename, frameinfo.lineno)	
                print('ERROR RELEASEEVENT_EXCEPTION: ' + str(e))
                traceback.print_exc()
                exit(1)

        if isinstance(r_dict, dict):
                repos.get_Repo(full_repo_name, created_at, json_payload, record_d, r_dict, db)
        else:
                raise Exception("'r_dict' (%s) is not a dict!\n%s" % (r_dict, record_d))





        # actor making the releasing
        try:
                if isinstance(record_d['actor'], dict):
                        actor_dict = record_d['actor']
                        actors.get_Actor(full_repo_name, actor_dict, record_d, db, created_at)
                elif isinstance(record_d['actor'], str):
                        actor_dict = {'login' : record_d['actor']}
                        actors.get_Actor(full_repo_name, actor_dict, record_d, db, created_at)
                elif isinstance(record_d['actor_attributes'], dict):
                                actor_dict = record_d['actor_attributes']
                                actors.get_Actor(full_repo_name, actor_dict, record_d, db, created_at)
                else:
                        print("record_d: " + str(record_d))
                        print("HAVEN'T FOUND P_DICT")
        except KeyError as ke:
                actor_dict = None
                print('actor_dict: ' + str(actor_dict))
                frameinfo = getframeinfo(currentframe())
                print(frameinfo.filename, frameinfo.lineno)	
                print('record_d: ' + str(record_d))
                print('KEYERROR RELEASEEVENT_EXCEPTION: ' + str(ke))
                exit(1)
        except Exception as e:
                frameinfo = getframeinfo(currentframe())
                print(frameinfo.filename, frameinfo.lineno)	
                print('ERROR RELEASEEVENT_EXCEPTION: ' + str(e))
                traceback.print_exc()
                exit(1)

        # actor owning the repo
        if isinstance(actor_dict, dict):
                actors.get_Actor(full_repo_name, actor_dict, record_d, db, created_at)
        else:
                raise Exception("'actor_dict' (%s) is not a dict!\n%s" % (actor_dict, record_d))
