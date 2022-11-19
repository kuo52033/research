# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 21:52:45 2020

@author: tim
"""

import requests
from bs4 import BeautifulSoup
import json
import pyodbc
 
def main():
    for i in range(0 , 1020 , 20):
        resp = requests.get('https://acs-garena.leagueoflegends.com/v1/stats/player_history/TW/104398370?begIndex='+str(i)+'&endIndex='+str(i+20)+'&')
        data = json.loads(resp.text)
        game = data['games']['games']

        for recentgame in game:
            game = requests.get("https://acs-garena.leagueoflegends.com/v1/stats/game/TW/"+str(recentgame['gameId']))
            doc = json.loads(game.text)
            record(doc)
        
    

def record(doc):
    conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0}; SERVER=192.168.0.15\SQLEXPRESS; DATABASE=lol; UID=sa; PWD=a27336622')
    cursor = conn.cursor()
    
    player = []
    '''420 = 一般積分 440 = 彈性積分'''
    
    if int(doc['gameDuration'])<300 :
        return
    
    if str(doc['queueId'])!='420' and str(doc['queueId'])!='440':
        return
    
    
    if doc['teams'][0]['win'] =='Win':
        win = '100'
    else:
        win = '200'
        
    '''insert game'''
    cursor.execute("insert into game values(?,?,?)",doc['gameId'],doc['gameDuration'],win)
    cursor.commit()
    
    for i in range(2):
        '''insert team'''
        cursor.execute("insert into team values(?,?,?,?,?,?,?,?,?,?,?,?)",doc['gameId'],doc['teams'][i]['teamId'],doc['teams'][i]['towerKills'],doc['teams'][i]['inhibitorKills'], \
        doc['teams'][i]['baronKills'],doc['teams'][i]['dragonKills'],doc['teams'][i]['riftHeraldKills'],doc['teams'][i]['bans'][0]['championId'],doc['teams'][i]['bans'][1]['championId'], \
        doc['teams'][i]['bans'][2]['championId'],doc['teams'][i]['bans'][3]['championId'],doc['teams'][i]['bans'][4]['championId'])
        
        cursor.commit()

       
    for i in range(10):
        
        '''insert fight'''
        cursor.execute("insert into fight values(?,?,?,?,?,?,?,?,?,?)",doc['gameId'],doc['participantIdentities'][i]['player']['accountId'],doc['participants'][i]['teamId'],doc['participants'][i]['championId'],doc['participants'][i]['stats']['kills'], \
        doc['participants'][i]['stats']['deaths'],doc['participants'][i]['stats']['assists'],doc['participants'][i]['stats']['champLevel'],doc['participants'][i]['stats']['largestKillingSpree'], \
        doc['participants'][i]['stats']['largestMultiKill'] )

        '''insert damage'''
        cursor.execute("insert into damage values(?,?,?,?,?,?,?,?,?,?,?,?,?)",doc['gameId'],doc['participantIdentities'][i]['player']['accountId'],doc['participants'][i]['stats']['totalDamageDealtToChampions'],doc['participants'][i]['stats']['physicalDamageDealtToChampions'],doc['participants'][i]['stats']['magicDamageDealtToChampions'], \
        doc['participants'][i]['stats']['trueDamageDealtToChampions'],doc['participants'][i]['stats']['totalDamageDealt'],doc['participants'][i]['stats']['physicalDamageDealt'],doc['participants'][i]['stats']['magicDamageDealt'], \
        doc['participants'][i]['stats']['trueDamageDealt'] , doc['participants'][i]['stats']['largestCriticalStrike'],doc['participants'][i]['stats']['damageDealtToObjectives'],doc['participants'][i]['stats']['damageDealtToTurrets'])
        
        '''insert heal''' 
        cursor.execute("insert into heal values(?,?,?,?,?,?,?)",doc['gameId'],doc['participantIdentities'][i]['player']['accountId'],doc['participants'][i]['stats']['totalHeal'],doc['participants'][i]['stats']['totalDamageTaken'],doc['participants'][i]['stats']['physicalDamageTaken'], \
        doc['participants'][i]['stats']['magicalDamageTaken'],doc['participants'][i]['stats']['trueDamageTaken'])
       
        '''insert ward'''
        cursor.execute("insert into ward values(?,?,?,?,?)",doc['gameId'],doc['participantIdentities'][i]['player']['accountId'],doc['participants'][i]['stats']['wardsPlaced'],doc['participants'][i]['stats']['wardsKilled'],doc['participants'][i]['stats']['visionWardsBoughtInGame'])
        
        '''insert gold'''
        cursor.execute("insert into gold values(?,?,?,?,?,?,?,?)",doc['gameId'],doc['participantIdentities'][i]['player']['accountId'],doc['participants'][i]['stats']['goldEarned'],doc['participants'][i]['stats']['goldSpent'],doc['participants'][i]['stats']['totalMinionsKilled'], \
        doc['participants'][i]['stats']['neutralMinionsKilled'],doc['participants'][i]['stats']['neutralMinionsKilledTeamJungle'],doc['participants'][i]['stats']['neutralMinionsKilledEnemyJungle'])
        
        '''insert item'''
        cursor.execute("insert into item values(?,?,?,?,?,?,?,?,?)",doc['gameId'],doc['participantIdentities'][i]['player']['accountId'],doc['participants'][i]['stats']['item0'],doc['participants'][i]['stats']['item1'],doc['participants'][i]['stats']['item2'], \
        doc['participants'][i]['stats']['item3'],doc['participants'][i]['stats']['item4'],doc['participants'][i]['stats']['item5'], doc['participants'][i]['stats']['item6'])
        
        cursor.commit()
        
        '''insert player'''
        player.clear()
        cursor.execute("select accountid from player where accountid = ? " , doc['participantIdentities'][i]['player']['accountId'])
        rows = cursor.fetchall()
        for row in rows:
            player.append(row.accountid)
        if not player:
            cursor.execute("insert into player values(?,?,?,?)",doc['participantIdentities'][i]['player']['accountId'], doc['participantIdentities'][i]['player']['summonerId'] , doc['participantIdentities'][i]['player']['summonerName'] , doc['participantIdentities'][i]['player']['platformId'])
            cursor.commit()

if __name__ == '__main__':
    main()
