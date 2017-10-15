#!/usr/bin/python           # This is server.py file
import socket               # Import socket module
import argparse
import random
import string
import struct
import os
import sys


def server(port, word, ip):
    word, wordLen = hangman(word)
    guesses = 3
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname() # Get local machine name
    blankW = '_' * wordLen
    blankW = bytes(blankW, 'utf-8')
    package = struct.pack('!bb8s', wordLen, guesses, blankW)
    blankW = blankW.decode("utf-8")
    if ip != None:
        s.bind((ip, port))        # Bind to the port
    else:
        s.bind((host, port))
    s.listen(10)                 # Now wait for client connection.
    i = 1
    while i <= 10:
        c, addr = s.accept()     # Establish connection with client. This where
        cid = os.fork()
        if cid == 0:
            send(c, package)
            while blankW != word and guesses > 0:
                guess = recv(c)
                guess = struct.unpack('!s', guess)
                guess = list(guess[0].decode("utf-8"))
                if guess[0] in word:
                    index = [pos for pos, char in enumerate(word) if char == guess[0]]
                    listWord = list(blankW)
                    for i in index:
                        listWord[i] = guess[0]
                    blankW = ''.join(listWord)
                else:
                    guesses-=1
                blankW = bytes(blankW, 'utf-8')
                package = struct.pack('!bb8s', wordLen, guesses, blankW)
                send(c, package)
                blankW = blankW.decode("utf-8")
            c.close()                # Close the connection
        else:
            i += 1
    s.close() # Closing server socketindex =


def client(port, ip):
    s = socket.socket()  # Create a socket object
    host = socket.gethostname()  # Get local machine name
    s.connect((ip, port))
    startWord = recv(s)  # this is where client (or server) waits, WAITALL blocks
    wordLen, guesses, gameWord = struct.unpack('!bb8s', startWord)
    gameWord = gameWord.decode("utf-8")
    while guesses > 0 and '_' in gameWord:
        print ('Board: ', gameWord, '(',guesses, 'guesses left )')
        guess = ''
        while len(guess) != 1:
            guess = input('Enter guess: ')
        guess = guess.lower()
        guess = str.encode(guess)
        message = struct.pack('!s', guess)
        send(s, message)
        startWord = recv(s)  # this is where client (or server) waits, WAITALL blocks
        wordLen, guesses, gameWord = struct.unpack('!bb8s', startWord)
        gameWord = gameWord.decode("utf-8")
    if guesses > 0:
        print('You won')
    else:
        print('You lost')
    s.close  # Close the socket when done


def hangman(word):
    if word is None:
        word = ''
        for i in range(random.randint(1, 8)):
            word += (random.choice(string.ascii_lowercase))
    wordlen = len(word)
    return word, wordlen


def recv(connection):
    psize = connection.recv(4, socket.MSG_WAITALL)
    psize = struct.unpack('!i', psize)
    return connection.recv(psize[0], socket.MSG_WAITALL)


def send(connection, message):
    psize = len(message)
    psize = struct.pack('!i', psize)
    connection.send(psize)
    connection.send(message)

def main():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('--mode', choices=['client', 'server'], required=True, help='client or server mode')
    parser.add_argument('--port', type=int, required=True, help='port number')
    parser.add_argument('--word', help='word to be guessed')
    parser.add_argument('--ip', help='IP address for client')
    args = parser.parse_args()
    mode = args.mode
    port = args.port
    word = args.word
    ip = args.ip
    if mode == 'server':
        server(port, word, ip)

    else:
        client(port, ip)

main()
