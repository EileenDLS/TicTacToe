import pygame
import sys

# Initialize pygame
pygame.init()

# Setup window
window_size = 300
window = pygame.display.set_mode((window_size, window_size))
pygame.display.set_caption("Tic Tac Toe")

# Setup colors and font
white = (255, 255, 255)
black = (0, 0, 0)
font = pygame.font.Font(None, 36)

# Game variables
grid = [['' for _ in range(3)] for _ in range(3)]  # 3x3 grid to store X and O
current_player = 'X'  # Start with player X
running = True
game_over = False

# Draw grid lines
def draw_grid():
    pygame.draw.line(window, black, (100, 0), (100, 300), 2)
    pygame.draw.line(window, black, (200, 0), (200, 300), 2)
    pygame.draw.line(window, black, (0, 100), (300, 100), 2)
    pygame.draw.line(window, black, (0, 200), (300, 200), 2)

# Draw X and O
def draw_xo():
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == 'X':
                pygame.draw.line(window, black, (j*100 + 20, i*100 + 20), (j*100 + 80, i*100 + 80), 2)
                pygame.draw.line(window, black, (j*100 + 20, i*100 + 80), (j*100 + 80, i*100 + 20), 2)
            elif cell == 'O':
                pygame.draw.circle(window, black, (j*100 + 50, i*100 + 50), 30, 2)

# Check if the game is over
def is_winner(player):
    for row in grid:
        if all([cell == player for cell in row]):
            return True
    for col in range(3):
        if all([grid[row][col] == player for row in range(3)]):
            return True
    if all([grid[i][i] == player for i in range(3)]) or all([grid[i][2-i] == player for i in range(3)]):
        return True
    return False

# Check for a tie
def is_tie():
    return all([cell in ['X', 'O'] for row in grid for cell in row])

# Minimax AI
def minimax(board, depth, is_maximizing):
    if is_winner('X'):
        return -10
    elif is_winner('O'):
        return 10
    elif is_tie():
        return 0

    if is_maximizing:
        max_eval = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'O'
                    eval = minimax(board, depth + 1, False)
                    board[i][j] = ''
                    max_eval = max(eval, max_eval)
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'X'
                    eval = minimax(board, depth + 1, True)
                    board[i][j] = ''
                    min_eval = min(eval, min_eval)
        return min_eval

# Find the best move
def find_best_move():
    best_val = float('-inf')
    move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if grid[i][j] == '':
                grid[i][j] = 'O'
                move_val = minimax(grid, 0, False)
                grid[i][j] = ''
                if move_val > best_val:
                    move = (i, j)
                    best_val = move_val
    return move

# Main loop
while running:
    window.fill(white)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over and current_player == 'X':
            mouseX, mouseY = event.pos
            clicked_row = mouseY // 100
            clicked_col = mouseX // 100

            if grid[clicked_row][clicked_col] == '':
                grid[clicked_row][clicked_col] = current_player
                if is_winner(current_player):
                    print(f'Player {current_player} wins!')
                    game_over = True
                elif is_tie():
                    print('The game is a tie!')
                    game_over = True
                else:
                    current_player = 'O'
                    
    if current_player == 'O' and not game_over:
        best_move = find_best_move()
        grid[best_move[0]][best_move[1]] = 'O'
        if is_winner('O'):
            print('Player O wins!')
            game_over = True
        elif is_tie():
            print('The game is a tie!')
            game_over = True
        else:
            current_player = 'X'
        
    draw_grid()
    draw_xo()
    pygame.display.flip()
    pygame.time.Clock().tick(30)

pygame.quit()
sys.exit()