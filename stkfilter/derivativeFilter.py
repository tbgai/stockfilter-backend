# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 21:32:58 2019

@author: jingzl

stock filter algorithm method ： Derivative one / two
"""
import numpy as np
import matplotlib.pyplot as plt
from stkfilter.stockquery import StockQuery
from stkfilter import cons as ct


class DerivativeFilter( object ):

    def __init__( self, sid, path, basestock, second_derivative, delta_one, 
                 delta_two, result_days ):
        self.sid = sid
        self.base_path = path
        self.basestock = basestock
        self.basestock_num = len( basestock )
        self.second_derivative = second_derivative
        self.delta_one = delta_one
        self.delta_two = delta_two
        self.result_days = result_days
        self.output_path = ct.OUTPUT_DIR
        
        self.basefactor1 = [] # 基准数据的一阶导
        self.basefactor2 = [] # 基准数据的二阶导
        self.resultStock = [] # 过滤出来的股票列表
    
    def filterStock( self ):
        
        '''
        提前计算出基础数据的一阶导，二阶导数据
        1. 获取股票列表数据，进行循环
        2. 通过股票代码，获取单个股票的最近30天数据
        3. 对股票进行一阶导、二阶导计算
        4. 进行相关性分析比较
        5. 将过滤出来的股票数据的一阶导和二阶导数据绘制输出，同时绘制基础数据的一阶导/二阶导
        6. 再次获取过滤出来的股票最近100天的数据，绘制曲线输出
        7. 处理下一个股票
        '''
        self.basefactor1 = self.createFactor( self.basestock )
        if ( self.second_derivative ):
            self.basefactor2 = self.createFactor( self.basefactor1 )

        stockquery = StockQuery( self.base_path )
        stocklist = stockquery.getStockBasicData()
        print( stocklist )
        return;
        length = len(stocklist)
        length = 200
        # 股票处理循环
        for i in range(length):
            '''
            更新处理进度
            '''
            
            
            dl = stockquery.getSingleStockData( stocklist[i], self.basestock_num )
            if len(dl) == self.basestock_num:
                # 处理
                if not self.second_derivative:
                    self.filterStockbyDerivativeOne( stockquery, stocklist[i], dl )
                else:
                    self.filterStockbyDerivativeTwo( stockquery, stocklist[i], dl )
            else:
                # 记录错误日志
                pass
                
        # 输出股票代码到数据库
        resary = np.array( self.resultStock )
        stockquery.saveFilterRes( self.sid, resary )

    def createFactor( self, ls ):
        # 斜率计算，求一阶导
        factorls = []
        size = len(ls)
        i = 0
        for item in ls:
            if i == size-1:
                break;
            # 斜率计算
            factor = (float(ls[i+1])-float(ls[i]))
            factorls.append( factor )
            i = i+1
        return factorls

    def filterStockbyDerivativeOne( self, stockquery, stock_code, stockdata ):
        # 通过求导来对单个股票数据进行过滤
        fls = self.createFactor( stockdata )
        if self.compareFactor( self.basefactor1, fls ):
            self.resultStock.append( stock_code )
            '''
            绘制基准数与股票值的图
            绘制一阶导值得图
            绘制该股票仅100交易日图
            '''
            '''
            plt.cla()
            plt.title( stock_code+u"与基准股票值比较", fontproperties="SimHei" )
            x = np.arange(self.basestock_num)
            plt.plot( x, self.basestock, "ro-", x, stockdata, "bo--" )
            plt.savefig( self.output_path+stock_code+".jpg", dpi=600 )
            '''
            
            dl = stockquery.getSingleStockData( stock_code, self.result_days )
            if len(dl) > 0:
                plt.cla()
                plt.title( stock_code+u"最近"+str(self.result_days)+u"个交易日", 
                          fontproperties="SimHei" )
                x = np.arange( self.result_days )
                plt.plot( x, dl, "bo-" )
                plt.savefig( self.output_path+stock_code+"_"+str(self.result_days)+".jpg", dpi=600 )
                
            
            plt.cla()
            plt.title( stock_code+u"与基准模型一阶变化比较(最近"+str(self.basestock_num)
                                +u"个交易日)", fontproperties="SimHei" )
            x = np.arange(len(self.basefactor1))
            plt.plot( x, self.basefactor1, "ro-", x, fls, "bo--" )
            plt.savefig( self.output_path+stock_code+"_D1"+".jpg", dpi=600 )

    def filterStockbyDerivativeTwo( self, stockquery, stock_code, stockdata ):
        # 通过求二阶导来对股票进行过滤
        fls = self.createFactor( stockdata )
        fls2 = self.createFactor( fls )
        if self.compareFactor( self.basefactor2, fls2 ):
            self.resultStock.append( stock_code )
            '''
            绘制二阶导值得图
            绘制该股票仅100交易日图
            '''
            dl = stockquery.getSingleStockData( stock_code, self.result_days )
            if len(dl) > 0:
                plt.cla()
                plt.title( stock_code+u"最近"+str(self.result_days)+u"个交易日", 
                          fontproperties="SimHei" )
                x = np.arange( self.result_days )
                plt.plot( x, dl, "bo-" )
                plt.savefig( self.output_path+stock_code+"_"+str(self.result_days)+".jpg", dpi=600 )
                
            
            plt.cla()
            plt.title( stock_code+u"与基准模型二阶变化比较(最近"+str(self.basestock_num)
                                +u"个交易日)", fontproperties="SimHei" )
            x = np.arange(len(self.basefactor1))
            plt.plot( x, self.basefactor1, "ro-", x, fls, "bo--" )
            plt.savefig( self.output_path+stock_code+"_D2"+".jpg", dpi=600 )

    def compareFactor( self, basefls, fls ):
        # 斜率因子比较
        if len(basefls) != len(fls):
            return False
        count = 0
        delta = self.delta_one
        if self.second_derivative:
            delta = self.delta_two
        for i in range(len(basefls)):
            if abs(basefls[i]-fls[i]) < delta:
                count = count + 1
        
        '''
        此处要求所有的节点数据均在设定的delta值内，这样做有很大局限性
        可能部分股票值的比值更好，但可能会被排除外
        这个地方待改进
        count < len(basefls)/2
        '''
        if count == len(basefls):
            return True
        else:
            return False

