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
            if P1.find_path(game_board._game_pieces) == "Game_Over_Win":
				#P1 wins
                pass
            elif P1.find_path(game_board._game_pieces) == "Game_Over_Lose":
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
            if P2.find_path(game_board._game_pieces) == "Game_Over_Win":
				#P2 wins
                pass
            elif P2.find_path(game_board._game_pieces) == "Game_Over_Lose":
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
    game_board.draw(screen)
    for p in game_board._game_pieces:
        p.draw(screen)
    pygame.display.flip()

pygame.quit()