#%% 
import pandas as pd
import matplotlib
import os
import math
#%% 
df = pd.DataFrame()
i = 0
for f in os.listdir(r"C:\Users\jokub\Desktop\Work\algoritmai\new\data\equity-minute-data"):
    try:
        df2 = pd.read_csv('{}/{}'.format(r"C:\Users\jokub\Desktop\Work\algoritmai\new\data\equity-minute-data", f))
        df = df.append(df2)
        i+=1
    except:
        print(f'i{i}')
# %%
df['Date Time'] = df[['Date',' Time']].apply(lambda x : '{}{}'.format(x[0],x[1]), axis=1)
df = df[['Date Time', ' Open', ' High', ' Low', ' Close', ' Volume']]
df['Date Time'] = pd.to_datetime(df['Date Time'])
# %%
df.rename(columns = {' Open' : 'open', ' High':'high', ' Low':'low', ' Close' : 'close', ' Volume' : 'volume'}, inplace = True)
# %%
df.to_csv("SPY_from_git.csv", sep=',', encoding='utf-8')
# %%
