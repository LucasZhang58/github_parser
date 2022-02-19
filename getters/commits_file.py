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



def get_author_login_helper(in_dict, record_d):
        if 'actor' in in_dict:
                if isinstance(in_dict['actor'], str):
                        return in_dict['actor']
                elif isinstance(in_dict['actor'], dict):
                        if 'login' in in_dict['actor']:
                                return in_dict['actor']['login']
                        else:
                                # frameinfo = getframeinfo(currentframe())
                                # print(frameinfo.filename, frameinfo.lineno)	
                                # print("login is not in in_dict['actor']")
                                # print('record_d: ' + str(record_d))
                                return

                else:
                        frameinfo = getframeinfo(currentframe())
                        print(frameinfo.filename, frameinfo.lineno)
                        print("in_dict['actor'] is not a string nor a dict")
                        print('record_d: ' + str(record_d))
                        return

        elif 'actor_attributes' in in_dict:
                if isinstance(in_dict['actor_attributes'], dict):
                        return in_dict['actor_attributes']['login']

                elif isinstance(in_dict['actor_attributes'], str):
                        print("'{}'['actor_attributes'] is a string!!!!!!".format(in_dict))
                        print('"{}": '.format(in_dict) + str(in_dict) + 'FFFFFFFFFFFFFFFFFFFFF')
                        return
                else:
                        frameinfo = getframeinfo(currentframe())
                        print(frameinfo.filename, frameinfo.lineno)
                        print("in_dict['actor_attributes'] is not a string nor a dict")
                        print('record_d: ' + str(record_d))
                        return

        elif 'org' in in_dict:
                if isinstance(in_dict['org'], dict):
                        return in_dict['org']['login']
                else:
                        frameinfo = getframeinfo(currentframe())
                        print(frameinfo.filename, frameinfo.lineno)
                        print("in_dict['org'] is not a dict")
                        print('record_d: ' + str(record_d))
                        return

        else:
                frameinfo = getframeinfo(currentframe())
                print(frameinfo.filename, frameinfo.lineno)	
                print("author email is not in indict!!!!!!!")
                print('"{}": '.format(in_dict) + str(in_dict) + 'EEEEEEEEEEEEEEEEEE')
                return

def get_message_helper(in_dict, record_d):
        if 'commits' in in_dict:
                if isinstance(in_dict['commits'][0], dict):
                        return in_dict['commits'][0]['message']
                else:
                        frameinfo = getframeinfo(currentframe())
                        print(frameinfo.filename, frameinfo.lineno)
                        print("in_dict['commits'][0] is not a dict")
                        print('record_d: ' + str(record_d))
                        return

        elif 'shas' in in_dict:
                if in_dict['shas'][0]:
                        if isinstance(in_dict['shas'][0], list):
                                return in_dict['shas'][0][2]
                        else:
                                frameinfo = getframeinfo(currentframe())
                                print(frameinfo.filename, frameinfo.lineno)
                                print("in_dict['shas'][0] is not a list")
                                print('record_d: ' + str(record_d))
                                return
                else:
                        frameinfo = getframeinfo(currentframe())
                        print(frameinfo.filename, frameinfo.lineno)
                        print("in_dict['shas'][0] is an empty list")
                        print('record_d: ' + str(record_d))
                        return
                        
        else:
                frameinfo = getframeinfo(currentframe())
                print(frameinfo.filename, frameinfo.lineno)	
                print("message is not in indict!!!!!!!")
                print('"{}": '.format(in_dict) + str(in_dict) + 'EEEEEEEEEEEEEEEEEE')
                return

                # commit_id
def get_commit_id_helper(in_dict, record_d):
        if 'commits' in in_dict:
                if in_dict['commits']:
                        if isinstance(in_dict['commits'][0], dict):
                                return in_dict['commits'][0]['sha']
                        else:
                                frameinfo = getframeinfo(currentframe())
                                print(frameinfo.filename, frameinfo.lineno)	
                                print("in_dict['commits'][0] is not a dict")
                                print('record_d: ' + str(record_d))
                                return
                else:
                        # frameinfo = getframeinfo(currentframe())
                        # print(frameinfo.filename, frameinfo.lineno)	
                        # print("in_dict['commits'] is an empty list")
                        # print('record_d: ' + str(record_d))
                        return


        elif 'shas' in in_dict:
                if in_dict['shas']:
                        if isinstance(in_dict['shas'][0], list):
                                return in_dict['shas'][0][1]
                        else:
                                frameinfo = getframeinfo(currentframe())
                                print(frameinfo.filename, frameinfo.lineno)	
                                print("in_dict['shas'][0] is not a dict")
                                print('record_d: ' + str(record_d))
                                return
                else:
                        return
                                # frameinfo = getframeinfo(currentframe())
                                # print(frameinfo.filename, frameinfo.lineno)	
                                # print("in_dict['shas'] list is empty")
                                # print('record_d: ' + str(record_d))

        else:
                frameinfo = getframeinfo(currentframe())
                print(frameinfo.filename, frameinfo.lineno)	
                print("commit_id is not in indict!!!!!!!")
                print('"{}": '.format(in_dict) + str(in_dict) + 'EEEEEEEEEEEEEEEEEE')
                return


def get_author_name_helper(in_dict, record_d):
        if 'actor_attributes' in in_dict:
                if isinstance(in_dict['actor_attributes'], dict):
                        if 'name' in in_dict['actor_attributes']:
                                return in_dict['actor_attributes']['name']
                        elif 'payload' in in_dict:
                                if 'shas' in in_dict['payload']:
                                        if in_dict['payload']['shas']:
                                                if in_dict['payload']['shas'][0]:
                                                        return in_dict['payload']['shas'][0][3]
                                                else:
                                                        frameinfo = getframeinfo(currentframe())
                                                        print(frameinfo.filename, frameinfo.lineno)
                                                        print("in_dict['payload']['shas'][0] is an empty list")
                                                        print('record_d: ' + str(record_d))
                                                        return
                                        else:
                                                # frameinfo = getframeinfo(currentframe())
                                                # print(frameinfo.filename, frameinfo.lineno)
                                                # print("in_dict['payload']['shas'] is an empty list")
                                                # print('record_d: ' + str(record_d))
                                                return
                                else:
                                        frameinfo = getframeinfo(currentframe())
                                        print(frameinfo.filename, frameinfo.lineno)
                                        print("shas not in in_dict['payload']")
                                        print('record_d: ' + str(record_d))
                                        return
                        else:
                                frameinfo = getframeinfo(currentframe())
                                print(frameinfo.filename, frameinfo.lineno)
                                print("name is not in in_dict['actor_attributes']")
                                print('record_d: ' + str(record_d))
                                return
                else:
                        frameinfo = getframeinfo(currentframe())
                        print(frameinfo.filename, frameinfo.lineno)
                        print('actor_attributes is not in in_dict')
                        print('record_d: ' + str(record_d))
                        return

        elif 'commits' in in_dict:
                if in_dict['commits']:
                        if isinstance(in_dict['commits'][0], dict):
                                if isinstance(in_dict['commits'][0]['author'], dict):
                                        return in_dict['commits'][0]['author']['name']
                                else:
                                        frameinfo = getframeinfo(currentframe())
                                        print(frameinfo.filename, frameinfo.lineno)
                                        print("in_dict['commits'][0]['author'] is not a dict")
                                        print('record_d: ' + str(record_d))
                                        return
                        else:
                                frameinfo = getframeinfo(currentframe())
                                print(frameinfo.filename, frameinfo.lineno)
                                print("in_dict['commits'][0] is not a dict")
                                print('record_d: ' + str(record_d))
                                return
                else:
                        # frameinfo = getframeinfo(currentframe())
                        # print(frameinfo.filename, frameinfo.lineno)
                        # print("in_dict['commits'] is an empty list")
                        # print('record_d: ' + str(record_d))
                        return

        elif 'shas' in in_dict:

                if isinstance(in_dict['shas'][0], list):
                        return in_dict['shas'][0][3]
                else:
                        frameinfo = getframeinfo(currentframe())
                        print(frameinfo.filename, frameinfo.lineno)
                        print("author name is not in in_dict['shas'][0]")
                        print('record_d: ' + str(record_d))
                        return
        elif 'payload' in in_dict:
                if 'shas' in in_dict['payload']:
                        if in_dict['payload']['shas']:
                                if isinstance(in_dict['payload']['shas'][0], list):
                                        return in_dict['payload']['shas'][0][3]
                                else:
                                        # frameinfo = getframeinfo(currentframe())
                                        # print(frameinfo.filename, frameinfo.lineno)
                                        # print("author name is not in in_dict['payload']['shas'][0]")
                                        # print('record_d: ' + str(record_d))
                                        return
                        else:
                                # frameinfo = getframeinfo(currentframe())
                                # print(frameinfo.filename, frameinfo.lineno)
                                # print("in_dict['payload']['shas'] is an empty list")
                                # print('record_d: ' + str(record_d))
                                return

                elif 'commits' in in_dict['payload']:
                        if isinstance(in_dict['payload']['commits'], list):
                                if in_dict['payload']['commits']:
                                        if isinstance(in_dict['payload']['commits'][0]['author'], dict):
                                                return in_dict['payload']['commits'][0]['author']['name']
                                        else:
                                                # frameinfo = getframeinfo(currentframe())
                                                # print(frameinfo.filename, frameinfo.lineno)
                                                # print("in_dict['payload']['commits'][0]['author'] is not a dict")
                                                # print('record_d: ' + str(record_d))
                                                return
                                else:
                                        # frameinfo = getframeinfo(currentframe())
                                        # print(frameinfo.filename, frameinfo.lineno)
                                        # print("in_dict['payload']['commits'] is an empty list")
                                        # print('record_d: ' + str(record_d))
                                        return
                        else:
                                # frameinfo = getframeinfo(currentframe())
                                # print(frameinfo.filename, frameinfo.lineno)
                                # print("in_dict['payload']['commits'] is not a list")
                                # print('record_d: ' + str(record_d))
                                return


                else:
                        # frameinfo = getframeinfo(currentframe())
                        # print(frameinfo.filename, frameinfo.lineno)
                        # print("shas is not in in_dict['payload']")
                        # print('record_d: ' + str(record_d))
                        return


        else:
                frameinfo = getframeinfo(currentframe())
                print(frameinfo.filename, frameinfo.lineno)
                print("author name is not in indict!!!!!!!")
                print('"{}": '.format(str(in_dict)) + str(in_dict) + 'EEEEEEEEEEEEEEEEEE')	
                print('record_d: ' + str(record_d))
                return

def get_author_email_helper(in_dict, record_d):
        if 'actor_attributes' in in_dict:
                if isinstance(in_dict['actor_attributes'], dict):
                        if 'email' in in_dict['actor_attributes']:
                                return in_dict['actor_attributes']['email']
                        else:
                                frameinfo = getframeinfo(currentframe())
                                print(frameinfo.filename, frameinfo.lineno)
                                print("email is not in in_dict['actor_attributes']")
                                print('record_d: ' + str(record_d))
                                return

                elif isinstance(in_dict['actor_attributes'], str):
                        print("'{}'['actor_attributes'] is a string!!!!!!".format(in_dict))
                        print('"{}": '.format(in_dict) + str(in_dict) + 'FFFFFFFFFFFFFFFFFFFFF')
                        return
                else:
                        frameinfo = getframeinfo(currentframe())
                        print(frameinfo.filename, frameinfo.lineno)
                        print("in_dict['actor_attributes'] is neither a dict nor string")
                        print('record_d: ' + str(record_d))
                        return

        elif 'commits' in in_dict:      
                if in_dict['commits']:
                        if isinstance(in_dict['commits'][0]['author'], dict):
                                return in_dict['commits'][0]['author']['email']
                        else:
                                frameinfo = getframeinfo(currentframe())
                                print(frameinfo.filename, frameinfo.lineno)	
                                print("in_dict['commits'][0]['author'] is not a dict")
                                print('record_d: ' + str(record_d))
                                return
                else:
                        # frameinfo = getframeinfo(currentframe())
                        # print(frameinfo.filename, frameinfo.lineno)
                        # print("in_dict['commits'] is an empty list")
                        # print('record_d: ' + str(record_d))
                        return


        else:
                frameinfo = getframeinfo(currentframe())
                print(frameinfo.filename, frameinfo.lineno)	
                print("author email is not in indict!!!!!!!")
                print('"{}": '.format(in_dict) + str(in_dict) + 'EEEEEEEEEEEEEEEEEE')
                return

def get_PushEvent(repo_name, created_at, json_payload, record_d, db, commits, commit_past_repo_names):
        commited_at = created_at
        author_name = None
        author_email = None
        message = None

        # frameinfo = getframeinfo(currentframe())
        # print(frameinfo.filename, frameinfo.lineno)
        try:
                # author name
                if 'shas' in json_payload:
                        if json_payload['shas']:
                                if isinstance(json_payload['shas'][0], list):
                                       # print('prwgfqregtngjtngjiwengjnt4jgnwgnjengnerjogenrnfornj')
                                        author_name = get_author_name_helper(json_payload, record_d)
                                else:
                                        frameinfo = getframeinfo(currentframe())
                                        print(frameinfo.filename, frameinfo.lineno)
                                        print("json_payload['shas'][0] is not a list")
                                        print('json_payload: ' + str(json_payload))
                        elif 'actor_attributes' in json_payload:
                                author_name = get_author_name_helper(json_payload, record_d)
                        elif 'actor_attributes' in record_d:
                                author_name = get_author_name_helper(record_d, record_d)
                        else:
                                author_name = None
                                # frameinfo = getframeinfo(currentframe())
                                # print(frameinfo.filename, frameinfo.lineno)
                                # print("json_payload['shas'][0] is an empty list")
                                # print('record_d: ' + str(record_d))
                if 'shas' in record_d:
                        author_name = get_author_name_helper(record_d, record_d)
                if 'commits' in json_payload:
                        author_name = get_author_name_helper(json_payload, record_d)
                if 'commits' in record_d:
                        author_name = get_author_name_helper(record_d, record_d)
                if 'actor_attributes' in json_payload:
                        author_name = get_author_name_helper(json_payload, record_d)
                if 'actor_attributes' in record_d:
                        author_name = get_author_name_helper(record_d, record_d)
                elif 'actor' in record_d:
                        author_name = get_author_name_helper(record_d, record_d)
                elif 'actor' in json_payload:
                        author_name = get_author_name_helper(json_payload, record_d)
                else:
                        print('actor is not in record_d nor payload')
                        frameinfo = getframeinfo(currentframe())
                        print(frameinfo.filename, frameinfo.lineno)
                        print('record_d: ' + str(record_d))

                # author email
                if 'actor_attributes' in record_d:
                        author_email = get_author_email_helper(record_d, record_d)
                elif 'commits' in json_payload:
                        author_email = get_author_email_helper(json_payload, record_d)
                elif 'actor_attributes' in json_payload:
                        author_email = get_author_email_helper(json_payload, record_d)
                else:
                        pass
                        # print('actor_attributes is not in record_d nor payload')
                        # frameinfo = getframeinfo(currentframe())
                        # print(frameinfo.filename, frameinfo.lineno)
                        # print('record_d: ' + str(record_d))


                # author_login
                if 'actor' in record_d:
                        author_login = get_author_login_helper(record_d, record_d)
                elif 'actor' in json_payload:
                        author_login = get_author_login_helper(json_payload, record_d)
                elif 'org' in record_d:
                        author_login = get_author_login_helper(record_d, record_d)
                elif 'org' in json_payload:
                        author_login = get_author_login_helper(json_payload, record_d)
                elif 'actor_attributes' in record_d:
                        author_login = get_author_login_helper(record_d, record_d)
                elif 'actor_attributes' in json_payload:
                        author_login = get_author_login_helper(json_payload, record_d)
                else:
                        print('actor, org, and actor_attributes are in neither record nor payload')
                        frameinfo = getframeinfo(currentframe())
                        print(frameinfo.filename, frameinfo.lineno)
                        print('record_d: ' + str(record_d))



                # message
                if 'message' in record_d:
                        author_email = get_author_email_helper(record_d, record_d)
                        print('message found in record_d!')

                elif 'message' in json_payload:
                        author_email = get_author_email_helper(json_payload, record_d)
                        print('message found in json_payload!')

                else:
                        pass
                        # print('message is not in record_d nor payload')
                        # frameinfo = getframeinfo(currentframe())
                        # print(frameinfo.filename, frameinfo.lineno)
                        # print('record_d: ' + str(record_d))

                

                # commit_id
                if 'shas' in json_payload:
                        commit_id = get_commit_id_helper(json_payload, record_d)
                elif 'shas' in record_d:
                        commit_id = get_commit_id_helper(record_d, record_d)
                elif 'commits' in json_payload:
                        commit_id = get_commit_id_helper(json_payload, record_d)
                elif 'commits' in record_d:
                        commit_id = get_commit_id_helper(record_d, record_d)
                else:
                        print('commit_id not found in record_d nor payload')
                        frameinfo = getframeinfo(currentframe())
                        print(frameinfo.filename, frameinfo.lineno)
                        print('record_d: ' + str(record_d))


        except Exception as e:
                frameinfo = getframeinfo(currentframe())
                print(frameinfo.filename, frameinfo.lineno)	
                print('PUSHEVENT_EXCEPTION: ' + str(e) + 'AAAAAAAAAAAAA')
                print('record_d: ' + str(record_d))
                traceback.print_exc()
                exit(1)

        commit = {'commited_at' : created_at}
        if author_name:
                commit['author_name'] = author_name
        if author_email:
                commit['author_email'] = author_email
        if author_login:
                commit['author_login'] = author_login
        
        if message:
                commit['message'] =  message

        if commit_id:
                commit['commit_id'] =  commit_id

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
  
        # # save in the database
        # try:
        #         db.add_data(full_repo_name, created_at, 'commits', commits_dict)
        # except Exception as e:
        #         print("Failed to save %s PushEvent record at %s: %s" % \
        #                         (full_repo_name, created_at, str(e)))
        #         traceback.print_exc()
        #         frameinfo = getframeinfo(currentframe())
        #         print(frameinfo.filename, frameinfo.lineno)


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