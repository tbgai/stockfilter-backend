# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 21:40:42 2019

@author: jingzl

parse stock data from db
"""
import datetime
import pandas as pd
import numpy as np
import MySQLdb
from stkfilter import cons as ct
from stkfilter.configparser import ConfigParser


class StockQuery( object ):
    
    def __init__( self, path ):
        config_file = path + ct.CONFIG_FNAME
        config = ConfigParser()
        config.parse( config_file )
        if config.parse( config_file ):
            self.db_host = config.db_host
            self.db_port = config.db_port
            self.db_user = config.db_user
            self.db_passwd = config.db_passwd
            self.db_name = config.db_name
            self.db_charset = config.db_charset
            
            self.dbcon = self.connectdb()
        else:
            print( "解析配置文件失败，请检查配置文件！" )
    
    def __del__( self ):
        self.dbcon.close()
    
    def connectdb( self ):
        dbcon = MySQLdb.connect(host=self.db_host, port=self.db_port, 
                         user=self.db_user, passwd=self.db_passwd, 
                         db=self.db_name, charset=self.db_charset )        
        return dbcon
    
    def getStockBasicData( self ):
        
        # 获取所有的股票列表信息
        sql = 'select ts_code,symbol from stock_basic'
        cursor = self.dbcon.cursor()
        try:
            cursor.execute( sql )
            results = cursor.fetchall()
            a = []
            for row in results:
                ts_code = row[0]
                symbol = row[1]
                a.append([ts_code,symbol])
            
            df = pd.DataFrame( a, columns=['ts_code','symbol'], index=np.arange(len(a)))
            return df
        except:
            print( "Error: unable to fecth stocklist data" )
        

    def getSingleStockData( self, ts_code, length ):
        
        #pro = ts.pro_api( token=TUSHARE_TOKEN )
        '''
        因接口无法根据记录数返回，考虑到正常交易日是工作日，所以按照两倍长度获取数据，
        然后截取 length 数量的数据返回
        '''
        today = datetime.date.today()
        hisday = today - datetime.timedelta(days=2*length)
        start_date = hisday.strftime("%Y%m%d")
        end_date = today.strftime("%Y%m%d")
        
        #print( length )
        #print( start_date )
        #print( end_date )
        
        '''
        df = pro.query( 'daily', ts_code=ts_code, start_date=start_date,
                       end_date=end_date, fields='trade_date,close')
        dl = df.ix[:,1].values.tolist()
        dl.reverse()
        if len(dl) < length:
            return []
        else:
            return dl[0:length]
        '''
        pass

    def saveFilterRes( self, sid, resary ):
        '''
        1. 更新结果表
        2. 打包压缩结果图片
        3. 更新进度表
        '''
        pass
    
    def queryPos( self, sid ):
        
        pos = 101
        
        res = { 'pos': pos }
        return res
    
    
    def queryFilterRes( self, sid ):
        
        res = { 'res': '000111.SZ,000222.SZ,000234.SZ',
               'purl':'http://47.104.252.239/test.tar.gz' }
        return res
    
    
    
    
    