#---------------------------------------------------------------------------------
#   
#   Assignement: Quantitative Investment Solutions Coding Assignment
#   Question: 1 - Metrics 
#   File: SSMIF2020P1.py
#   
#   Agatha Malinowski
#   
#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
#
#   Load all dependencies
#
#---------------------------------------------------------------------------------
import pandas as pd
import pandas_datareader as pdr
import math
from datetime import date, timedelta
import sys


#---------------------------------------------------------------------------------
#
# Daily_Returns: Function
#
# Parameters: 
#   data: Times series
#
#   Calculate daily returns of on Adjusted Close
#   Returns daily percentage change of the Adjsuted Close.
#
#--------------------------------------------------------------------------------
def Daily_Returns(data):
	dailyreturn = data['Adj Close'].pct_change() 
	return list(dailyreturn)
#--------------------------------------------------------------------------------
#   End of Daily_Returns
#--------------------------------------------------------------------------------


#---------------------------------------------------------------------------------
#
# Monthly_Var: Function
#
# Parameters: 
#   confidence: Degree of confidence; Default value 0.05
#
#   Calculates monthly Value At Risk (VaR) based on the provided degree of 
#   confidence (defult 0.05). Time series data is retrieved from the internet
#   (Yahoo)
#
#--------------------------------------------------------------------------------
def Monthly_VaR(ticker, confindence = 0.05):
	ticker = ticker.upper()
	startdate = '2019-01-01'
	enddate = '2019-12-31'
	interval = 'd'

	if ticker == '':
		print('[ERROR] Error supply ticker')

	try:
		data = pdr.get_data_yahoo(ticker, interval = interval, start = startdate, end = enddate)
	except:
		print("[ERROR] Unexpected error:", sys.exc_info())
		print("[ERROR] Check your inputs dumbo!")
			
	d_return = Daily_Returns(data)  # Calculate daily percent return for the data series

	d_mean = sum(d_return[1:]) / len(d_return[1:])  # Mean of the daily percentage returns
	d_variance = sum([((x - d_mean) ** 2) for x in d_return[1:]]) / len(d_return[1:])    # Calculate variance
	d_std = d_variance ** 0.5 # Calculate standard deviation
        
	d_return.sort()
	zscore = (d_return[round(len(d_return[1:])*confindence)]-d_mean)/d_std

	d_VaR = zscore * d_std  # Calculate daily VaR
	m_VaR = d_VaR * (20 ** 0.5) #Calculate monthly VaR

	return m_VaR
#--------------------------------------------------------------------------------
# End of Monthly_Var
#--------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
#
# Monthly_CVaR: Function
#
# Parameters: 
#   ticker:     Symbol of a stock 
#   confidence: Degree of confidence; Default value 0.05
#
#   Calculates conditional monthly Value At Risk (VaR) based on the provided degree of 
#   confidence (defult 0.05). Time series data is retrieved from the internet
#   (Yahoo)
#
#--------------------------------------------------------------------------------
def Monthly_CVaR(ticker, confindence = 0.05):
	ticker = ticker.upper()
	startdate = '2019-01-01'
	enddate = '2019-12-31'
	interval = 'd'

	if ticker == '':
		print('Error supply ticker')

	try:
		data = pdr.get_data_yahoo(ticker, interval = interval, start = startdate, end = enddate)
	except:
		print("[ERROR] Unexpected error:", sys.exc_info())
		print("[ERROR] Check your inputs dumbo!.")

	d_return = Daily_Returns(data) # Daily percent return
	d_mean = sum(d_return[1:]) / len(d_return[1:])  # Mean of the daily percentage returns

	d_return.sort() # sort the percentage return list
	d_CVaR = 1/round(len(d_return[1:])*confindence) * sum(d_return[1:round(len(d_return[1:])*confindence)])  # Calculate daily CVaR
	m_CVaR = d_CVaR * (20 ** 0.5) #Calculate monthly VaR

	return m_CVaR
#--------------------------------------------------------------------------------
# End of Monthly_CVaR
#--------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
#
# Monthly_Volatility: Function
#
# Parameters: 
#   ticker:     Symbol of a stock 
#   confidence: Degree of confidence; Default value 0.05
#
#   Calculates volatility for a given ticker. Time series data is retrieved 
#   from the internet (Yahoo)
#
#--------------------------------------------------------------------------------
def Monthly_Volatility(ticker):
	ticker = ticker.upper()
	startdate = '2019-01-01'
	enddate = '2019-12-31'
	interval = 'd'

	if ticker == '':
		print('Error supply ticker')

    # Retrieve time series data from yahoo finance
	try:
		data = pdr.get_data_yahoo(ticker, interval = interval, start = startdate, end = enddate)
	except:
		print("[ERROR] Unexpected error:", sys.exc_info())
		print("[ERROR] Check your inputs dumbo!")
			
	d_return = Daily_Returns(data)  # Calculate daily percentage return 

	d_mean = sum(d_return[1:]) / len(d_return[1:])  # Mean of the daily percentage returns
	d_variance = sum([((x - d_mean) ** 2) for x in d_return[1:]]) / len(d_return[1:])    # Calculate variance
	d_std = d_variance ** 0.5 # Calculate standard deviation

	# Calcualte monthly volatility 
	# Assumes 250 trading days in a year 
	mVolatility = d_std * math.sqrt(250)
	
	return mVolatility
#--------------------------------------------------------------------------------
# End of Monthly_Volatility
#--------------------------------------------------------------------------------


#--------------------------------------------------------------------------------
# Initialize Data for MSFT
#--------------------------------------------------------------------------------
print("")
MVaR_msft = Monthly_VaR('MSFT')
print("Monthly VaR: ",MVaR_msft)

MCVaR_msft = Monthly_CVaR('MSFT')
print("Monthly CVaR: ",MCVaR_msft)

MVolatility_msft = Monthly_Volatility('MSFT')
print("Monthly Volatility: ",MVolatility_msft)
