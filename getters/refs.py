from platform import release
import traceback
import json
import os
import sys
from inspect import currentframe, getframeinfo
from getters import repos, persons


##########################
# Create Events
##########################

def get_CreateEvent(repo_name, created_at, json_payload, db, record_d, ref_past_repo_names):

        if '"payload":' in str(record_d): #if payload is in the record
                if json_payload['ref_type'] == 'branch':
                        try:
                                branch_name = json_payload['ref']
                                
                        except KeyError as ke:
                                print('GET_CREATEEVENT_KEYERROR: ' + str(ke))
                                branch_name = None
                        except Exception as e:

                                frameinfo = getframeinfo(currentframe())
                                print(frameinfo.filename, frameinfo.lineno)     
                                print('CREATEEVENT_EXCEPTION: ' + str(e))
                                traceback.print_exc()
                                exit(1)


                else: #equal to 'tag'
                        try:
                                tag_name = json_payload['ref']
                                
                        except KeyError as ke:
                                print('GET_CREATEVENT_KEYERROR: ' + str(ke))
                                tag_name = None
                        except Exception as e:

                                frameinfo = getframeinfo(currentframe())
                                print(frameinfo.filename, frameinfo.lineno)     
                                print('CREATEEVENT_EXCEPTION: ' + str(e))
                                traceback.print_exc()
                                exit(1)


                try:
                        created_at = json_payload['created_at']
                        
                except KeyError as ke:
                        created_at = created_at
                except Exception as e:

                        frameinfo = getframeinfo(currentframe())
                        print(frameinfo.filename, frameinfo.lineno)     
                        print('CREATEEVENT_EXCEPTION: ' + str(e))
                        traceback.print_exc()
                        exit(1)
                        
##################################################################
        else: #if payload isn't in the record
                if record_d['ref'] == 'branch':

                        try:
                                branch_name = record_d['ref']
                                
                        except KeyError as ke:
                                print('GET_CREATEVENT_KEYERROR: ' + str(ke))
                                branch_name = None
                        except Exception as e:

                                frameinfo = getframeinfo(currentframe())
                                print(frameinfo.filename, frameinfo.lineno)     
                                print('CREATEEVENT_EXCEPTION: ' + str(e))
                                traceback.print_exc()
                                exit(1)

                else:
                        try:
                                tag_name = record_d['ref']
                                
                        except KeyError as ke:
                                print('GET_CREATEVENT_KEYERROR: ' + str(ke))
                                tag_name = None
                        except Exception as e:

                                frameinfo = getframeinfo(currentframe())
                                print(frameinfo.filename, frameinfo.lineno)     
                                print('CREATEEVENT_EXCEPTION: ' + str(e))
                                traceback.print_exc()
                                exit(1)

                try:
                        created_at = record_d['created_at']
                        
                except KeyError as ke:
                        created_at = created_at
                except Exception as e:

                        frameinfo = getframeinfo(currentframe())
                        print(frameinfo.filename, frameinfo.lineno)     
                        print('CREATEEVENT_EXCEPTION: ' + str(e))
                        traceback.print_exc()
                        exit(1)

 

        branch_dict = {}
        if created_at:
                branch_dict['created_at'] = created_at
        
        if branch_name:
                branch_dict['branch_name'] = branch_name
    
        
        tag_dict = {}
        if created_at:
                tag_dict['created_at'] = created_at
        
        if tag_name:
                tag_dict['tag_name'] = tag_name






        if branch_name:
                if branch_name not in str(ref_past_repo_names['{}'.format(repo_name)]['branches']) and not ref_past_repo_names['{}'.format(repo_name)]['branches']:
                        ref_past_repo_names['{}'.format(repo_name)]['branches'] = [branch_dict]
                else:
                        ref_past_repo_names['{}'.format(repo_name)]['branches'].append(branch_dict)


        if tag_name:
                if tag_name not in str(ref_past_repo_names['{}'.format(repo_name)]['tag']) and not ref_past_repo_names['{}'.format(repo_name)]['branches']:
                        ref_past_repo_names['{}'.format(repo_name)]['tag'] = [tag_dict]
                else:
                        ref_past_repo_names['{}'.format(repo_name)]['tag'].append(tag_dict)




        # save in the database
        try:
                db.add_data(repo_name, created_at, 'refs', ref_past_repo_names['{}'.format(repo_name)])
        except Exception as e:
                print("Failed to save %s ref output at %s: %s" % \
                                (repo_name, created_at, str(e)))
                traceback.print_exc()


        event_type = 'CreateEvent'

        repos.get_Repo(repo_name, created_at, json_payload, record_d, db, event_type)

        persons.get_Person(repo_name, created_at, json_payload, record_d, db, event_type)