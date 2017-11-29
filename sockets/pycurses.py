import sys,os
import curses
import socket
import thread
import string
import select
from collections import deque

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 11000))

players = {}

def recieve(socket, queue):
    buffer = socket.recv(2048)
    split = string.split(buffer)
    for field in split:
        queue.append(field)

def draw_menu(stdscr):
    k = 0
    #cursor_x = 0
    #cursor_y = 0
    last_command = ""

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # Loop where k is the last character pressed
    while (k != ord('q')):
        move = ""
        commands = deque()

        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # This changes terminal size
        #print "\x1b[8;50;80t"

        if k == curses.KEY_DOWN:
            move = "d"
        elif k == curses.KEY_UP:
            move = "u"
        elif k == curses.KEY_RIGHT:
            move = "r"
        elif k == curses.KEY_LEFT:
            move = "l"
        elif k == ord('q'):
            s.send("q:" + str(player.player_id))


        if move != "":
            s.send("m:" + str(my_id) + ":" + move + "\n")

        #cursor_x = max(0, cursor_x)
        #cursor_x = min(width-1, cursor_x)

        #cursor_y = max(0, cursor_y)
        #cursor_y = min(height-1, cursor_y)

        # Declaration of strings
        #title = "Curses example"[:width-1]
        #subtitle = "Written by Adam McPherson and Brandon Hartshorn"[:width-1]
        #keystr = "Last key pressed: {}".format(k)[:width-1]
        #if k == 0:
            #keystr = "No key press detected..."[:width-1]

        # Centering calculations
        #start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
        #start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
        #start_x_keystr = int((width // 2) - (len(keystr) // 2) - len(keystr) % 2)
        #start_y = int((height // 2) - 2)

        # Rendering some text
        #whstr = "Width: {}, Height: {}".format(width, height)
        #stdscr.addstr(0, 0, whstr, curses.color_pair(1))

        # Turning on attributes for title
        #stdscr.attron(curses.color_pair(2))
        #stdscr.attron(curses.COLOR_MAGENTA)

        # Rendering title
        #stdscr.addstr(start_y, start_x_title, title)

        # Turning off attributes for title
        #stdscr.attroff(curses.color_pair(2))
        #stdscr.attroff(curses.COLOR_MAGENTA)

        # Print rest of text
        #player = "O"[:width-1]
        #stdscr.addstr(10, 10, player)
        #stdscr.addstr(cursor_y, cursor_x, "O")

        readable, w, e = select.select([s],[],[],0.01)
        for sock in readable:
            recieve(s, commands)

        while len(commands) > 0:
            command = string.split(commands.popleft(), ":")
            if command[0] == "q":
                # print("Recieved quit")
                s.close()
                exit()
            elif command[0] == "i":
                my_id = int(command[1])
                # print("My id is: " + str(my_id))
            elif command[0] == "p":
                players[command[1]] = [command[2], command[3]]

            last_command = str(command)

        #create statusbar string
        statusbarstr = "Press 'q' to exit | Command: {} | Output: {}".format(last_command, move)
        #render Players
        for i, p in players.iteritems():
            stdscr.addstr(int(p[1]), int(p[0]), "O")


        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

def main():
    curses.wrapper(draw_menu)

if __name__ == "__main__":
    main()
