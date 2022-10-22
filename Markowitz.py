import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
np.random.seed(52)
df1 = pd.DataFrame(pd.read_csv('5 stock.csv'))
#producing random weights
def rand_weights(n):
    k = np.random.rand(n)
    return k / sum(k)
#log returns
for i in df1.columns:
    df1[i]=np.log(df1[i]/df1[i].shift(1))
port = pd.Series(df1['ABEV3.SA'].mul(0))
mean = []
std = []
sharpe = []
temp = []
weights = []
#producing portfolios
for j in range (1000):
    port = pd.Series(df1['ABEV3.SA'].mul(0))
    count = 0
    temp = rand_weights(5)
    #
    for i in df1.columns:
        t = temp[count]
        count += 1
        port = port.add(df1[i].mul(t))
    mean.append(np.mean(port))
    std.append(np.std(port))
    sharpe.append(np.mean(port)/np.std(port, ddof=1))
    weights.append(temp)
fig = plt.figure()
plt.plot(std, mean, 'o', markersize=5)
plt.xlabel('std')
plt.ylabel('mean')
plt.title('Mean and Std of 5 stock')
maxS = max(sharpe)
print("Max sharpe index:", sharpe.index(maxS), " weights", weights[sharpe.index(maxS)])