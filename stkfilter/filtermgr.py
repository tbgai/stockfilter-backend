# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 18:52:17 2019

@author: jingzl

filtermgr.py
"""

class FilterMgr( object ):
    
    def __init__( self ):
        pass
    
    def version( self ):
        return "v0.1"
    
    def stockfilter( self, request ):
        
        # 如果key不存在，则报400 error
        #print( request.headers )
        #print( request.form )
        #print( request.form['basestk'])
        
        basestk = request.form['basestk']
        delta2 = request.form['delta2']
        delta1factor = request.form['delta1factor']
        delta2factor = request.form['delta2factor']
        stkcount = request.form['stkcount']
        #print( "收到的数据：{0},\n{1},\n{2},\n{3},\n{4}\n".format(
        #        basestk, delta2, delta1factor, delta2factor, stkcount ) )
        
        # 启动线程去执行分析任务
        # 返回客户端sid
        
        
        sid = "f098213123ssfsdf8890"
        res = { 'sid': sid }
        return res 

    def querypos( self, request ):
        
        # GET
        sid = request.args.get('sid')
        print( "收到的数据：{0}".format(sid) )
        
        # test
        pos = 101
        
        
        res = { 'pos': pos }
        return res

    def queryres( self, request ):
        
        # GET
        sid = request.args.get('sid')
        print( "收到的数据：{0}".format(sid) )
        
        
        res = { 'res': '000111.SZ' }
        return res






