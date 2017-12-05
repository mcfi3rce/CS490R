class Player:
    player_id = -1

    has_ball = False
    num_points = 0
    loc_x = 0
    loc_y = 0

    #client_socket = 

    def __init__ (self, id):
        self.player_id = id

    def parse_command(command):
        # Command comes in as an array
        # Confirm array is correctly sized
        if len(command) == 4 and command[3] != "" and int(command[1]) == self.player_id:
            self.loc_x = command[2]
            self.loc_y = command[3]
            if command[4] == "0":
                self.has_ball = False
            elif command[4] == "1":
                self.has_ball = True


