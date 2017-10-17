#!/usr/bin/python           # This is server.py file
"""This runs a client and server for a game of hangman over a network. Clients
 get 3 guesses to guess the provided word"""
import socket               # Import socket module
import argparse
import string
import struct
import os
import sys
import atexit



def server(port, word, ipnum):
    """This creates the server for the game"""
# creates socket to accept connections
    wordlen = len(word)
    guesses = 3
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    blankw = '_' * wordlen
    blankw = bytes(blankw, 'utf-8')
    package = struct.pack('!b{:d}s'.format(wordlen), guesses, blankw)
    blankw = blankw.decode("utf-8")
    if ipnum is None:
        ipnum = socket.gethostname()
    sock.bind((ipnum, port))
    sock.listen(10)                 # Now wait for client connection.
    i = 1
    while i <= 10:\
        # allows up to 10 connections to game
        con, _addr = sock.accept()
        cid = os.fork()
        if cid == 0:
            send(con, package)
            # accepts guesses and sends updated info to client until word is
            # guessed or player runs out of guesses
            while blankw != word and guesses > 0:
                _psize, guess = recv(con)
                guess = struct.unpack('!s', guess)
                guess = list(guess[0].decode("utf-8"))
                if guess[0] in word and guess[0] not in blankw:
                    index = [pos for pos, char in enumerate(word)
                             if char == guess[0]]
                    listword = list(blankw)
                    for i in index:
                        listword[i] = guess[0]
                    blankw = ''.join(listword)
                else:
                    guesses -= 1
                blankw = bytes(blankw, 'utf-8')
                package = struct.pack('!b{:d}s'.format(wordlen), guesses, blankw)
                send(con, package)
                blankw = blankw.decode("utf-8")
            closeconnection(con)                # Close the connection
        else:
            i += 1
    closeconnection(sock)
    atexit.register(closeconnection(sock))


def client(port, ipnum):
    """creates the client to play the game"""
    sock = socket.socket()
    if ipnum is None:
        ipnum = socket.gethostname()
    sock.connect((ipnum, port))
    wordlen, startword = recv(sock)
    guesses, gamewrd = struct.unpack('!b{:d}s'.format(wordlen-1), startword)
    gamewrd = gamewrd.decode("utf-8")
    #keeps guessing until player runs out of guesses or word is guessed
    while guesses > 0 and '_' in gamewrd:
        print('Board: ', gamewrd, '(', guesses, 'guesses left )')
        guess = ''
        while len(guess) != 1:
            guess = input('Enter guess: ')
        guess = guess.lower()
        guess = str.encode(guess)
        message = struct.pack('!s', guess)
        send(sock, message)
        wordlen, startword = recv(sock)
        guesses, gamewrd = struct.unpack('!b{:d}s'.format(wordlen-1), startword)
        gamewrd = gamewrd.decode("utf-8")
    print('Board: ', gamewrd)
    if guesses > 0:
        print('You won')
    else:
        print('You lost')
    closeconnection(sock)


def recv(connection):
    """reads size of incoming packet and then reads packet"""
    try:
        psize = connection.recv(4, socket.MSG_WAITALL)
        psize = struct.unpack('!i', psize)
        return psize[0], connection.recv(psize[0], socket.MSG_WAITALL)
    except TimeoutError:
        print("Timeout")


def closeconnection(connection):
    """closes the socket"""
    connection.close()


def send(connection, message):
    """Sends size of packet and then actual packet"""
    psize = len(message)
    psize = struct.pack('!i', psize)
    connection.send(psize)
    connection.send(message)


def main():
    """Parses command line arguments, starts server or client"""
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument(
        '--mode', choices=['client', 'server'],
        required=True, help='client or server mode'
    )
    parser.add_argument('--port', type=int, required=True, help='port number')
    parser.add_argument('--word', help='word to be guessed')
    parser.add_argument('--ip', help='IP address for client')
    args = parser.parse_args()
    mode = args.mode
    port = args.port
    word = args.word
    ipnum = args.ip
    if mode == 'server':
        if word is None:
            print("Need to provide word to start game as server")
            exit()
        server(port, word, ipnum)

    else:
        client(port, ipnum)

main()
