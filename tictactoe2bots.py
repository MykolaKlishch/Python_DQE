"""Simulates bot vs bot tic-tac-toe game

test if the bots are perfect tic-tac-toe players
"""

from tictactoe import victory
from tictactoe_bot import choose_pos_bot


def bot_vs_bot():
    global log
    board = [i + 1 for i in range(9)]  # position numbers
    for move in range(9):
        player = ('x', 'o')[move % 2]
        pos = choose_pos_bot(board, player)
        board[pos - 1] = player
        log += f'{player}{pos}-'
        if victory(board, player):
            log += f'{player}_won!\n'
            break
    else:
        log += 'draw!\n'


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
    print(log)
    print('--------------------------------')
    for game in sorted(set(log.split('\n'))):
        print(game)
    print(len(set(log.strip().split('\n'))), 'combinations out of 48')
    # 48 == 3 distinct combinations * 4 rotations * 4 reflections


log = ''

if __name__ == '__main__':
    _main()

