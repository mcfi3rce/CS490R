import socket
import thread

class Player:
    player_id = -1
    loc_x = 0
    loc_y = 0

def client_thread(clientsocket, address, id):
   print("player" + str(id) + ": " +str(address) + " connected")

   clientsocket.send(str(start))

   m = int(clientsocket.recv(10))
   result.r = m

   clientsocket.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 11000))

s.listen(5)

next_id = 0
players = []
while 1:
   (clientsocket, address) = s.accept()
   thread.start_new_thread(client_thread, (clientsocket, address, id))
   next_id = next_id + 1

