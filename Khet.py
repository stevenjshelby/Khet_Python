import sys, pygame
from Khet_Classes import *

# Initialize the PyGame
pygame.init()

# Set the height and width of the screen
size = width, height = 683, 477 #583,477
screen = pygame.display.set_mode(size)



# Define colors
black = (0, 0, 0)

# Game Variables
player_turn = 0 #0 = pregame, 1 = P1 turn, 2 = P2 turn
initial_game_layout = 1 #3 available options
game_board = Game_Board(initial_game_layout)
P1 = Player("P1", [[0,0],"Down"])
P2 = Player("P2", [[9,7],"Up"])
p1_win = False
p2_win = False

# -------- Main Program Loop -----------
done = False
while not done:
    global game_board
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
		
        # Get Input for Player Turns & Menu Stuff
        if player_turn == 0:
            # This is where any menu screen stuff would go
            # Right now it just jumps straight into P1 turn
            player_turn = 1
        elif player_turn == 1:
            pass
        elif player_turn == 2:
            pass
    
    # Fire the laser depending on whos turn it is
    if player_turn == 1:
        l_path = P1.find_path(game_board)
        game_board.draw_laser(l_path, screen)
        done =  True ############## this line temporary for debugging ##############
    elif player_turn == 2:
        player_turn = 1
        
    # Draw everything
    screen.fill(black)
    game_board.draw(screen)
    for p in game_board._game_pieces:
        p.draw(screen)
    pygame.display.flip()

pygame.quit()