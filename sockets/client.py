import socket
import thread
import string
from collections import deque

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 11000))

commands = deque()

def recieve(socket, queue):
    buffer = s.recv(2048)
    split = string.split(buffer)
    for field in split:
        queue.append(field)
            

recieve(s, commands)


while True:

    recieve(s, commands)

    while len(commands) > 0:
        command = string.split(commands.popleft(), ":")
        if command[0] == "q":
            print("Recieved quit")
            s.close()
            exit()
        elif command[0] == "i":
            my_id = int(command[1])
            print("My id is: " + str(my_id))
        else:
            print(command)
    #sleep(1)
s.send("u\n")


