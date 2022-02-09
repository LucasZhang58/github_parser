import html
from platform import release
import traceback
import json
import os
import sys
from inspect import currentframe, getframeinfo



##########################
# Fork Events
##########################

def get_ForkEvent(repo_name, created_at, json_payload, db):


        try:
                if isinstance(json_payload['forkee'], int):
                        forkee = json_payload['forkee']
                else:
                        forkee = json_payload['forkee']['id']
        except KeyError as ke:
     
                forkee = None
        except Exception as e:
                frameinfo = getframeinfo(currentframe())
                print(frameinfo.filename, frameinfo.lineno)     
                print('FORKEVENT_EXCEPTION: ' + str(e))
                exit(1)

        try:
                if isinstance(json_payload['forkee'], int):
                        created_at = created_at
                else:
                        created_at = json_payload['forkee']['created_at']
        except KeyError as ke:
     
                created_at = created_at
        except Exception as e:
                created_at = created_at
                frameinfo = getframeinfo(currentframe())
                print(frameinfo.filename, frameinfo.lineno)     
                print('FORKEVENT_EXCEPTION: ' + str(e))
                exit(1)

        try:
                if isinstance(json_payload['forkee'], int):
                        updated_at = None
                else:
                        updated_at = json_payload['forkee']['updated_at']
        except KeyError as ke:
     
                updated_at = None
        except Exception as e:
                frameinfo = getframeinfo(currentframe())
                print(frameinfo.filename, frameinfo.lineno)     
                print('FORKEVENT_EXCEPTION: ' + str(e))
                exit(1)

        try:
                if isinstance(json_payload['forkee'], int):
                        pushed_at = None
                else:
                        pushed_at = json_payload['forkee']['pushed_at']
        except KeyError as ke:
     
                pushed_at = None
        except Exception as e:
                frameinfo = getframeinfo(currentframe())
                print(frameinfo.filename, frameinfo.lineno)     
                print('FORKEVENT_EXCEPTION: ' + str(e))
                exit(1)

        try:
                if isinstance(json_payload['forkee'], int):
                        description = None
                else:
                        description = json_payload['forkee']['description']
        except KeyError as ke:
     
                description = None
        except Exception as e:
                frameinfo = getframeinfo(currentframe())
                print(frameinfo.filename, frameinfo.lineno)     
                print('FORKEVENT_EXCEPTION: ' + str(e))
                exit(1)

        try:
                if isinstance(json_payload['forkee'], int):
                        language = None
                else:
                        language = json_payload['forkee']['language']
        except KeyError as ke:
     
                language = None
        except Exception as e:
                frameinfo = getframeinfo(currentframe())
                print(frameinfo.filename, frameinfo.lineno)     
                print('FORKEVENT_EXCEPTION: ' + str(e))
                exit(1)

        try:
                if isinstance(json_payload['forkee'], int):
                        size = None
                else:
                        size = json_payload['forkee']['size']
        except KeyError as ke:
     
                size = None
        except Exception as e:
                frameinfo = getframeinfo(currentframe())
                print(frameinfo.filename, frameinfo.lineno)     
                print('FORKEVENT_EXCEPTION: ' + str(e))
                exit(1)
        try:
                if isinstance(json_payload['forkee'], int):
                        watchers = None
                else:
                        watchers = json_payload['forkee']['watchers']
        except KeyError as ke:
     
                watchers = None
        except Exception as e:
                frameinfo = getframeinfo(currentframe())
                print(frameinfo.filename, frameinfo.lineno)     
                print('FORKEVENT_EXCEPTION: ' + str(e))
                exit(1)

        forks_dict = { 'created_at' : created_at}

        if forkee:
                forks_dict['forkee'] = forkee

        if updated_at:
                forks_dict['updated_at'] = updated_at

        if pushed_at:
                forks_dict['pushed_at'] = pushed_at

        if description:
                forks_dict['description'] = description

        if language:
                forks_dict['language'] = language

        if size:
                forks_dict['size'] = size
        
        if watchers:
                forks_dict['watchers'] = watchers


        
   


        # save in the database
        try:
                db.add_data(repo_name, created_at, 'forks', forks_dict)
        except Exception as e:
                print("Failed to save %s ForkEvent record at %s: %s" % \
                                (repo_name, created_at, str(e)))





        # event_type = 'ForkEvent'

        # get_Person(repo_name, created_at, json_payload, output_path, lock, event_type)

