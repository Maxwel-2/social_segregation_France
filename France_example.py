from sklearn.neighbors import KDTree
import numpy as np
import pandas as pd 
from sklearn.utils import shuffle 
import matplotlib.pyplot as plt
import datetime 
import geopandas as gp
import os 


PATH=os.getcwd()+"/" # Put social_segregation_france file path here 

######### P A R I S #########

time=datetime.datetime.now()
## DATA ##
data = pd.read_csv(PATH + "LOGPARISPF.CSV", sep=";")
IRIS_B=gp.read_file(PATH +'CONTOURS-IRIS_2-1_SHP_LAMB93_FE-2015/CONTOURS-IRIS.shp')
IRIS_B['x']=IRIS_B.geometry.centroid.x
IRIS_B['y']=IRIS_B.geometry.centroid.y
PARIS=IRIS_B[IRIS_B['NOM_COM'].str.match('Paris')]
PARIS=PARIS.drop(PARIS[PARIS["NOM_COM"]=="Parisot"].index)
PARIS=PARIS.drop(PARIS[PARIS["NOM_COM"]=="Paris-l'Hôpital"].index)
PARIS=PARIS.drop(PARIS[PARIS['NOM_IRIS'].str.match('Bois')].index)
PARIS=PARIS.drop(PARIS[PARIS['NOM_IRIS'].str.match('Jardin du Luxembourg')].index)
df=PARIS.ix[:,('x','y','CODE_IRIS','NOM_IRIS','geometry')]
df['CODE_IRIS']=pd.to_numeric(df.CODE_IRIS)
data2= pd.merge(df,data,on="CODE_IRIS",how="outer")
data2=data2.fillna(value=0)
data2=data2[data2["logt"]!=0]
df=data2
df['taux_base']=df["logs"]/df["logt"]
df['sorted_index']= None
df['state_logt']= None
df['state_logs']= None
df['taux']= None
df['check']=None
## INDEX RANDOMIZATION ##
df=shuffle(df)
df=df.reset_index(drop=True)
## TRESHOLD COMPUTATION ##
taux_global=df.logs.sum()/df.logt.sum()
seuil=0.05
s= [taux_global*(1-seuil), taux_global*(1+seuil)]
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
    df.taux[x]= np.ones((1,len(df)))
## ALL AGREGATION LEVELS COMPUTATION ##
for i in range(len(df)) : 
    for j in range(len(df)) : 
        if j == 0 : 
            df.state_logt[i][0,j]=df.logt[i]
            df.state_logs[i][0,j]=df.logs[i]
            df.taux[i][0,j]=df.state_logs[i][0,j]/df.state_logt[i][0,j]
            if s[0] <df.taux[i][0,j]<s[1] : 
                df.check[i]= 0
        else : 
            df.state_logt[i][0,j]= df.state_logt[i][0,(j-1)] + df.logt[df.sorted_index[i][0,j]] 
            df.state_logs[i][0,j]= df.state_logs[i][0,(j-1)] + df.logs[df.sorted_index[i][0,j]]
            df.taux[i][0,j]= df.state_logs[i][0,j]/df.state_logt[i][0,j]
            if (s[0] <df.taux[i][0,j]<s[1]) and (df.check[i] is None) : 
                df.check[i]=j
## DISPLAY ##
pd.set_option("display.max_columns", df.shape[1])
pd.set_option("display.max_rows", 10)
df
## DATA VISUALZATION ##
plt.figure()
plt.title("Trajectories")
plt.axhline(y=s[0],color="black")
plt.axhline(y=s[1],color="black")
for i in range(len(df)) :     
    plt.plot(pd.Series(df.taux[i].ravel()))
    plt.axvline(x=df.check[i],lw=0.2)
plt.show()
df.plot(column='check',cmap='plasma')
df.plot(column='taux_base',cmap='viridis_r')
## WORKING TIME
datetime.datetime.now()-time


######### B O R D E A U X #########

time=datetime.datetime.now()
## DATA ##
data = pd.read_csv(PATH +"Bordeaux.CSV", sep=";")
df=IRIS_B.ix[:,('x','y','CODE_IRIS','NOM_IRIS','geometry')]
df['CODE_IRIS']=df['CODE_IRIS'].astype(str)
data['CODE_IRIS']=data['CODE_IRIS'].astype(str)
data2= pd.merge(df,data,on="CODE_IRIS",how="right")
data2=data2.fillna(value=0)
data2=data2[data2["logt"]!=0]
df=data2
df['taux_base']=df["logs"]/df["logt"]
df['sorted_index']= None
df['state_logt']= None
df['state_logs']= None
df['taux']= None
df['check']=None
## INDEX RANDOMIZATION ##
df=shuffle(df)
df=df.reset_index(drop=True)
## TRESHOLD COMPUTATION ##
taux_global=df.logs.sum()/df.logt.sum()
seuil=0.05
s= [taux_global*(1-seuil), taux_global*(1+seuil)]
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
    df.taux[x]= np.ones((1,len(df)))
## ALL AGREGATION LEVELS COMPUTATION ##
for i in range(len(df)) :
    for j in range(len(df)) :
        if j == 0 :
            df.state_logt[i][0,j]=df.logt[i]
            df.state_logs[i][0,j]=df.logs[i]
            df.taux[i][0,j]=df.state_logs[i][0,j]/df.state_logt[i][0,j]
            if s[0] <df.taux[i][0,j]<s[1] :
                df.check[i]= 0
        else :
            df.state_logt[i][0,j]= df.state_logt[i][0,(j-1)] + df.logt[df.sorted_index[i][0,j]]
            df.state_logs[i][0,j]= df.state_logs[i][0,(j-1)] + df.logs[df.sorted_index[i][0,j]]
            df.taux[i][0,j]= df.state_logs[i][0,j]/df.state_logt[i][0,j]
            if (s[0] <df.taux[i][0,j]<s[1]) and (df.check[i] is None) :
                df.check[i]=j
## DISPLAY ##
pd.set_option("display.max_columns", df.shape[1])
pd.set_option("display.max_rows", 10)
df
## DATA VISUALZATION ##
plt.figure()
plt.title("Trajectoires")
plt.axhline(y=s[0],color="black")
plt.axhline(y=s[1],color="black")
for i in range(len(df)) :
    plt.plot(pd.Series(df.taux[i].ravel()))
    plt.axvline(x=df.check[i],lw=0.2)
plt.show()
df.plot(column='check',cmap='plasma')
df.plot(column='taux_base',cmap='viridis_r')
## WORKING TIME ##
datetime.datetime.now()-time

######### G R E N O B L E #########

time=datetime.datetime.now()
## DATA ##
data = pd.read_csv(PATH +"Grenoble.CSV", sep=";")
df=IRIS_B.ix[:,('x','y','CODE_IRIS','NOM_IRIS','geometry')]
df['CODE_IRIS']=df['CODE_IRIS'].astype(str)
data['CODE_IRIS']=data['CODE_IRIS'].astype(str)
data2= pd.merge(df,data,on="CODE_IRIS",how="right")
data2=data2.fillna(value=0)
data2=data2[data2["logt"]!=0]
df=data2
df['taux_base']=df["logs"]/df["logt"]
df['sorted_index']= None
df['state_logt']= None
df['state_logs']= None
df['taux']= None
df['check']=None
## INDEX RANDOMIZATION ##
df=shuffle(df)
df=df.reset_index(drop=True)
## TRESHOLD COMPUTATION ##
taux_global=df.logs.sum()/df.logt.sum()
seuil=0.05
s= [taux_global*(1-seuil), taux_global*(1+seuil)]
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
    df.taux[x]= np.ones((1,len(df)))
## ALL AGREGATION LEVELS COMPUTATION ##
for i in range(len(df)) :
    for j in range(len(df)) :
        if j == 0 :
            df.state_logt[i][0,j]=df.logt[i]
            df.state_logs[i][0,j]=df.logs[i]
            df.taux[i][0,j]=df.state_logs[i][0,j]/df.state_logt[i][0,j]
            if s[0] <df.taux[i][0,j]<s[1] :
                df.check[i]= 0
        else :
            df.state_logt[i][0,j]= df.state_logt[i][0,(j-1)] + df.logt[df.sorted_index[i][0,j]]
            df.state_logs[i][0,j]= df.state_logs[i][0,(j-1)] + df.logs[df.sorted_index[i][0,j]]
            df.taux[i][0,j]= df.state_logs[i][0,j]/df.state_logt[i][0,j]
            if (s[0] <df.taux[i][0,j]<s[1]) and (df.check[i] is None) :
                df.check[i]=j
## DISPLAY ##
pd.set_option("display.max_columns", df.shape[1])
pd.set_option("display.max_rows", 10)
df
## DATA VISUALZATION ##
plt.figure()
plt.title("Trajectoires")
plt.axhline(y=s[0],color="black")
plt.axhline(y=s[1],color="black")
for i in range(len(df)) :
    plt.plot(pd.Series(df.taux[i].ravel()))
    plt.axvline(x=df.check[i],lw=0.2)
plt.show()
df.plot(column='check',cmap='plasma')
df.plot(column='taux_base',cmap='viridis_r')
## WORKING TIME ##
datetime.datetime.now()-time

######### L I L L E #########

time=datetime.datetime.now()
## DATA ##
data = pd.read_csv(PATH +"Lille.CSV", sep=";")
df=IRIS_B.ix[:,('x','y','CODE_IRIS','NOM_IRIS','geometry')]
df['CODE_IRIS']=df['CODE_IRIS'].astype(str)
data['CODE_IRIS']=data['CODE_IRIS'].astype(str)
data2= pd.merge(df,data,on="CODE_IRIS",how="right")
data2=data2.fillna(value=0)
data2=data2[data2["logt"]!=0]
df=data2
df['taux_base']=df["logs"]/df["logt"]
df['sorted_index']= None
df['state_logt']= None
df['state_logs']= None
df['taux']= None
df['check']=None
## INDEX RANDOMIZATION ##
df=shuffle(df)
df=df.reset_index(drop=True)
## TRESHOLD COMPUTATION ##
taux_global=df.logs.sum()/df.logt.sum()
seuil=0.05
s= [taux_global*(1-seuil), taux_global*(1+seuil)]
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
    df.taux[x]= np.ones((1,len(df)))
## ALL AGREGATION LEVELS COMPUTATION ##
for i in range(len(df)) :
    for j in range(len(df)) :
        if j == 0 :
            df.state_logt[i][0,j]=df.logt[i]
            df.state_logs[i][0,j]=df.logs[i]
            df.taux[i][0,j]=df.state_logs[i][0,j]/df.state_logt[i][0,j]
            if s[0] <df.taux[i][0,j]<s[1] :
                df.check[i]= 0
        else :
            df.state_logt[i][0,j]= df.state_logt[i][0,(j-1)] + df.logt[df.sorted_index[i][0,j]]
            df.state_logs[i][0,j]= df.state_logs[i][0,(j-1)] + df.logs[df.sorted_index[i][0,j]]
            df.taux[i][0,j]= df.state_logs[i][0,j]/df.state_logt[i][0,j]
            if (s[0] <df.taux[i][0,j]<s[1]) and (df.check[i] is None) :
                df.check[i]=j
## DISPLAY ##
pd.set_option("display.max_columns", df.shape[1])
pd.set_option("display.max_rows", 10)
df
## DATA VISUALZATION ##
plt.figure()
plt.title("Trajectoires")
plt.axhline(y=s[0],color="black")
plt.axhline(y=s[1],color="black")
for i in range(len(df)) :
    plt.plot(pd.Series(df.taux[i].ravel()))
    plt.axvline(x=df.check[i],lw=0.2)
plt.show()
df.plot(column='check',cmap='plasma')
df.plot(column='taux_base',cmap='viridis_r')
## WORKING TIME ##
datetime.datetime.now()-time

######### L Y O N #########

time=datetime.datetime.now()
## DATA ##
data = pd.read_csv(PATH +"Lyon.CSV", sep=";")
df=IRIS_B.ix[:,('x','y','CODE_IRIS','NOM_IRIS','geometry')]
df['CODE_IRIS']=df['CODE_IRIS'].astype(str)
data['CODE_IRIS']=data['CODE_IRIS'].astype(str)
data2= pd.merge(df,data,on="CODE_IRIS",how="right")
data2=data2.fillna(value=0)
data2=data2[data2["logt"]!=0]
df=data2
df['taux_base']=df["logs"]/df["logt"]
df['sorted_index']= None
df['state_logt']= None
df['state_logs']= None
df['taux']= None
df['check']=None
## INDEX RANDOMIZATION ##
df=shuffle(df)
df=df.reset_index(drop=True)
## TRESHOLD COMPUTATION ##
taux_global=df.logs.sum()/df.logt.sum()
seuil=0.05
s= [taux_global*(1-seuil), taux_global*(1+seuil)]
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
    df.taux[x]= np.ones((1,len(df)))
## ALL AGREGATION LEVELS COMPUTATION ##
for i in range(len(df)) :
    for j in range(len(df)) :
        if j == 0 :
            df.state_logt[i][0,j]=df.logt[i]
            df.state_logs[i][0,j]=df.logs[i]
            df.taux[i][0,j]=df.state_logs[i][0,j]/df.state_logt[i][0,j]
            if s[0] <df.taux[i][0,j]<s[1] :
                df.check[i]= 0
        else :
            df.state_logt[i][0,j]= df.state_logt[i][0,(j-1)] + df.logt[df.sorted_index[i][0,j]]
            df.state_logs[i][0,j]= df.state_logs[i][0,(j-1)] + df.logs[df.sorted_index[i][0,j]]
            df.taux[i][0,j]= df.state_logs[i][0,j]/df.state_logt[i][0,j]
            if (s[0] <df.taux[i][0,j]<s[1]) and (df.check[i] is None) :
                df.check[i]=j
## DISPLAY ##
pd.set_option("display.max_columns", df.shape[1])
pd.set_option("display.max_rows", 10)
df
## DATA VISUALZATION ##
plt.figure()
plt.title("Trajectoires")
plt.axhline(y=s[0],color="black")
plt.axhline(y=s[1],color="black")
for i in range(len(df)) :
    plt.plot(pd.Series(df.taux[i].ravel()))
    plt.axvline(x=df.check[i],lw=0.2)
plt.show()
df.plot(column='check',cmap='plasma')
df.plot(column='taux_base',cmap='viridis_r')
## WORKING TIME ##
datetime.datetime.now()-time

######### M A R S E I L L E #########

time=datetime.datetime.now()
## DATA ##
data = pd.read_csv(PATH +"Marseille.CSV", sep=";")
df=IRIS_B.ix[:,('x','y','CODE_IRIS','NOM_IRIS','geometry')]
df['CODE_IRIS']=df['CODE_IRIS'].astype(str)
data['CODE_IRIS']=data['CODE_IRIS'].astype(str)
data2= pd.merge(df,data,on="CODE_IRIS",how="right")
data2=data2.fillna(value=0)
data2=data2[data2["logt"]!=0]
df=data2
df['taux_base']=df["logs"]/df["logt"]
df['sorted_index']= None
df['state_logt']= None
df['state_logs']= None
df['taux']= None
df['check']=None
## INDEX RANDOMIZATION ##
df=shuffle(df)
df=df.reset_index(drop=True)
## TRESHOLD COMPUTATION ##
taux_global=df.logs.sum()/df.logt.sum()
seuil=0.05
s= [taux_global*(1-seuil), taux_global*(1+seuil)]
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
    df.taux[x]= np.ones((1,len(df)))
## ALL AGREGATION LEVELS COMPUTATION ##
for i in range(len(df)) :
    for j in range(len(df)) :
        if j == 0 :
            df.state_logt[i][0,j]=df.logt[i]
            df.state_logs[i][0,j]=df.logs[i]
            df.taux[i][0,j]=df.state_logs[i][0,j]/df.state_logt[i][0,j]
            if s[0] <df.taux[i][0,j]<s[1] :
                df.check[i]= 0
        else :
            df.state_logt[i][0,j]= df.state_logt[i][0,(j-1)] + df.logt[df.sorted_index[i][0,j]]
            df.state_logs[i][0,j]= df.state_logs[i][0,(j-1)] + df.logs[df.sorted_index[i][0,j]]
            df.taux[i][0,j]= df.state_logs[i][0,j]/df.state_logt[i][0,j]
            if (s[0] <df.taux[i][0,j]<s[1]) and (df.check[i] is None) :
                df.check[i]=j
## DISPLAY ##
pd.set_option("display.max_columns", df.shape[1])
pd.set_option("display.max_rows", 10)
df
## DATA VISUALZATION ##
plt.figure()
plt.title("Trajectoires")
plt.axhline(y=s[0],color="black")
plt.axhline(y=s[1],color="black")
for i in range(len(df)) :
    plt.plot(pd.Series(df.taux[i].ravel()))
    plt.axvline(x=df.check[i],lw=0.2)
plt.show()
df.plot(column='check',cmap='plasma')
df.plot(column='taux_base',cmap='viridis_r')
## WORKING TIME ##
datetime.datetime.now()-time

######### N A N T E S #########

time=datetime.datetime.now()
## DATA ##
data = pd.read_csv(PATH +"Nantes.CSV", sep=";")
df=IRIS_B.ix[:,('x','y','CODE_IRIS','NOM_IRIS','geometry')]
df['CODE_IRIS']=df['CODE_IRIS'].astype(str)
data['CODE_IRIS']=data['CODE_IRIS'].astype(str)
data2= pd.merge(df,data,on="CODE_IRIS",how="right")
data2=data2.fillna(value=0)
data2=data2[data2["logt"]!=0]
df=data2
df['taux_base']=df["logs"]/df["logt"]
df['sorted_index']= None
df['state_logt']= None
df['state_logs']= None
df['taux']= None
df['check']=None
## INDEX RANDOMIZATION ##
df=shuffle(df)
df=df.reset_index(drop=True)
## TRESHOLD COMPUTATION ##
taux_global=df.logs.sum()/df.logt.sum()
seuil=0.05
s= [taux_global*(1-seuil), taux_global*(1+seuil)]
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
    df.taux[x]= np.ones((1,len(df)))
## ALL AGREGATION LEVELS COMPUTATION ##
for i in range(len(df)) :
    for j in range(len(df)) :
        if j == 0 :
            df.state_logt[i][0,j]=df.logt[i]
            df.state_logs[i][0,j]=df.logs[i]
            df.taux[i][0,j]=df.state_logs[i][0,j]/df.state_logt[i][0,j]
            if s[0] <df.taux[i][0,j]<s[1] :
                df.check[i]= 0
        else :
            df.state_logt[i][0,j]= df.state_logt[i][0,(j-1)] + df.logt[df.sorted_index[i][0,j]]
            df.state_logs[i][0,j]= df.state_logs[i][0,(j-1)] + df.logs[df.sorted_index[i][0,j]]
            df.taux[i][0,j]= df.state_logs[i][0,j]/df.state_logt[i][0,j]
            if (s[0] <df.taux[i][0,j]<s[1]) and (df.check[i] is None) :
                df.check[i]=j
## DISPLAY ##
pd.set_option("display.max_columns", df.shape[1])
pd.set_option("display.max_rows", 10)
df
## DATA VISUALZATION ##
plt.figure()
plt.title("Trajectoires")
plt.axhline(y=s[0],color="black")
plt.axhline(y=s[1],color="black")
for i in range(len(df)) :
    plt.plot(pd.Series(df.taux[i].ravel()))
    plt.axvline(x=df.check[i],lw=0.2)
plt.show()
df.plot(column='check',cmap='plasma')
df.plot(column='taux_base',cmap='viridis_r')
## WORKING TIME ##
datetime.datetime.now()-time

######### N I C E  #########

time=datetime.datetime.now()
## DATA ##
data = pd.read_csv(PATH +"Nice.CSV", sep=";")
df=IRIS_B.ix[:,('x','y','CODE_IRIS','NOM_IRIS','geometry')]
data['CODE_IRIS']=pd.to_numeric(data.CODE_IRIS, errors='ignore')
df['CODE_IRIS']= pd.to_numeric(df.CODE_IRIS, errors='coerce')
data2=df.merge(data,on="CODE_IRIS",how="right")
data2=data2.fillna(value=0)
data2=data2[data2["logt"]!=0]
df=data2
df['taux_base']=df["logs"]/df["logt"]
df['sorted_index']= None
df['state_logt']= None
df['state_logs']= None
df['taux']= None
df['check']=None
## INDEX RANDOMIZATION ##
df=shuffle(df)
df=df.reset_index(drop=True)
## TRESHOLD COMPUTATION ##
taux_global=df.logs.sum()/df.logt.sum()
seuil=0.05
s= [taux_global*(1-seuil), taux_global*(1+seuil)]
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
    df.taux[x]= np.ones((1,len(df)))
## ALL AGREGATION LEVELS COMPUTATION ##
for i in range(len(df)) :
    for j in range(len(df)) :
        if j == 0 :
            df.state_logt[i][0,j]=df.logt[i]
            df.state_logs[i][0,j]=df.logs[i]
            df.taux[i][0,j]=df.state_logs[i][0,j]/df.state_logt[i][0,j]
            if s[0] <df.taux[i][0,j]<s[1] :
                df.check[i]= 0
        else :
            df.state_logt[i][0,j]= df.state_logt[i][0,(j-1)] + df.logt[df.sorted_index[i][0,j]]
            df.state_logs[i][0,j]= df.state_logs[i][0,(j-1)] + df.logs[df.sorted_index[i][0,j]]
            df.taux[i][0,j]= df.state_logs[i][0,j]/df.state_logt[i][0,j]
            if (s[0] <df.taux[i][0,j]<s[1]) and (df.check[i] is None) :
                df.check[i]=j
## DISPLAY ##
pd.set_option("display.max_columns", df.shape[1])
pd.set_option("display.max_rows", 10)
df
## DATA VISUALZATION ##
plt.figure()
plt.title("Trajectoires")
plt.axhline(y=s[0],color="black")
plt.axhline(y=s[1],color="black")
for i in range(len(df)) :
    plt.plot(pd.Series(df.taux[i].ravel()))
    plt.axvline(x=df.check[i],lw=0.2)
plt.show()
df.plot(column='check',cmap='plasma')
df.plot(column='taux_base',cmap='viridis_r')
## WORKING TIME ##
datetime.datetime.now()-time

######### T O U L O N #########

time=datetime.datetime.now()
## DATA ##
data = pd.read_csv(PATH +"Toulon.CSV", sep=";")
df=IRIS_B.ix[:,('x','y','CODE_IRIS','NOM_IRIS','geometry')]
df['CODE_IRIS']=df['CODE_IRIS'].astype(str)
data['CODE_IRIS']=data['CODE_IRIS'].astype(str)
data2= pd.merge(df,data,on="CODE_IRIS",how="right")
data2=data2.fillna(value=0)
data2=data2[data2["logt"]!=0]
df=data2
df['taux_base']=df["logs"]/df["logt"]
df['sorted_index']= None
df['state_logt']= None
df['state_logs']= None
df['taux']= None
df['check']=None
## INDEX RANDOMIZATION ##
df=shuffle(df)
df=df.reset_index(drop=True)
## TRESHOLD COMPUTATION ##
taux_global=df.logs.sum()/df.logt.sum()
seuil=0.05
s= [taux_global*(1-seuil), taux_global*(1+seuil)]
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
    df.taux[x]= np.ones((1,len(df)))
## ALL AGREGATION LEVELS COMPUTATION ##
for i in range(len(df)) :
    for j in range(len(df)) :
        if j == 0 :
            df.state_logt[i][0,j]=df.logt[i]
            df.state_logs[i][0,j]=df.logs[i]
            df.taux[i][0,j]=df.state_logs[i][0,j]/df.state_logt[i][0,j]
            if s[0] <df.taux[i][0,j]<s[1] :
                df.check[i]= 0
        else :
            df.state_logt[i][0,j]= df.state_logt[i][0,(j-1)] + df.logt[df.sorted_index[i][0,j]]
            df.state_logs[i][0,j]= df.state_logs[i][0,(j-1)] + df.logs[df.sorted_index[i][0,j]]
            df.taux[i][0,j]= df.state_logs[i][0,j]/df.state_logt[i][0,j]
            if (s[0] <df.taux[i][0,j]<s[1]) and (df.check[i] is None) :
                df.check[i]=j
## DISPLAY ##
pd.set_option("display.max_columns", df.shape[1])
pd.set_option("display.max_rows", 10)
df
## DATA VISUALZATION ##
plt.figure()
plt.title("Trajectoires")
plt.axhline(y=s[0],color="black")
plt.axhline(y=s[1],color="black")
for i in range(len(df)) :
    plt.plot(pd.Series(df.taux[i].ravel()))
    plt.axvline(x=df.check[i],lw=0.2)
plt.show()
df.plot(column='check',cmap='plasma')
df.plot(column='taux_base',cmap='viridis_r')
## WORKING TIME ##
datetime.datetime.now()-time

######### T O U L O U S E #########


time=datetime.datetime.now()
## DATA ##
data = pd.read_csv(PATH +"Toulouse.CSV", sep=";")
df=IRIS_B.ix[:,('x','y','CODE_IRIS','NOM_IRIS','geometry')]
df['CODE_IRIS']=df['CODE_IRIS'].astype(str)
data['CODE_IRIS']=data['CODE_IRIS'].astype(str)
data2= pd.merge(df,data,on="CODE_IRIS",how="right")
data2=data2.fillna(value=0)
data2=data2[data2["logt"]!=0]
df=data2
df['taux_base']=df["logs"]/df["logt"]
df['sorted_index']= None
df['state_logt']= None
df['state_logs']= None
df['taux']= None
df['check']=None
## INDEX RANDOMIZATION ##
df=shuffle(df)
df=df.reset_index(drop=True)
## TRESHOLD COMPUTATION ##
taux_global=df.logs.sum()/df.logt.sum()
seuil=0.05
s= [taux_global*(1-seuil), taux_global*(1+seuil)]
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
    df.taux[x]= np.ones((1,len(df)))
## ALL AGREGATION LEVELS COMPUTATION ##
for i in range(len(df)) :
    for j in range(len(df)) :
        if j == 0 :
            df.state_logt[i][0,j]=df.logt[i]
            df.state_logs[i][0,j]=df.logs[i]
            df.taux[i][0,j]=df.state_logs[i][0,j]/df.state_logt[i][0,j]
            if s[0] <df.taux[i][0,j]<s[1] :
                df.check[i]= 0
        else :
            df.state_logt[i][0,j]= df.state_logt[i][0,(j-1)] + df.logt[df.sorted_index[i][0,j]]
            df.state_logs[i][0,j]= df.state_logs[i][0,(j-1)] + df.logs[df.sorted_index[i][0,j]]
            df.taux[i][0,j]= df.state_logs[i][0,j]/df.state_logt[i][0,j]
            if (s[0] <df.taux[i][0,j]<s[1]) and (df.check[i] is None) :
                df.check[i]=j
## DISPLAY ##
pd.set_option("display.max_columns", df.shape[1])
pd.set_option("display.max_rows", 10)
df
## DATA VISUALZATION ##
plt.figure()
plt.title("Trajectoires")
plt.axhline(y=s[0],color="black")
plt.axhline(y=s[1],color="black")
for i in range(len(df)) :
    plt.plot(pd.Series(df.taux[i].ravel()))
    plt.axvline(x=df.check[i],lw=0.2)
plt.show()
df.plot(column='check',cmap='plasma')
df.plot(column='taux_base',cmap='viridis_r')
## WORKING TIME ##
datetime.datetime.now()-time
