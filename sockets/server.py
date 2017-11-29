import socket
import thread
import select
import time
import string
import Queue
from collections import deque

class Player:
    player_id = -1

    # Last movement direction from client: None, Up, Down, Left, Right
    last_dir = "n"
    loc_x = 0
    loc_y = 0

    def __init__ (self, id):
        self.player_id = id

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
                quit = True
                break
                #s.close()
                #exit()
            elif input[0] == "m":
                print("Player " + input[1] + " wants to move " + input[2])
            else:
                print(input)

    #for i in range(1, 10):
        #clientsocket.send("p:" + str(i) + "\n")
        #time.sleep(1)
   #m = int(clientsocket.recv(10))
   #result.r = m

    clientsocket.send("q\n")
    clientsocket.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 11000))

s.listen(5)

next_id = 0
players = []
moves = Queue.Queue()
while True:
   (clientsocket, address) = s.accept()
   thread.start_new_thread(client_thread, (clientsocket, address, next_id))
   next_id = next_id + 1

