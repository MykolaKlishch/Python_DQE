"""Simulates bot vs bot tic-tac-toe game

test if the bots are perfect tic-tac-toe players
"""

from tictactoe import victory
from tictactoe_bot import choose_pos_bot


def bot_vs_bot():
    board = [i + 1 for i in range(9)]  # position numbers
    for move in range(9):
        player = ('x', 'o')[move % 2]
        pos = choose_pos_bot(board, player)
        board[pos - 1] = player
        print(f'{player}{pos}-', end='')
        if victory(board, player):
            print(f'{player}_won!')
            break
    else:
        print('draw!')


def _main():
    while True:
        try:
            iterations = int(input('Number of iterations: '))
        except ValueError:
            print('Input should  integer')
        else:
            break
    for i in range(iterations):
        bot_vs_bot()


if __name__ == '__main__':
    _main()

