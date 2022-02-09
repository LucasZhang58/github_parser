from lib2to3.pytree import convert
import os
from pydoc import cram
import time
import redis
from inspect import currentframe, getframeinfo
import traceback

class Database:
        def __init__(self):
                self.__r = redis.StrictRedis()

        def add_data(self, repo_name, created_at, data_type, data_dict):


                try:

                         # convert None to ''
                        converted_data = {}
                        for k, v in data_dict.items():

                                if v == None:
                                        v = ''
                                else:
                                        v = str(v)

                                converted_data[k] = v 


                        
                        if repo_name == None:
                                repo_name = 'repo_name_None'
                                exit

                        if data_type == None:
                                data_type = 'data_type_None'
                                exit

                        if created_at == None:
                                created_at = 'created_at_None'
                                exit

                        key = repo_name + '%' + data_type + '%' + created_at

                        self.__r.hmset(key, converted_data)

                        key = repo_name + '%' + data_type
                        self.__r.sadd(key, created_at)

                except Exception as e:
                        print('ERROR: ' + str(e))
                        traceback.print_exc()
                        frameinfo = getframeinfo(currentframe())
                        print(frameinfo.filename, frameinfo.lineno)
                        exit(1)
