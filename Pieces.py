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
        if gameboard.get_cell_status(cell) == 'piece':
            piece = gameboard.get_piece_by_cell(cell)
            piece._cell_location = self._cell_location
            if piece.id == 'obelisk' and piece._Stacked == True:
                piece = gameboard.get_piece_by_cell(cell)
                piece._cell_location = self._cell_location
            
        self._cell_location = cell
    
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
        
        new_list = [cell for cell in cell_list if not gameboard.get_piece_by_cell(cell) or 
                                                    gameboard.get_piece_by_cell(cell).id == 'obelisk' or
                                                     gameboard.get_piece_by_cell(cell).id == 'pyramid' ]
        
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