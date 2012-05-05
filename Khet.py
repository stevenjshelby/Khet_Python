import sys, pygame
from Khet_Classes import Game_Piece, Pharaoh, Djed, Obelisk, Pyramid

# Read the game piece setup from a text file
# The three starting configuration in the game will be provided but
# it is very simple to create your own layout.
def create_pieces(init_layout):
    with open("initial_layouts/piece_config_"+str(init_layout)+".txt") as f:
        temp_piece_list = []
        lines = f.readlines()
        for line in lines:
            if line.startswith("#") or line.strip() == "":
                continue
            split = line.split(", ")
            color = split[0]
            type = split[1]
            x = split[2]
            y = split[3]
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
                                                split[4],
                                                "red"))
                elif type == "Obelisk":
                    if split[4] == 'True':
                        temp_piece_list.append(Pharaoh([x, y], 
                                                       pygame.image.load("art/r_Obelisk.png"), 
                                                       "red"))
                        temp_piece_list.append(Pharaoh([x, y], 
                                                       pygame.image.load("art/r_Obelisk.png"), 
                                                       "red"))
                    else:
                        temp_piece_list.append(Pharaoh([x, y], 
                                                       pygame.image.load("art/r_Obelisk.png"), 
                                                       "red"))
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
                                                split[4],
                                                "gray"))
                elif type == "Obelisk":
                    if split[4] == 'True':
                        temp_piece_list.append(Pharaoh([x, y], 
                                                       pygame.image.load("art/g_Obelisk.png"), 
                                                       "gray"))
                        temp_piece_list.append(Pharaoh([x, y], 
                                                       pygame.image.load("art/g_Obelisk.png"), 
                                                       "gray"))
                    else:
                        temp_piece_list.append(Pharaoh([x, y], 
                                                       pygame.image.load("art/g_Obelisk.png"), 
                                                       "gray"))
    return temp_piece_list
    
# Initialize the PyGame
pygame.init()

# Set the height and width of the screen
size = width, height = 683, 477 #583,477
screen = pygame.display.set_mode(size)

# Load the Game Board image
gameboard = pygame.image.load("art/game_board.png")

# Define colors
black = (0, 0, 0)

# Game Variables
player_turn = 1
initial_game_layout = 1 #3 available options
game_pieces = create_pieces(initial_game_layout)

# -------- Main Program Loop -----------
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        
    
    # Draw everything
    screen.fill(black)
    screen.blit(gameboard, gameboard.get_rect())
    for p in game_pieces:
        p.draw(screen)
    pygame.display.flip()

pygame.quit()