import sys, pygame
    
pygame.init()

# Set the height and width of the screen
size = width, height = 583, 477
screen = pygame.display.set_mode(size)

# Load the art
gameboard = pygame.image.load("art/game_board.png")
r_pharaoh_piece = pygame.image.load("art/r_Pharaoh.png")
g_pharaoh_piece = pygame.image.load("art/g_Pharaoh.png")

# Used to manage screen update speed
clock=pygame.time.Clock()

class Pharaoh(object):
    def __init__(self, loc, img):
        self._cell_location = loc
        self._art = img
        self._alive = True
    
    def cell_to_pos(self):
        x = 28 + (self._cell_location[0] * 53)
        y = 28 + (self._cell_location[1] * 53)
        return (x, y)

r_phar = Pharaoh([0,0], r_pharaoh_piece)
g_phar = Pharaoh([5,5], g_pharaoh_piece)

# -------- Main Program Loop -----------
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    screen.blit(gameboard, gameboard.get_rect())
    screen.blit(r_phar._art, r_phar.cell_to_pos())
    screen.blit(g_phar._art, g_phar.cell_to_pos())
    pygame.display.flip()

pygame.quit()