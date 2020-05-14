"""Implements player vs bot tic-tac-toe game

The bot is hard-wired
i.e. implemented w/o ML
"""

# !!! debug choose_pos_bot() function
# !!! documentation for choose_pos_bot() function
# !!! bot vs bot

import random
import re
from tictactoe import visualize, victory, get_pos as get_pos_player

FORKS = {
    # indexes for board list:
    # 0 1 2
    # 3 4 5
    # 6 7 8
    # keys - fork combinations (as indexes for board list)
    # values - two ways to complete each fork (as indexes for board list)
    (0, 1, 4): (2, 8),
    (1, 4, 3): (5, 7),
    (4, 3, 0): (6, 8),
    (3, 0, 1): (2, 6),
    (1, 2, 5): (0, 8),
    (2, 5, 4): (6, 8),
    (5, 4, 1): (3, 7),
    (4, 1, 2): (0, 6),
    (3, 4, 7): (1, 5),
    (4, 7, 6): (2, 8),
    (7, 6, 3): (0, 8),
    (6, 3, 4): (0, 2),
    (4, 5, 8): (0, 2),
    (5, 8, 7): (2, 6),
    (8, 7, 4): (0, 6),
    (7, 4, 5): (1, 3),
    (0, 4, 2): (1, 6, 8),
    (2, 4, 8): (0, 5, 6),
    (8, 4, 6): (0, 2, 7),
    (6, 4, 0): (2, 3, 8),
    (0, 2, 8): (1, 4, 5),
    (2, 8, 6): (4, 5, 7),
    (8, 6, 0): (3, 4, 7),
    (6, 0, 2): (1, 3, 4),
}

THREES = {  # indexes combinations for board list corresponding to:
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # horizontal lines
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # vertical lines
    (0, 4, 8), (2, 4, 6)              # diagonals
}


def initialize_players():
    """Allows the player to choose
    to play as x or y.
    Bot will pick another side.
    :return: tuple(str)
    """
    print('Choose your side:\n'
          'Player x (starts the game)\n'
          'Player o (follows player x)\n'
          'Type x or o to choose: ', end='')
    while True:
        human = input()
        if not re.match(r'^[xo]$', human):  # incorrect input
            print('Please type a single character (x or o): ', end='')
            continue
        bot = 'o' if human == 'x' else 'x'
        return human, bot


def choose_pos_bot(board, player):
    opponent = 'o' if player == 'x' else 'x'

    comb_comp = set()
    # mark this(these) cell(s) to complete the line or block opponent's line

    # 1. Win: If the player has two in a row,
    # they can place a third to get three in a row.
    for L in THREES:  # L stands for line
        marks = set(board[index] for index in L)
        if len(marks) == 2 and len(marks - {'x', 'o'}) == 1:
            comp = marks - {'x', 'o'}
            # mark this cell to complete the line or block opponent's line
            if player in marks:   # player can complete the line
                return list(comp).pop()  # (1)
            if opponent in marks:
                comb_comp.update(comp)

    # 2. Block: If the opponent has two in a row,
    # the player must play the third themselves to block the opponent.
    if comb_comp:  # opponent can mark this(these) cell(s) to complete the line
        return list(comb_comp).pop()  # (2)

    comb_comp = set()
    # mark this(these) cell(s) to make the fork(s) or prevent the opponent from creating a fork

    # 3. Fork: Create an opportunity where the player
    # has two ways to win (two non-blocked lines of 2).
    for f in FORKS.keys():
        if len(set(board[index] for index in FORKS[f]) - {'x', 'o'}) != 2:
            break  # fork that is not open is not a fork
        marks = set(board[index] for index in f)
        if len(marks) == 2 and len(marks - {'x', 'o'}) == 1:
            comp = marks - {'x', 'o'}
            # mark this cell to make the fork or prevent the opponent from creating a fork
            if player in marks:  # player can make a fork
                return list(comp).pop()  # (3)
            if opponent in marks:  # (4)
                comb_comp.update(comp)

    # 4. Blocking an opponent's fork:
    # 4.1. If there is only one possible fork for the opponent,
    #      the player should block it.
    if len(comb_comp) == 1:
        return list(comb_comp).pop()  # (4.1)

    # 4.2. Otherwise, the player should create a two in a row
    #      to force the opponent into defending,
    #      as long as it doesn't result in them creating a fork.
    #      For example, if "x" has two opposite corners
    #      and "O" has the center, "o" must not play a corner
    #      in order to win. (Playing a corner in this scenario
    #      creates a fork for "x" to win.)
    if len(comb_comp) > 1:
        comp_2_in_row = {}
        # mark any of these(these) cell(s) to make two in a row
        # this will be a dictionary, unlike comb_comp
        # keys - cells that the opponent will mark to defend themselves
        # values - cells that we can mark to make two in a row
        #          forcing the opponent into defending
        # and vice versa (!)
        for L in THREES:  # L stands for line
            marks = set(board[index] for index in L)
            if len(marks) == 3 and player in marks and opponent not in marks:
                first_cell, second_cell = tuple(marks - {'x', 'o'})
                comp_2_in_row[first_cell] = second_cell
                comp_2_in_row[second_cell] = first_cell
        # now we know all the ways to create two in a row
        # (if there are ways to do it)
        # and we know how the opponent will defend themselves
        # but we should ensure that the opponent won't make a fork
        # while defending.

        for f in FORKS.keys():
            if len(set(board[index] for index in FORKS[f]) - {'x', 'o'}) != 2:
                break  # fork that is not open is not a fork
            marks = set(board[index] for index in f)
            if len(marks) == 2 and opponent in marks and player not in marks:
                comp = list(marks - {'x', 'o'}).pop()
                if comp in comp_2_in_row.keys():
                    del comp_2_in_row[comp]
        if comp_2_in_row:
            return list(i for i in comp_2_in_row.values()).pop()  # # (4.2)

    # 5. Center: A player marks the center.
    # (If it is the first move of the game, playing on a corner
    # gives the second player more opportunities to make a mistake
    # and may therefore be the better choice; however, it makes
    # no difference between perfect players.)
    if 5 in board and player == 'o':
        return 5

    # 6. Opposite corner: If the opponent is in the corner,
    # the player plays the opposite corner.
    corners = {0: 8, 2: 6, 8: 0, 6: 2}  # indexes
    key_list = [i for i in corners.keys()]
    random.shuffle(key_list)
    for corner in key_list:
        if (board[corner] == opponent
                and board[corners[corner]] not in {'x', 'o'}):
            return corners[corner] + 1
            # position number, not index in board list

    # 7. Empty corner: The player plays in a corner square.
    corners = [0, 2, 6, 8]
    random.shuffle(corners)
    for corner in corners:
        if board[corner] not in {'x', 'o'}:
            return board[corner]

    # 8. Empty side: The player plays in a middle square on any of the 4 sides.
    sides = [0, 2, 6, 8]
    random.shuffle(sides)
    for side in sides:
        if board[side] not in {'x', 'o'}:
            return board[side]

    # just in case:
    return list(
        set(board) - {'x', 'o'}
    ).pop(round(random.random() * len(board)))


def _main():
    human, bot = initialize_players()
    board = [i + 1 for i in range(9)]  # position numbers
    if 'x' == human:
        visualize(board)
    for move in range(9):
        player = ('x', 'o')[move % 2]
        if player == human:
            board[get_pos_player(board, player) - 1] = player
        if player == bot:
            pos = choose_pos_bot(board, player)
            board[pos - 1] = player
            print(f'Player {player} (bot): {pos}')
        visualize(board)
        if victory(board, player):
            print(f'Player {player} won!')
            exit()
    print('Draw!')


if __name__ == '__main__':
    _main()
