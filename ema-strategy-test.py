#1.8.2020 python for finance second lesson
#Backtesting a strategy based on crossings of two EMA of different periods
#check if shorter EMA is higher than longer EMA on each day in given timeframe
#If shorter>longer -> uptrend. if shorter<longer -> downtrend
#Simulate entering and closing position on crossings
#show results and summary statistics to check strategy

import yfinance as yf
import numpy as nu
import datetime as dt
import pandas as pd

ticker=input("Enter a stock ticker symbol: ")
print(ticker)

startyear=2010
startmonth=1
startday=1
start=dt.datetime(startyear,startmonth,startday)
end=dt.datetime.now()
data = yf.download(ticker,start,end)

#list of all EMA in use (6 for shorter, 6 for longer)
emasUsed=[3,5,8,10,12,15,30,35,40,45,50,60]

#setting up all EMAs(ewm) with span from ema list
for x in emasUsed:
  ema=x
  data["EMA_"+str(ema)]=data.iloc[:,4].ewm(span=ema, adjust=False).mean().round(2)

print(data.tail())

#pos defines if we entr position(1), num for tracking current, percentchange for results of trades
pos=0
num=0
percentchange=[]

for i in data.index:
  #minimum of short-term emas
  cmin=min(data["EMA_3"][i],data["EMA_5"][i],data["EMA_8"][i],data["EMA_10"][i],data["EMA_12"][i],data["EMA_15"][i])
  #maximum of long-term emas
  cmax=max(data["EMA_30"][i],data["EMA_35"][i],data["EMA_40"][i],data["EMA_45"][i],data["EMA_50"][i],data["EMA_60"][i])
  close=data["Adj Close"][i]

  #define if minimum of short-term emas is above or below maximums of long-term emas
  if(cmin>cmax):
    print("Upward Trend")
    #if in upward trend and no position, open position at close price
    if(pos==0):
      bp=close
      pos=1
      print("Buying now at "+str(bp))

  elif(cmin<cmax):
    print("Downward Trend")
    #if in downward trend and have position, close it
    if(pos==1):
      sp=close
      pos=0
      print("Selling now at "+str(sp))
      pc=(sp/bp-1)*100
      #add pc for closed position to percentchange list
      percentchange.append(pc)    
  
  #if dataset ended and still have position, close it
  if(num==data["Adj Close"].count()-1 and pos==1):
    sp=close
    pos=0
    print("Selling to close test at "+str(sp))
    pc=(sp/bp-1)*100
    percentchange.append(pc)

  #add to num with each row iteration
  num+=1

print(percentchange)

#calculate position statistics for each item in percentchange list
profit=0
numprofits=0
losses=0
numlosses=0
totalreturn=1

for i in percentchange:
  if(i>0):
    profit+=i
    numprofits+=1
  else:
    losses+=i
    numlosses+=1
  totalreturn=totalreturn*((i/100)+1)

#calculate return as %, av. profit and loss, profit/loss ratio
totalreturn=round((totalreturn-1)*100,2)
if(numprofits>0):
  avgprofit=profit/numprofits
  maxprofit=str(max(percentchange))
else:
  avgprofit=0
  maxprofit="undefined"

if(numlosses>0):
  avglosses=losses/numlosses
  maxlosses=str(min(percentchange))
  ratio=str(-avgprofit/avglosses)
else:
  avglosses=0
  maxlosses="undefined"
  ratio="infinite"

if(numprofits>0 or numlosses>0):
  battingavg=numprofits/(numprofits+numlosses)
else:
  battingavg=0

#print all stuff in nice form
print()
print("Results for "+ ticker +" going back to "+str(data.index[0])+", Sample size: "+str(numprofits+numlosses)+" trades")
print("EMAs used: "+str(emasUsed))
print("Batting Avg: "+ str(battingavg))
print("Gain/loss ratio: "+ ratio)
print("Average Gain: "+ str(avgprofit))
print("Average Loss: "+ str(avglosses))
print("Max Return: "+ maxprofit)
print("Max Loss: "+ maxlosses)
print("Total return over "+str(numprofits+numlosses)+ " trades: "+ str(totalreturn)+"%" )
print()