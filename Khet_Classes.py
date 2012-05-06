import sys, pygame

# Base class for all of the different game pieces
class Game_Piece(object):
    _cell_location = None
    _base_art = pygame.image.load('art/r_pharaoh.png')
    _art = pygame.image.load('art/r_pharaoh.png')
    _direction = 1
    _color = None
    
    # Constructor
    def __init__(self, loc, img, col):
        self._cell_location = loc
        self._base_art = img
        self._art = img
        self._color = col
    
    # Convert the [x, y] cell position to the [x, y] coordinates on the screen
    def cell_to_pos(self):
        x = 28 + (int(self._cell_location[0]) * 53)
        y = 28 + (int(self._cell_location[1]) * 53)
        return [x, y]
    
    # Move the piece the specifies x and y values
    def move(self, cell, gameboard):
        self._cell_location[0] = cell[0]
        self._cell_location[1] = cell[1]
    
    # Draw the piece to the screen, called by the main program loop
    def draw(self, the_screen):
        self.adjust_image()
        the_screen.blit(self._art, self.cell_to_pos())
        pygame.display.flip()
    
    # Rotate the piece
    def rotate(self, turn_dir):
        pass
        # Defined in base-classes
        
    # Apply the correct image and image rotation
    def adjust_image(self):
        pass
        # Defined in the classes that ened it
    
    # Return a list of the valid surrounding cells
    # Need to override in Djed class and Obelisk class
    def get_surrounding_cells(self, cell_pos, gameboard):
        cell_list = []
        
        x = cell_pos[0]
        y = cell_pos[1]
        
        if x > 0:
            cell_list.append([x - 1, y])
        if x < 9:
            cell_list.append([x + 1, y])
        if y > 0:
            cell_list.append([x, y - 1])
        if y < 7:
            cell_list.append([x, y + 1])
        if x > 0 and y > 0:
            cell_list.append([x - 1, y - 1])
        if x < 9 and y < 7:
            cell_list.append([x + 1, y + 1])
        if y > 0 and x < 9:
            cell_list.append([x + 1, y - 1])
        if y < 7 and x > 0:
            cell_list.append([x - 1, y + 1])
        
        new_list = [cell for cell in cell_list if not gameboard.get_piece_by_cell(cell)]
        
        return new_list
    
    # Receives a direction and returns the direction the laser would reflect.
    # Returns 'die' if it kills the piece
    def pass_laser(self, indir):
        pass
        # Defined in sub-classes
        
class Pharaoh(Game_Piece):
    id = 'pharaoh'
    def pass_laser(self, indir):
        #Game over if this piece dies
        return 'die'
        
class Pyramid(Game_Piece):
    id = 'pyramid'
    def __init__(self, loc, img, dir, col):
        self._cell_location = loc
        self._base_art = img
        self._art = img
        self._color = col
        self._direction = dir
        
    def rotate(self, turn_dir):
        if turn_dir == 'L':
            self._direction -= 1
            if self._direction < 1:
                self._direction += 4
        elif turn_dir == 'R':
            self._direction += 1
            if self._direction > 4:
                self._direction -= 4
        
    def adjust_image(self):
        if self._direction == 1:
            self._art = self._base_art
        elif self._direction == 2:
            self._art = pygame.transform.rotate(self._base_art, -90)
        elif self._direction == 3:
            self._art = pygame.transform.rotate(self._base_art, 180)
        elif self._direction == 4:
            self._art = pygame.transform.rotate(self._base_art, 90)
        
    def pass_laser(self, in_dir):
        if self._direction == 1:
            if in_dir == 'Left':
                return 'Down'
            elif in_dir == 'Up':
                return 'Right'
            else:
                # This piece will die now
                return 'die'
        elif self._direction == 3:
            if in_dir == 'Right':
                return 'Up'
            elif in_dir == 'Down':
                return 'Left'
            else:
                # This piece will die now
                return 'die'
        elif self._direction == 4:
            if in_dir == 'Down':
                return 'Right'
            elif in_dir == 'Left':
                return 'Up'
            else:
                # This piece will die now
                return 'die'
        elif self._direction == 2:
            if in_dir == 'Up':
                return 'Left'
            elif in_dir == 'Right':
                return 'Down'
            else:
                # This piece will die now
                return 'die'
                
class Djed(Game_Piece):
    id = 'djed'
    def __init__(self, loc, img, dir, col):
        self._cell_location = loc
        self._base_art = img
        self._art = img
        self._color = col
        self._direction = dir
        
    def rotate(self, turn_dir):
        if self._direction == 1:
            self._direction = 2
        else:
            self._direction = 1
    
    def adjust_image(self):
        if self._direction == 1:
            self._art = self._base_art
        elif self._direction == 2:
            self._art = pygame.transform.rotate(self._base_art, 90)
            
    def pass_laser(self, in_dir):
        if self._direction == 1:
            if in_dir == 'Up':
                return 'Right'
            elif in_dir == 'Down':
                return 'Left'
            elif in_dir == 'Left':
                return 'Up'
            elif in_dir == 'Right':
                return 'Down'
        elif self._direction == 2:
            if in_dir == 'Up':
                return 'Left'
            elif in_dir == 'Down':
                return 'Right'
            elif in_dir == 'Left':
                return 'Down'
            elif in_dir == 'Right':
                return 'Up'
    
    # Need to override the move for Djed because it can switch places with pieces
    def move(self, cell, gameboard):
        self._cell_location[0] = cell[0]
        self._cell_location[1] = cell[1]
                
        
        # Need to add code to be able to switch places with pieces
    
    # Need to modify 
    def get_surrounding_cells(self, cell_pos, gameboard):
        cell_list = []
        
        x = cell_pos[0]
        y = cell_pos[1]
        
        if x > 0:
            cell_list.append([x - 1, y])
        if x < 9:
            cell_list.append([x + 1, y])
        if y > 0:
            cell_list.append([x, y - 1])
        if y < 7:
            cell_list.append([x, y + 1])
        if x > 0 and y > 0:
            cell_list.append([x - 1, y - 1])
        if x < 9 and y < 7:
            cell_list.append([x + 1, y + 1])
        if y > 0 and x < 9:
            cell_list.append([x + 1, y - 1])
        if y < 7 and x > 0:
            cell_list.append([x - 1, y + 1])
        
        new_list = [cell for cell in cell_list if not gameboard.get_piece_by_cell(cell)]
        
        return new_list  
        
class Obelisk(Game_Piece):
    id = 'obelisk'
    _base_art_stacked = pygame.image.load("art/g_Pyramid.png")
    _Stacked = False;
    
    def __init__(self, loc, img, stack_img, col, stacked):
        self._cell_location = loc
        self._base_art = img
        self._base_art_stacked = stack_img
        self._art = img
        self._color = col
        self._Stacked = stacked
        
    def pass_laser(self, indir):
        #This piece dies from all sides
        return 'die'
    
    def adjust_image(self):
        if self._Stacked:
            self._art = self._base_art_stacked
        else:
            self._art = self._base_art
            
    # Need to override the move for Obelisk because it can stack with other obelisks
    def move(self, cell, gameboard):
        old_loc = [self._cell_location[0], self._cell_location[1]]
        
        if gameboard.get_cell_status(cell) == 'piece':
            piece = gameboard.get_piece_by_cell(cell)
            if piece.id == 'obelisk' and piece._Stacked == False:
                piece._Stacked = True
            self._Stacked = True
            
        self._cell_location = cell
        
        if gameboard.get_cell_status(old_loc) == 'piece':
            piece = gameboard.get_piece_by_cell(old_loc)
            if piece.id == 'obelisk':
                piece._Stacked = False
                piece.draw(gameboard.the_screen)
            self._Stacked = False
        
        
    def get_surrounding_cells(self, cell_pos, gameboard):
        cell_list = []
        
        x = cell_pos[0]
        y = cell_pos[1]
        
        if x > 0:
            cell_list.append([x - 1, y])
        if x < 9:
            cell_list.append([x + 1, y])
        if y > 0:
            cell_list.append([x, y - 1])
        if y < 7:
            cell_list.append([x, y + 1])
        if x > 0 and y > 0:
            cell_list.append([x - 1, y - 1])
        if x < 9 and y < 7:
            cell_list.append([x + 1, y + 1])
        if y > 0 and x < 9:
            cell_list.append([x + 1, y - 1])
        if y < 7 and x > 0:
            cell_list.append([x - 1, y + 1])
        
        new_list = [cell for cell in cell_list if not gameboard.get_piece_by_cell(cell) or 
                                                    (gameboard.get_piece_by_cell(cell).id == 'obelisk' 
                                                     and not gameboard.get_piece_by_cell(cell)._Stacked)]
        
        return new_list
        
class Game_Board(object):
    # Load the Game Board image
    _art = pygame.image.load("art/game_board.png")
    _cell_art = [pygame.image.load("art/cell_empty.png"),
                 pygame.image.load("art/cell_red.png"),
                 pygame.image.load("art/cell_gray.png")]
    _initial_layout = 1
    _game_pieces = []
    _current_highlighted_cell = None
    the_screen = None
    
    # Constructor
    def __init__(self, init_layout, screen):
        _initial_layout = init_layout
        self.create_pieces()
        self.the_screen = screen
    
    # Draw the game board image to the screen
    def draw(self):
        self.the_screen.blit(self._art, self._art.get_rect())
        for p in self._game_pieces:
            p.draw(self.the_screen)
        pygame.display.flip()
    
    # Return the status of a cell...
    # Possible Values: "piece", "wall", or "empty"
    def get_cell_status(self, cell_pos):
        for piece in self._game_pieces:
            if piece._cell_location == cell_pos:
                return 'piece'
            if cell_pos[0] < 0 or cell_pos[0] > 9:
                return 'wall'
            if cell_pos[1] < 0 or cell_pos[1] > 7:
                return 'wall'
                
        return 'empty'
    
    # Returns the piece located at a specified cell location
    def get_piece_by_cell(self, cell_pos):
        for piece in self._game_pieces:
            if piece._cell_location == cell_pos:
                return piece
        return False
    
    # Returns the center coordinates of the cell location
    def get_center_by_cell(self, cell_pos):
        center_x = 52 + cell_pos[0] * 53
        center_y = 52 + cell_pos[1] * 53
        
        return [center_x, center_y]
        
    # Convert the [x, y] cell position to the [x, y] coordinates on the screen
    def coords_to_cell(self, coords):
        x = int(coords[0]-28) / 53
        y = int(coords[1]-28) / 53
        return [x, y]
        
    # Convert the [x, y] coords to the [x, y] cell position on the screen
    def cell_to_coords(self, cell):
        x = 28 + (int(cell[0]) * 53)
        y = 28 + (int(cell[1]) * 53)
        return [x, y]
        
    # Draw the transparent highlights around valid cells when player clicks a piece
    def draw_highlight(self, cells, center_cell):
        hl_img = pygame.image.load("art/hl.png")
        h2_img = pygame.image.load("art/h2.png")
        for cell in cells:
            self.the_screen.blit(hl_img, self.cell_to_coords(cell))
        self.the_screen.blit(h2_img, self.cell_to_coords(center_cell))
        pygame.display.flip()
        self._current_highlighted_cell = center_cell
    
    # Remove highlighting from cells
    def reset_cells(self, cells):
        cell_list = cells
        
        if not self._current_highlighted_cell == None:
                piece = self.get_piece_by_cell(self._current_highlighted_cell)
                cell_list.append(piece._cell_location)
                
        for cell in cell_list:
            if self.get_cell_status(cell) == 'empty':
                # Redraw the empty cell
                if cell[0] == 0 or (cell[0] == 1 and cell[1] == 0) or (cell[0] == 1 and cell[1] == 7):
                    # Empty red cell
                    self.the_screen.blit(self._cell_art[1], self.cell_to_coords(cell))
                elif cell[0] == 9 or (cell[0] == 8 and cell[1] == 0) or (cell[0] == 8 and cell[1] == 7):
                    # Empty gray cell
                    self.the_screen.blit(self._cell_art[2], self.cell_to_coords(cell))
                else:
                    # Empty cell
                    self.the_screen.blit(self._cell_art[0], self.cell_to_coords(cell))
            elif self.get_cell_status(cell) == 'piece':
                self.the_screen.blit(self.get_piece_by_cell(cell)._art, self.cell_to_coords(cell))
        pygame.display.flip()
        self._current_highlighted_cell = None
                
    # Draw the laser beams
    def draw_laser(self, l_path):
        # Define the line color...Change it with (R,G,B) values
        red = (255, 0, 0)
        
        path_point_1 = l_path[0][0]
        indir = l_path[0][1]
        path_point_center_1 = self.get_center_by_cell(path_point_1)
        if indir == 'Up':
            path_point_center_1[1] += 24
        elif indir == 'Down':
            path_point_center_1[1] -= 24
        
        for i in xrange(len(l_path)-2):
            path_point_2 = l_path[i+1][0]
            path_point_center_2 = self.get_center_by_cell(path_point_2)
            
            pygame.draw.line(self.the_screen, red, path_point_center_1, path_point_center_2, 2)
            pygame.display.flip()
            pygame.time.wait(200)
            
            path_point_1 = path_point_2
            path_point_center_1 = self.get_center_by_cell(path_point_1)
        
        path_point_2 = l_path[len(l_path)-1][0]
        path_point_center_2 = self.get_center_by_cell(path_point_2)
        if l_path[len(l_path)-2][1] == 'Up':
            path_point_center_2[1] += 24
        elif l_path[len(l_path)-2][1] == 'Down':
            path_point_center_2[1] -= 24
        elif l_path[len(l_path)-2][1] == 'Left':
            path_point_center_2[0] += 24
        elif l_path[len(l_path)-2][1] == 'Right':
            path_point_center_2[0] -= 24
            
        pygame.draw.line(self.the_screen, red, path_point_center_1, path_point_center_2, 2)
        pygame.display.flip()
        pygame.time.wait(200)
            
    # Read the game piece setup from a text file
    # The three starting configuration in the game will be provided but
    # it is very simple to create your own layout.
    def create_pieces(self):
        with open("initial_layouts/piece_config_"+str(self._initial_layout)+".txt") as f:
            temp_piece_list = []
            lines = f.readlines()
            for line in lines:
                if line.startswith("#") or line.strip() == "":
                    continue
                split = line.split(", ")
                color = split[0]
                type = split[1]
                x = int(split[2])
                y = int(split[3])
                if color == "red":
                    if type == "Pharaoh":
                        temp_piece_list.append(Pharaoh([x, y], 
                                                       pygame.image.load("art/r_Pharaoh.png"), 
                                                       "red"))
                    elif type == "Pyramid":
                        temp_piece_list.append(Pyramid([x, y], 
                                                       pygame.image.load("art/r_Pyramid.png"), 
                                                       int(split[4]),
                                                       "red"))
                    elif type == "Djed":
                        temp_piece_list.append(Djed([x, y], 
                                                    pygame.image.load("art/r_Djed.png"),
                                                    int(split[4]),
                                                    "red"))
                    elif type == "Obelisk":
                        if split[4].strip() == 'True':
                            temp_piece_list.append(Obelisk([x, y], 
                                                           pygame.image.load("art/r_Obelisk.png"),
                                                           pygame.image.load("art/r_Stacked_Obelisk.png"),  
                                                           "red",
                                                           True))
                            temp_piece_list.append(Obelisk([x, y], 
                                                           pygame.image.load("art/r_Obelisk.png"), 
                                                           pygame.image.load("art/r_Stacked_Obelisk.png"), 
                                                           "red",
                                                           True))
                        else:
                            temp_piece_list.append(Obelisk([x, y], 
                                                           pygame.image.load("art/r_Obelisk.png"), 
                                                           pygame.image.load("art/r_Stacked_Obelisk.png"), 
                                                           "red",
                                                           False))
                elif color == 'gray':
                    if type == "Pharaoh":
                        temp_piece_list.append(Pharaoh([x, y], 
                                                       pygame.image.load("art/g_Pharaoh.png"), 
                                                       "gray"))
                    elif type == "Pyramid":
                        temp_piece_list.append(Pyramid([x, y], 
                                                       pygame.image.load("art/g_Pyramid.png"), 
                                                       int(split[4]),
                                                       "gray"))
                    elif type == "Djed":
                        temp_piece_list.append(Djed([x, y], 
                                                    pygame.image.load("art/g_Djed.png"),
                                                    int(split[4]),
                                                    "gray"))
                    elif type == "Obelisk":
                        if split[4].strip() == 'True':
                            temp_piece_list.append(Obelisk([x, y], 
                                                           pygame.image.load("art/g_Obelisk.png"), 
                                                           pygame.image.load("art/g_Stacked_Obelisk.png"), 
                                                           "gray",
                                                           True))
                            temp_piece_list.append(Obelisk([x, y], 
                                                           pygame.image.load("art/g_Obelisk.png"), 
                                                           pygame.image.load("art/g_Stacked_Obelisk.png"), 
                                                           "gray",
                                                           True))
                        else:
                            temp_piece_list.append(Obelisk([x, y], 
                                                           pygame.image.load("art/g_Obelisk.png"), 
                                                           pygame.image.load("art/g_Stacked_Obelisk.png"), 
                                                           "gray",
                                                           False))
        self._game_pieces = temp_piece_list
    
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
		