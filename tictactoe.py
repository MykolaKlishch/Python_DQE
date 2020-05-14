"""Tic-tac-toe game simulator"""


VICTORY_COMBINATIONS = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # horizontal lines
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # vertical lines
    (0, 4, 8), (2, 4, 6)              # diagonals
)

PLAYERS = ('o', 'x')                  # player marks


def visualize(board):
    """Prints the current state of game board
    :return: None
    """
    for i in range(3):
        if i == 0:
            print('┌───┬───┬───┐')
        print(f'│ {board[i*3]} │ {board[i*3 + 1]} │ {board[i*3 + 2]} │')
        if i <= 1:
            print('├───┼───┼───┤')
        if i == 2:
            print('└───┴───┴───┘')


def move_is_legit(board, position):
    """Checks if the move is possible
    :param board: list
    :param position: int
        from 1 to 9 only!
        if the same integer value is present in board list
        it means that this square is still empty
    :return: boolean
    """
    return position in board


def victory(board, player):
    """Checks if the particular player has won the game
    :param board: list
    :param player: str
        'x' or 'o'
    :return: boolean
    """
    for L in VICTORY_COMBINATIONS:
        if board[L[0]] == board[L[1]] == board[L[2]] == player:
            return True
    return False


def _main():
    board = [i + 1 for i in range(9)]
    visualize(board)
    moves_left = 9
    while moves_left > 0:
        player = PLAYERS[moves_left % 2]
        try:
            position = int(input(f'Player {player}: '))
            if not 1 <= position <= 9:
                raise ValueError
        except ValueError:
            print('Input should be a single digit '
                  'from 1 to 9. Please try again.')
            continue
        else:
            if move_is_legit(board, position):
                board[position-1] = player
                visualize(board)
                moves_left -= 1
            else:
                print('Impossible move. Please try again.')
                continue
            if victory(board, player):
                print(f'Player {player} won!')
                break
            else:
                if moves_left == 0:
                    print('Draw!')


if __name__ == "__main__":
    _main()
