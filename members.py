import html
from platform import release
import traceback
import json
import os
import sys
from inspect import currentframe, getframeinfo

##########################
# Member Events
##########################

def get_MemberEvent(repo_name, created_at, json_payload, db, record, member_past_repo_names, members_dict):


        if repo_name not in member_past_repo_names:


                members_dict['{}'.format(repo_name)] = [record]
                

        else:
                members_dict['{}'.format(repo_name)].append(record)

        member_past_repo_names.add(repo_name)

                

        # save in the database
        try:
                db.add_data(repo_name, created_at, 'members', members_dict)
        except Exception as e:
                print("Failed to save %s MemberEvent record at %s: %s" % \
                                (repo_name, created_at, str(e)))
        

        # event_type = 'MemberEvent'

        # get_Person(repo_name, created_at, json_payload, output_path, lock, event_type)




