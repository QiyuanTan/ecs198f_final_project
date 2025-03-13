def get_piece(board, square:str) -> str:
    """
    Args:
        board (list): 2D list representing the chess board
        square (str): algebraic notation of the square (e.g. 'e2')
    Returns:
        str: The piece on the square in the board
    """
    col = ord(square[0]) - ord('a')
    row = 8 - int(square[1])
    return board[row][col]

def is_horizontal_move(start, end):
    raise NotImplementedError

def is_vertical_move(start, end):
    raise  NotImplementedError

def is_diagonal_move(start, end):
    raise NotImplementedError

def empty_between_horizontal(board, start, end):
    raise NotImplementedError

def empty_between_vertical(board, start, end):
    raise NotImplementedError

def empty_between_diagonal(board, start, end):
    raise NotImplementedError
