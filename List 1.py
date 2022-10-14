#import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np

#stockInfo = yf.Ticker('PETR4.SA').info
#stockInfo.keys() for other properties you can explore
#can use period="" instead of start,end
#valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
#valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo)
#priceHistory = yf.download("dvn",start="2021-08-07",end="2021-08-14")
#tickArray=['vale3.sa','petr4.sa','itub4.sa','abev3.sa','jbss3.sa']
"""
# grabbing close data with yfinance
df = pd.DataFrame(yf.Ticker(tickArray[0]).history(start="2017-01-01",end="2022-09-10", actions=False)['Close'])
for i in range(1,5):
    temp = yf.Ticker(tickArray[i]).history(start="2017-01-01",end="2022-09-10", actions=False)['Close']
    tempdf=pd.DataFrame(temp)
    df.insert(i,tickArray[i],tempdf['Close'],allow_duplicates=True)
print(df)
df.to_csv('5 stock.csv', index=False)

# much simpler way to grab close data with yfinance
price_h = yf.download('vale3.sa petr4.sa itub4.sa abev3.sa jbss3.sa',start="2017-01-01",end="2022-10-09")['Adj Close']
df = pd.DataFrame(price_h)
print(df)
df.to_csv('5 stock.csv', index=False)
"""
df1 = pd.DataFrame(pd.read_csv('5 stock.csv'))
"""
# comparing asset growth by dividing by starting point
dfcom = pd.DataFrame(pd.read_csv('5 stock.csv'))
for i in range(5):
    temp = df2.iat[0,i]
    for j in range (1437):
        dfcom.iat[j,i]=df1.iat[j,i]/temp
# much simpler way to divide columns
for i in df1.columns:
   df1[i]=df1[i].div(df1[i][0])
df1.plot.line()      
"""
"""
#Moving average calculation 5 days
MAlist = [[],[],[],[],[]]
for i in range(len(df1.columns)):
    Templist = []
    for j in range (0,1437,5):
        temp = 0
        count = 1435
        if j<1435:
            Templist.append((df1.iat[j,i]+df1.iat[j+1,i]+df1.iat[j+2,i]+df1.iat[j+3,i]+df1.iat[j+4,i])/5)
    Templist.append((df1.iat[1436,i]+df1.iat[1435,i])/2)
    MAlist[i].extend(Templist)
MAf = pd.DataFrame(MAlist).T
#MAf.plot()
#plt.show()
"""
#Alternative simpler moving average 5 days
movavg = pd.DataFrame(df1)
for i in df1.columns:
    df1[i+' average'] = df1[i].rolling(window=5).mean()
df1.plot()
plt.show()
#Simple moving average 20 days
df1 = pd.read_csv('5 stock.csv')
for i in df1.columns:
    df1[i+' average'] = df1[i].rolling(window=20).mean()
df1.plot()
plt.show()
#calculating annual returns
df1 = pd.read_csv('5 stock.csv')
for i in df1.columns:
    tempReturn=pow((df1.at[1436,i]/df1.at[0,i]),1/5.772)-1
    print("annual return (%) ",i," ",tempReturn*100)
for i in df1.columns:
    tempReturn=math.log(df1.at[1436,i]/df1.at[0,i])/5.772
    print("annual log return (%) ",i," ",tempReturn*100)
#calculating log return histogram
df2 = pd.Series(np.log(df1['ABEV3.SA']/(df1['ABEV3.SA'].shift(1))))
df2.plot.hist()
plt.show()
#annual return mean and sd + sharpe + portfolio
Rat = []
sharpeS = 0
for i in df1.columns:
    temp = []
    for j in range(5):
        temp.append(math.log(df1.at[(j+1)*249,i]/df1.at[j*249,i]))
    temp.append(math.log(df1.at[1436,i]/df1.at[1245,i])/0.772)
    print(i," mean(%):", np.mean(temp)*100, " stdev:", np.std(temp, ddof=1), " sharpe:",np.mean(temp)/np.std(temp, ddof=1))
    sharpeS = sharpeS+np.mean(temp)/np.std(temp, ddof=1)
    Rat.append(np.mean(temp)/np.std(temp, ddof=1))
port = pd.Series(df1['ABEV3.SA'].mul(0))
count = 0
for i in df1.columns:
    temp = Rat[count]/sharpeS
    count += 1
    port = port.add(df1[i].mul(temp))
temp = []
for j in range(5):
    temp.append(math.log(port[(j+1)*249]/port[j*249]))
temp.append(math.log(port[1436]/port[1245])/0.772)
print("Portfolio mean(%):", np.mean(temp)*100, " stdev:", np.std(temp, ddof=1), " sharpe:",np.mean(temp)/np.std(temp, ddof=1))
#graphing portfolio returns + everything else
df1['Portfolio'] = port
for i in df1.columns:
    df1[i]=df1[i].div(df1[i][0])
df1.plot()
plt.show()
    