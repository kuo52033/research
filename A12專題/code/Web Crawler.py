#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import json
import pyodbc
from bs4 import BeautifulSoup
import pandas as pd
import re

def main():
    conn = pyodbc.connect(
        'DRIVER={SQL Server Native Client 11.0};SERVER=140.136.150.82\SQLEXPRESS; DATABASE=lol; UID=sa; PWD=a27336622')
    cursor = conn.cursor()
    playerid = '133414312'
    count = 0
    gameid_ = []
    while 1:
        break_ = False
        if count != 0:
            cursor.execute("select top 1 accountid from player where crawl = '' ")
            rows = cursor.fetchall()
            for row in rows:
                playerid = row.accountid
        for i in range(0, 250, 20):
            gameid_.clear()
            count = 1
            try:
                resp = requests.get(
                    'https://acs-garena.leagueoflegends.com/v1/stats/player_history/TW/' + str(
                        playerid) + '?begIndex=' + str(i) + '&endIndex=' + str(i + 20) + '&')

                data = json.loads(resp.text)
                game = data['games']['games']

                for recentgame in game:
                    gameid_.clear()
                    gameid = recentgame['gameId']

                    if str(recentgame['queueId']) != '420':
                        continue

                    cursor.execute("select gameid from game where gameid = ? ", gameid)
                    rows = cursor.fetchall()
                    for row in rows:
                        gameid_.append(row.gameid)
                    if len(gameid_) != 0:
                        continue
                    gameversion = recentgame["gameVersion"].split(".")[0]
                    if gameversion != '10':
                        break_ = True
                        break
                    if int(recentgame['gameDuration']) < 300:
                        continue
                    eachgame = requests.get("https://acs-garena.leagueoflegends.com/v1/stats/game/TW/" + str(gameid))
                    #time = requests.get(
                        #"https://acs-garena.leagueoflegends.com/v1/stats/game/TW/" + str(gameid) + "/timeline")
                    doc = json.loads(eachgame.text)
                    #doc2 = json.loads(time.text)
                    #timeline(doc2, doc, gameid)
                    record(doc)
                if break_ ==True:
                    break
            except:
                continue
        conn.execute("update player set crawl = 'yes' where accountid = ? " , playerid)
        conn.commit()


def record(doc):
    conn = pyodbc.connect(
        'DRIVER={SQL Server Native Client 11.0};SERVER=140.136.150.82\SQLEXPRESS; DATABASE=lol; UID=sa; PWD=a27336622')
    cursor = conn.cursor()

    player = []
    lane_ = []
    try:
        for i in range(10):
            if doc['participants'][i]['timeline']['role'] == 'DUO_SUPPORT':
                lane_.append('SUPPORT')
            elif doc['participants'][i]['timeline']['role'] == 'DUO_CARRY':
                lane_.append('ADC')
            else:
                lane_.append(doc['participants'][i]['timeline']['lane'])
    except:
        return

    for k in ('TOP' , 'MIDDLE' , 'ADC' , 'SUPPORT' , 'JUNGLE'):
        if lane_[:5].count(k) != 1:
            return
    for k in ('TOP' , 'MIDDLE' , 'ADC' , 'SUPPORT' , 'JUNGLE'):
        if lane_[5:10].count(k) != 1:
            return

    try:
        if doc['teams'][0]['win'] == 'Win':
            win = '100'
        else:
            win = '200'
    except:
        return

    '''insert game'''
    cursor.execute("insert into game values(?,?,?)", doc['gameId'], doc['gameDuration'], win)
    cursor.commit()
    try:
        for i in range(10):
            '''insert fight'''
            cursor.execute("insert into fight values(?,?,?,?,?)", doc['gameId'],
                           doc['participantIdentities'][i]['player']['accountId'], doc['participants'][i]['teamId'],
                           doc['participants'][i]['championId'] ,lane_[i] )

            cursor.commit()

            #insert player
            player.clear()
            cursor.execute("select accountid from player where accountid = ? ",
                           str(doc['participantIdentities'][i]['player']['accountId']))
            rows = cursor.fetchall()
            for row in rows:
                player.append(row.accountid)

            if len(player) == 0:
                cursor.execute("insert into player values(?,?,?,?)", str(doc['participantIdentities'][i]['player']['accountId']),
                               doc['participantIdentities'][i]['player']['summonerId'],
                               doc['participantIdentities'][i]['player']['summonerName'] , '')
                cursor.commit()
    except:
        return

resp = requests.get('https://www.op.gg/champion/statistics')
soup = BeautifulSoup(resp.text, 'html.parser')
soup = soup.find('div' , 'champion-index__champion-list')
road  = soup.find_all('div' , 'champion-index__champion-item__positions')
road_ = []
dic = {'champion':[] , 'road':[]}
champ_road = pd.DataFrame(dic)

for i in road:
    road_.append(i.text)

champ_ = []
for i in soup:
    if i.get('data-champion-key') == 'monkeyking':
        champ_.append('MonkeyKing')
    elif i.get('data-champion-key') == 'drmundo':
        champ_.append('DrMundo')
    elif i.get('data-champion-key') == 'jarvaniv':
        champ_.append('JarvanIV')
    elif i.get('data-champion-key') == 'kogmaw':
        champ_.append('KogMaw')
    elif i.get('data-champion-key') == 'masteryi':
        champ_.append('MasterYi')
    elif i.get('data-champion-key') == 'missfortune':
        champ_.append('MissFortune')
    elif i.get('data-champion-key') == 'reksai':
        champ_.append('RekSai')
    elif i.get('data-champion-key') == 'tahmkench':
        champ_.append('TahmKench')
    elif i.get('data-champion-key') == 'twistedfate':
        champ_.append('TwistedFate')
    elif i.get('data-champion-key') == 'xinzhao':
        champ_.append('XinZhao')
    elif i.get('data-champion-key') == 'aurelionsol':
        champ_.append('AurelionSol')
    elif i.get('data-champion-key') == 'leesin':
        champ_.append('LeeSin')
    else:
        champ_.append(i.get('data-champion-key').capitalize())
        
k = 0
for i in road_:
    r = re.findall('.{2}',i)
    for j in r:
        if j == "下路":
            w = {'champion':champ_[k] , 'road': 'BOTTOM'}
            champ_road = champ_road.append(w , ignore_index= True)
        elif j =='輔助':
            w = {'champion':champ_[k] , 'road': 'SUPPORT'}
            champ_road = champ_road.append(w , ignore_index= True)
        elif j =='中路':
            w = {'champion':champ_[k] , 'road': 'MID'}
            champ_road = champ_road.append(w , ignore_index= True)
        elif j =='上路':
            w = {'champion':champ_[k] , 'road': 'TOP'}
            champ_road = champ_road.append(w , ignore_index= True)
        elif j =='打野':
            w = {'champion':champ_[k] , 'road': 'JUNGLE'}
            champ_road = champ_road.append(w , ignore_index= True)
    k = k+1

    
    

