#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 23:11:48 2020

@author: Manuel Navas
"""
from pandas_datareader import data
from pandas_ods_reader import read_ods
from scipy.stats import norm
import math
from datetime import datetime
import matplotlib.pyplot as plt 
import pandas as pd

MS_p1 = data.DataReader("MS", data_source='yahoo',   # Assigning MS_p1 "MS"
                        start='2020-1-17',           # Morgan Stanley stock 
                        end='2020-4-17')['Adj Close']# prices from yahoo fin
                                                     # between start and end
                                                     # date   

MS1 = MS_p1.resample('W-FRI').last()                 # Adjusting from daily to
                                                     # weekly data

path = "/home/stochasticity/Documents/MSC43_JAN1521.ods"
# path contains data for "MSC43_Jan1521" or Morgan Stanley Call strike price
# 43 expiring January 15, 2021. Prices are weekly. 

df = read_ods(path, "Sheet1")                        # turning csv data into
                                                     # python data frame

df['stocks'] = MS1.array                             # adding stock price col-
                                                     # to option price datafr-
                                                     # ame

pathp = "/home/stochasticity/Documents/MSP50_JAN1521.ods"
# path contains data for "MSP50_Jan1521" or Morgan Stanley Put strike price
# 50 expiring January 15, 2021. Prices are weekly. 

dfp = read_ods(pathp, "Sheet1")                      # turning pathp csv data
                                                     # into data frame

dfp['stocks'] = MS1.array                            # dfp is dataframe with
                                                     # dates, option prices a-
                                                     # stock prices
#----------------------------------------------------------------------------#
# Another Morgan Stanley example
morgan_adj = data.DataReader("MS", data_source='yahoo',
                             start='2019-10-30',
                             end='2020-1-30')['Adj Close']
morgan_weekly = morgan_adj.resample('W-FRI').last()
morganpath_sample2p = "/home/stochasticity/Documents/MSP40_JAN1521_SNOV0119.ods"
morgan_sample2p = read_ods(morganpath_sample2p, "Sheet1")
morgan_sample2p['stocks'] = morgan_weekly.array 

# A Deutsche Bank example
DB_p1 = data.DataReader("DB", data_source='yahoo',
                        start='2020-1-17',
                        end='2020-4-17')['Adj Close']
DB1 = DB_p1.resample('W-FRI').last()
path1 = "/home/stochasticity/Documents/DBC5_JAN1521.ods"
df1 = read_ods(path1, "Sheet1")
df1['stocks'] = DB1.array

path1p = "/home/stochasticity/Documents/DBP8_JAN1521.ods"
df1p = read_ods(path1p, "Sheet1")
df1p['stocks'] = DB1.array
#----------------------------------------------------------------------------------------------------



class optionsman: 

    def __init__(self, symbol, dataframe, strike, optiontype, exp):
        self.dataframe = dataframe         # returns entire dataframe 
        self.options = dataframe["options"]# returns column of option prices 
        self.stocks = dataframe["stocks"]  # returns column of stock prices
        self.date = dataframe["date"]      # returns column of dates
        self.optiontype = optiontype       # returns put or call
        self.exp = exp                     # returns data of expiration
        self.strike = strike               # returns option strike price
        self.name = symbol                 # returns stock symbol
        self.vol_df = pd.DataFrame(columns=['option', 'sigma'])
       
    def duration_agg(self):                # creates a column in dataframe 
        list_exp = []                      # with amount of time left until 
                                           # expiration
        for value in range(len(self.dataframe)):
            start_date = str(self.date[value])
            end_date = str(self.exp)
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            duration = end-start 
            list_exp.append(duration.days/7)
        self.dataframe.insert(2, "duration", list_exp)
        return(self.dataframe)
        
    def bisec_method_c(self, option, istock, d):
        # Bisection method for some implied volatility value between 
        # a= 0.01 and b = 1
        i = 0
        Statement = True
        a = 0.01
        b = 1
        while Statement:
            i = i+1
            c = (a+b)/2
            tester = self.black_scholes(c, istock, d, None)
            if tester > option:
                b = c
            else:
                a = c
            if i>100 or (abs(option-self.black_scholes(c, istock, d, None))<0.001):
                Statement = False
        # stop after 100 iterations or if the differenced between the option 
        # price and calculated option price is less than 0.001
        templist = []
        templist.append(c)
        templist.append(i)
        return(templist)
        # returns an array with approximated implied volatility and number
        # of iterations to converge to approximated value


    def black_scholes(self, guess, price, time_to_maturity, dividends_df):
        
        optiontype = self.optiontype
        T = time_to_maturity/52
        rf = 0.015
        Strike = self.strike
        if dividends_df == None:
            dividends_df = 0
        else:
            dividends_df = dividends_df
        So = price
        d1t = math.log(So/Strike)+(rf+guess*guess/2)*T
        d1b = guess*math.sqrt(T)
        d1 = d1t/d1b
        d2 = d1 - guess*math.sqrt(T)
        if optiontype == "call":
            value = So*norm.cdf(d1) - Strike*math.exp(-rf*T)*norm.cdf(d2)
        else:
            value = Strike*math.exp(-rf*T)*norm.cdf(-d2)-So*norm.cdf(-d1)
        return(value)
        
    def loop(self):
        self.duration_agg()
        temp = []
        steps = []
        for value in range(len(self.dataframe)):
            temp.append(self.bisec_method_c(self.dataframe['options'][value],
                                            self.dataframe['stocks'][value],
                                            self.dataframe['duration'][value])[0])   
            steps.append(self.bisec_method_c(self.dataframe['options'][value],
                                             self.dataframe['stocks'][value],
                                             self.dataframe['duration'][value])[1])
        self.dataframe.insert(4, "sig_hat", temp)
        self.dataframe.insert(5, "steps", steps)  

    def vol_plot(self):
        trim = self.dataframe[['date','sig_hat']]
        timeseriesdf = trim.set_index('date')
        fig, ax = plt.subplots(figsize = (12,10))
        ax.plot(timeseriesdf, marker = 'o', linestyle = '--')
        ax.set_ylabel('Implied Volatility')
        ax.set_title(str(self.name)+' : Implied Volatility')
        ax.set_xlabel('Date')
        ax.legend(["Sigma"])
        fig.autofmt_xdate()
    
    def subs_4(self):
        fig, axs = plt.subplots(2,2, figsize = (12,10), sharex = True)
        fig.suptitle(str(self.name)+' Subplots (USD)')
        axs[0,0].plot(self.dataframe['date'], self.dataframe['stocks'], 
                      marker = 'o', linestyle = '--', color = 'red')
        axs[0,0].set_title('Stock Price')
        axs[0,0].grid(True)
        axs[0,1].plot(self.dataframe['date'], self.dataframe['options'], 
                      marker = 's', linestyle = '--', color = 'm')
        axs[0,1].set_title(str(self.optiontype).capitalize()+
                           ' Price @ K = '+str(self.strike))
        axs[0,1].grid(True)
        axs[1,0].plot(self.dataframe['date'], 
                      self.dataframe['sig_hat'],
                      marker = 'o', linestyle = '--')
        axs[1,0].set_title('Implied Vol.')
        axs[1,0].grid(True)
        
        Vix = data.DataReader("^VIX", data_source='yahoo',
                              start= str(self.dataframe['date'][0]), 
                              end=str(self.dataframe['date'][len(self.dataframe)-1]))['Adj Close'].resample('W-FRI').last()
        axs[1,1].plot(Vix.values, marker = 'o', 
                      linestyle = '--', color = 'c')
        axs[1,1].set_title('VIX')
        axs[1,1].grid(True)
      
        fig.autofmt_xdate()
        
    def fancy_table(self):
        
        mod_table = self.dataframe.rename(columns={'options':str(self.optiontype).capitalize()+' K='+
                                                   str(self.strike), 'stocks':str(self.name).capitalize(),
                                                   'sig_hat':'Implied Vol.'})
        return(mod_table.style.background_gradient(cmap='Blues'))   



msp1 = optionsman("Morgan Stanley", dfp, 50, "put", "2021-01-15")
msp2 = optionsman("Morgan Stanley", morgan_sample2p, 40, "put", "2021-01-15")

dbc1 = optionsman('Deutsche Bank', df1, 5, 'call', '2021-01-15')
dbp1 = optionsman('Deutsche Bank', df1p, 8, 'put', '2021-01-15')
