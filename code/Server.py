#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import socket 


import threading

ip = socket.gethostbyname(socket.gethostname()) 
port = 45535

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
server.bind((ip , port))

Format = "utf-8"
Header = 64 
global client_list 
client_list = []

class client: 
    
    def __init__(self, conn, addr):
        self.conn = conn 
        self.addr = addr 
        self.winrate_msg = [] 
        self.player_road = [] 
        self.summonerid = ['0', '1', '2', '3', '4'] 
        self.banchamp = [] 
        self.ourteam = [] 
        self.theirteam = [] 
        self.all_champ = copy.deepcopy(all_champ) 
        self.imformation = True 
        self.client_index = None 
        self.mcts_action = False

    def run(self):
        try:
            while True:
                msg = str(self.conn.recv(Header), encoding=Format).replace("\r\n", '')
                if msg == 'End':
                    break
                else:
                    self.winrate_msg.append(msg)

            msg = str(self.conn.recv(Header), encoding=Format).replace("\r\n", '')
            for i in range(5):
                self.player_road.append(position[int(msg.split(' ')[i])])
            self.team = msg.split(' ')[5]
            self.pick_order = msg.split(' ')[6]
            print(self.player_road)
            print("team: ", self.team)         
            print("pick_order", self.pick_order)

            self.handle_winrate()

            if self.pick_order in ('0', '5', '6'):
                self.start_mcts()
                self.mcts_action = True

            msg = str(self.conn.recv(Header), encoding=Format).replace("\r\n", '')
            for i in msg.split(' '):
                if i:
                    self.banchamp.append(i)
            print("ban: ", self.banchamp)

            if self.pick_order not in ('0', '5', '6'):
                msg = str(self.conn.recv(Header), encoding=Format).replace("\r\n", '')
                for i in msg.split(' '):
                    if i:
                        self.ourteam.append(i)
                print('our_team:', self.ourteam)

                if self.pick_order != '1' and self.pick_order != '2':
                    msg = str(self.conn.recv(Header), encoding=Format).replace("\r\n", '')
                    for i in msg.split(' '):
                        if i:
                            self.theirteam.append(i)
                    print('their_team:', self.theirteam)

                if self.pick_order != '9':
                    self.start_mcts()
                    self.mcts_action = True
                else:
                    action_msg = ''
                    print('final_pick')
                    for action in self.red_final():
                        action_msg = action_msg + action +' '
                    self.conn.send(action_msg.encode(Format))
                    print('Recommend_End')

            if self.pick_order != '9':
                msg = str(self.conn.recv(Header), encoding=Format).replace("\r\n", '')
                if msg == 'Mcts_End':
                    action_msg = ''
                    print('mcts_end')
                    self.mcts1.terminate()
                    print(self.mcts1.current_node.visit)
                    for action in self.recommend():
                        action_msg = action_msg + action +' '
                    self.conn.send(action_msg.encode(Format))
                    print('Recommend_End')

            msg = str(self.conn.recv(Header), encoding=Format).replace("\r\n", '')
            if msg == 'Pick_End':
                print('pick_end')
                self.final_winrate()
            print('socket end')
            self.disconnect()
            print_tree(self.mcts1.current_node)
            
        except Exception as e:
            if self.mcts_action == True:
                self.mcts1.terminate()
            print(e)
            self.disconnect()

    def final_winrate(self):

        ourchamp = []

        msg = str(self.conn.recv(Header), encoding=Format).replace("\r\n", '')
        for i in msg.split(' '):
            if i:
                ourchamp.append(i)

        self.winrate_rfc = pd.DataFrame(columns=feature)
        self.winrate_rfc.loc[0] = 0

        if self.team == '2':
            self.winrate_rfc['TEAM'] = 0
        else:
            self.winrate_rfc['TEAM'] = 1
        i = 0
        total = 0

        for c in ourchamp:
            self.winrate_rfc[c] = 1
            w = self.player_winrate.loc[self.player_winrate['player'] == str(i), :]
            if c not in w['champion'].tolist():
                total += 0
            else:
                w = w.loc[w['champion'] == c, :]['winrate'].values[0]
                total += float(w)
            i += 1
        self.winrate_rfc['TOTAL_WINRATE'] = total
        probability = rfc.predict_proba(self.winrate_rfc)[0]

        if self.team == '2':
            pro = probability[0] * 100
            self.conn.send(str(pro).encode(Format))
            print("winrate:%f " %(pro))
        else:
            pro = probability[1] * 100
            self.conn.send(str(pro).encode(Format))
            print("winrate:%f " %(pro))

    def red_final(self):

        action = []
        tail = pd.DataFrame(columns=feature)
        tail.loc[0] = 0
        if self.team == '2':
            tail['TEAM'] = 0
        else:
            tail['TEAM'] = 1
        total_winrate = 0

        for i in range(4):
            a = self.player_winrate.loc[self.player_winrate['player'] == str(i), :]
            a = a.loc[a['champion'] == self.ourteam[i], :]
            if len(a) == 0:
                total_winrate += 0
            else:
                total_winrate += float(a['winrate'].values[0])
            tail[self.ourteam[i]] = 1

        tail['TOTAL_WINRATE'] = total_winrate

        n = self.player_winrate.loc[self.player_winrate['player'] == '4', :]
        c = n['champion'].tolist()
        w = n['winrate'].tolist()

        for i in range(4):
            rep = self.ourteam[i]
            if rep in c:
                w.remove(w[c.index(rep)])
                c.remove(rep)

        for i in range(5):
            rep = self.theirteam[i]
            if rep in c:
                w.remove(w[c.index(rep)])
                c.remove(rep)

        for i in self.banchamp:
            if i in c:
                w.remove(w[c.index(i)])
                c.remove(i)

        tail2 = pd.concat([tail] * len(c)).reset_index(drop=True)

        for i in range(len(tail2)):
            tail2.iloc[i, 1] += float(w[i])
            tail2.iloc[i, tail2.columns == c[i]] = 1

        pro = rfc.predict_proba(tail2)
        if self.team == '2':
            best = np.max(pro, axis=0)[0]
        else:
            best = np.max(pro, axis=0)[1]

        for i in range(len(pro)):
            if self.team == '2':
                if pro[i][0] == best:
                    action.append(c[i])
            else:
                if pro[i][1] == best:
                    action.append(c[i])
        '''
        count = 0
        while count <5:
            count +=1
            random_top = top_rank.loc[top_rank['road'] == self.player_road[4]  , :].sample(n = 1)
            d = random_top['champion'].values[0]
            if d in self.banchamp or d in action or d in self.ourteam or d in self.theirteam:
                continue
            else:
                break

        action.insert(0 , d)
        '''


        print('action: ' ,  action)
        print('winrate: ' , best)

        return action

    def recommend(self):

        if self.pick_order == '2':
            self.summonerid[1], self.summonerid[2] = self.summonerid[2], self.summonerid[1]
            self.player_road[1], self.player_road[2] = self.player_road[2], self.player_road[1]
        elif self.pick_order == '4':
            self.summonerid[3], self.summonerid[4] = self.summonerid[4], self.summonerid[3]
            self.player_road[3], self.player_road[4] = self.player_road[4], self.player_road[3]
        elif self.pick_order == '8':
            self.summonerid[2], self.summonerid[3] = self.summonerid[3], self.summonerid[2]
            self.player_road[2], self.player_road[3] = self.player_road[3], self.player_road[2]
        elif self.pick_order == '6':
            self.summonerid[0], self.summonerid[1] = self.summonerid[1], self.summonerid[0]
            self.player_road[0], self.player_road[1] = self.player_road[1], self.player_road[0]

        weight = []
        action = []        
        their = []
        
        if self.pick_order != '0':
            msg = str(self.conn.recv(Header), encoding=Format).replace("\r\n", '')
            for i in msg.split(' '):
                if i:
                    their.append(i)
                
        for child in self.mcts1.current_node.children:
            if child.champion in self.banchamp or child.champion in self.ourteam or child.champion in their :
                if self.team == '1':
                    weight.append(0)
                else:
                    weight.append(100)
            else:
                weight.append(child.win / child.visit)
                    
        if self.team == '1':
            max_n = max(weight)
        else:
            max_n = min(weight)

        for i in range(len(weight)):
            if weight[i] == max_n:
                action.append(self.mcts1.current_node.children[i].champion)


        '''  
        if self.team == '1':
            myroad = self.player_road[int(self.pick_order)]
        else:
            myroad = self.player_road[int(self.pick_order)-5]

        count = 0
        while count <5:
            count +=1
            random_top = top_rank.loc[top_rank['road'] == myroad  , :].sample(n = 1)
            d = random_top['champion'].values[0]
            if d in self.banchamp or d in action or d in self.ourteam or d in self.theirteam:
                continue
            else:
                break

        action.insert(0 , d)
        '''
        print('their: ' , their)
        print('action: ' ,  action)
        print('winrate: ' , max_n)

        return action

    def start_mcts(self):

        for i in self.theirteam:
            self.all_champ.remove(i)

        if self.pick_order not in ('0' , '5' , '6'):
            for i in self.banchamp:
                self.all_champ.remove(i)

        self.start_node = node('Start', '', self.client_index)
        self.mcts1 = mcts()
        self.mcts1.root = self.start_node
        if self.pick_order not in ('0', '5', '6'):
            node1 = node(self.ourteam[0], '0', self.client_index)
            self.start_node.children.append(node1)
            node1.parent = self.start_node
            self.mcts1.current_node = node1
            if self.pick_order in ('3', '4', '7', '8', '9'):
                node2 = node(self.ourteam[1], '1', self.client_index)
                node1.children.append(node2)
                node2.parent = node1
                self.mcts1.current_node = node2
                if self.pick_order in ('3', '4', '9'):
                    node3 = node(self.ourteam[2], '2', self.client_index)
                    node2.children.append(node3)
                    node3.parent = node2
                    self.mcts1.current_node = node3
                    if self.pick_order == '9':
                        node4 = node(self.ourteam[3], '3', self.client_index)
                        node3.children.append(node4)
                        node4.parent = node3
                        self.mcts1.current_node = node4
        else:
            self.mcts1.current_node = self.start_node

        if self.pick_order == '2':
            self.summonerid[1], self.summonerid[2] = self.summonerid[2], self.summonerid[1]
            self.player_road[1], self.player_road[2] = self.player_road[2], self.player_road[1]
        elif self.pick_order == '4':
            self.summonerid[3], self.summonerid[4] = self.summonerid[4], self.summonerid[3]
            self.player_road[3], self.player_road[4] = self.player_road[4], self.player_road[3]
        elif self.pick_order == '8':
            self.summonerid[2], self.summonerid[3] = self.summonerid[3], self.summonerid[2]
            self.player_road[2], self.player_road[3] = self.player_road[3], self.player_road[2]
        elif self.pick_order == '6':
            self.summonerid[0], self.summonerid[1] = self.summonerid[1], self.summonerid[0]
            self.player_road[0], self.player_road[1] = self.player_road[1], self.player_road[0]

        print('start mcts')
        thread = threading.Thread(target=self.mcts1.simulate)
        thread.start()


    def handle_winrate(self):
        dic = {'player': [], 'champion': [], 'winrate': []}
        self.player_winrate = pd.DataFrame(dic)
        for msg in self.winrate_msg:
            w = {'player': msg.split(' ')[0], 'champion': msg.split(' ')[1], 'winrate': msg.split(' ')[2]}
            self.player_winrate = self.player_winrate.append(w, ignore_index=True)
        for i in range(5):
            if len(self.player_winrate.loc[self.player_winrate['player'] == str(i), :]) == 0:
                r = champion_road.loc[champion_road['road'] == self.player_road[i], :].sample(n=10)
                ch = r['champion'].tolist()
                ch[:] = [str(x) for x in ch]
                ex = pd.DataFrame(dic)
                ex['champion'] = ch
                ex['player'] = str(i)
                ex['winrate'] = 40
                self.player_winrate = self.player_winrate.append(ex, ignore_index=True)

    def disconnect(self):
        client_list[self.client_index] = 0
        self.conn.close()
        print(f"{self.addr} disconnect")
        
def create_client(conn, addr): 
    print(f"[new connection] {addr} connected")
    client_ = client(conn , addr) 
    client_list.append(client_) 
    client_.client_index = client_list.index(client_) 
    client_.run()

def Start_Server(): 
    server.listen(5)   
    while True:
        conn, addr = server.accept()
        #print(f"[active connections] {threading.activeCount()-1}")
        thread = threading.Thread(target = create_client , args = (conn , addr))
        thread.start()
        
if __name__ == '__main__': 
    all_champ = ['266', '103', '84', '12', '32', '34', '1', '523', '22', '136', '268', '432', '53', '63', '201', '51', '164', '69', '31', '42', '122', '131', '36', '119', '245', '60', '28', '81', '9', '114', '105', '3', '41', '86', '150', '79', '104', '120', '74', '420', '39', '427', '40', '59', '24', '126', '202', '222', '145', '429', '43', '30', '38', '55', '10', '141', '85', '121', '203', '240', '96', '7', '64', '89', '127', '876', '236', '117', '99', '54', '90', '57', '11', '21', '62', '82', '25', '267', '75', '111', '518', '76', '56', '20', '2', '61', '516', '80', '78', '555', '246', '133', '497', '33', '421', '58', '107', '92', '68', '13', '360', '113', '235', '875', '35', '98', '102', '27', '14', '15', '72', '37', '16', '50', '517', '134', '223', '163', '91', '44', '17', '412', '18', '48', '23', '4', '29', '77', '6', '110', '67', '45', '161', '254', '112', '8', '106', '19', '498', '101', '5', '157', '83', '777', '350', '154', '238', '115', '26', '142', '143' , '147' , '526'] 
    feature = ['TEAM', 'TOTAL_WINRATE', '1', '10', '101', '102', '103', '104', '105', '106', '107', '11', '110', '111', '112', '113', '114', '115', '117', '119', '12', '120', '121', '122', '126', '127', '13', '131', '133', '134', '136', '14', '141', '142', '143', '145' ,'147', '15', '150', '154', '157', '16', '161', '163', '164', '17', '18', '19', '2', '20', '201', '202', '203', '21', '22', '222', '223', '23', '235', '236', '238', '24', '240', '245', '246', '25', '254', '26', '266', '267', '268', '27', '28', '29', '3', '30', '31', '32', '33', '34', '35', '350', '36','360', '37', '38', '39', '4', '40', '41', '412', '42', '420', '421', '427', '429', '43', '432', '44', '45', '48', '497', '498', '5', '50', '51', '516', '517', '518', '523', '53', '54', '55', '555', '56', '57', '58', '59', '6', '60', '61', '62', '63', '64', '67', '68', '69', '7', '72', '74', '75', '76', '77', '777', '78', '79', '8', '80', '81', '82', '83', '84', '85', '86', '875', '876', '89', '9', '90', '91', '92', '96', '98', '99' , '526']
    pickle_in = open('lol_single.pickle','rb') 
    rfc = pickle.load(pickle_in) 
    champion_road = pd.read_csv(r'champ_road.csv') 
    champion_road = champion_road.drop(columns = 'Unnamed: 0') 
    position = ["TOP", "JUNGLE", "MID", "BOTTOM", "SUPPORT"] 
    print("server is starting....")
    Start_Server()

