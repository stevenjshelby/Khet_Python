import sys, pygame

class Game_Piece(object):
    _cell_location = None
    _base_art = pygame.image.load('art/r_pharaoh.png')
    _art = pygame.image.load('art/r_pharaoh.png')
    _alive = True
    _direction = 1
    _color = None
    
    def __init__(self, loc, img, col):
        self._cell_location = loc
        self._base_art = img
        self._art = img
        self._color = col
    
    def cell_to_pos(self):
        x = 28 + (int(self._cell_location[0]) * 53)
        y = 28 + (int(self._cell_location[1]) * 53)
        return [x, y]
    
    def move(self, x, y):
        if 0 <= x <= 1 and 0 <= y <= 1:
            self._cell_location[0] = x
            self._cell_location[1] = y
    
    def draw(self, the_screen):
        self.adjust_image()
        the_screen.blit(self._art, self.cell_to_pos())
        
    def rotate(self):
        pass
        # Defined in base-classes
        
    def adjust_image(self):
        pass
        # Defined in the classes that ened it
        
    def pass_laser(self):
        pass
        # Defined in sub-classes
        
class Pharaoh(Game_Piece):
    def pass_laser(self, indir):
        #Game over if this piece dies
        self._alive = False
        return 'die'
        
class Pyramid(Game_Piece):
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
            self._art = pygame.transform.rotate(self._base_art, 180)
        elif self._direction == 3:
            self._art = pygame.transform.rotate(self._base_art, 90)
        elif self._direction == 4:
            self._art = pygame.transform.rotate(self._base_art, -90)
        
    def pass_laser(self, in_dir):
        if self._direction == 1:
            if in_dir == 'Right':
                return 'Down'
            elif in_dir == 'Down':
                return 'Right'
            else:
                # This piece will die now
                self._alive = False
                return 'die'
        elif self._direction == 2:
            if in_dir == 'Left':
                return 'Up'
            elif in_dir == 'Up':
                return 'Left'
            else:
                # This piece will die now
                self._alive = False
                return 'die'
        elif self._direction == 3:
            if in_dir == 'Up':
                return 'Right'
            elif in_dir == 'Right':
                return 'Up'
            else:
                # This piece will die now
                self._alive = False
                return 'die'
        elif self._direction == 4:
            if in_dir == 'Down':
                return 'Right'
            elif in_dir == 'Right':
                return 'Down'
            else:
                # This piece will die now
                self._alive = False
                return 'die'
                
class Djed(Game_Piece):
    def __init__(self, loc, img, dir, col):
        self._cell_location = loc
        self._base_art = img
        self._art = img
        self._color = col
        self._direction = dir
        
    def rotate(self):
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
    def move(self, x, y):
        if 0 <= x <= 1 and 0 <= y <= 1:
            self._cell_location[0] = x
            self._cell_location[1] = y
        
        # Need to add code to be able to switch places with pieces
        
class Obelisk(Game_Piece):
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
        self._alive = False
        return 'die'
    
    def adjust_image(self):
        if self._Stacked:
            self._art = self._base_art_stacked
        else:
            self._art = self._base_art
            
    # Need to override the move for Obelisk because it can stack with other obelisks
    def move(self, x, y):
        if 0 <= x <= 1 and 0 <= y <= 1:
            self._cell_location[0] = x
            self._cell_location[1] = y
        
        # Need to add code to be able to stack
		
class Player(object):
    name = ""
    laser_movement = [] #[[0,0],"Down"] where [0,0] is the next cell the laser will hit and "Down" is the direction it enters that cell
	
    def __init__(self, name, laser_movement):
        self.name = name
        self.laser_movement = laser_movement
	
	# Return "Game_Over_Win" if killed other players Pharaoh
	# Return "Game_Over_Lose if killed your own Pharaoh (i.e. you're stupid.)
	# Else, Return ""
    def find_path(self, pieces):
        for piece in pieces:
            
		