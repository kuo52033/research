#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import pickle
import requests
import time
import re
import os
import json
import base64
import threading
import sys
from os import system, name
from random import choice
import multiprocessing as mp
import copy

class node():
    def __init__(self ,champ, player , index):
        self.champion = champ
        self.player = player
        self.win = 0
        self.visit = 0
        self.parent = None
        self.children = []
        self.client_index = index
        
    
    #獲取可執行動作
    def get_available(self):
        if self.is_root():
            available = self.parent.get_available()
            available.remove(self.champion)
        else:
            available = client_list[self.client_index].all_champ[:]
            
        return available
    
    #select公式
    def ucb_fun(self , c_param = 2):
        if self.visit == 0:      
            w = 50
        else:
            if client_list[self.client_index].team =='1':
                w = self.win/self.visit + c_param * np.sqrt(np.log(self.parent.visit)/self.visit)
            else:
                w = (1-self.win/self.visit) + c_param * np.sqrt(np.log(self.parent.visit)/self.visit)
        
        return w
    
    #根據ucb公式選最大值
    def select(self):
        weight = [child.ucb_fun(2) for child in self.children]
        action = pd.Series(data = weight).idxmax()
        next_action = self.children[action]
        
        return next_action
    
    #擴充新動作
    def expand(self):
        level = self.level()
          
        if level == 1:
            expand =  client_list[self.client_index].player_winrate.loc[client_list[self.client_index].player_winrate['player'] == client_list[self.client_index].summonerid[0] , :]
            available = self.get_available()
            for c in expand['champion']:
                if c in available:
                    child = node(c , client_list[self.client_index].summonerid[0] , self.client_index)
                    child.parent = self
                    self.children.append(child)
            child = self.children[0]

            return child
        else:
            if len(self.children) == 0:
                player = client_list[self.client_index].summonerid[level-1]
                random_blue = client_list[self.client_index].player_winrate.loc[client_list[self.client_index].player_winrate['player'] == player , :]
                random_champ = random_blue.sample(n = 1)
                while random_champ['champion'].values[0] not in self.get_available():
                     random_champ = random_blue.sample(n = 1)
                child = node(random_champ['champion'].values[0], player , self.client_index)
                child.parent = self
                self.children.append(child)
            else:
                remain = self.remain_champ()
                expand_champ = np.random.choice(remain , size = 1)
                child = node(expand_champ[0]  , self.children[0].player , self.client_index)
                child.parent = self
                self.children.append(child) 
                
        return child
    
    #檢查是否擴充完
    def remain_champ(self):

        remain = client_list[self.client_index].player_winrate.loc[client_list[self.client_index].player_winrate['player'] == self.children[0].player , :]['champion'].values.tolist()
       
        for childs in self.children:
            remain.remove(childs.champion)
        available = self.get_available()
        remain2 = remain[:]
        for i in remain:
            if i not in available:
                remain2.remove(i)
                
        return remain2
                      
    #模擬對戰
    def rollout(self):     
             
        #s = time.time()
        play = pd.DataFrame(columns= feature)
        play.loc[0] = 0
        total_winrate = 0
        blue_action = 0     

        n = self
        while n.is_root():
            blue_action +=1
            play[n.champion] =1
            winrate = client_list[self.client_index].player_winrate.loc[client_list[self.client_index].player_winrate['player'] == n.player , :]
            if n.champion not in winrate['champion'].tolist():
                total_winrate += 0
            else:
                winrate = winrate.loc[winrate['champion'] == n.champion , : ]
                total_winrate += float(winrate['winrate'].values[0])
            n = n.parent
        
  
        for i in range(blue_action , 5):
            random = client_list[self.client_index].player_winrate.loc[client_list[self.client_index].player_winrate['player'] == client_list[self.client_index].summonerid[i] , :]           
            r = random.sample(n = 1)
            champ = r['champion'].values[0]
            total_winrate += float(r['winrate'].values[0])
            play[champ] =1

        if client_list[self.client_index].team == '2':
            play['TEAM'] = 0
        else:
            play['TEAM'] = 1
            
        play['TOTAL_WINRATE'] = total_winrate
        
        probability = rfc.predict_proba(play)[0]
           
        if probability[0]>probability[1]:
            winner = 0
        else:
            winner = 1
        
        return winner
    
    #根據rollout結果更新節點
    def update(self , win):
        self.visit +=1
        self.win += win    
        if self.is_root():
            self.parent.update(win)
            
        return 
           
    def level(self):
        count = 1
        n = self
        while n.is_root():
            n = n.parent
            count +=1
            
        return count
    
    def is_root(self):
        return self.parent
    
    
class mcts:
    def __init__(self):
        self.root  = None
        self.current_node = None
        self.running = True
    
    def simulate(self):
        while self.running == True:
            leaf = self.policy()
            winner = leaf.rollout()
            leaf.update(winner)
        return 
    
    def policy(self):
        current = self.current_node
        
        while True:
            if len(current.children) ==0:
                return current.expand()
            elif len(current.remain_champ()) == 0:
                current = current.select()
                if current.visit == 0:
                    return current
                if current.level() == 6:
                    return current
            else:
                return current.expand()
        return current
        
    def terminate(self):
        self.running = False
               
def print_tree(current):
    space = ' ' * current.level() *5
    prefix = space +"|__ " 
    print(prefix + current.champion+' '+str(current.win)+' / '+str(current.visit))
    if current.children:
        for child in current.children:
            print_tree(child)
        
       

