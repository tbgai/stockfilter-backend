# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 17:50:44 2019

@author: jingzl

stockfilter.py

"""
import os
import sys

# import libraries in lib directory
base_path = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(base_path, 'lib'))


from flask import Flask 

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, this is stockfilter'

@app.route('/sf/api/v1.0/filter/', methods=['POST'])
def filter():
    return 'filter process ...'

@app.route('/sf/api/v1.0/querypos/', methods=['GET'])
def querypos():
    return 60

