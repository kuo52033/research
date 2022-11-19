# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 16:56:47 2019

@author: 8877k
"""

#此程式用來爬蟲範例 以OPGG上路排行為例
#先呼叫該有的函示庫 mysql.connector我是另外下載

import requests
from bs4 import BeautifulSoup






def main():
    id1 = 0
    com = 1
    # while(com <= 1500):
    new_string = str(com)
    
    try:
        #下載此頁面內容
        resp = requests.get('https://tw.op.gg/champion/statistics')
    except: 
        k=0
        
    # 以BeautifulSoup解析 HTML 程式碼
    soup = BeautifulSoup(resp.text, 'html.parser')   
    
    # 在解析的程式碼中找到tbody下tabItem champion-trend-tier-TOP的tag
    main_titles = soup.find('tbody', 'tabItem champion-trend-tier-TOP')
    to_tr = main_titles.find_all('tr')
    
    # 根據圖片判斷rank 我暫時妹想到更好的方法
    rank_1 = '//opgg-static.akamaized.net/images/site/champion/icon-champtier-1.png'
    rank_2 = '//opgg-static.akamaized.net/images/site/champion/icon-champtier-2.png'
    rank_3 = '//opgg-static.akamaized.net/images/site/champion/icon-champtier-3.png'
    rank_4 = '//opgg-static.akamaized.net/images/site/champion/icon-champtier-4.png'
    rank_5 = '//opgg-static.akamaized.net/images/site/champion/icon-champtier-5.png'
    arr_rank = [rank_1, rank_2, rank_3, rank_4, rank_5]
    
    
    
    for title in to_tr:
        #find只會找一個tag 而find_all會找你目前資料的所有tag
        hero = title.find('div', 'champion-index-table__name')
        lane = title.find('div', 'champion-index-table__position')
        win_and_pick_rate = title.find_all('td', 'champion-index-table__cell champion-index-table__cell--value')  
        hero_rank = title.find_all('img')
        t3 = 0
        for i in hero_rank:
            if i.get('src') and ((i.get('src') == rank_1) or (i.get('src') == rank_2) or (i.get('src') == rank_3) or (i.get('src') == rank_4) or (i.get('src') == rank_5)):
                t3 = i.get('src')
                break
        
        # .text就是裡面的文字
        print(hero.text.strip(), end = ' ')
        print(lane.text.strip(), end = ' ')
        for win_pick in win_and_pick_rate:
            print(win_pick.text.strip(), end = " ")
        for i in range(len(arr_rank)):
            if(arr_rank[i] == t3):
                print(i+1, '\n')
                break
           
     
            
        
        com+=1
        
        
                

        id1 += 1
        

  

if __name__ == '__main__':
    main()