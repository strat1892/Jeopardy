# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 21:34:14 2018

@author: Peter
"""

import socket

import os
import sys
from pynput.keyboard import Key, KeyCode, Listener
import threading

clear = lambda: os.system('cls')

def on_press(key):
    if key == Key.tab:
        nothing = 0
    

def on_release(key):

    if key == Key.space: 
        message = '0'
        s.send(str.encode(message))
    elif key == Key.esc:
        sys.exit(0)
        
def client_listen():
    while True:
        data = s.recv(1024)
        clear()
        print(data.decode('utf-8'))
              

    
#this should be the IP address and port of the server you are trying to connect to
host = '192.168.0.169'

port = 12345

#note that the client port will be randomly generated withing the session layer
#of the OSI model. This is so that incoming traffic can be routed to the correct
#Program

#create the socket
s = socket.socket()

#connect to the socket with the above IP and port
s.connect((host, port))
data = s.recv(1024)
print(data.decode('utf-8'))
name_m = input()
s.send(str.encode(name_m))

t = threading.Thread(target=client_listen)
t.start()

with Listener(
            on_press=on_press,
            on_release=on_release) as listener:
    listener.join() 

