from platform import release
import traceback
import json
import os
import sys
from inspect import currentframe, getframeinfo
from getters import repos, persons
import getters.name as name

##########################
# Create Events
##########################
def get_attributes(json_payload, record_d):
        try:
                try:
                        type_name = json_payload['ref']
                except KeyError as ke:
                        try:
                                type_name = record_d['ref']
                        except KeyError as ke:
                                try:
                                        type_name = record_d['name']
                                except KeyError as ke:
                                        type_name = None
                try:
                        return type_name, json_payload['created_at']
                except KeyError as ke:
                        record_created_at = None
                        return type_name, record_created_at
        except Exception as e:
                print('record_d: ' + str(record_d))
                frameinfo = getframeinfo(currentframe())
                print(frameinfo.filename, frameinfo.lineno)	
                print('get_attributes CREATEEVENT_EXCEPTION: ' + str(e))
                traceback.print_exc()
                exit(1)

def get_CreateEvent(repo_name, created_at, json_payload, record_d, db, ref_past_repo_names):
        try:
                try:

                        if json_payload['ref_type'] == 'branch':
                                branch_name, record_created_at = get_attributes(json_payload, record_d)
                                ref_helper(repo_name, created_at, record_d, json_payload, db, branch_name, record_created_at, ref_past_repo_names, 'branch')

                except KeyError as ke:
                        try:
                                if json_payload['object'] == 'branch':
                                        branch_name, record_created_at = get_attributes(json_payload, record_d)
                                        ref_helper(repo_name, created_at, record_d, json_payload, db, branch_name, record_created_at, ref_past_repo_names, 'branch')

                        except KeyError as ke:
                                try:
                                        if record_d['ref_type'] == 'branch':
                                                branch_name, record_created_at = get_attributes(json_payload, record_d)
                                                ref_helper(repo_name, created_at, record_d, json_payload, db, branch_name, record_created_at, ref_past_repo_names, 'branch')
                                except KeyError as ke:
                                        pass

                try:
                        if json_payload['ref_type'] == 'tag':
                                tag_name, record_created_at = get_attributes(json_payload, record_d)
                                ref_helper(repo_name, created_at, record_d, json_payload, db, tag_name, record_created_at, ref_past_repo_names, 'tag')
                except KeyError as ke:	
                        try:
                                if json_payload['object'] == 'tag':
                                        branch_name, record_created_at = get_attributes(json_payload, record_d)
                                        ref_helper(repo_name, created_at, record_d, json_payload, db, branch_name, record_created_at, ref_past_repo_names, 'branch')		
                        except KeyError as ke:
                                try:
                                        if record_d['ref_type'] == 'tag':
                                                branch_name, record_created_at = get_attributes(json_payload, record_d)
                                                ref_helper(repo_name, created_at, record_d, json_payload, db, branch_name, record_created_at, ref_past_repo_names, 'branch')	
                                except KeyError as ke:
                                        pass

                try:
                        if json_payload['ref_type'] == 'repository':
                                tag_name, record_created_at = get_attributes(json_payload, record_d)
                                ref_helper(repo_name, created_at, record_d, json_payload, db, tag_name, record_created_at, ref_past_repo_names, 'tag')
                except KeyError as ke:	
                        try:
                                if json_payload['object'] == 'repository':
                                        branch_name, record_created_at = get_attributes(json_payload, record_d)
                                        ref_helper(repo_name, created_at, record_d, json_payload, db, branch_name, record_created_at, ref_past_repo_names, 'branch')		
                        except KeyError as ke:
                                try:
                                        if record_d['ref_type'] == 'repository':
                                                branch_name, record_created_at = get_attributes(json_payload, record_d)
                                                ref_helper(repo_name, created_at, record_d, json_payload, db, branch_name, record_created_at, ref_past_repo_names, 'branch')	
                                except KeyError as ke:
                                        pass
        except Exception as e:
                print('record_d: ' + str(record_d) + ' is of type ' + str(record_d))
                frameinfo = getframeinfo(currentframe())
                print(frameinfo.filename, frameinfo.lineno)	
                print('get_CreateEvent CREATEEVENT_EXCEPTION: ' + str(e))
                traceback.print_exc()
                exit(1)

def ref_helper(repo_name, created_at, record_d, json_payload, db, type_name, record_created_at, ref_past_repo_names, ref_type):
        try:
                full_repo_name = name.get_full_repo_name(json_payload, record_d, repo_name)

                #create type_dict to append to the branches, tag, or repository key-value pair
                type_dict = {}
                if record_created_at:
                        type_dict['record_created_at'] = record_created_at
                if type_name:
                        try:
                                type_dict['{}_name'.format(ref_type)] = type_name
                        except KeyError as ke:
                                print('re_helper, type_name Error: ' + str(ke))
                ref_type_plural = ''
                if ref_type == 'branch':
                        ref_type_plural = 'branches'

                if ref_type == 'tag':
                        ref_type_plural = 'tags'

                if ref_type == 'repository':
                        ref_type_plural = 'repositories'

                try:
                        if  full_repo_name not in  ref_past_repo_names:
                                ref_past_repo_names[full_repo_name] = {ref_type_plural : [type_dict]}
                                #print(ref_past_repo_names['{}'.format(full_repo_name)])
                        else:
                                if ref_type_plural not in ref_past_repo_names[full_repo_name]:
                                        ref_past_repo_names[full_repo_name][ref_type_plural] = [type_dict]
                                else:
                                        ref_past_repo_names[full_repo_name][ref_type_plural].append(type_dict)
                except KeyError as ke:
                        print('KEYERROR re_helper, if full_repo_name not in ref_past_repo_names["{}".format(full_repo_name)] and not ref_past_repo_names["{}".format(full_repo_name)]: ' + str(ke))
                        traceback.print_exc()

                # save in the database
                try:
                        db.add_data(full_repo_name, created_at, 'refs', type_dict)
                except Exception as e:
                        print("Failed to save %s ref output at %s: %s" % \
                                        (full_repo_name, created_at, str(e)))
                        traceback.print_exc()

                # save repo informtion
                try:
                        r_dict = record_d['repo']
                except KeyError as ke:
                        try:
                                r_dict = record_d['repository']
                        except KeyError as ke:
                                frameinfo = getframeinfo(currentframe())
                                print(frameinfo.filename, frameinfo.lineno)	
                                print('KEYERROR CREATEEVENT_EXCEPTION: ' + str(ke))
                                exit(1)
                except Exception as e:
                        frameinfo = getframeinfo(currentframe())
                        print(frameinfo.filename, frameinfo.lineno)	
                        traceback.print_exc()
                        print('ERROR CREATEEVENT_EXCEPTION: ' + str(e))
                        exit(1)

                if isinstance(r_dict, dict):
                        repos.get_Repo(full_repo_name, created_at, json_payload, record_d, r_dict, db)

                # save person information
                try:
                        if isinstance(record_d['actor'], dict):
                                p_dict = record_d['actor']
                                persons.get_Person(full_repo_name, created_at, json_payload, record_d, p_dict, db)
                        elif isinstance(record_d['actor_attributes'], dict):
                                        p_dict = record_d['actor_attributes']
                                        persons.get_Person(full_repo_name, created_at, json_payload, record_d, p_dict, db)
                        else:
                                print("record_d: " + str(record_d))
                                print("HAVEN'T FOUND P_DICT")
                except KeyError as ke:
                        exit(1)
                except Exception as e:
                        frameinfo = getframeinfo(currentframe())
                        print(frameinfo.filename, frameinfo.lineno)	
                        print('ERROR CREATEEVENT_EXCEPTION: ' + str(e))
                        traceback.print_exc()
                        exit(1)

                full_repo_name = name.get_full_repo_name(json_payload, record_d, repo_name)

                if isinstance(p_dict, dict):
                        persons.get_Person(full_repo_name, created_at, json_payload, record_d, p_dict, db)
                else:
                        print('p_dict: ' + str(p_dict))
                        print('P_DICT IS NOT A DICT!!!!!!!!!!!!!!!!')
        except Exception as e:
                print('record_d: ' + str(record_d) + ' is of type ' + str(record_d))
                frameinfo = getframeinfo(currentframe())
                print(frameinfo.filename, frameinfo.lineno)	
                print('ref_helper CREATEEVENT_EXCEPTION: ' + str(e))
                traceback.print_exc()
                exit(1)




        