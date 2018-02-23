# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 21:24:13 2018

@author: strat
"""

import socket
import os, sys
import threading
from pynput.keyboard import Key, KeyCode, Listener
clear = lambda: os.system('cls')

with open("first_round.txt") as f:
    q_board = f.readlines()
    print(q_board)
q_board = [x.strip("\n") for x in q_board]

#build matrix for board
m_board=[[0 for x in range(6)] for y in range(5)]
for x in range(5):
    for y in range(6):
        m_board[x][y] = str(x*100 + 100)


num_players = int(input('Enter the number of players: '))
playernum = 0;
name = threading.local()
name = threading.local()
c_socket = []

def on_press(key):
    if key == Key.tab:
        clear()
  
def on_release(key):
      
    if key == KeyCode(char='q'):
        send_to_all('This is a question')
        clear()

    elif key == KeyCode(char='b'):
        clear()
        draw_board()



def draw_board():
    board = ""
    board = draw_horiz(board)
    board += "\n"
    #add in column titles
    for l in range(0,6):
        board = board + q_board[l * 11]

    for m in range(0,5):
        board = draw_square(board, m)
        board += "\n"
        board = draw_horiz(board)
 
        
    print(board)
    
def draw_square(s_board, x):
    s_board = s_board + "\n|   " + m_board[x][0] + "   |"
    for i in range(1,6):
        s_board = s_board + "   " + m_board[x][i] + "   |"
    return s_board

def draw_horiz(h_board):
    #draw horizantal line
    for l in range(0, 6):
        h_board = h_board + '----------'
    return h_board
    
def register_user(j, client_c):
    score = 0
    print('Registering player number: ', j)
    client_c.send(str.encode('Enter your name'))
    name = client_c.recv(1024).decode('utf-8')
    print('Player number ', j, ' name is', name)
    message = '\n Welcome ' + str(name) + ', you have been registered, good luck!!! \n Press Space to buzz in \n Press 1 For Your Score \n Press 2 For The Board'
    client_c.send(str.encode(message))
    while True:
        c_message = client_c.recv(1024).decode('utf-8')
        if c_message[0] == '1':
            client_c.send(str.encode('Your score is: ' + str(score)))
        elif c_message[0] == '0':
            print(name, ' Has buzzed in')
            client_c.send(str.encode('Press 1. For your score: \n Press enter to buzz in '))
            score += 10;

def send_to_all(blast_message):
    for k in range(0 , num_players):
        c_socket[k].send(str.encode(blast_message))

#def server_commands():
    

#this is the server so ask the OS what the computer name is
host = '192.168.0.169'
#specify a port
port = 12345;

#create the socket
s = socket.socket()

#bind the socket to the port
s.bind((host, port))
print('Listening for incoming connections ')
threads = []


for i in range(0, num_players):
    
    #specify that we will accept 5 connections
    s.listen(5)

    #accept the first connection
    c, addr = s.accept()
    c_socket.append(c)
    #Notify the user that a connection was made
    print('connected to: ', addr, 'player number: ', i)
    t = threading.Thread(target=register_user, args=(playernum, c, ))
    threads.append(t)
    t.start()
    playernum += 1                    

#ask for input
print('All players entered')
for i in range(0, num_players):
    namet = threads[i].name
    print(namet)

# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

