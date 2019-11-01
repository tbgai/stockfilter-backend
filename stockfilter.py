# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 17:50:44 2019

@author: jingzl

stockfilter.py

"""
import os
import sys
from flask import Flask, make_response, request
import json
from stkfilter.filtermgr import FilterMgr

# import libraries in lib directory
base_path = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(base_path, 'lib'))

app = Flask(__name__)


@app.route('/')
def home():
    filtermgr = FilterMgr(base_path)
    return filtermgr.version()

@app.route('/sf/api/v1.0/stockfilter/', methods=['POST'])
def stockfilter():
    filtermgr = FilterMgr( base_path )
    rst = make_response( json.dumps(filtermgr.stockfilter(request)) )
    rst.headers['Access-Control-Allow-Origin'] = '*'
    #rst.headers['Access-Control-Allow-Methods'] = 'POST'
    rst.mimetype = 'application/json'
    return rst

@app.route('/sf/api/v1.0/querypos/', methods=['GET'])
def querypos():
    filtermgr = FilterMgr( base_path )
    rst = make_response( filtermgr.querypos(request) )
    rst.headers['Access-Control-Allow-Origin'] = '*'
    return rst

@app.route('/sf/api/v1.0/queryres/', methods=['GET'])
def queryres():
    filtermgr = FilterMgr( base_path )
    rst = make_response( filtermgr.queryres(request) )
    rst.headers['Access-Control-Allow-Origin'] = '*'
    return rst

@app.route('/sf/api/v1.0/stockgraph/', methods=['POST'])
def stockgraph():
    filtermgr = FilterMgr( base_path )
    rst = make_response( json.dumps( filtermgr.stockgraph(request) ) )
    rst.headers['Access-Control-Allow-Origin'] = '*'
    rst.mimetype = 'application/json'
    return rst


