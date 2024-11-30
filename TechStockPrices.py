import sys
import pandas as pd
import plotly.express as px
import seaborn as sb
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from datetime import datetime


# Data
Data = pd.read_csv("F:\DataAnalysis\TechStockPrices\TechStockPrices2.csv")

# converting Date->string to Date2->Datetime
# creation of Date2 column
dateFormat = '%Y-%m-%d'
Date2 = []
for i in range(2857):
   Date = datetime.strptime(str(Data['Date'][i]), dateFormat)
   Date2.append(Date)

Data['Date2'] = Date2
Data.to_csv("F:\DataAnalysis\TechStockPrices\TechStockPrices2.csv", index=False)


# creation of average column
Average = []
for i in range(2857):
    average = (Data['Open'][i] + Data['High'][i] + Data['Low'][i] + Data['Close'][i])/4
    Average.append(average)

Data['Average'] = Average
Data.to_csv("F:\DataAnalysis\TechStockPrices\TechStockPrices2.csv", index=False)


# creation of Domain column
Differance2 = []
Domain = []
for i in range(2857):
    difference = pd.Series([Data['Low'][i], Data['High'][i]]).diff()
    Differance2.append(difference)
for x in range(2857):
    Domain.append(Differance2[x][1])
Data['Domain'] = Domain
Data.to_csv("F:\DataAnalysis\TechStockPrices\TechStockPrices2.csv", index=False)


# Dataframes
DataFrame = pd.DataFrame(Data, columns=['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
DataFrame2 = pd.DataFrame(Data, columns=['Date2', 'Close'])
DataFrame3 = pd.DataFrame(Data, columns=['Date2', 'Volume'])
DataFrame4 = pd.DataFrame(Data, columns=['Domain', 'Volume'])

# moving average
window_size = 120
Data['high_smooth'] = Data['High'].rolling(window=window_size).mean()
plt.figure(figsize=(12, 6))

plt.plot(Data['High'], label='Original High', color='blue')
plt.plot(Data['high_smooth'], label=f'Moving Average (Window={window_size})', color='orange', linestyle='--')
plt.ylabel('High')
plt.title('Original vs Moving Average')
plt.legend()
plt.show()

# Domain chart
# 1
line = sb.lineplot(data=Data, x='Date2', y='Domain', color='blue')
plt.title('Price Changes Domain Over Time')
plt.xlabel('Date')
plt.show()
# 2 : Evolution chart
#fig, axs = plt.subplots(1, constrained_layout=True)
#fig.suptitle('evolution')
#axs.plot(Data['Domain'])
#plt.show()


# charts

plot = sb.kdeplot(Data, x='Average', color='blue')
plt.title('Stock Price Probability Distribution')
plt.xlabel('')
plt.ylabel('Price')
plt.show()
plot2 = sb.kdeplot(Data, x='Date2', y='Open', color='red')
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()
sb.lineplot(data=Data, x='Date2', y='Close', label='Price', color='blue')
plt.xlabel('Date')
plt.ylabel('Price')
plt.title('Stock Price Over Time')
plt.show()
line2 = sb.lineplot(data=Data, x='Date2', y='Volume', color='Green')
plt.title('Stock Volume Evolution Over Time')
plt.xlabel('Date')
plt.show()
regg = sb.regplot(x=Data['Volume'], y=Data['Close'], data=Data, color='orange')
plt.title('Regression Plot')
plt.ylabel('Price')
plt.show()
line3 = sb.lineplot(data=Data, x='Close', y='Volume', color='blue')
plt.title('Stock Volume Evolution Over Price Changes')
plt.xlabel('Price')
plt.show()


# descriptive statistics
missing = Data.isnull().mean()
Describe = Data.describe()
skew = DataFrame.skew()
kurt = DataFrame.kurt()
correlation = DataFrame.corr()

# RUN to text file
with open("F:\DataAnalysis\TechStockPrices\TechStockPrices.txt", 'w') as file:
    sys.stdout = file
    print(Data.head(5))
    print('\nData Information:\n')
    print(Data.info())
    print('\nMissing Values:\n', missing)
    print('\nDescriptive Statistics:\n', Describe)
    print('\nPrice Probability Distribution: Log-Normal')
    print('\nKurtosis:\n', kurt)
    print('\nSkewness:\n', skew)
    print('\nCorrelation Matrix:\n', correlation)
    print('\nPrice and Date correlation:\n', DataFrame2.corr())
    print('\nVolume and Date correlation:\n', DataFrame3.corr())
    print('\nVolume and Domain correlation:\n', DataFrame4.corr())
    
