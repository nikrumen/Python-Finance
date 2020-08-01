#1.8.20 python for finance first lesson

import yfinance as yf
import numpy as nu
import datetime as dt
import pandas as pd

# User inputs ticker, output ticker, 
ticker=input("Enter your stock ticker symbol: ")
print(ticker)

#make datetime object so python can process it as datetime
startyear=2019
startmonth=1
startday=1
start=dt.datetime(startyear,startmonth,startday)
end=dt.datetime.now()

#getting and storing data for input tciker between two dates in dataframe
data = yf.download(ticker,start,end)
print(data)

#set moving average
ma=50
smaString="Sma_"+str(ma)

#creates column with smaString; it is rolling moving average with window size=ma
#its source is 4th column in data 
data[smaString]=data.iloc[:,4].rolling(window=ma).mean()
#first 50 days are empty, so delete them
data=data.iloc[ma:]

#compare adj close with ma in each row and count number of higher and lower closes
#can call column as index "iloc[:,4]" or name "["Adj Close"]"
numHigher=0
numLower=0
for i in data.index:
  if(data["Adj Close"][i]>data[smaString][i]):
    print("The Close is higher")
    numHigher+=1
  else:
    print("The close is lower")
    numLower+=1
print("Close>MA "+str(numHigher)+" times")
print("Close<MA "+str(numLower)+" times")

print("Test Commit")