"""A bot that implements a strategy
of a perfect tic-tac-toe player
i.e. it can either win or draw.
The bot is implemented as function bot().
The bot is hard-wired, i.e. implemented w/o ML.
"""

import random

FORKS = {
    # indexes for board list:
    # 0 1 2
    # 3 4 5
    # 6 7 8
    # keys - fork combinations (as indexes for board list)
    # values - ways to extend each fork into three in a row
    (0, 1, 3): (2, 6),
    (0, 1, 4): (2, 7, 8),
    (0, 2, 4): (1, 6, 8),
    (0, 2, 6): (1, 3, 4),
    (0, 2, 8): (1, 4, 5),
    (0, 3, 4): (5, 6, 8),
    (0, 4, 6): (2, 3, 8),
    (0, 6, 8): (3, 4, 7),
    (1, 2, 4): (0, 6, 7),
    (1, 2, 5): (0, 8),
    (1, 3, 4): (5, 7),
    (1, 4, 5): (3, 7),
    (2, 4, 5): (3, 6, 8),
    (2, 4, 8): (0, 5, 6),
    (2, 6, 8): (4, 5, 7),
    (3, 4, 6): (0, 2, 5),
    (3, 4, 7): (1, 5),
    (3, 6, 7): (0, 8),
    (4, 5, 7): (1, 3),
    (4, 5, 8): (0, 2, 3),
    (4, 6, 7): (1, 2, 8),
    (4, 6, 8): (0, 2, 7),
    (4, 7, 8): (0, 1, 6),
    (5, 7, 8): (2, 6)
}

LINES = {  # indexes combinations for three in a row:
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # horizontal lines
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # vertical lines
    (0, 4, 8), (2, 4, 6)              # diagonals
}

CORNERS = {  # indexes combinations for opposite corners
    (0, 8), (2, 6)
}


def bot(board, player):
    """Implements a strategy of a perfect tic-tac-toe player.

    The strategy is implemented as a sequence of cases
    that should be checked one after another
    until the right case is found:

    #1. Win: If the player has two in a row,
    they can place a third to get three in a row.

    #2. Block: If the opponent has two in a row,
    the player must play the third themselves to block the opponent.

    #3. Fork: Create an opportunity where the player
    has two ways to win (two non-blocked lines of 2).

    #4. Blocking an opponent's fork:
    4.1. If there is only one possible fork for the opponent,
         the player should block it.
    4.2. Otherwise, the player should create a two in a row
         to force the opponent into defending,
         as long as it doesn't result in them creating a fork.
         For example, if "x" has two opposite corners
         and "O" has the center, "o" must not play a corner
         in order to win. (Playing a corner in this scenario
         creates a fork for "x" to win.)

    #5. Center: A player marks the center.
    (If it is the first move of the game, playing on a corner
    gives the second player more opportunities to make a mistake
    and may therefore be the better choice; however, it makes
    no difference between perfect players.)

    #6. Opposite corner: If the opponent is in the corner,
    the player plays the opposite corner.

    #7. Empty corner: The player plays in a corner square.

    #8. Empty side: The player plays in a middle square
    on any of the 4 sides.

    strategy description from:
    en.wikipedia.org/wiki/Tic-tac-toe (15.05.2020)

    :param board: list
    :param player: str
    :return: int
    """
    opponent = 'o' if player == 'x' else 'x'
    true_forks = _select_true_forks(board, FORKS.keys())
    params = {  # case: parameters set for _complete_combinations()
        '1': (board, LINES, player),
        '2': (board, LINES, opponent),
        '3': (board, true_forks, player),
        '4': (board, true_forks, opponent),
        '6': (board, CORNERS, opponent)
    }
    for case in '12345678':
        if case in params.keys():
            comp_comb = _complete_combinations(*params[case])
            if case == '4' and len(comp_comb) > 1:  # case 4.2
                comp_comb = _complete_combinations(
                    board, LINES, player, s=3, warning=comp_comb)
            if comp_comb:
                return list(comp_comb).pop(
                    round(random.random() * len(comp_comb)) - 1)
        elif case == '5':
            if 5 in board and (player == 'o' or random.random() <= 0.2):
                return 5  # player x will start from 5 in 20% of cases
        elif case in '78':
            corners, sides = [1, 3, 7, 9], [2, 4, 6, 8]
            random.shuffle(corners)
            random.shuffle(sides)
            for pos in corners + sides + [5]:
                if pos in board:
                    return pos


def _select_true_forks(board, forks):
    """A fork that is not open is not a fork.
    :param board: list
    :param forks: iterable of tuples
    :return: set
    """
    true_forks = set()
    for fork in forks:
        if len(set(board[index] for index in FORKS[fork])
               - {'x', 'o'}) > 1:
            true_forks.add(fork)
    return true_forks


def _complete_combinations(board, combinations,
                           player, s=2, warning=None):
    """Returns a set of cells that can be marked
    to complete the combinations (lines or forks).
    Calling this function with player=opponent
    returns the combinations that opponent can complete
    in the next turn - so these combinations can be blocked.

    marks - a set of symbols (players' marks or digits)
    in a particular combination on the board (line, fork, etc.)
    s - a critical length of marks set.
    Example:
    check if the player can complete the line.
    1) len(marks) == s == 2
    2) player's mark 'x' is present in the set
    3) opponent's mark 'o' is absent in the set
    Each line has 3 cells. From (1, 2, 3) it follows that:
       * two of the cells are already marked 'x';
       * the third one is still vacant.
    This means that marks = {'x', some_int}
    and some_int is the exact position that should
    be marked to complete the line.

    warning - don't provoke the opponent
    into marking these positions.

    :param board: list
    :param combinations: set of tuples
    :param player: string
    :param s: int
    :param warning: set
    :return: set
    """
    opponent = 'o' if player == 'x' else 'x'
    comp_comb = set()
    for comb in combinations:
        marks = set(board[index] for index in comb)
        if len(marks) == s and player in marks and opponent not in marks:
            if s == 3 and warning:
                marks = _handle_warning(marks, warning)
            comp_comb.update(marks - {'x', 'o'})
    return comp_comb


def _handle_warning(marks, warning):
    """Excludes those positions from marks
    which can provoke the opponent to make a fork.
    :param marks: set
    :param warning: set
        don't provoke the opponent
        into marking these positions.
    :return: set
    """
    exclude = set()
    for mark in marks:
        if mark in warning:
            exclude.update(marks - {mark})
    return marks - exclude
