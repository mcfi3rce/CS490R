import socket
import thread
import select
import time
import string
import argparse
import signal
import sys
from player import Player
from collections import deque

AREA_WIDTH = 78
AREA_HEIGHT = 25

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", type=int, help="port number to connect to")
parser.add_argument("-i", "--ip", help="ip address to connect to")
args = parser.parse_args()

# set up socket parameters
port = 11000
ip = ""
if args.port:
    port = args.port

if args.ip:
    ip = args.ip

players = {}

def handler_sigint(signal, frame):
    print("Recieved SIGINT, server exiting")
    try:
        s.close()
    except signal.error as msg:
        print(msg)
    sys.exit()

signal.signal(signal.SIGINT, handler_sigint)

def recieve(socket, queue):
    buffer = socket.recv(2048)
    split = string.split(buffer)
    for field in split:
        queue.append(field)

def client_thread(clientsocket, address, id):
    inputs = deque()
    quit = False

    # Server log
    print("player " + str(id) + ": " +str(address) + " connected")

    # Create new player for this connection
    player = Player(id)
    players[player.player_id] = player

    # send the client his id
    clientsocket.send("i:" + str(player.player_id) + "\n")

    while quit != True:
        readable, w, e = select.select([clientsocket],[],[],0.001)
        for sock in readable:
            recieve(sock, inputs)

        while len(inputs) > 0:
            input = string.split(inputs.popleft(), ":")
            if input[0] == "q":
                print("Player " + input[1] + " quit")
                try:
                    clientsocket.send("q")
                except socket.error as msg:
                    print("Player " + input[1] + " disconnected")
                try:
                    del players[player.player_id]
                except KeyError as msg:
                    print("Player already deleted")
                quit = True
                try:
                    clientsocket.close()
                except socket.error as msg:
                    print(msg)
                break
                #exit()
            elif input[0] == "m":
                print("Player " + input[1] + " wants to move " + input[2])
                if input[2] == "u":
                    player.loc_y = (player.loc_y - 1) % AREA_HEIGHT
                elif input[2] == "d":
                    player.loc_y = (player.loc_y + 1) % AREA_HEIGHT
                elif input[2] == "r":
                    player.loc_x = (player.loc_x + 1) % AREA_WIDTH
                elif input[2] == "l":
                    player.loc_x = (player.loc_x - 1) % AREA_WIDTH

                player.last_dir = input[2]
                players[player.player_id] = player
            else:
                print(input)

        for i, p in players.iteritems():
            try:
                clientsocket.send("p:" + str(p.player_id) + ":" + str(p.loc_x) + ":" + str(p.loc_y) + "\n")
            except socket.error as msg:
                print("Player seems to have disconnected, closing socket")
                try:
                    del players[player.player_id]
                except KeyError as msg:
                    print("Player already deleted")
                try:
                    clientsocket.close()
                except socket.error as msg:
                    print("Socket already closed")
                quit = True
                break

        time.sleep(0.1)

    #clientsocket.send("q\n")
    #clientsocket.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ip, port))

s.listen(5)

next_id = 0
while True:
   (clientsocket, address) = s.accept()
   thread.start_new_thread(client_thread, (clientsocket, address, next_id))
   next_id = next_id + 1

