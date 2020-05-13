"""Tic-tac-toe game simulator"""


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
        from 1 to 9
    :return: boolean
    """
    return isinstance(board[position - 1], int)


def victory(board):
    """Checks if any player has won the game
    :param board: list
    :return: describe it !!!
    """
    pass


def _main():
    board = [i + 1 for i in range(9)]
    visualize(board)
    print(move_is_legit(board, 1))


if __name__ == "__main__":
    _main()
