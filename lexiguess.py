#!/usr/bin/python           # This is server.py file
import socket               # Import socket module
import argparse


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
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname() # Get local machine name
    print(host)
    s.bind((host, port))        # Bind to the port
    s.listen(5)                 # Now wait for client connection.
    while True:
        c, addr = s.accept()     # Establish connection with client. This where
            #server waits
        print('Got connection')
        c.send(b'Test')
        #Comment the line below and try changing the bytes on the receiving
        #end on the client
        c.close()                # Close the connection
    s.close() # Closing server socket

else:
    import socket  # Import socket module

    s = socket.socket()  # Create a socket object
    host = socket.gethostname()  # Get local machine name
    print(host)
    s.connect((host, port))
    print(s.recv(4, socket.MSG_WAITALL))  # this is where client (or server) waits, WAITALL blocks
    s.close  # Close the socket when done
