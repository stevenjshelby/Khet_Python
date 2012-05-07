import sys, pygame
from Pieces import *

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
    
    black = (0,0,0)
    white = (255,255,255)
    
    # Constructor
    def __init__(self, init_layout, screen):
        _initial_layout = init_layout
        self.create_pieces()
        self.the_screen = screen
    
    # Draw the game board image to the screen
    def draw(self, turn, font):
        self.the_screen.blit(self._art, self._art.get_rect())
        for p in self._game_pieces:
            p.draw(self.the_screen)
        turn_text = font.render("Player "+str(turn)+"'s Turn", True, self.white, self.black)
        turn_text_size = [turn_text.get_width(), turn_text.get_height()]
        self.the_screen.blit(turn_text, [self._art.get_width()/2-turn_text_size[0]/2, 0])
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
    
