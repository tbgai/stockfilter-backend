# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 17:50:44 2019

@author: jingzl

stockfilter.py

"""
import os
import sys
from flask import Flask 
from stkfilter.filtermgr import FilterMgr

# import libraries in lib directory
base_path = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(base_path, 'lib'))

app = Flask(__name__)

@app.route('/')
def home():
    filtermgr = FilterMgr()
    return filtermgr.version()

@app.route('/sf/api/v1.0/stockfilter/', methods=['POST'])
def stockfilter():
    filtermgr = FilterMgr()
    return filtermgr.stockfilter()

@app.route('/sf/api/v1.0/querypos/', methods=['GET'])
def querypos():
    filtermgr = FilterMgr()
    return filtermgr.querypos()


