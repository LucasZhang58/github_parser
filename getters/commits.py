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






def get_author_name_helper(in_dict):
        if isinstance(in_dict['actor'], str):
                return in_dict['actor']
        elif isinstance(in_dict['actor'], dict):
                return in_dict['actor']['login']
        else:
                frameinfo = getframeinfo(currentframe())
                print(frameinfo.filename, frameinfo.lineno)	
                return

def get_author_email_helper(in_dict):
        if isinstance(in_dict['actor_attributes'], dict):
                return in_dict['actor_attributes']['email']
        elif isinstance(in_dict['actor_attributes'], str):
                print("'{}'['actor_attributes'] is a string!!!!!!".format(in_dict))
                print('"{}": '.format(in_dict) + str(in_dict))
        else:
                frameinfo = getframeinfo(currentframe())
                print(frameinfo.filename, frameinfo.lineno)	
                print("author email is not in indict!!!!!!!")
                print('"{}": '.format(in_dict) + str(in_dict))
                return

def get_message_helper(in_dict):
        if isinstance(in_dict['message'], str):
                print("'{}'['message'] is a string!!!!!!".format(in_dict))
                print('"{}": '.format(in_dict) + str(in_dict))
                return in_dict['message']

        elif isinstance(in_dict['message'], dict):
                print(in_dict['message'])
                print('"{}": '.format(in_dict) + str(in_dict))
                return in_dict['message']
        else:
                frameinfo = getframeinfo(currentframe())
                print(frameinfo.filename, frameinfo.lineno)	
                print("meesage is not in '{}'!!!!!!!".format(in_dict))
                print('"{}": '.format(in_dict) + str(in_dict))
                return





def get_PushEvent(repo_name, created_at, json_payload, record_d, db, commits, commit_past_repo_names):
        commited_at = created_at
        author_name = None
        author_email = None
        message = None

        frameinfo = getframeinfo(currentframe())
        print(frameinfo.filename, frameinfo.lineno)
        try:
                # author name
          
                if 'actor' in record_d:
                        author_name = get_author_name_helper(record_d)
                elif 'actor' in json_payload:
                        author_name = get_author_name_helper(json_payload)
                else:
                        print('actor is not in record_d nor payload')
                        frameinfo = getframeinfo(currentframe())
                        print(frameinfo.filename, frameinfo.lineno)
                        print('record_d: ' + str(record_d))

                # author email
                if 'actor_attributes' in record_d:
                        author_email = get_author_email_helper(record_d)
                elif 'actor_attributes' in json_payload:
                        author_email = get_author_email_helper(json_payload)
                else:
                        print('actor_attributes is not in record_d nor payload')
                        frameinfo = getframeinfo(currentframe())
                        print(frameinfo.filename, frameinfo.lineno)
                        print('record_d: ' + str(record_d))

                # message
                if 'message' in record_d:
                        author_email = get_author_email_helper(record_d)
                elif 'message' in json_payload:
                        author_email = get_author_email_helper(json_payload)
                else:
                        print('message is not in record_d nor payload')
                        frameinfo = getframeinfo(currentframe())
                        print(frameinfo.filename, frameinfo.lineno)
                        print('record_d: ' + str(record_d))




                        

                # # author email
                # try:
                #         if len(json_payload['commits']) != 0:
                #                 author_email = json_payload['commits'][0]['author']['email']
                #         else:
                #                 author_email = None
                # except KeyError as ke:
                #         author_email = None


                # # commit message
                # message = None
                # try:
                #         message = json_payload['message']
                # except KeyError as ke:
                #         message = None
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


        # # check for repo and actor_attributes in a record
        # if '"repo":' in str(record_d) and '"repository":' in str(record_d):
        #         frameinfo = getframeinfo(currentframe())
        #         print(frameinfo.filename, frameinfo.lineno)	
        #         print('REPO_and_REPOSITORY_in_the_same_record_EXCEPTION: ' + str(e))
        #         exit(1)

        # try:
        #         r_dict = record_d['repo']
        # except KeyError as ke:
        #         try:
        #                 r_dict = record_d['repository']
        #         except KeyError as ke:
        #                 frameinfo = getframeinfo(currentframe())
        #                 print(frameinfo.filename, frameinfo.lineno)	
        #                 print('KEYERROR RELEASEEVENT_EXCEPTION: ' + str(ke))
        #                 exit(1)

        # except Exception as e:
        #         frameinfo = getframeinfo(currentframe())
        #         print(frameinfo.filename, frameinfo.lineno)	
        #         print('ERROR RELEASEEVENT_EXCEPTION: ' + str(e))
        #         traceback.print_exc()
        #         exit(1)

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
        #         print('KEYERROR RELEASEEVENT_EXCEPTION: ' + str(ke))
        #         exit(1)
        # except Exception as e:
        #         frameinfo = getframeinfo(currentframe())
        #         print(frameinfo.filename, frameinfo.lineno)	
        #         print('ERROR RELEASEEVENT_EXCEPTION: ' + str(e))
        #         traceback.print_exc()
        #         exit(1)

        # # actor owning the repo
        # if isinstance(actor_dict, dict):
        #         actors.get_Actor(full_repo_name, actor_dict, record_d, db, created_at)
        # else:
        #         raise Exception("'actor_dict' (%s) is not a dict!\n%s" % (actor_dict, record_d))
