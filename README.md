# implied_vol.py

## Table of contents
* [About](#about)
* [Example](#example)
* [Libraries](#libraries)
* [Setup](#setup)
* [Errors](#errors)
* [Ideas](#ideas)

## About
Implied volatility is an important measurement for market makers and may be used to "monitor the market's opinion about the volatility of a particular stock"
(Pg. 340, Hull). Implied Volatility may be solved for by finding the value of sigma given the current price of some option. One problem is that
the Black-Scholes-Mertons equations are not invertible; therefore the calculation of implied volatility requires numerical methods. This algorithm 
calculates implied volatiltiy using an adjusted bisection method for various options. In addition the algorithm allows users to visualize the time series
of implied volatility for those options.

## Example
For this example I will be using msp1, a data frame with put prices with strike 50, and stock prices of Morgan Stanley 
for given date interval.<br/> 

--Given that users have followed directions given in setup section, algo should run as follows--<br/>

Run implied_vol.py, and check object.dataframe to make sure object was created: 
[![Screenshot-from-2020-12-03-08-03-08.png](https://i.postimg.cc/3NFN1GTF/Screenshot-from-2020-12-03-08-03-08.png)](https://postimg.cc/fSkMTJkV)

Run object.loop() and then object.dataframe to see the addition of calculated implied volatility at specified date, and number of steps
the adjusted bisection method took to find an approximate answer. 
[![Screenshot-from-2020-12-03-08-03-20.png](https://i.postimg.cc/50tsbBP6/Screenshot-from-2020-12-03-08-03-20.png)](https://postimg.cc/d7z29ycY)

Run object.fancy_table() to view a gradient filled table. 
[![Screenshot-from-2020-12-03-08-03-30.png](https://i.postimg.cc/NfRSNxZc/Screenshot-from-2020-12-03-08-03-30.png)](https://postimg.cc/bsNmr1zC)

Run object.vol_plot() to view a time series of the calculated implied volatility or run object.subs_4() to view four time series subplots 
which include: implied volatility, stock price, option price and the CBOE volatility index. 
[![Screenshot-from-2020-12-03-08-03-42.png](https://i.postimg.cc/pT91KQK3/Screenshot-from-2020-12-03-08-03-42.png)](https://postimg.cc/xJ2R2zxP)

## Libraries
pandas_datareader - required to access stock price data from yahoo finance. <br/>
pandas_ods_reader - required for linux users to access ods files. Mac and windows users will need a library that reads excel files. <br/>
scipy.stats - required to calculate CDF for normal distributions. <br/>
math - required.<br/>
datetime - necessary to calculate time until expiration.<br/>
matplotlib.pyplot - required for visualization.<br/>
pandas - necessary for dataframes.<br/>

## Setup 
Git clone https://github.com/manuelnjit/implied_volatility.git <br/>
Open implied_vol.py on preferred IDE and change path, pathp, morganpath_sample2p, path1 and path1p
in implied_vol.py to the location of those same files on the users computer. <br/>
Run implied_vol.py, and try running object.dataframe for one of the initilized objects at the bottom of 
implied_vol.py (msp1, msp2, dbc1, dbp1). <br/>
Continue from section Example. 

## Errors
The calculation of implied volatility does not take into consideration the present value of future dividend payments, it assumes
that there are no dividend payments which is inaccurate. 

## Ideas
**Generalize optionsman**: One example may be having optionsman run data.DataReader when it's called rather than collecting the data
before hand, in addition it would be nice to give optionsman the capability of modifying the data when called. For example, 
if we were interested in looking at daily, weekly, bi-weekly or any time frame of interest giving optionsman a parameter that would
modify the data for the user. 

**Adding the present value of future dividends to the implied volatility calculation**

**Automating optionsman**: One example would be to give optionsman the capability of automatically acquiring option price data; similarly to 
pandas_datareader. 

**Adding a statistics method**: One example would be to create a method inside optionsman that could return n number of stocks 
whose time series is highly correlated with the stock time series you are interested in. In addition it would be neat to allow this
process to look into various autocorrelations at certain lags as well. 
