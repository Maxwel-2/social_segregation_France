from sklearn.neighbors import KDTree
import numpy as np
import pandas as pd 
from sklearn.utils import shuffle 
import matplotlib.pyplot as plt
import datetime 
import geopandas as gp
time=datetime.datetime.now()
## DATA ##
df=   ### STEP 2
### CHOOSE VARIABLES ### STEP 3
df['logs']= # under-population
df['logt']= # total-population
####################
df['base_ratio']=df["logs"]/df["logt"]
df['sorted_index']= None
df['state_logt']= None
df['state_logs']= None
df['ratio']= None
df['check']=None
df['x']=df.geometry.centroid.x
df['y']=df.geometry.centroid.y
## INDEX RANDOMIZATION ##
df=shuffle(df)
df=df.reset_index(drop=True)
## TRESHOLD COMPUTATION ##
global_rate=df.logs.sum()/df.logt.sum()
tresh=0.05  # You can change the treshold here 
s= [global_rate*(1-tresh), global_rate*(1+tresh)]
## KDTREE COMPUTATION ##
kdt = KDTree(df[['x', 'y']])
## NEAREST NEIGHBOORS COMPUTATION ##
for x in range(len(df)): 
    origin= np.stack((df.x[x],df.y[x]),axis=-1)
    origin_kdt = np.expand_dims(origin, axis=0)
    nearest_point_index = kdt.query(origin_kdt, k=len(df), return_distance=True)
    df.sorted_index[x]=nearest_point_index[1]
    df.state_logs[x]= np.ones((1,len(df)))
    df.state_logt[x]= np.ones((1,len(df)))
    df.ratio[x]= np.ones((1,len(df)))
## ALL AGREGATION LEVELS COMPUTATION ##
for i in range(len(df)) : 
    for j in range(len(df)) : 
        if j == 0 : 
            df.state_logt[i][0,j]=df.logt[i]
            df.state_logs[i][0,j]=df.logs[i]
            df.ratio[i][0,j]=df.state_logs[i][0,j]/df.state_logt[i][0,j]
            if s[0] <df.ratio[i][0,j]<s[1] :
                df.check[i]= 0
        else : 
            df.state_logt[i][0,j]= df.state_logt[i][0,(j-1)] + df.logt[df.sorted_index[i][0,j]] 
            df.state_logs[i][0,j]= df.state_logs[i][0,(j-1)] + df.logs[df.sorted_index[i][0,j]]
            df.ratio[i][0,j]= df.state_logs[i][0,j]/df.state_logt[i][0,j]
            if (s[0] <df.ratio[i][0,j]<s[1]) and (df.check[i] is None) :
                df.check[i]=j
## DISPLAY ##
pd.set_option("display.max_columns", df.shape[1])
pd.set_option("display.max_rows", df.shape[0])
df
## DATA VISUALZATION ##
plt.figure()
plt.title("Trajectoires")
plt.axhline(y=s[0],color="black")
plt.axhline(y=s[1],color="black")
for i in range(len(df)) :     
    plt.plot(pd.Series(df.ratio[i].ravel()))
    plt.axvline(x=df.check[i])
plt.show()
df.plot(column='check',cmap='plasma')
df.plot(column='base_ratio',cmap='viridis')
## WORKING TIME
datetime.datetime.now()-time
