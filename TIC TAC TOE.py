import tkinter as tk
import math

# Global variables
player = "X"
ai = "O"
board = [[' ' for _ in range(3)] for _ in range(3)]
buttons = []

# Function to check for a winner
def check_winner(board):
    # Check rows, columns, and diagonals for a winner
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != ' ':
            return row[0]

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != ' ':
            return board[0][col]

    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != ' ':
        return board[0][0]
    
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != ' ':
        return board[0][2]
    
    return None

# Function to check if the board is full
def is_board_full(board):
    for row in board:
        if ' ' in row:
            return False
    return True

# Minimax algorithm
def minimax(board, depth, is_maximizing):
    winner = check_winner(board)
    if winner == ai:
        return 1
    elif winner == player:
        return -1
    elif is_board_full(board):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = ai
                    score = minimax(board, depth + 1, False)
                    board[i][j] = ' '
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = player
                    score = minimax(board, depth + 1, True)
                    board[i][j] = ' '
                    best_score = min(score, best_score)
        return best_score

# Function to find the best move for AI
def best_move():
    best_score = -math.inf
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = ai
                score = minimax(board, 0, False)
                board[i][j] = ' '
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

# Function to handle a player move
def player_move(row, col):
    if board[row][col] == ' ':
        board[row][col] = player
        buttons[row][col].config(text=player, state=tk.DISABLED, disabledforeground="blue")
        winner = check_winner(board)
        if winner or is_board_full(board):
            end_game(winner)
            return
        ai_move()

# Function to let the AI make its move
def ai_move():
    move = best_move()
    if move:
        board[move[0]][move[1]] = ai
        buttons[move[0]][move[1]].config(text=ai, state=tk.DISABLED, disabledforeground="red")
        winner = check_winner(board)
        if winner or is_board_full(board):
            end_game(winner)

# Function to end the game and display the winner
def end_game(winner):
    if winner == player:
        status_label.config(text="Congratulations, you win!", fg="green")
    elif winner == ai:
        status_label.config(text="AI wins. Better luck next time!", fg="red")
    else:
        status_label.config(text="It's a tie!", fg="#53331F")

    for row in buttons:
        for button in row:
            button.config(state=tk.DISABLED)

# Function to reset the game
def reset_game():
    global board
    board = [[' ' for _ in range(3)] for _ in range(3)]
    for row in buttons:
        for button in row:
            button.config(text=" ", state=tk.NORMAL)
    status_label.config(text="Your turn!", fg="black")

# Set up the main game window
window = tk.Tk()
window.title("Tic Tac Toe with AI")
window.geometry("400x450")
window.configure(bg="#CD8C8C")

# GUI Layout
frame = tk.Frame(window)
frame.pack()

for i in range(3):
    row_buttons = []
    for j in range(3):
        button = tk.Button(frame, text=" ", font=('Times', 24), width=5, height=2,
                           command=lambda i=i, j=j: player_move(i, j))
        button.grid(row=i, column=j, padx=5, pady=5)
        row_buttons.append(button)
    buttons.append(row_buttons)

status_label = tk.Label(window, text="Your turn!", font=('Times', 16), bg="lightgray")
status_label.pack(pady=10)

reset_button = tk.Button(window, text="Reset Game", command=reset_game, font=('Times', 14))
reset_button.pack(pady=10)

# Start the GUI loop
window.mainloop()
