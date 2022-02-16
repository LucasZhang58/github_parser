import html
from platform import release
import traceback
import json
import os
import sys
from inspect import currentframe, getframeinfo
from getters import persons, repos, helpers
import name

##########################
# Person
##########################

def get_Person(full_repo_name, created_at, json_payload, record_d, in_dict, db):
        try:

                # String ID
                try:
                        user_login = in_dict['login']
                except KeyError:
                        if 'url' in in_dict:
                                user_login = name.url2actor(in_dict['url'])

                # validation: absolutely mandatory field
                if not user_login:
                        #raise Exception("User name ('login') info not available!")
                        return

                # Type: can be either 'User' or 'Organization'
                try:
                        user_type = in_dict['type']
                except KeyError:
                        try:
                                user_type = helpers.get_user_type_from_url(in_dict)
                        except KeyError as ke:
                                try:
                                        user_type = helpers.get_user_type_from_url(record_d['actor'])
                                except KeyError as ke:
                                        print('KEYERROR: ' + str(ke))
                                        print('record_d: ' + str(record_d))


                if user_type != 'user':
                        return
                        # print('user_type: ' + str(user_type))
                        # raise Exception('user_type is not user!')
                        # print('in_dict: ' + str(in_dict))
                        # print('record_d: ' + str(record_d))
                        # user_type = 'org' # TODO check this

                # Integer ID
                try:
                        user_id = in_dict['id']
                except KeyError:
                        user_id = None

                # Name
                try:
                        user_name = in_dict['name']
                except KeyError:
                        user_name = None

                # Email
                try:
                        user_email = in_dict['email']
                except KeyError:
                        user_email = None

                # Company
                try:
                        user_company = in_dict['company']
                except KeyError:
                        user_company = None

                # Location
                try:
                        user_location = in_dict['location']
                except KeyError:
                        user_location = None

                # Avatar URL
                try:
                        avatar_url = in_dict['avatar_url']
                except KeyError:
                        avatar_url = None

                # Gravatar ID
                try:
                        gravatar_id = in_dict['gravatar_id']
                except KeyError:
                        gravatar_id = None

                # URL
                try:
                        user_url = in_dict['url']
                except KeyError:
                        user_url = None

                # Blog
                try:
                        user_blog = in_dict['blog']
                except KeyError:
                        user_blog = None

        except Exception as e:
                url = None
                frameinfo = getframeinfo(currentframe())
                print(frameinfo.filename, frameinfo.lineno)	
                print(record_d)
                print('PERSONEVENT_EXCEPTION: ' + str(e))
                traceback.print_exc()
                exit(1)
                                
        person_dict = {
                'login'			: user_login,
                'type'			: user_type,
        }

        if user_id:
                person_dict['id'] =  user_id
        if avatar_url:
                person_dict['avatar_url'] = avatar_url
        if gravatar_id:
                person_dict['gravatar_id'] = gravatar_id
        if user_url:
                person_dict['url'] = user_url
        if user_company:
                person_dict['company'] = user_company
        if user_blog:
                person_dict['blog'] = user_blog
        if user_name:
                person_dict['name'] = user_name
        if user_location:
                person_dict['location'] = user_location
        if user_email:
                person_dict['email'] = user_email

        # save in the database
        try:
                db.add_user(user_login, person_dict)
        except Exception as e:
                print("Failed to save %s person data at %s: %s" % \
                                (full_repo_name, created_at, str(e)))
                traceback.print_exc()
                frameinfo = getframeinfo(currentframe())
                print(frameinfo.filename, frameinfo.lineno)
