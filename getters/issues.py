import traceback
from inspect import currentframe, getframeinfo
from getters import actors, repos, name

##########################
# Issues Events
##########################


# def get_issue_time_at_helper_a(in_dict, type_at, in_dict_2, created_at):

#         if in_dict['action'] == type_at and isinstance(in_dict_2, dict):
#                 if type_at == 'opened':
#                         # frameinfo = getframeinfo(currentframe())
#                         # print(frameinfo.filename, frameinfo.lineno)
#                         return in_dict_2['created_at']
#                 elif type_at == 'closed':
#                         # frameinfo = getframeinfo(currentframe())
#                         # print(frameinfo.filename, frameinfo.lineno)
#                         return in_dict_2['closed_at']
#                 else:
#                         print("record_d doesn't have 'action'")
#                         frameinfo = getframeinfo(currentframe())
#                         print(frameinfo.filename, frameinfo.lineno)
#                         print('record: ' + str(in_dict))
#                         return created_at


# def get_issue_time_at_helper_b(in_dict, type_at, created_at):

#         if in_dict['action'] == type_at:
#                 if type_at == 'opened':
#                         # frameinfo = getframeinfo(currentframe())
#                         # print(frameinfo.filename, frameinfo.lineno)
#                         return in_dict['created_at']
#                 elif type_at == 'closed':
#                         # frameinfo = getframeinfo(currentframe())
#                         # print(frameinfo.filename, frameinfo.lineno)
#                         return in_dict['closed_at']
#                 else:
#                         print("in_dict doesn't have 'action'")
#                         frameinfo = getframeinfo(currentframe())
#                         print(frameinfo.filename, frameinfo.lineno)
#                         print('in_dict: ' + str(in_dict))
#                         return created_at




# def action_in_helper(created_at, in_dict, type_at):
#         try:  
#                 try:
#                         if isinstance(in_dict['issue'], dict):
#                                 # frameinfo = getframeinfo(currentframe())
#                                 # print(frameinfo.filename, frameinfo.lineno)
#                                 # print('get_issue_time_at_helper_a(in_dict, type_at, in_dict["issue"]["state"]): ' + str(get_issue_time_at_helper_a(in_dict, type_at, in_dict['issue']['state'], created_at)))
#                                 return get_issue_time_at_helper_a(in_dict, type_at, in_dict['issue']['state'], created_at)
#                         elif isinstance(in_dict['issue'], int):
#                                 frameinfo = getframeinfo(currentframe())
#                                 # print(frameinfo.filename, frameinfo.lineno)
#                                 # print('get_issue_time_at_helper_a(in_dict, type_at, in_dict["action"]): ' + str(get_issue_time_at_helper_a(in_dict, type_at, in_dict['action'], created_at)))
#                                 return get_issue_time_at_helper_a(in_dict, type_at, in_dict['action'], created_at)
#                         else:
#                                 # frameinfo = getframeinfo(currentframe())
#                                 # print(frameinfo.filename, frameinfo.lineno)
#                                 # print('It seems like "{}"["issue"] is neither a dict nor an int'.format(in_dict))
#                                 return created_at

#                 except KeyError as ke:
#                         try:
#                                 # frameinfo = getframeinfo(currentframe())
#                                 # print(frameinfo.filename, frameinfo.lineno)
#                                 # print("get_issue_time_at_helper_a(in_dict, type_at, in_dict['milestone']['state']): " + str(get_issue_time_at_helper_a(in_dict, type_at, in_dict['milestone']['state'])))
#                                 return get_issue_time_at_helper_a(in_dict, type_at, in_dict['milestone']['state'], created_at)
#                         except KeyError as ke:
#                                 try:
#                                         # frameinfo = getframeinfo(currentframe())
#                                         # print(frameinfo.filename, frameinfo.lineno)
#                                         return get_issue_time_at_helper_b(in_dict, type_at, created_at)
#                                 except KeyError as ke:
#                                         print("'action' not found in record_d nor json_payload")
#                                         print('record_d: ' + str(in_dict))
#                                         frameinfo = getframeinfo(currentframe())
#                                         print(frameinfo.filename, frameinfo.lineno)
#                                         return created_at
#         except Exception as e:
#                 frameinfo = getframeinfo(currentframe())
#                 print(frameinfo.filename, frameinfo.lineno)
#                 print('record_d: ' + str(in_dict))	
#                 print('ERROR ISSUEEVENT_EXCEPTION get_issue_time_at(created_at, json_payload, record_d, type_at): : ' + str(e))
#                 traceback.print_exc()
#                 exit(1)


# def get_issue_time_at(created_at, json_payload, record_d, type_at):
#         if 'action' in record_d:
#                 # frameinfo = getframeinfo(currentframe())
#                 # print(frameinfo.filename, frameinfo.lineno)
#                 # print('action_in_helper(created_at, record_d, type_at): ' + str(action_in_helper(created_at, record_d, type_at)))
#                 return action_in_helper(created_at, record_d, type_at)
   
#         elif 'action' in json_payload:
#                 # frameinfo = getframeinfo(currentframe())
#                 # print(frameinfo.filename, frameinfo.lineno)
#                 # print('action_in_helper(created_at, json_payload, type_at): ' + str(action_in_helper(created_at, json_payload, type_at)))
#                 # print('record_d: ' + str(record_d))
#                 return action_in_helper(created_at, json_payload, type_at)

#         else:
#                 print('record_d: ' + str(record_d))
#                 frameinfo = getframeinfo(currentframe())
#                 print(frameinfo.filename, frameinfo.lineno)
#                 return


def get_IssuesEvent(repo_name, created_at, json_payload, record_d, db):
        # issue_id = None	   
        # issue_created_at = None
        # issue_closed_at = None
        # description = None
        # user = None
        # try:
        #                 #get issue ID
        #                 if 'issue' in record_d:
        #                         if isinstance(record_d['issue'], int):
        #                                 issue_id = record_d['issue']
        #                         elif isinstance(record_d['issue'], dict):
        #                                 issue_id = record_d['issue']['issue_id']
        #                         else:
        #                                 print('record_d: ' + str(record_d))
        #                                 frameinfo = getframeinfo(currentframe())
        #                                 print(frameinfo.filename, frameinfo.lineno)
        #                                 issue_id = None
        #                                 raise Exception('issue is not an int or a dict')
        #                 elif 'issue' in json_payload:
        #                         if isinstance(json_payload['issue'], int):
        #                                 issue_id = json_payload['issue']
        #                         elif isinstance(json_payload['issue'], dict):
        #                                 if 'id' in json_payload['issue']:
        #                                         issue_id = json_payload['issue']['id']
        #                                 else:
        #                                         print('id is not in json_payload["issue"] when json_payload["issue"] is not a dict')
        #                         else:
        #                                 print('issue is in json_payload but is not an int')
        #                                 print('json_payload: ' + str(json_payload))
        #                                 frameinfo = getframeinfo(currentframe())
        #                                 print(frameinfo.filename, frameinfo.lineno)
        #                 else:
        #                         print('issue is neither in record_d nor json_payload')
        #                         print('json_payload: ' + str(json_payload))
        #                         frameinfo = getframeinfo(currentframe())
        #                         print(frameinfo.filename, frameinfo.lineno)

        #                 try:
        #                         if isinstance(json_payload['issue'], int):
        #                                 issue_id = json_payload['issue']
        #                 except KeyError as ke:
        #                         issue_id = None
        #                         # time_at
        #                 if 'action' in record_d:
        #                         if record_d['action'] == 'opened':
        #                                 issue_created_at = get_issue_time_at(created_at, json_payload, record_d, 'opened')   

        #                         elif record_d['action'] == 'closed':
        #                                 issue_closed_at = get_issue_time_at(created_at, json_payload, record_d, 'closed')
        #                         elif json_payload['action'] == 'reopened':
        #                                 issue_closed_at = get_issue_time_at(created_at, json_payload, record_d, 'opened')

        #                         else:
        #                                 print('action is in record_d but is neither opened nor closed')
        #                                 print('record_d: ' + str(record_d))
        #                                 frameinfo = getframeinfo(currentframe())
        #                                 print(frameinfo.filename, frameinfo.lineno)

        #                 elif 'action' in json_payload:
        #                         if json_payload['action'] == 'opened':
        #                                 issue_created_at = get_issue_time_at(created_at, json_payload, record_d, 'opened')
        #                         elif json_payload['action'] == 'closed':
        #                                 issue_closed_at = get_issue_time_at(created_at, json_payload, record_d, 'closed')
        #                         elif json_payload['action'] == 'reopened':
        #                                 issue_closed_at = get_issue_time_at(created_at, json_payload, record_d, 'opened')

        #                         else:
        #                                 print('action is in json_payload but is neither opened nor closed nor reopened')
        #                                 print('json_payload: ' + str(json_payload))
        #                                 frameinfo = getframeinfo(currentframe())
        #                                 print(frameinfo.filename, frameinfo.lineno)
        #                 else:
        #                         print('action is in neither record_d nor json_payload')
        #                         print('record_d: ' + str(record_d))
        #                         frameinfo = getframeinfo(currentframe())
        #                         print(frameinfo.filename, frameinfo.lineno)	
        # except Exception as e:
        #         frameinfo = getframeinfo(currentframe())
        #         print(frameinfo.filename, frameinfo.lineno)	
        #         print('ERROR ISSUEEVENT_EXCEPTION: ' + str(e))
        #         traceback.print_exc()
        #         exit(1)
        # # print('issue_created_at: ' + str(issue_created_at))
        # # print('issue_closed_at: ' + str(issue_closed_at))
        # # frameinfo = getframeinfo(currentframe())
        # # print(frameinfo.filename, frameinfo.lineno)



        # try:    # get description
        #         description = record_d['body']
        # except KeyError as ke:
        #         description = None

        # try:    # get user
        #         if 'user' in record_d:
        #                 if isinstance(record_d['user'], dict):
        #                         user = record_d['user']['login']
        #         elif 'payload' in record_d:
        #                 if 'actor' in json_payload:
        #                         user = json_payload['actor']
        #                 elif 'actor' in record_d:
        #                         if isinstance(record_d['actor'], str):
        #                                 user = record_d['actor']
        #                         elif isinstance(record_d['actor'], dict):
        #                                 user = record_d['actor']['login']
        #                         else:
        #                                 print('actor in record_d is not a str nor a dict')
        #                                 print('record_d: ' + str(record_d))
        #                                 frameinfo = getframeinfo(currentframe())
        #                                 print(frameinfo.filename, frameinfo.lineno)

        #                 else:
        #                         print('actor is not in json_payload')
        #                         print('reacord_d: ' + str(record_d))
        #                         frameinfo = getframeinfo(currentframe())
        #                         print(frameinfo.filename, frameinfo.lineno)

        #         elif 'actor' in record_d:
        #                 if isinstance(record_d['actor'], str):
        #                         user = record_d['actor']
        #                 else:
        #                         print('is actor a dict?')
        #                         print('record_d: ' + str(record_d))
        #                         frameinfo = getframeinfo(currentframe())
        #                         print(frameinfo.filename, frameinfo.lineno)

        #         elif 'user' in record_d['issue']:
        #                 if isinstance(record_d['issue'], dict):
        #                         if isinstance(record_d['issue']['user'], dict):
        #                                 user = record_d['issue']['user']['login']
        #                         else:
        #                                 print('record_d: ' + str(record_d))
        #                                 print("record_d['issue']['user'] is not a dict")
        #                                 frameinfo = getframeinfo(currentframe())
        #                                 print(frameinfo.filename, frameinfo.lineno)
        #                 else:
        #                         print('record_d: ' + str(record_d))
        #                         print("record_d['issue'] is not a dict")
        #                         frameinfo = getframeinfo(currentframe())
        #                         print(frameinfo.filename, frameinfo.lineno)


        #         else:   
        #                 print("Seems like record_d doesn't contain user_id record_d: " + str(record_d))
        #                 user = None
        # except KeyError as ke:

        #         print('Trying to find username: ' + print(str(ke)))
        #         print('record_d: ' + str(record_d))
        #         frameinfo = getframeinfo(currentframe())
        #         print(frameinfo.filename, frameinfo.lineno)	
        # try:
        #         if isinstance(record_d['issue'], dict):
        #                 if isinstance(record_d['issue']['assignee'], dict):
        #                         assignee = record_d['issue']['assignee']['id']
        #                 else:
        #                         print('record_d: ' + str(record_d))
        #                         print("record_d['issue']['assignee'] is not a dict")
        #                         frameinfo = getframeinfo(currentframe())
        #                         print(frameinfo.filename, frameinfo.lineno)
        #         else:
        #                 print('record_d: ' + str(record_d))
        #                 print("record_d['issue'] is not a dict")
        #                 frameinfo = getframeinfo(currentframe())
        #                 print(frameinfo.filename, frameinfo.lineno)
        #                 assignee = None

        # except KeyError as ke:
        #         assignee = None
        # try:    # get title
        #         if isinstance(record_d['issue'], dict):
        #                 title = record_d['issue']['title']
        # except KeyError as ke:
        #         try:
        #                 if 'title' in record_d:
        #                         title = record_d['title']
        #                 else:
        #                         # print('record_d: ' + str(record_d))
        #                         # print("it looks like title isn't in record_d")
        #                         # frameinfo = getframeinfo(currentframe())
        #                         # print(frameinfo.filename, frameinfo.lineno)
        #                         title = None
        #         except KeyError as ke:
        #                 title = None
        # except Exception as e:
        #         frameinfo = getframeinfo(currentframe())
        #         print(frameinfo.filename, frameinfo.lineno)	
        #         print('record_d: ' + str(record_d))
        #         print('ISSUEEVENT_EXCEPTION: ' + str(e))
        #         traceback.print_exc()
        #         exit(1)

        # if description:
        #         print('description: ' + str(description))
        # else:
        #         print('description is NONE')
        #         print('record_d: ' + str(record_d))

        # if assignee:
        #         print('assignee: ' + str(assignee))
        # else:
        #         print('assignee is NONE')
        #         print('record_d: ' + str(record_d))


        # if title:
        #         print('title: ' + str(title))
        # else:
        #         print('title is NONE')
        #         print('record_d: ' + str(record_d))

        # if issue_closed_at:
        #         print('issue_closed_at: ' + str(issue_closed_at))
        # else:
        #         print('issue_closed_at is NONE')
        #         print('record_d: ' + str(record_d))

        # if issue_created_at:
        #         print('issue_created_at: ' + str(issue_created_at))
        # else:
        #         print('issue_created_at is NONE')
        #         print('record_d: ' + str(record_d))
        
        
        # issues_dict = {'issue_created_at' : issue_created_at}
        # if issue_id:
        #         issues_dict['ID'] = issue_id

        # if issue_closed_at:
        #         issues_dict['closed_at'] = issue_closed_at

        # if description:
        #         issues_dict['description'] = description

        # if user:
        #         issues_dict['user'] = user

        # if assignee:
        #         issues_dict['assignee'] = assignee

        # if title:
        #         issues_dict['title'] = title

        full_repo_name = name.get_full_repo_name(json_payload, record_d, repo_name)

        # # save in the database
        # try:
        #         db.add_data(full_repo_name, created_at, 'issues', issues_dict)
        # except Exception as e:
        #         print("Failed to save %s IssuesEvent record at %s: %s" % \
        #                         (full_repo_name, created_at, str(e)))
                # traceback.print_exc()




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
        #                 print('KEYERROR RELEASEEVENT_EXCEPTION: ' + str(ke))
        #                 exit(1)

        # except Exception as e:
        #         frameinfo = getframeinfo(currentframe())
        #         print(frameinfo.filename, frameinfo.lineno)	
        #         print('ERROR RELEASEEVENT_EXCEPTION: ' + str(e))
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
