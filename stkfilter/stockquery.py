# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 21:40:42 2019

@author: jingzl

parse stock data from db
"""
import os, tarfile
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
        

    def getSingleStockData( self, ts_code, length, len_strict ):
        
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
            if len_strict and (len(dl) < length):
                print( "Error: sql:{0}".format(sql) )
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
        

    def make_targz(self, output_filename, source_dir):
        with tarfile.open(output_filename, "w:gz") as tar:
            tar.add(source_dir, arcname=os.path.basename(source_dir))

    def saveFilterRes( self, sid, resary, resimgary ):

        if len(resary) > 0:
            resinfo = ','.join(resary);
            
            source_dir = ct.OUTPUT_DIR + "{}".format(sid)
            zfile = "{}.tar.gz".format(sid)
            self.make_targz( '{0}{1}'.format(ct.OUTPUT_DIR,zfile), source_dir )
            
            df = pd.DataFrame( resimgary, columns=['stock_code','img1','img2'], 
                              index=np.arange(len(resimgary)))
            strimg = df.to_json(orient='split')
            print( strimg )
            sql = '''insert into filterres (sid,resinfo,zfile,imgs,updatetm) values 
            ('{0}','{1}','{2}','{3}','{4}')'''.format( sid, resinfo, zfile, strimg, 
            time.strftime("%Y%m%d%H%M%S") )
            
            try:
                cursor = self.dbcon.cursor()
                cursor.execute(sql)
                self.dbcon.commit()
            except:
                self.dbcon.rollback()
                print( "Error: unable to insert filter res - [filterres]" )
            
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
        
        sql = '''select resinfo,zfile,imgs from filterres where sid='{}'
        '''.format( sid )
        try:
            cursor = self.dbcon.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()
            resinfo = ""
            zfile = ""
            imgs = ""
            for row in results:
                resinfo = row[0]
                zfile = row[1]
                imgs = row[2]
            if len(resinfo) > 0:
                res = { 'res':resinfo, 'purl':ct.DOWNLOAD_URL+zfile, 'imgs':imgs }
            else:
                res = { 'res':resinfo, 'purl':zfile, 'imgs':imgs }
            return res
        except:
            print( "Error: unable to fetch res data - [filterres]" )
            return ""
    
    
    
    