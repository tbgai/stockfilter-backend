# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 18:52:17 2019

@author: jingzl

filtermgr.py
"""
import uuid
import threading
from stkfilter.derivativeFilter import DerivativeFilter
from stkfilter.stockquery import StockQuery


def derivativeFilterStock( sid, path, basestk, delta2, delta1factor, 
                          delta2factor, stkcount ):
    #print( "线程任务中收到的数据：{0},\n{1},\n{2},\n{3},\n{4}\n".format(
    #           basestk, delta2, delta1factor, delta2factor, stkcount ) )
    dfs = DerivativeFilter( sid, path, basestk, delta2, delta1factor, 
                           delta2factor, stkcount )
    dfs.filterStock()


class FilterMgr( object ):
    
    def __init__( self, path ):
        self.base_path = path
    
    def version( self ):
        return "v0.1"
    
    def stockfilter( self, request ):
        
        # Session ID
        SID = uuid.uuid1()
        strSID = "{}".format( SID )
        
        # 如果key不存在，则报400 error
        #print( request.headers )
        #print( request.form )
        #print( request.form['basestk'])
        basestk = request.form['basestk'].split(',')
        delta2 = int(request.form['delta2'])
        delta1factor = float(request.form['delta1factor'])
        delta2factor = float(request.form['delta2factor'])
        stkcount = int(request.form['stkcount'])
        
        thd = threading.Thread( target=derivativeFilterStock, name=strSID,
                               args=(strSID, self.base_path, basestk, delta2, 
                                     delta1factor, delta2factor, stkcount) )
        thd.start()

        res = { 'sid': strSID }
        return res

    def querypos( self, request ):
        
        # GET
        sid = request.args.get('sid')
        #print( "收到的数据：{0}".format(sid) )
        '''
        查询数据库的进度表，并获取当前sid下的进度信息返回
        '''
        stockquery = StockQuery( self.base_path )
        return stockquery.queryPos( sid )

    def queryres( self, request ):
        
        # GET
        sid = request.args.get('sid')
        #print( "收到的数据：{0}".format(sid) )
        '''
        查询当前sid下的结果信息
        '''
        stockquery = StockQuery( self.base_path )
        return stockquery.queryFilterRes( sid )

    def stockgraph( self, request ):

        SID = uuid.uuid1()
        strSID = "{}".format( SID )
        basestk = request.form['basestk'].split(',')

        dfs = DerivativeFilter( strSID, self.base_path, basestk )
        imgls = dfs.baseGraph()
        if len(imgls) == 3:
            res = { 'img1':imgls[0], 'img2':imgls[1], 'img3':imgls[2] }
        else:
            res = { 'img1':'', 'img2':'', 'img3':'' }
        return res





