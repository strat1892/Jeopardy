# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 21:24:13 2018

@author: strat
"""

import socket
import os, sys
import threading
from pynput.keyboard import Key, Listener
clear = lambda: os.system('cls')

score = 0;

num_players = int(input('Enter the number of players: '))
playernum = 0;
name = threading.local()
name = threading.local()

def on_press(key):
    if key == Key.tab:
        clear()
  
def on_release(key):
    if key == Key.space: 
        clear()

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



#def server_commands():
    

#this is the server so ask the OS what the computer name is
host = '10.1.10.175'
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

