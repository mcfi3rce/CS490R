import socket
import thread
import select
import time
import string
import argparse
from collections import deque

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

class Player:
    player_id = -1

    # Last movement direction from client: None, Up, Down, Left, Right
    last_dir = ""
    loc_x = 0
    loc_y = 0

    def __init__ (self, id):
        self.player_id = id

players = {}

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
                    s.send("q")
                except socket.error as msg:
                    print("Player " + input[1] + " disconnected")
                del players[player.player_id]
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
                    player.loc_y = (player.loc_y - 1) % 25
                elif input[2] == "d":
                    player.loc_y = (player.loc_y + 1) % 25
                elif input[2] == "r":
                    player.loc_x = (player.loc_x + 1) % 80
                elif input[2] == "l":
                    player.loc_x = (player.loc_x - 1) % 80

                player.last_dir = input[2]
                players[player.player_id] = player
            else:
                print(input)

        for i, p in players.iteritems():
            clientsocket.send("p:" + str(p.player_id) + ":" + str(p.loc_x) + ":" + str(p.loc_y) + "\n")

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

