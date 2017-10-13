#!/usr/bin/python           # This is server.py file
import socket               # Import socket module
import argparse
import random
import string
import struct
import os

def server(port, word, ip):
    word, wordLen = hangman(word)
    guesses = 3
    #startInfo = struct.pack('!', word, wordLen, guesses)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname() # Get local machine name
    word = bytes(word, 'utf-8')
    package = struct.pack('!hh8s', wordLen, guesses, word)
    print(struct.calcsize('!hh8s'))
    print(package)
    s.bind((ip, port))        # Bind to the port
    s.listen(10)                 # Now wait for client connection.
    i = 1
    while i <= 10:
        c, addr = s.accept()     # Establish connection with client. This where
        cid = os.fork()
        if cid == 0:
            c.send(package)
            c.close()                # Close the connection
        else:
            i += 1
    s.close() # Closing server socket

def client(port, ip):
    s = socket.socket()  # Create a socket object
    host = socket.gethostname()  # Get local machine name
    print(host)
    s.connect((ip, port))
    startWord = (s.recv(12, socket.MSG_WAITALL))  # this is where client (or server) waits, WAITALL blocks
    wordLen, guesses, word = struct.unpack('!hh8s', startWord)
    print(wordLen, guesses, word)
    s.close  # Close the socket when done

def hangman(word):
    if word is None:
        word = ''
        for i in range(random.randint(1,8)):
            word += (random.choice(string.ascii_lowercase))
    wordLen = len(word)
    return (word, wordLen)



def main():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('--mode', choices = ['client', 'server'], required=True, help='client or server mode')
    parser.add_argument('--port', type=int, required=True, help='port number')
    parser.add_argument('--word', help='word to be guessed')
    parser.add_argument('--ip', help='IP address for client')
    args = parser.parse_args()
    print(args)
    mode = args.mode
    port = args.port
    word = args.word
    ip = args.ip
    if mode == 'server':
        server(port, word, ip)

    else:
        client(port, ip)

main()