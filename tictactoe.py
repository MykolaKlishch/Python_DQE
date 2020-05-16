"""Tic-tac-toe game implementation

There are 3 possible game modes:
1) human vs human
2) human vs bot
3) bot vs bot
A bot uses a strategy of a perfect tic-tac-toe player
i.e. it can either win or draw. For proper implementation
of 2nd and 3rd modes, tictactoe_bot module should be imported.
In case of ImportError, the bot is replaced with a substitute
that makes random moves.
"""

import random
import re
import sys

try:
    from tictactoe_bot import bot  # smart bot (original)
except ImportError:
    def bot(board, player):  # stupid random bot (substitute)
        vacant_positions = list(set(board) - {'x', 'o'})
        random.shuffle(vacant_positions)
        player += "I don't care! I just mark a random empty cell!"
        return vacant_positions.pop()

MSG_MODE = """Choose game mode:
1) human vs human
2) human vs bot
3) bot vs bot
Press 1, 2 or 3 to choose: """
MSG_SIDE = """Choose your side:
Player x (starts the game)
Player o (follows player x)
Type x or o to choose: """
MSG_MOVE = "Player {}: "
MSG_ITER = "Number of iterations: "
RE_MODE = r'^[123]$'
RE_SIDE = r'^[xo]$'
RE_MOVE = r'^[1-9]$'
RE_ITER = r'^[1-9]+[0-9]*$'
HINT_MODE = "Please type a single digit from 1 to 3: "
HINT_SIDE = "Please type a single character (x or o): "
HINT_MOVE = "Please type a single digit from 1 to 9: "
HINT_ITER = "Input should be integer. Please try again: "
log = ''


def visualize(board, entities):
    """Prints the current state of game board (for humans).
    :param board: list
    :param entities: dict
    :return: None
    """
    if 'human' not in entities.values():
        return
    for i in range(3):
        if i == 0:
            print('┌───┬───┬───┐')
        print(f'│ {board[3 * i]} │ {board[3 * i + 1]} │ {board[3 * i + 2]} │')
        if i <= 1:
            print('├───┼───┼───┤')
        if i == 2:
            print('└───┴───┴───┘')


def game(entities):
    """Implements game process in all 3 modes
    Returns game result
    :param entities: dict
    :return: str
    """
    board = [i + 1 for i in range(9)]  # position numbers
    visualize(board, entities)
    for move in range(9):
        player = ('x', 'o')[move % 2]
        board[get_pos(board, player, entities) - 1] = player
        visualize(board, entities)
        if victory(board, player):
            return f'Player {player} won!'
    return 'Draw!'


def victory(board, player):
    """Checks if the particular player has won the game.
    Uses tuples with indexes.
    :param board: list
    :param player: str
    :return: boolean
    """
    for L in (  # indexes combinations for board list corresponding to:
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # horizontal lines
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # vertical lines
            (0, 4, 8), (2, 4, 6)  # diagonals
    ):
        if board[L[0]] == board[L[1]] == board[L[2]] == player:
            return True
    return False


def get_pos(board, player, entities):
    """Next move of the player (human or bot).
    If player is human, the function checks
    if the move is possible.
    :param entities: dict
    :param board: list
    :param player: str
    :return: int
    """
    if entities[player] == 'human':
        while True:
            position = int(validate_input(
                MSG_MOVE.format(player), RE_MOVE, HINT_MOVE))
            if position not in board:
                print('Impossible move. Please try again.')
                continue
            break
    else:
        position = bot(board, player)
        if 'human' in entities.values():
            print(f'Player {player} (bot): {position}')
        else:
            global log
            log += f'{player}{position}-'
    return position


def validate_input(inp_msg, template, hint):
    """Takes the input and checks if it is correct.
    :param inp_msg: str
    :param template: str (regex)
    :param hint: str
    :return: str
    """
    while True:
        entry = input(inp_msg)
        if re.match(template, entry):
            return entry
        else:
            inp_msg = hint
            continue


def initialize():
    """Assigns who is human and who is bot.
    :return: dict
    """
    if 'tictactoe_bot' not in sys.modules.keys():
        print('tictactoe_bot module has not been imported.\n'
              '"Human vs bot" and "bot vs bot" modes are still available.\n'
              'However, the smart bot is replaced with a stupid substitute.')
    else:
        print('tictactoe_bot has been imported successfully!')
    game_mode = validate_input(MSG_MODE, RE_MODE, HINT_MODE)
    if game_mode == '3':
        return {'x': 'bot', 'o': 'bot'}
    elif game_mode == '1':
        return {'x': 'human', 'o': 'human'}
    elif game_mode == '2':
        human_ = validate_input(MSG_SIDE, RE_SIDE, HINT_SIDE)
        bot_ = 'o' if human_ == 'x' else 'x'
        return {human_: 'human', bot_: 'bot'}


def print_log():
    """Outputs log of iterated "bot vs bot" games
    :return: None
    """
    print('\n===========All games:===========\n')
    print(log)
    all_combinations = sorted(set(log.strip().split('\n')))
    print('========All combinations:=======\n')
    for record in all_combinations:
        print(record)
    print(f'\n{len(all_combinations)} game combinations '
          + 'out of 48' * ('tictactoe_bot' in sys.modules.keys()))
    # 48 == 3 distinct combinations * 4 rotations * 4 reflections


def _main():
    entities = initialize()
    if 'human' in entities.values():
        print(game(entities))  # print game result
    else:
        iterations = int(validate_input(MSG_ITER, RE_ITER, HINT_ITER))
        global log
        for i in range(iterations):
            log_outcome = game(entities)
            log += log_outcome + '\n'
        print_log()


if __name__ == '__main__':
    _main()
