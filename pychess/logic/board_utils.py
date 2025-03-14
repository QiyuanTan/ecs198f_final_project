def get_piece(board, square:str) -> str:
    """
    Args:
        board (list): 2D list representing the chess board
        square (str): algebraic notation of the square (e.g. 'e2')
    Returns:
        str: The piece on the square in the board
    """
    row, col = str2index(square)
    return board[row][col]

def str2index(square) -> tuple:
    """
    Function to convert algebraic notation to board index
    Args:
        square: string notation of the square (e.g. 'e2')

    Returns: a tuple of the row and column index

    """
    if square is tuple:
        return square

    try:
        col = ord(square[0]) - ord('a')
        row = 8 - int(square[1])
        return row, col
    except (TypeError, IndexError):
        raise TypeError("Invalid square format. Must be a string in algebraic notation (e.g. 'e2')")

def move_piece(board, start, end):
    """
    Function to move a piece from the start square to the end square
    Args:
        board: 2D list representing the chess board
        start: string or tuple of the starting square.
        end: string or tuple of the ending square.
    Format of input:
        start: 'e2' or (6, 4)
        end: 'e4' or (4, 4)
    Returns:

    """
    start_row, start_col = str2index(start)
    end_row, end_col = str2index(end)
    board[end_row][end_col] = board[start_row][start_col]
    board[start_row][start_col] = ''

def is_horizontal_move(start, end):
    """
    Function to determine if the move is horizontal
    Args:
        start: string or tuple of the starting square.
        end: string or tuple of the ending square.
    Format of input:
        start: 'e2' or (6, 4)
        end: 'e4' or (4, 4)
    Returns:

    """
    start_row, start_col = str2index(start)
    end_row, end_col = str2index(end)
    return start_row == end_row and start_col != end_col

def is_vertical_move(start, end):
    """
    Function to determine if the move is vertical
    Args:
        start: string or tuple of the starting square.
        end: string or tuple of the ending square.
    Format of input:
        start: 'e2' or (6, 4)
        end: 'e4' or (4, 4)
    Returns:

    """
    start_row, start_col = str2index(start)
    end_row, end_col = str2index(end)
    return start_row != end_row and start_col == end_col

def is_diagonal_move(start, end):
    """
    Function to determine if the move is diagonal
    Args:
        start: string or tuple of the starting square.
        end: string or tuple of the ending square.
    Format of input:
        start: 'e2' or (6, 4)
        end: 'e4' or (4, 4)
    Returns:

    """
    start_row, start_col = str2index(start)
    end_row, end_col = str2index(end)
    return abs(start_row - end_row) == abs(start_col - end_col)

def empty_between_horizontal(board, start, end):
    """
    Function to determine if there are any pieces between the start and end square horizontally,
    including the ending square
    Args:
        board: 2D list representing the chess board
        start: string or tuple of the starting square.
        end: string or tuple of the ending square.
    Format of input:
        start: 'e2' or (6, 4)
        end: 'e4' or (4, 4)
    Returns:
        bool: True if there are no pieces between the start and end square.
        False otherwise.
    """
    start_row, start_col = str2index(start)
    end_row, end_col = str2index(end)

    if not is_horizontal_move(start, end):
        raise ValueError("Start and end square must be on the same row for horizontal move")

    delta = 1 if start_col < end_col else -1
    for col in range(start_col + delta, end_col, delta):
        if board[start_row][col] != '':
            return False

    return True

def empty_between_vertical(board, start, end):
    """
    Function to determine if there are any pieces between the start and end square vertically,
    including the ending square
    Args:
        board: 2D list representing the chess board
        start: string or tuple of the starting square.
        end: string or tuple of the ending square.
    Format of input:
        start: 'e2' or (6, 4)
        end: 'e4' or (4, 4)
    Returns:
        bool: True if there are no pieces between the start and end square.
        False otherwise.
    """
    start_row, start_col = str2index(start)
    end_row, end_col = str2index(end)

    if not is_vertical_move(start, end):
        raise ValueError("Start and end square must be on the same column for vertical move")

    delta = 1 if start_row < end_row else -1
    for row in range(start_row + delta, end_row, delta):
        if board[row][start_col] != '':
            return False

    return True


def empty_between_diagonal(board, start, end):
    """
    Function to determine if there are any pieces between the start and end square diagonally,
    including the ending square
    Args:
        board: 2D list representing the chess board
        start: string or tuple of the starting square.
        end: string or tuple of the ending square.
    Format of input:
        start: 'e2' or (6, 4)
        end: 'e4' or (4, 4)
    Returns:
        bool: True if there are no pieces between the start and end square.
        False otherwise.
    """
    start_row, start_col = str2index(start)
    end_row, end_col = str2index(end)

    if not is_diagonal_move(start, end):
        raise ValueError("Start and end square must be on the same diagonal for diagonal move")

    row_delta = 1 if start_row < end_row else -1
    col_delta = 1 if start_col < end_col else -1

    row, col = start_row + row_delta, start_col + col_delta
    while row <= end_row and row_delta == 1 or row >= end_row and row_delta == -1:
        if board[row][col] != '':
            return False
        row += row_delta
        col += col_delta

    return True