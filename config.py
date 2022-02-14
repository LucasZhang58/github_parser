#!/usr/bin/python

#################################################################
# Configuration parser
#################################################################
class Config():
    __configParser = None

    def __init__(self, file_path="config"):
        try:
            import sys
            import os
            if not os.path.exists(file_path) or not os.path.isfile(file_path):
                raise Exception("Invalid config file %s" % (file_path))

            if sys.version_info[0] < 3:
                import ConfigParser
                self.__configParser = ConfigParser.RawConfigParser()
            else:
                import configparser
                self.__configParser = configparser.RawConfigParser()
            self.__configParser.read(file_path)

        except ImportError as ie:
            raise Exception("configparser module not available. Please install")

        except Exception as e:
            raise Exception("Error parsing " + file_path + ": " + str(e))

    def get(self, opt, sec="Main"):
        if not self.__configParser:
            return None
        try:
            return self.__configParser.get(sec, opt)
        except Exception as e:
            #raise Exception("Error getting config for " + \
            #                    sec + " :" + cfg + ": " + str(e))
            return None

