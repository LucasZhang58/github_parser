import html
from platform import release
import traceback
import json
import os
import sys
from inspect import currentframe, getframeinfo


##########################
# REPO
##########################

def get_Repo(repo_name, created_at, json_payload, db, event_type):

        repo_name = repo_name
        repo_url = None

        created_at = None

        repo_description = None
        repo_homepage = None
        size = None
        language = None
        license = None
        owner = None
        is_forked = None

        # Get repo_name an repo_url
        if isinstance(json_payload['repo'], dict):
                try:
                        repo_url = json_payload['repo']['url']
                        
                except KeyError as ke:

                        repo_url = None
                except Exception as e:
                        frameinfo = getframeinfo(currentframe())
                        print(frameinfo.filename, frameinfo.lineno)     
                        print('GET_REPO_EXCEPTION: ' + str(e))
                        exit(1)

                try:
                        repo_name = json_payload['repo']['name']
                        
                except KeyError as ke:

                        repo_name = repo_name
                except Exception as e:
                        frameinfo = getframeinfo(currentframe())
                        print(frameinfo.filename, frameinfo.lineno)     
                        print('GET_REPO_EXCEPTION: ' + str(e))
                        exit(1)

        else: 
                repo_name = repo_name
                repo_url = None


        # CreateEvent has created_at and repo_description
        if event_type == 'CreateEvent':
                if json_payload['ref_type'] == 'branch' and json_payload['ref'] == 'master':
                        created_at = created_at
                else:
                        created_at = None

        # ForkEvent may have language. owner, and is_forked
        if event_type == 'ForkEvent':
                pass




        repo_dict = {
                        'repo_name' : repo_name,
                        'repo_url' : repo_url,
                        'created_at' : created_at,
                        'repo_description' :  repo_description,
                        'repo_homepage' : repo_homepage,
                        'size' : size,
                        'language' : language,
                        'license' : license,
                        'owner' : owner,
                        'is_forked' : is_forked
                }

        if '/' in repo_name:
                user_id, repo_name = repo_name.split('/')
        else:
                repo_name = repo_name
                user_id = None

        if user_id != None:
                user_dir_path = os.path.join(output_path, user_id)
        else:
                user_dir_path = output_path

        if not os.path.exists(user_dir_path):
                os.mkdir(user_dir_path)

        repo_dir_path = os.path.join(user_dir_path, repo_name)
        if not os.path.exists(repo_dir_path):
                os.mkdir(repo_dir_path)

        completeName = os.path.join(repo_dir_path, 'repo_' + str(user_id) + ".json")


        # if file exists, load prev data		
        if os.path.exists(completeName):
                try:
                        with open(completeName, 'r') as f:
                                d = f.read()
                                data = json.loads(d)
                except Exception as e:
                        frameinfo = getframeinfo(currentframe())
                        print(frameinfo.filename, frameinfo.lineno)     
                        print(str(e))
                        print('getRepo: Exit')
                        exit(1)


        data = repo_dict

        output_file_data = json.dumps(data)
        with open(completeName, 'w') as f:
                f.write(output_file_data)






