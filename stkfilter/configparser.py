# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 10:46:36 2019

@author: jingzl

parse config data
"""
import yaml


class ConfigParser( object ):
    
    db_host = ""
    db_port = 0
    db_user = ""
    db_passwd = ""
    db_name = ""
    db_charset = ""

    def __init__(self):
        pass

    def parse( self, filename ):
        
        f = open( filename, 'r' ).read()
        configs = yaml.safe_load( f )
        if configs:
            
            self.db_host = configs['db']['host']
            self.db_port = configs['db']['port']
            self.db_user = configs['db']['user']
            self.db_passwd = configs['db']['passwd']
            self.db_name = configs['db']['dbname']
            self.db_charset = configs['db']['charset']
            
            return True
        else:
            return False

