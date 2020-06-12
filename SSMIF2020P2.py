#---------------------------------------------------------------------------------
#   Agatha Malinowski
#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
#
#   Load all dependencies
#
#---------------------------------------------------------------------------------
import sqlite3
import pandas_datareader as pdr
from datetime import date
import sys


#---------------------------------------------------------------------------------
#
# Daily_Returns: Function
#
# Parameters: 
#   data: Times series as a list
#
#   Calculate Daily Returns Based on Adjusted Close
#
#--------------------------------------------------------------------------------
def Daily_Returns(data):
    pctchange = []
    for a,b in zip(data[::1], data[1::1]):
        value = (b/a) - 1
        pctchange.append( value )

    return pctchange
#----------------------------------------------------------------------------
#   End of Daily_Returns
#----------------------------------------------------------------------------


#---------------------------------------------------------------------------------
#
# Monthly_Var: Function
#
# Parameters: 
#   confidence: Degree of confidence; Default value 0.05
#
#   Calculates monthly Value At Risk (VaR) based on the provided degree of 
#   confidence (defult 0.05). Time series data is retrieved from a database 
#   file named SSMIF.db. The database file is expected to be located in the 
#   same folder as the program file. 
#
#--------------------------------------------------------------------------------
def Monthly_VaR(confindence = 0.05):

    try:    
        
        # Access time series data from SSMIF database
        # Database file is expected to be located in the same folder as the program file.
        conn = sqlite3.connect('SSMIF.db')
        conn.row_factory = lambda cursor, row: row[0]
        c = conn.cursor()
    
        data = c.execute("select Adj_Close from Stock_Data;").fetchall()
    
        conn.commit()
        conn.close()
        # Finished database operations

        d_return = Daily_Returns(data) # Daily percent return
        d_mean = sum(d_return) / len(d_return)  # Mean of the daily percentage returns
        d_variance = sum([((x - d_mean) ** 2) for x in d_return]) / len(d_return)    # Calculate variance
        d_std = d_variance ** 0.5 # Calculate standard deviation
        
        d_return.sort()
        zscore = (d_return[round(len(d_return[1:])*confindence)]-d_mean)/d_std

        d_VaR = zscore * d_std  # Calculate daily VaR
        m_VaR = d_VaR * (20 ** 0.5) #Calculate monthly VaR
        
        return m_VaR
    except:
        print("Unexpected error:", sys.exc_info())
        print('Database insert failed!') 
#----------------------------------------------------------------------------
# End of Monthly_Var
#----------------------------------------------------------------------------


#----------------------------------------------------------------------------
#   Fill_Table: Function
#
#   Parameters: 
#       ticker: Accepts a valid symbol of a tradable security
#
#   Retrieves time series data for a given ticker from the internet (Yahoo)
#   Data is stored in SSMIF.db database. The database file is created in the 
#   same folder as the program. 
#
#   !!!!! Function deletes ALL previously stored data. !!!!! 
#  
#----------------------------------------------------------------------------
def Fill_Table(ticker):
    ticker = ticker.upper()
    startdate = '2019-01-01'
    enddate = '2019-12-31'
    interval = 'd'
    
    try:    # Get the time series data for a given ticker from Yahoo 
        data = pdr.get_data_yahoo(ticker, interval = interval, start = startdate, end = enddate)
    except:
        print("[ERROR-Fill_Table] Unexpected error:", sys.exc_info())
        print('[ERROR-Fill_Table] Getting time series data from the internet')  

    # Clear the old data from the Stock_Data table
    try:    
        conn = sqlite3.connect('SSMIF.db')
        c = conn.cursor()
        
        c.execute("DROP table Stock_Data;") # run SQL statement erasing old data

        conn.commit()   # commit new transactions to the database
        conn.close()    # close the database connection
    except:
        print('[INFO-Fill_Table] Unable to clear the Stock_Data table. Continuing. ') 

    # Create Stock_Data tabel if it does not exists, and 
    # inserts data from pandas dataframe into the database
    try:    
        conn = sqlite3.connect('SSMIF.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS "Stock_Data" (
                "Timestamp" INTEGER NOT NULL,
                "Open" DECIMAL(10,1),
                "High" DECIMAL(10, 2),
                "Low" DECIMAL(10, 3),
                "Close" DECIMAL(10, 5),
                "Adj_Close" decimal(10,6));""")
    
        # Iterate through the time series data in data and insert each row to the database
        for index, row in data.iterrows():
            values = (index.value,row['High'], row['Low'], row['Open'], row['Close'], row['Adj Close'])
            c.execute("insert into Stock_Data values (?,?,?,?,?,?)", values)

        conn.commit()  # commit new transaction to the database
        conn.close()   # close the database connection
        # Finished database operations
    except:
        print("[ERROR-Fill_Table] Unexpected error:", sys.exc_info())
        print('[ERROR-Fill_Table] Database insert failed')  
#----------------------------------------------------------------------------
# End of Fill_Table
#----------------------------------------------------------------------------


#----------------------------------------------------------------------------
#
# Main program
#
#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# Populate database with a test time series data for the given ticker
#----------------------------------------------------------------------------
Fill_Table('msft')

#----------------------------------------------------------------------------
# Calculate Monthly VaR based on the data stored in the local DB
#----------------------------------------------------------------------------
MVaR_msft = Monthly_VaR()
print("")
print("Monthly VaR: ",MVaR_msft)

