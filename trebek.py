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



playernum = 0;  #Assign number as players connect
threads = []    #List for threads
name = threading.local() #check can prob get rid of this
player_name = []    #list of player names
c_socket = []   #list of player connections
player_score = []   #Keep track of scores
question_live = False   #Has a question been asked
player_buzz = False     #Can someone buzz in
prize = 0;      #What the current value of question is
question = "  " #String of question
cursor_pos = 189 #Position in string of first square

def on_press(key):
    if key == Key.delete:
        sys.exit(0)
  
def on_release(key):
    global prize
    global cursor_pos
    if key == KeyCode(char='q'):
        x = int(input("Row 0 - 5  "))
        y = int(input("Column: 0 - 4  "))
        question = q_board[x*11 + 2*y + 1]
        prize = y*100 + 100
        m_board[y][x] = "   "
        
        
        global question_live
        question_live = True
        send_to_all(question)
        clear()

    elif key == KeyCode(char='b'):
        host_board()
        
    elif key == Key.right:
        cursor_pos += 10
        host_board()

    elif key == Key.left:
        cursor_pos -= 10
        host_board()

    elif key == Key.down:
        cursor_pos += 123
        host_board()

    elif key == Key.up:
            cursor_pos -= 123
            host_board()

def draw_board():
    board="\n-"
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

    for i in range(0, playernum):
        board += "\n" + player_name[i] + ": Score: " + str(player_score[i])

    board += "\n" + question
    return board

#Adds to the board the curor to select the question
def host_board():
    clear()
    message = draw_board()
    message = message[:cursor_pos] + '*' + message[cursor_pos + 1:]
    print(message)
    
    
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
    global question_live
    global player_answer
    global player_score
    print('Registering player number: ', j)
    client_c.send(str.encode('Enter your name'))
    player_name.append(client_c.recv(1024).decode('utf-8'))
    player_score.append(0)
    print('Player number ', j, ' name is', player_name[j])
    message = (
        '\n Welcome ' + str(player_name[j]) + ', you have been registered, good luck!!!\n'
        'Press Space to Buzz in\n')
    message = message + str(draw_board())
    client_c.send(str.encode(message))
    while True:
        c_message = client_c.recv(1024).decode('utf-8')
        message = draw_board()
        client_c.send(str.encode(message))
        
        if question_live:
                client_c.send(str.encode(message + "****************** Answer**********************"))
                print(player_name[j] + " has buzzed in")
                player_buzz = True
                answer = input("Correct? y/n ")
                if answer == 'y':
                    question_live = False
                    player_score[j] += prize
                    send_to_all(message + "\nCorrect!!!! You won: " + str(prize) )
                    
                else:
                    play_buzz = False
                    player_score[j] -= prize
                    send_to_all(message + "\nIncorrect \n" + question)
        else:
            client_c.send(str.encode(message + "\nPlease wait for a question to buzz in"))
            
       

def send_to_all(blast_message):
    for k in c_socket:
        k.send(str.encode(blast_message))

def connection():
    global playernum
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
host_board()

#This is the main thread that accepts connections
conn_thread = threading.Thread(target=connection)
conn_thread.start()
    
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

