"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Check if it's a terminal board
    if terminal(board):
        return None
    
    # If the board is in the initial state, then return X
    if board == initial_state():
        return X
    else:
        x, o = 0, 0
        for row in board:
            for cell in row:
                if cell == X:
                    x += 1
                elif cell == O:
                    o += 1
    
    # If x is smaller or equals to o, then it's X turn
    if x <= o:
        return X
    return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()

    # Verify if board is in terminal state
    if terminal(board):
        return None

    # Find empty cells
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    
    return possible_actions
    

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Validate action
    if action not in actions(board):
        raise Exception("action is not valid")
    
    # Make move
    board_copy = deepcopy(board)
    turn = player(board)
    i, j = action[0], action[1]
    board_copy[i][j] = turn
    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Find winner by row
    for row in board:
        if row[0] != EMPTY and (row[0] == row[1] and row[1] == row[2]):
            return row[0]
        
    # Find winner by column
    for i in range(3):
        if board[0][i] != EMPTY and (board[0][i] == board[1][i] and board[1][i] == board[2][i]):
            return board[0][i]
        
    # Find winner by diagonal
    if board[1][1] != EMPTY and ((board[0][0] == board[1][1] and board[1][1] == board[2][2]) or (board[2][0] == board[1][1] and board[1][1] == board[0][2])):
        return board[1][1]

    # No winner so far
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Check for a winner
    if winner(board):
        return True

    # If there's empty cell, then the game still in progress
    for row in board:
        if EMPTY in row:
            return False
    
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # Check for a winner
    if winner(board) != None:
        player_winner = winner(board)
        if player_winner == X:
            # X has won
            return 1
        # O has won
        return -1
    # Tie
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # Function max-value
    def max_value(board):
        v = -math.inf
        if terminal(board):
            return utility(board)
        for action in actions(board):
            v = max(v, min_value(result(board, action)))
        return v
    
    # Function min-value
    def min_value(board):
        v = math.inf
        if terminal(board):
            return utility(board)
        for action in actions(board):
            v = min(v, max_value(result(board, action)))
        return v
        
    # Check for terminal board
    if terminal(board):
        return None

    # Find the actual player best move
    turn = player(board)
    if turn == X:
        value = max_value(board)
        for action in actions(board):
            if value == min_value(result(board, action)):
                return action
    else:
        value = min_value(board)
        for action in actions(board):
            if value == max_value(result(board, action)):
                return action