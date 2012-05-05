import sys, pygame
from Khet_Classes import *

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
player_turn = 0 #0 = pregame, 1 = P1 turn, 2 = P2 turn
initial_game_layout = 1 #3 available options
game_pieces = create_pieces(initial_game_layout)
P1 = Player("P1", [[0,0],"Down"])
P2 = Player("P2", [[9,7],"Up"])
p1_win = False
p2_win = False

# -------- Main Program Loop -----------
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
		
        # Players Turns/Menu Stuff
        if player_turn == 0:
            # This is where any menu screen stuff would go
            # Right now it just jumps straight into P1 turn
            player_turn = 1
        elif player_turn == 1:
            # This is where the code for getting the players move will go
            #
            #
            #
            #
            if P1.find_path(game_pieces) == "Game_Over_Win":
				#P1 wins
                pass
            elif P1.find_path(game_pieces) == "Game_Over_Lose":
				#P1 loses
                pass
            else:
                player_turn = 2
        elif player_turn == 2:
            # This is where the code for getting the players move will go
            #
            #
            #
            #
            if P2.find_path(game_pieces) == "Game_Over_Win":
				#P2 wins
                pass
            elif P2.find_path(game_pieces) == "Game_Over_Lose":
				#P2 loses
                pass
            else:
                player_turn = 1
        
        # After one of the players win run this code
        if p1_win:
            pass
        elif p2_win:
            pass
        
    
    # Draw everything
    screen.fill(black)
    screen.blit(gameboard, gameboard.get_rect())
    for p in game_pieces:
        p.draw(screen)
    pygame.display.flip()

pygame.quit()