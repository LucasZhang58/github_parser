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
# Issues Events
##########################

def get_IssuesEvent(repo_name, created_at, json_payload, record_d, db):
        issue_id = None	   
        issue_created_at = None
        issue_closed_at = None
        description = None
        user = None
        try:
                try:    #get issue ID
                        if isinstance(record_d['issue'], int):
                                issue_id = record_d['issue']
                        elif isinstance(record_d['issue'], dict):
                                issue_id = record_d['issue']['issue_id']
                        elif isinstance(json_payload['issue'], int):
                                issue_id = json_payload['issue']
                        else:
                                print('record_d: ' + str(record_d))
                                issue_id = None
                                raise Exception('issue is not an int or a dict')
                except KeyError as ke:
                        issue_id = None
                try:    #Get issue_created_at when action is equal to open
                        if record_d['action'] == 'opened' and isinstance(record_d['issue'], dict):
                                issue_created_at = record_d['issue']['created_at']
                        elif record_d['action'] == 'opened' and isinstance(record_d['milesone'], dict):
                                issue_created_at = record_d['milestone']['created_at']
                        else:
                                issue_created_at = None
                except KeyError as ke:
                        issue_created_at = None

                try:  #Get issue_closed_at when action is equal to closed
                        if record_d['action'] == 'closed' and isinstance(record_d['issue'], dict):
                                issue_closed_at = record_d['issue']['created_at']

                        elif record_d['action'] == 'closed' and isinstance(record_d['milestone'], dict):
                                issue_closed_at = record_d['milestone']['created_at']
                                
                        else:
                                issue_closed_at = None
                               # raise Exception('issue_closed_at is nethier in record_d["issue"] not record_d["milestone"]')
                except KeyError as ke:
                        issue_closed_at = None

                try:    # get description
                        description = record_d['body']
                except KeyError as ke:
                        description = None

                try:    # get user
                        if 'user' in record_d:
                                if isinstance(record_d['user'], dict):
                                        user = record_d['user']['id']
                        elif 'user' in record_d['issue']:
                                if isinstance(record_d['issue'], dict):
                                        if isinstance(record_d['issue']['user'], dict):
                                                user = record_d['issue']['user']['id']
                                        else:
                                                print('record_d: ' + str(record_d))
                                                print("record_d['issue']['user'] is not a dict")
                                else:
                                        print('record_d: ' + str(record_d))
                                        print("record_d['issue'] is not a dict")

                        else:   
                                print("Seems like record_d doesn't contain user_id record_d: " + str(record_d))
                                user = None
                except KeyError as ke:
                        user = None
                        try:
                                if isinstance(record_d['issue'], dict):
                                        if isinstance(record_d['issue']['assignee'], dict):
                                                assignee = record_d['issue']['assignee']['id']
                                        else:
                                                print('record_d: ' + str(record_d))
                                                print("record_d['issue']['assignee'] is not a dict")
                                else:
                                        print('record_d: ' + str(record_d))
                                        print("record_d['issue'] is not a dict")
                                        assignee = None

                        except KeyError as ke:
                                assignee = None
                try:    # get title
                        if isinstance(record_d['issue'], dict):
                                title = record_d['issue']['title']
                except KeyError as ke:
                        try:
                                if 'title' in record_d:
                                        title = record_d['title']
                                else:
                                        # print('record_d: ' + str(record_d))
                                        # print("it looks like title isn't in record_d")
                                        title = None
                        except KeyError as ke:
                                title = None
        except Exception as e:
                frameinfo = getframeinfo(currentframe())
                print(frameinfo.filename, frameinfo.lineno)	
                print('ISSUEEVENT_EXCEPTION: ' + str(e))
                traceback.print_exc()
                exit(1)
        
        issues_dict = {'issue_created_at' : issue_created_at}
        if issue_id:
                issues_dict['ID'] = issue_id

        if issue_closed_at:
                issues_dict['closed_at'] = issue_closed_at

        if description:
                issues_dict['description'] = description

        if user:
                issues_dict['user'] = user

        if assignee:
                issues_dict['assignee'] = assignee

        if title:
                issues_dict['title'] = title

        full_repo_name = name.get_full_repo_name(json_payload, record_d, repo_name)

        # save in the database
        try:
                db.add_data(full_repo_name, created_at, 'issues', issues_dict)
        except Exception as e:
                print("Failed to save %s IssuesEvent record at %s: %s" % \
                                (full_repo_name, created_at, str(e)))
                traceback.print_exc()

