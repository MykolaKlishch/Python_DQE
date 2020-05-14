"""Tic-tac-toe game implementation

Only two-player mode is available here
"""

import re


def visualize(board):
    """Prints the current state of game board.
    :return: None
    """
    for i in range(3):
        if i == 0:
            print('┌───┬───┬───┐')
        print(f'│ {board[i * 3]} │ {board[i * 3 + 1]} │ {board[i * 3 + 2]} │')
        if i <= 1:
            print('├───┼───┼───┤')
        if i == 2:
            print('└───┴───┴───┘')


def get_pos(board, player):
    """Processes input from a player.
    Checks if input is valid and the move is possible.
    If so, returns the position to be marked.
    :param board: list
    :param player: str
    :return: int
    """
    while True:
        position = input(f'Player {player}: ')
        if not re.match(r'^[1-9]$', position):  # incorrect input
            print('Input should be a single digit '
                  'from 1 to 9. Please try again.')
            continue
        position = int(position)
        if position not in board:  # selected cell is not empty
            print('Impossible move. Please try again.')
            continue
        return position


def victory(board, player):
    """Checks if the particular player has won the game.
    :param board: list
    :param player: str
        'x' or 'o'
    :return: boolean
    """
    for L in (  # indexes combinations for board list corresponding to:
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # horizontal lines
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # vertical lines
        (0, 4, 8), (2, 4, 6)              # diagonals
    ):
        if board[L[0]] == board[L[1]] == board[L[2]] == player:
            return True
    return False


def game():
    board = [i + 1 for i in range(9)]
    visualize(board)
    for move in range(9):
        player = ('x', 'o')[move % 2]
        board[get_pos(board, player) - 1] = player
        visualize(board)
        if victory(board, player):
            print(f'Player {player} won!')
            exit()
    print('Draw!')


if __name__ == '__main__':
    game()
