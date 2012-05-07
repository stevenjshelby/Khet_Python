import sys, pygame

class Player(object):
    name = ""
    laser_movement = [] #[[0,0],"Down"] where [0,0] is the next cell the laser will hit and "Down" is the direction it enters that cell
	
    # Constructor
    def __init__(self, name, laser_movement):
        self.name = name
        self.laser_movement = laser_movement
	
	# Find the path of the players laser beam
    def find_path(self, gameboard):
        pieces = gameboard._game_pieces
        l_path = []
        l_path.append(self.laser_movement)
        
        i = 0
        next_cell = [l_path[i][0][0], l_path[i][0][1]]
        while i >= 0:
            curr_dir = l_path[i][1]
            while not gameboard.get_cell_status(next_cell) == 'piece':
                if gameboard.get_cell_status(next_cell) == 'wall':
                    break
                else:
                    if curr_dir == 'Up':
                        next_cell[1] -= 1
                    elif curr_dir == 'Down':
                        next_cell[1] += 1
                    elif curr_dir == 'Left':
                        next_cell[0] -= 1
                    elif curr_dir == 'Right':
                        next_cell[0] += 1
           
            if gameboard.get_cell_status(next_cell) == 'wall':
                l_path.append([next_cell, 'Terminate'])
                i = -1
            else:
                # Must be a piece at the cell if made it here
                curr_piece = gameboard.get_piece_by_cell(next_cell)
                
                # The direction that this piece forwards the laser
                forward_dir = curr_piece.pass_laser(curr_dir)
                if forward_dir == 'die':
                    if curr_piece.id == 'pharaoh':
                        if curr_piece._color == 'red':
                            p1_win = True
                        elif curr_piece._color == 'gray':
                            p2_win = True
                        pieces.remove(curr_piece)
                    else:
                        pieces.remove(curr_piece)
                        if curr_piece.id == 'obelisk' and gameboard.get_piece_by_cell(next_cell):
                            gameboard.get_piece_by_cell(next_cell)._Stacked = False
                            
                    l_path.append([next_cell, 'Terminate'])
                    i = -1
                else:
                    l_path.append([next_cell, forward_dir])
                    if forward_dir == 'Up':
                        next_cell = [next_cell[0], next_cell[1] - 1]
                    if forward_dir == 'Down':
                        next_cell = [next_cell[0], next_cell[1] + 1]
                    if forward_dir == 'Left':
                        next_cell = [next_cell[0] - 1, next_cell[1]]
                    if forward_dir == 'Right':
                        next_cell = [next_cell[0] + 1, next_cell[1]]
                    i += 1
        
        return l_path
		