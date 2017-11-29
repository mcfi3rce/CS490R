import socket
import thread
import string

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 11000))

buffer = ''
buffer += s.recv(1)

split = string.split(buffer, "\n", 1)[0]
if len(split) >= 2:
    buffer = split[1]

my_id = int(split[0])
print("My id is: " + str(my_id))

#s.send(str(sum(range(m, m + 10))))

while True:
    buffer += s.recv(2048)
    split = string.split(buffer, "\n", 1)[0]
    if len(split) >= 2:
        buffer = split[1]


    if split[0] == "quit":
        print("Recieved quit")
        exit()
    else:
        print(split[0])


s.close()
