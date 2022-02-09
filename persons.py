import html
from platform import release
import traceback
import json
import os
import sys
from inspect import currentframe, getframeinfo





##########################
# Person
##########################

def get_Person(repo_name, created_at, json_payload, db, event_type):
        login = None
        id = None
        avatar_url = None
        type = None
        gravatar_id = None
        url = None

        # RELEASE EVENT
        if event_type == 'ReleaseEvent':
                try:
                        login = json_payload['release']['author']['login']
                except KeyError as ke:
                        print(str(ke))
                        login = None
                except Exception as e:

                        login = None
                        frameinfo = getframeinfo(currentframe())
                        print(frameinfo.filename, frameinfo.lineno)     
                        print('PERSONEVENT_EXCEPTION: ' + str(e))
                        exit(1)

                try:
                        id = json_payload['release']['author']['id']
                except KeyError as ke:
                        print(str(ke))
                        id = None
                except Exception as e:
                        id = None
                        frameinfo = getframeinfo(currentframe())
                        print(frameinfo.filename, frameinfo.lineno)     
                        print('PERSONEVENT_EXCEPTION: ' + str(e))
                        exit(1)

                try:
                        avatar_url = json_payload['release']['author']['avatar_url']
                except KeyError as ke:
                        print(str(ke))
                        avatar_url = None
                except Exception as e:
                        print(str(e))
                        avatar_url = None
                        frameinfo = getframeinfo(currentframe())
                        print(frameinfo.filename, frameinfo.lineno)     
                        print('PERSONEVENT_EXCEPTION: ' + str(e))
                        exit(1)
                        
                type = 'author'

                try:
                        gravatar_id = json_payload['release']['author']['gravatar_id']
                except KeyError as ke:
                        print(str(ke))
                        gravatar_id = None
                except Exception as e:
                        gravatar_id = None
                        frameinfo = getframeinfo(currentframe())
                        print(frameinfo.filename, frameinfo.lineno)     
                        print('PERSONEVENT_EXCEPTION: ' + str(e))
                        exit(1)
                        
                try:
                        url = json_payload['release']['author']['url']
                except KeyError as ke:
                        print(str(ke))
                        url = None
                except Exception as e:
                        url = None
                        frameinfo = getframeinfo(currentframe())
                        print(frameinfo.filename, frameinfo.lineno)     
                        print('PERSONEVENT_EXCEPTION: ' + str(e))
                        exit(1)
                        


        # FORK EVENT
        if event_type == 'ForkEvent':
                try:
                        login = json_payload['forkee']['owner']['login']
                except KeyError as ke:
                        print(str(ke))
                        login = None
                except Exception as e:
                        login = None
                        frameinfo = getframeinfo(currentframe())
                        print(frameinfo.filename, frameinfo.lineno)     
                        print('PERSONEVENT_EXCEPTION: ' + str(e))
                        exit(1)

                try:
                        id = json_payload['forkee']['owner']['id']
                except KeyError as ke:
                        print(str(ke))
                        id = None
                except Exception as e:
                        id = None
                        frameinfo = getframeinfo(currentframe())
                        print(frameinfo.filename, frameinfo.lineno)     
                        print('PERSONEVENT_EXCEPTION: ' + str(e))
                        exit(1)

                try:
                        avatar_url = json_payload['forkee']['owner']['avatar_url']
                except KeyError as ke:
                        print(str(ke))
                        avatar_url = None
                except Exception as e:
                        avatar_url = None
                        frameinfo = getframeinfo(currentframe())
                        print(frameinfo.filename, frameinfo.lineno)     
                        print('PERSONEVENT_EXCEPTION: ' + str(e))
                        exit(1)
                        


                type = 'owner'

                        
                try:
                        gravatar_id = json_payload['forkee']['owner']['gravatar_id']
                except KeyError as ke:
                        print(str(ke))
                        gravatar_id = None
                except Exception as e:
                        gravatar_id = None
                        frameinfo = getframeinfo(currentframe())
                        print(frameinfo.filename, frameinfo.lineno)     
                        print('PERSONEVENT_EXCEPTION: ' + str(e))
                        exit(1)
                        
                try:
                        url = json_payload['forkee']['owner']['url']
                except KeyError as ke:
                        print(str(ke))
                        url = None
                except Exception as e:
                        url = None
                        frameinfo = getframeinfo(currentframe())
                        print(frameinfo.filename, frameinfo.lineno)     
                        print('PERSONEVENT_EXCEPTION: ' + str(e))
                        exit(1)

                # MEMBER EVENT
                if event_type == 'MemberEvent':
                        try:
                                login = json_payload['member']['login']
                        except KeyError as ke:
                                print(str(ke))
                                login = None
                        except Exception as e:
                                login = None
                                frameinfo = getframeinfo(currentframe())
                                print(frameinfo.filename, frameinfo.lineno)     
                                print('PERSONEVENT_EXCEPTION: ' + str(e))
                                exit(1)

                        try:
                                id = json_payload['member']['id']
                        except KeyError as ke:
                                print(str(ke))
                                id = None
                        except Exception as e:
                                id = None
                                frameinfo = getframeinfo(currentframe())
                                print(frameinfo.filename, frameinfo.lineno)     
                                print('PERSONEVENT_EXCEPTION: ' + str(e))
                                exit(1)

                        try:
                                avatar_url = json_payload['member']['avatar_url']
                        except KeyError as ke:
                                print(str(ke))
                                avatar_url = None
                        except Exception as e:
                                avatar_url = None
                                frameinfo = getframeinfo(currentframe())
                                print(frameinfo.filename, frameinfo.lineno)     
                                print('PERSONEVENT_EXCEPTION: ' + str(e))
                                exit(1)
                                


                        type = 'member'

                                
                        try:
                                gravatar_id = json_payload['member']['gravatar_id']
                        except KeyError as ke:
                                print(str(ke))
                                gravatar_id = None
                        except Exception as e:
                                gravatar_id = None
                                frameinfo = getframeinfo(currentframe())
                                print(frameinfo.filename, frameinfo.lineno)     
                                print('PERSONEVENT_EXCEPTION: ' + str(e))
                                exit(1)
                                
                        try:
                                url = json_payload['member']['url']
                        except KeyError as ke:
                                print(str(ke))
                                url = None
                        except Exception as e:
                                url = None
                                frameinfo = getframeinfo(currentframe())
                                print(frameinfo.filename, frameinfo.lineno)     
                                print('PERSONEVENT_EXCEPTION: ' + str(e))
                                exit(1)

                # ISSUE EVENT
                if event_type == 'IssuesEvent':
                        if isinstance(json_payload['issue'], dict):
                                try:
                                        login = json_payload['issue']['user']['login']
                                except KeyError as ke:
                                        print(str(ke))
                                        login = None
                                except Exception as e:
                                        login = None
                                        frameinfo = getframeinfo(currentframe())
                                        print(frameinfo.filename, frameinfo.lineno)     
                                        print('PERSONEVENT_EXCEPTION: ' + str(e))
                                        exit(1)

                                try:
                                        id = json_payload['issue']['user']['id']
                                except KeyError as ke:
                                        print(str(ke))
                                        id = None
                                except Exception as e:
                                        id = None
                                        frameinfo = getframeinfo(currentframe())
                                        print(frameinfo.filename, frameinfo.lineno)     
                                        print('PERSONEVENT_EXCEPTION: ' + str(e))
                                        exit(1)

                                try:
                                        avatar_url = json_payload['issue']['user']['avatar_url']
                                except KeyError as ke:
                                        print(str(ke))
                                        avatar_url = None
                                except Exception as e:
                                        avatar_url = None
                                        frameinfo = getframeinfo(currentframe())
                                        print(frameinfo.filename, frameinfo.lineno)     
                                        print('PERSONEVENT_EXCEPTION: ' + str(e))
                                        exit(1)
                                        


                                type = 'user'

                                        
                                try:
                                        gravatar_id = json_payload['issue']['user']['gravatar_id']
                                except KeyError as ke:
                                        print(str(ke))
                                        gravatar_id = None
                                except Exception as e:
                                        gravatar_id = None
                                        frameinfo = getframeinfo(currentframe())
                                        print(frameinfo.filename, frameinfo.lineno)     
                                        print('PERSONEVENT_EXCEPTION: ' + str(e))
                                        exit(1)
                                        
                                try:
                                        url = json_payload['issue']['user']['url']
                                except KeyError as ke:
                                        print(str(ke))
                                        url = None
                                except Exception as e:
                                        url = None
                                        frameinfo = getframeinfo(currentframe())
                                        print(frameinfo.filename, frameinfo.lineno)     
                                        print('PERSONEVENT_EXCEPTION: ' + str(e))
                                        exit(1)
                        else:
                                return
                                        
                                        
                

                        person_dict = {
                                'login' : login,
                                'id' : id,
                                'avatar_url' : avatar_url,
                                'type' : type,
                                'gravatar_id' : gravatar_id,
                                'url' : url
                        }


                        if '/' in repo_name:
                                user_id, repo_name = repo_name.split('/')
                        else:
                                repo_name = repo_name
                                user_id = None

                        # check if user dir exist
                        if user_id != None:
                                user_dir_path = os.path.join(output_path, user_id)
                        else:
                                user_dir_path = output_path

                        if not os.path.exists(user_dir_path):
                                os.mkdir(user_dir_path)

                        repo_dir_path = os.path.join(user_dir_path, repo_name)
                        if not os.path.exists(repo_dir_path):
                                os.mkdir(repo_dir_path)

                        completeName = os.path.join(repo_dir_path, 'person_' + str(user_id) + ".json")


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
                                        print('getPerson: Exit')
                                        exit(1)


                        data = person_dict

                        output_file_data = json.dumps(data)
                        with open(completeName, 'w') as f:
                                f.write(output_file_data)
