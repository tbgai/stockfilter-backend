# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 21:40:42 2019

@author: jingzl

parse stock data from db
"""
import time
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
        
        today = datetime.date.today()
        hisday = today - datetime.timedelta(days=2*length)
        start_date = hisday.strftime("%Y%m%d")
        end_date = today.strftime("%Y%m%d")

        sql = '''select trade_date,vclose from stock_daily where ts_code='{0}' 
        and trade_date>='{1}' and trade_date<='{2}' order by trade_date desc 
        limit {3} '''.format( ts_code, start_date, end_date, length )
        cursor = self.dbcon.cursor()
        try:
            cursor.execute( sql )
            results = cursor.fetchall()
            a = []
            for row in results:
                trade_date = row[0]
                vclose = row[1]
                a.append([trade_date,vclose])
            df = pd.DataFrame( a, columns=['trade_date','vclose'], index=np.arange(len(a)))
            dl = df.ix[:,1].values.tolist()
            dl.reverse()
            if len(dl) < length:
                return []
            else:
                return dl
        except:
            print( "Error: unable to fecth stocklist data" )
            return []

    def updatePos( self, sid, pos ):
        '''
        1. 根据pos更新进度表
        2. 进度表包含：进度值，更新时间，sid
        '''
        pos = int(pos)
        update_time = time.strftime("%Y%m%d%H%M%S")
        
        sql = '''select * from procstatus where sid = '{0}'
            '''.format( sid )
        try:
            cursor = self.dbcon.cursor()
            cursor.execute(sql)
            if ( cursor.fetchone() != None ):
                # update
                sql2 = '''update procstatus set pos={0},updatetm='{1}' 
                where sid='{2}'
                '''.format(pos,update_time,sid)
                #print( sql2 )
                try:
                    cursor.execute(sql2)
                    self.dbcon.commit()
                except:
                    print("update db error - [procstatus]")
                    self.dbcon.rollback()
            else:
                # add
                sql3 = '''insert into procstatus (sid,pos,updatetm) 
                values ('{0}',{1},'{2}')
                '''.format(sid,pos,update_time)
                #print( sql3 )
                try:
                    cursor.execute(sql3)
                    self.dbcon.commit()
                except:
                    print("insert db error - [procstatus]")
                    self.dbcon.rollback()
                    
        except:
            print( "Error: unable to fecth data - [procstatus]" )
        

    def saveFilterRes( self, sid, resary ):
        '''
        1. 更新结果表
        2. 打包压缩结果图片
        3. 更新进度表
        '''
        #
        self.updatePos( sid, 100 )
    
    def queryPos( self, sid ):
        
        sql = '''select pos from procstatus where sid = '{0}'
            '''.format( sid )
        try:
            cursor = self.dbcon.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()
            a = []
            pos = 0
            for row in results:
                pos = row[0]
                a.append(pos)
            if len(a) > 0:
                pos = a[0]
            res = { 'pos': pos }
            return res
                    
        except:
            print( "Error: unable to fecth data - [procstatus]" )
            return ""
    
    
    def queryFilterRes( self, sid ):
        
        res = { 'res': '000111.SZ,000222.SZ,000234.SZ',
               'purl':'http://47.104.252.239/test.tar.gz' }
        return res
    
    
    
    
    