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
q_board = [x.strip("\n") for x in q_board]

#build matrix for board
m_board=[[0 for x in range(6)] for y in range(5)]
for x in range(5):
    for y in range(6):
        m_board[x][y] = str(x*100 + 100)


#num_players = int(input('Enter the number of players: '))

name = threading.local()
name = threading.local()
c_socket = []
global live
live = False
question = "  "

def on_press(key):
    if key == Key.tab:
        nothing = 0
  
def on_release(key):
      
    if key == KeyCode(char='q'):
        x = int(input("Column: 0 - 5  "))
        y = int(input("Row 0 - 4  "))
        question = q_board[x*11 + 2*y + 1]
        global live
        live = True
        send_to_all(question)
        clear()

    elif key == KeyCode(char='b'):
        clear()
        print(draw_board())
    



def draw_board():
    board="-"
    board = draw_horiz(board)
    #add in column titles
    for l in range(0,6):
        board = board + q_board[l * 11]

    board += "\n"
    board=draw_horiz(board)

    for m in range(0,5):
        board = draw_square(board, m)
        board += "\n"
        board = draw_horiz(board)      
    return board
    
def draw_square(s_board, x):
    s_board = s_board + "|   " + m_board[x][0] + "   |"
    for i in range(1,6):
        s_board = s_board + "   " + m_board[x][i] + "   |"
    return s_board

def draw_horiz(h_board):
    #draw horizantal line
    for l in range(0, 6):
        h_board = h_board + '----------'
    h_board += "\n"
    return h_board
    
def register_user(j, client_c):
    score = 0
    global live
    print('Registering player number: ', j)
    client_c.send(str.encode('Enter your name'))
    name = client_c.recv(1024).decode('utf-8')
    print('Player number ', j, ' name is', name)
    message = (
        '\n Welcome ' + str(name) + ', you have been registered, good luck!!!\n'
        'Press Space to Buzz in\n')
    message = message + str(draw_board())
    client_c.send(str.encode(message))
    while True:
        c_message = client_c.recv(1024).decode('utf-8')
        message = ("\n" + draw_board() +
                   "\nYour score is: " + str(score) +
                   "\n" + question)
        
        if live:
            message += "****************** Answer**********************"
            live = False
            answer = input("Correct? y/n  ")
            if answer:
                score += 100
            else:
                live = True
        else:
            message += "\nPlease wait for a question to buzz in"
            
        client_c.send(str.encode(message))

def send_to_all(blast_message):
    for k in c_socket:
        k.send(str.encode(blast_message))

def connection():
    playernum = 0;
    #specify that we will accept 5 connections
    s.listen(5)
    while True:
        c, addr = s.accept()
        c_socket.append(c)
        #Notify the user that a connection was made
        print('connected to: ', addr, 'player number: ', playernum)
        t = threading.Thread(target=register_user, args=(playernum, c, ))
        threads.append(t)
        t.start()
        playernum += 1   
    

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

#This is the main thread that accepts connections
conn_thread = threading.Thread(target=connection)
conn_thread.start()
    
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

