# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 00:00:32 2015

@author: zhengzhang
"""
from chat_utils import *
import chat_group
from plot import *
import matplotlib.pyplot as plt

class ClientSM:
    def __init__(self, s):
        self.state = S_OFFLINE
        self.peer = ''
        self.me = ''
        self.out_msg = ''
        self.s = s
        self.color = ''
        self.pcolor = ''
        self.chess = Chess(self.color)

    def set_state(self, state):
        self.state = state
        
    def get_state(self):
        return self.state
    
    def set_myname(self, name):
        self.me = name

    def get_myname(self):
        return self.me
      
    def peercolor(self):
        if self.color == 'black':
            self.pcolor = 'white'
        elif self.color == 'white':
            self.pcolor = 'black'
        return self.pcolor
    
    def winner(self):
        points = {self.color:0, self.pcolor:0}
        for c in self.chess.field_dic.values():             
            if c == self.color:  
                points[self.color] += 1  
            else:
                points[self.pcolor] += 1
        if points[self.color] > points[self.pcolor]:
            return '{} WINS WITH {}:{}'.format(self.color.upper(), points[self.color], points[self.pcolor])
        elif points[self.color] < points[self.pcolor]:
            return '{} LOSES WITH {}:{}'.format(self.color.upper(), points[self.color], points[self.pcolor])
        else:
            return 'DRAW WITH 18:18'
        
        
    def connect_to(self, peer):
        msg = M_CONNECT + peer
        mysend(self.s, msg)
        response = myrecv(self.s)
        if response == (M_CONNECT+'ok'):
            self.peer = peer
            self.out_msg += 'You are connected with '+ self.peer + '\n'
            return (True)
        elif response == (M_CONNECT + 'busy'):
            self.out_msg += 'User is busy. Please try again later\n'
        elif response == (M_CONNECT + 'hey you'):
            self.out_msg += 'Cannot talk to yourself (sick)\n'
        else:
            self.out_msg += 'User is not online, try again later\n'
        return (False)

    def disconnect(self):
        msg = M_DISCONNECT
        mysend(self.s, msg)
        self.out_msg += 'You are disconnected from ' + self.peer + '\n'
        self.peer = ''



    def proc(self, my_msg, peer_code, peer_msg):
        # message from user is in my_msg, if it has an argument (e.g. "p 3")
        # the the argument is in my_msg[1:]
        self.out_msg = ''
#==============================================================================
# Once logged in, do a few things: get peer listing, connect, search
# And, of course, if you are so bored, just go
# This is event handling instate "S_LOGGEDIN"
#==============================================================================
        if self.state == S_LOGGEDIN:
            # todo: can't deal with multiple lines yet
            if len(my_msg) > 0:
                
                if my_msg == 'q':
                    self.out_msg += 'See you next time!\n'
                    self.state = S_OFFLINE
                    
                elif my_msg == 'time':
                    mysend(self.s, M_TIME)
                    time_in = myrecv(self.s)
                    self.out_msg += "Time is: " + time_in
                            
                elif my_msg == 'who':
                    mysend(self.s, M_LIST)
                    who = myrecv(self.s)
                    self.out_msg += 'Here are all the users in the system:\n'
                    self.out_msg += who
                            
                elif my_msg[0] == 'c':
                    peer = my_msg[1:]
                    peer = peer.strip()
                    if self.connect_to(peer):
                        self.state = S_START
                        self.out_msg += 'Connect to {}. Chat away!\n'.format(peer)
                        self.out_msg += '-------------------------\n'
                        self.color = 'black'
                        self.turn = 1
                    else:
                        self.out_msg += 'Unsuccessful connection!\n'

                else:
                    self.out_msg += menu
                    
            if len(peer_msg) > 0:
                if peer_code == M_CONNECT:
                    self.peer = peer_msg
                    self.out_msg += 'Request from {} \n'.format(self.peer)
                    self.out_msg += 'You are connected with {}\n'.format(self.peer)
                    self.out_msg += 'Play away!\n'                 
                    self.out_msg += '-------------------------\n'
                    self.state = S_START
                    self.color = 'white'
                    self.turn = 2
                    
#==============================================================================
# Start chatting, 'bye' for quit
# This is event handling instate "S_CHATTING"
#==============================================================================
        elif self.state == S_START:
            print('chess')
            fig = plt.figure(figsize=(6,6), num=self.me + ' ' + self.color)
            ax = plt.gca()
            ax.set_axis_bgcolor('orange')
            plt.xlim(0,6)
            plt.ylim(0,6)
            plt.xticks([0, 1, 2, 3, 4, 5, 6], [r'', r'', r'', r'', r'', r''])
            plt.yticks([0, 1, 2, 3, 4, 5, 6], [r'', r'', r'', r'', r'', r''])
            plt.grid(color='black', linewidth=2.5)
            plt.draw()
            if self.turn == 1:
                self.state = S_MYTURN
            elif self.turn == 2:
                self.state = S_PTURN
        
        elif self.state == S_MYTURN:
            point = plt.ginput(1)
            intx, inty = self.chess.int_point(point)[0], self.chess.int_point(point)[1]
            final_color = self.chess.make_color(intx, inty, self.chess.field_dic, self.color, self.peercolor())
            if self.chess.field_dic[(intx, inty)] == 0 and final_color == self.color:
                plt.scatter([intx], [inty], s=350, color = final_color, marker='o')
                plt.draw()
                self.chess.field_dic[(intx, inty)] = final_color
                self.chess.step.append([intx, inty])
                print(intx, inty)
                if not self.chess.game_over(self.color, self.pcolor):
                    mysend(self.s, M_EXCHANGE + str(intx) + ',' + str(inty) + ',' + final_color) 
                    self.state = S_PTURN

                else:
                    print()
                    print('GAME OVER')
                    print(self.winner())
                    print(self.chess.field_dic)
                    mysend(self.s, M_EXCHANGE + self.winner() + "@" + str(self.chess.field_dic) + '@' + 'bye')
                    self.disconnect()
                    self.state = S_LOGGEDIN
                    self.peer = ''
                
        elif self.state == S_PTURN:
            print('waiting for response......')
            self.myc = myrecv(self.s)
            if len(self.myc) > 0 and self.myc[-3:] != 'bye':
                pclick0 = self.myc.split(',')
                px, py, p_color = float(pclick0[0]), float(pclick0[1]), pclick0[2]
                plt.scatter([px], [py], s=350, color=p_color, marker='o')
                self.chess.field_dic[(px, py)] = p_color 
                plt.draw()
                self.state = S_MYTURN
                
            else:
                pclick = self.myc.split('@')
                winner, str_dic = pclick[0], pclick[1]
                print()
                print('GAME OVER')
                print(winner)
                print(str_dic)
                self.state = S_LOGGEDIN

            # I got bumped out
            if peer_code == M_DISCONNECT:
                print('GAME OVER')
                self.state = S_LOGGEDIN

            # Display the menu again
            if self.state == S_LOGGEDIN:
                self.out_msg += menu
#==============================================================================
# invalid state                       
#==============================================================================
        else:
            self.out_msg += 'How did you wind up here??\n'
            print_state(self.state)
            
        return self.out_msg


