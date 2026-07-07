import numpy as np
import pygame
import sys

ROWS, COLS = 6, 7
SQUARESIZE = 100
width, height = COLS * SQUARESIZE, (ROWS + 1) * SQUARESIZE
BLUE, BLACK, RED, YELLOW, WHITE, GRAY = (0, 0, 255), (0, 0, 0), (255, 0, 0), (255, 255, 0), (255, 255, 255), (200, 200, 200)

def check_win(board, piece):
    for c in range(COLS - 3):
        for r in range(ROWS):
            if all(board[r][c + i] == piece for i in range(4)):
                return [(r, c + i) for i in range(4)]
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == piece for i in range(4)):
                return [(r + i, c) for i in range(4)]
    for c in range(COLS - 3):
        for r in range(ROWS - 3):
            if all(board[r + i][c + i] == piece for i in range(4)):
                return [(r + i, c + i) for i in range(4)]
    for c in range(COLS - 3):
        for r in range(3, ROWS):
            if all(board[r - i][c + i] == piece for i in range(4)):
                return [(r - i, c + i) for i in range(4)]
    return None

def get_valid_moves(board):
    return [c for c in range(COLS) if board[ROWS - 1][c] == 0]

def get_next_open_row(board, col):
    for r in range(ROWS):
        if board[r][col] == 0: return r
    return None

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def bfs_ai(board):
    moves = get_valid_moves(board)
    for col in moves:
        temp = board.copy()
        drop_piece(temp, get_next_open_row(temp, col), col, 1)
        if check_win(temp, 1): return col
    return moves[0] if moves else 0

def dfs_ai(board):
    moves = get_valid_moves(board)
    for col in reversed(moves):
        temp = board.copy()
        drop_piece( board.copy(), get_next_open_row(temp, col), col, 1)
        if check_win(temp, 1): return col
    return moves[-1] if moves else 0

def iddfs_ai(board):
    moves = get_valid_moves(board)
    for depth in range(1, 4):
        for col in moves:
            temp = board.copy()
            drop_piece(temp, get_next_open_row(temp, col), col, 1)
            if check_win(temp, 1): return col
    return moves[len(moves)//2] if moves else 0

def draw_board(screen, board, win_path=None):
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), 45)
    for c in range(COLS):
        for r in range(ROWS):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), 45)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), 45)
    if win_path:
        for (r, c) in win_path:
            pygame.draw.circle(screen, WHITE, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), 48, 5)
    pygame.display.update()

def start_menu(screen):
    pygame.font.init()
    font = pygame.font.SysFont("Arial", 40)
    buttons = {'1': pygame.Rect(250, 200, 200, 60), '2': pygame.Rect(250, 300, 200, 60), '3': pygame.Rect(250, 400, 200, 60)}
    while True:
        screen.fill(BLACK)
        screen.blit(font.render("Select AI Algorithm:", True, WHITE), (180, 100))
        for key, rect in buttons.items(): pygame.draw.rect(screen, GRAY, rect)
        screen.blit(font.render("BFS", True, BLACK), (315, 210))
        screen.blit(font.render("DFS", True, BLACK), (315, 310))
        screen.blit(font.render("IDDFS", True, BLACK), (300, 410))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for key, rect in buttons.items():
                    if rect.collidepoint(event.pos): return key

pygame.init()
screen = pygame.display.set_mode((width, height))
algo_choice = start_menu(screen)

if algo_choice == '1': print("AI using BFS: Checking all immediate moves\n")
elif algo_choice == '2': print("AI using DFS: Deep exploration of branches\n")
else: print("AI using IDDFS: Searching with increasing depth limits\n")

board = np.zeros((ROWS, COLS))
game_over, turn = False, 0

while not game_over:
    draw_board(screen, board)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and turn == 0:
            col = event.pos[0] // SQUARESIZE
            if col in get_valid_moves(board):
                drop_piece(board, get_next_open_row(board, col), col, 2)
                win_path = check_win(board, 2)
                if win_path:
                    draw_board(screen, board, win_path)
                    print("USER WINS!"); game_over = True
                turn = 1

    if turn == 1 and not game_over:
        pygame.time.wait(500)
        print(f"AI Exploring columns: {get_valid_moves(board)}")
        if algo_choice == '1': col = bfs_ai(board)
        elif algo_choice == '2': col = dfs_ai(board)
        else: col = iddfs_ai(board)
        drop_piece(board, get_next_open_row(board, col), col, 1)
        win_path = check_win(board, 1)
        if win_path:
            draw_board(screen, board, win_path)
            print("AI WINS!"); game_over = True
        turn = 0

pygame.time.wait(5000)