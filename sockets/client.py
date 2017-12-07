import curses
import socket
import string
import select
import time
import argparse
from player import Player
from collections import deque

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", type=int, help="port number to connect to")
parser.add_argument("-i", "--ip", help="ip address to connect to")
args = parser.parse_args()

# set up socket parameters
port = 11000
ip = "localhost"
if args.port:
    port = args.port

if args.ip:
    ip = args.ip

players = {}

# set up the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))

def recieve(socket, queue):
    buffer = socket.recv(2048)
    split = string.split(buffer)
    for field in split:
        queue.append(field)

def game_loop(stdscr):
    k = 0
    #cursor_x = 0
    #cursor_y = 0
    last_command = ""

    # Clear and refresh the screen for a blank canvas
    stdscr.erase()
    stdscr.refresh()
    stdscr.nodelay(True)

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK) 
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_WHITE)
    
    curses.curs_set(0)
    curses.resizeterm(28, 80)

    quit = False

    # Loop where k is the last character pressed
    while quit != True:
        move = ""
        commands = deque()

        # Initialization
        stdscr.erase()
        height, width = stdscr.getmaxyx()

        if k == curses.KEY_DOWN or k == ord('j'):
            move = "d"
        elif k == curses.KEY_UP or k == ord('k'):
            move = "u"
        elif k == curses.KEY_RIGHT or k == ord('l'):
            move = "r"
        elif k == curses.KEY_LEFT or k == ord('h'):
            move = "l"
        elif k == ord('p'):
            prompt_message = "Please enter the 'Character' you would like to be"
            prompt = stdscr.subwin(3,len(prompt_message) + 4, 13, 10)
            prompt.attron(curses.color_pair(1))
            prompt.border()
            prompt.attroff(curses.color_pair(1))
            prompt.addstr(1,2, prompt_message)
            prompt.refresh()
            c = -1
            while (c > 126 or c < 33):
                c = prompt.getch()
            s.send("c:" + str(my_id) + ":" + chr(c) + "\n")
        elif k == ord('q'):
            s.send("q:" + str(my_id))
            quit = True

        if move != "":
            s.send("m:" + str(my_id) + ":" + move + "\n")

        readable, w, e = select.select([s],[],[],0.01)
        for sock in readable:
            recieve(s, commands)

        while len(commands) > 0:
            command = string.split(commands.popleft(), ":")
            if command[0] == "q":
                quit = True
                #s.close()
                #exit()
            elif command[0] == "i":
                my_id = int(command[1])
                # print("My id is: " + str(my_id))
            elif command[0] == "p" and len(command) == 5 and command[4] != "":
                players[int(command[1])] = [command[2], command[3], command[4]]

            last_command = str(command)

        #create statusbar string
        statusbarstr = "Press 'q' to exit | Command: {} | Movement: {}".format(last_command, move)
        #render Players
        for i, p in players.iteritems():
            if (i == my_id):
                stdscr.addstr(int(p[1]) + 1, int(p[0]) + 1, p[2], curses.color_pair(2))
            else:
                stdscr.addstr(int(p[1]) + 1, int(p[0]) + 1, p[2], curses.color_pair(1))


        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(26, 1, statusbarstr)
        stdscr.addstr(26, len(statusbarstr), " " * (80 - len(statusbarstr)))
        stdscr.attroff(curses.color_pair(3)) 
        stdscr.border()

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

    # When game loop is finished
    s.close()
    exit()

def main():
    curses.wrapper(game_loop)

if __name__ == "__main__":
    main()
