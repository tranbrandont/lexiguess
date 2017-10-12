#!/usr/bin/python           # This is server.py file
import socket               # Import socket module
import argparse
import random
import string
import struct

def server(port, word):
    word, wordLen = hangman(word)
    guesses = 3
    #startInfo = struct.pack('!', word, wordLen, guesses)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname() # Get local machine name
    startword = word.encode('ascii')
    s.bind((host, port))        # Bind to the port
    s.listen()                 # Now wait for client connection.
    while True:
        c, addr = s.accept()     # Establish connection with client. This where

        print('Got connection')
        c.send(startword)
        c.close()                # Close the connection
    s.close() # Closing server socket

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
        server(port, word)

    else:
        import socket  # Import socket module

        s = socket.socket()  # Create a socket object
        host = socket.gethostname()  # Get local machine name
        print(host)
        s.connect((host, port))
        startWord = (s.recv(4, socket.MSG_WAITALL))  # this is where client (or server) waits, WAITALL blocks
        print(startWord.decode())
        s.close  # Close the socket when done

main()


