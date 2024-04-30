#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import numpy as np
import pandas as pd
import pyodbc
import json
import requests
import pickle

conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0}; SERVER=140.136.150.82\SQLEXPRESS; DATABASE=lol; UID=sa; PWD=a27336622')

query = "select fight.gameid ,fight.champion as champ_name ,  win  , teamid from fight join game on game.gameid = fight.gameid join player on player.accountid = fight.accountid"
data = pd.read_sql(query, conn)
#i = data["gameid"].unique().tolist() 
#data["gameid"] = data["gameid"].apply(lambda x: i.index(x)) #將gameid 轉為從0開始
data.iloc[: , 2 ] = (data['win'] =='100').astype('int') #100 = 藍方(1) 200 = 紅方(0)
data.iloc[: , 3 ] = (data['teamid'] =='100').astype('int') #100 = 藍方(1) 200 = 紅方(0)


x = pd.get_dummies(data.champ_name) 
x2 = data.loc[: , data.columns != 'champ_name']
x = pd.concat([x , x2] , axis = 1)
a = pd.DataFrame()
f = lambda x , y:1 in y.iloc[: , x].values
f2 = lambda x , y : (y.iloc[: , x] == 1).tolist().index(True)

for i in range(2002300 , len(x["gameid"]) , 10):
    y = x.iloc[i:i+10, :]
    for j in range(0 , len(y.columns)-3):
        if f(j , y):
            if y['teamid'].iloc[f2(j , y)] == 1:
                y.iloc[: , j] = 1
            else:
                y.iloc[: , j] = 2
        else:
            continue
    y = y.iloc[: , y.columns != 'teamid']
    b = y.drop_duplicates(subset=None, keep='first', inplace=False)
    a = pd.concat([a , b])
    
a_red = a
a_blue = a
    
for i in range(len(a_red)):
    for j in range(len(a_red.columns)):
        if a_red.iloc[i , j] == 1:
            a_red.iloc[i , j] = 0      
        elif a_red.iloc[i , j] == 2:
            a_red.iloc[i , j] = 1
            
for i in range(len(a_blue)):
    for j in range(len(a_blue.columns)):
        if a_blue.iloc[i , j] == 2:
            a_blue.iloc[i , j] = 0
            
conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0}; SERVER=140.136.150.82\SQLEXPRESS; DATABASE=lol; UID=sa; PWD=a27336622')
query = "select win , fight.gameid , teamid , lane , fight.champion , player.summonerid from fight join game on game.gameid = fight.gameid join player on player.accountid = fight.accountid"
data_w = pd.read_sql(query, conn)
data_w.iloc[: , 0 ] = (data_w['win'] =='100').astype('int') #100 = 藍方(1) 200 = 紅方(0)
data_w.iloc[: , 2 ] = (data_w['teamid'] =='100').astype('int')
data_w['winrate'] = 0
data_w['number'] = 0

dic = {"gameid":[] , "WIN":[] , "TOP":[] , "MIDDLE":[], "ADC":[] , "SUPPORT":[] , "JUNGLE":[] , "TEAM":[] }
data2 = pd.DataFrame(dic)
lane = ["TOP" , "MIDDLE" , "ADC" , "SUPPORT" , "JUNGLE"]
for i in lane:
    winrate = data_w.query("lane == @i & teamid == 0")
    data2[i] = winrate.reset_index(drop = True)["winrate"]
win = data_w.query("lane == 'MIDDLE' & teamid ==0")
data2["WIN"] = win.reset_index(drop = True)["win"]
data2["TEAM"] = win.reset_index(drop = True)["teamid"]
data2["gameid"] = win.reset_index(drop = True)["gameid"]
data2["TOTAL_WINRATE"] = data2["TOP"]+data2["MIDDLE"]+data2["ADC"]+data2["SUPPORT"]+data2["JUNGLE"]


data1 = pd.DataFrame(dic)
lane = ["TOP" , "MIDDLE" , "ADC" , "SUPPORT" , "JUNGLE"]
for i in lane:
    winrate = data_w.query("lane == @i & teamid == 1")
    data1[i] = winrate.reset_index(drop = True)["winrate"]
win = data_w.query("lane == 'MIDDLE' & teamid ==1")
data1["WIN"] = win.reset_index(drop = True)["win"]
data1["TEAM"] = win.reset_index(drop = True)["teamid"]
data1["gameid"] = win.reset_index(drop = True)["gameid"]
data1["TOTAL_WINRATE"] = data1["TOP"]+data1["MIDDLE"]+data1["ADC"]+data1["SUPPORT"]+data1["JUNGLE"]


sum_blue = pd.merge(data1 , a_blue , on='gameid')
sum_red = pd.merge(data2 , a_red , on='gameid')
summ = sum_red.append(sum_blue).reset_index(drop = True)
summ2 = summ.drop(columns = ["win" , "gameid","TOP" , "MIDDLE" , "ADC" , "SUPPORT" , "JUNGLE"])
summ2 = summ2.dropna()

att = summ2.iloc[: , summ2.columns != 'WIN']
lab = summ2.iloc[: , summ2.columns == 'WIN']
xtrain , xtest ,ytrain , ytest = train_test_split(att , lab , test_size = 0.3)
#index重新排序
for i in (xtrain , xtest ,ytrain , ytest):
    i.index = range(i.shape[0])
rfc = RandomForestClassifier( n_estimators= 70 , random_state=30)
rfc = rfc.fit(xtrain , ytrain.values.ravel())
score  = rfc.score(xtest , ytest)
print(score)

ypred = rfc.predict(xtest)
print("confusion matrix:\n" , confusion_matrix(ytest , ypred))
print(classification_report(ytest, ypred , target_names=['red' , 'blue']))

with open('lol_single.pickle','wb') as f:
     pickle.dump(rfc, f)

