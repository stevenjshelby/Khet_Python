import sys, pygame
from Khet_Classes import *

# Initialize the PyGame
pygame.init()

# Set the height and width of the screen
size = width, height = 683, 477 #583,477
screen = pygame.display.set_mode(size)

# Define colors and font
black = (0, 0, 0)
white = (255, 255, 255)
font = pygame.font.Font(None, 35)

# Game Variables
player_turn = 1 #0 = pregame, 1 = P1 turn, 2 = P2 turn
initial_game_layout = 1 #3 available options
game_board = Game_Board(initial_game_layout, screen)
P1 = Player("P1", [[0,0],"Down"])
P2 = Player("P2", [[9,7],"Up"])
p1_win = False
p2_win = False

# -------- Main Program Loop -----------
done = False
screen.fill(black)
game_board.draw()
while not done:
    # Getting the input form the user
    surrounding = []
    curr_piece = None
    selected = False
    drawing = False
    moved = False
    while not drawing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                drawing = True
                player_turn = -1
                break
        
            # Get Input for Player Turns & Menu Stuff
            if player_turn == 0:
                # This is where any menu screen stuff would go
                # Right now it just jumps straight into P1 turn
               pass
               
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                m_pos = pygame.mouse.get_pos()
                m_cell = game_board.coords_to_cell(m_pos)
                        
                if selected:
                    for cell in surrounding:
                        if m_cell == cell:
                            game_board.reset_cells(prev_surrounding)
                            curr_piece.move(cell, game_board)
                            moved = True
                            continue
                            
                if game_board.get_cell_status(m_cell) == 'piece':
                    if player_turn == 1 :
                        if game_board.get_piece_by_cell(m_cell)._color == 'red':
                            curr_piece = game_board.get_piece_by_cell(m_cell)
                            surrounding = curr_piece.get_surrounding_cells(m_cell, game_board)
                            game_board.reset_cells(prev_surrounding)
                            game_board.draw_highlight(surrounding, m_cell)
                            selected = True
                    elif player_turn == 2:
                        if game_board.get_piece_by_cell(m_cell)._color == 'gray':
                            curr_piece = game_board.get_piece_by_cell(m_cell)
                            surrounding = curr_piece.get_surrounding_cells(m_cell, game_board)
                            game_board.reset_cells(prev_surrounding)
                            game_board.draw_highlight(surrounding, m_cell)
                            selected = True
            elif event.type == pygame.KEYDOWN and selected and (curr_piece.id == 'pyramid' or curr_piece.id == 'djed'):
                if event.key == 113:
                    curr_piece.rotate('L')
                    game_board.reset_cells(prev_surrounding)
                    moved = True
                elif event.key == 119:
                    curr_piece.rotate('R')
                    game_board.reset_cells(prev_surrounding)
                    moved = True
            
            if moved and not drawing:
                text1 = font.render("Press Enter to Fire Laser", True, white, black)
                text2 = font.render("Player "+str(player_turn), True, white, black)
                text1_size = [text1.get_width(), text1.get_height()]
                text2_size = [text2.get_width(), text2.get_height()]
                
                screen.blit(text1, [size[0]/2 - text1_size[0]/2, size[1]/2 - text1_size[1]/2])
                screen.blit(text2, [size[0]/2 - text2_size[0]/2, size[1]/2 - text1_size[1]*1.5])
                pygame.display.flip()
            
            if moved and event.type == pygame.KEYDOWN and event.key == 13:
                drawing = True
                        
        # Used to clear highlighted cells on new click                
        prev_surrounding = surrounding
    
    game_board.draw()
    
    # The drawing of the lasers
    if player_turn == 1:
        
        l_path = P1.find_path(game_board)
        game_board.draw_laser(l_path)
        pygame.time.wait(1200)
        player_turn = 2
    elif player_turn == 2:
        l_path = P2.find_path(game_board)
        game_board.draw_laser(l_path)
        pygame.time.wait(1200)
        player_turn = 1
    
    game_board.draw()
    
    

pygame.quit()