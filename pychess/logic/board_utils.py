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
    if isinstance(square, tuple):
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

def is_square_attacked(board, square, color):
    """
    Check if a given square is attacked by the opponent's pieces.

    Args:
        board (list): The chessboard.
        square (str): The square to check (e.g., "e1").
        color (str): The color of the player ("w" or "b").

    Returns:
        bool: True if the square is attacked, False otherwise.
    """
    opponent_color = "b" if color == "w" else "w"
    row, col = 8 - int(square[1]), ord(square[0]) - ord('a')

    # Check for pawn attacks
    pawn_row_offset = -1 if opponent_color == "w" else 1
    for pawn_col_offset in [-1, 1]:
        r, c = row + pawn_row_offset, col + pawn_col_offset
        if 0 <= r < 8 and 0 <= c < 8 and board[r][c].lower() == 'p' and board[r][c].islower() == (opponent_color == "b"):
            return True

    # Check for knight attacks
    knight_moves = [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2)]
    for dr, dc in knight_moves:
        r, c = row + dr, col + dc
        if 0 <= r < 8 and 0 <= c < 8 and board[r][c].lower() == 'n' and board[r][c].islower() == (opponent_color == "b"):
            return True

    # Check for rook/queen attacks (horizontal/vertical)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in directions:
        r, c = row, col
        while 0 <= r < 8 and 0 <= c < 8:
            r += dr
            c += dc
            if 0 <= r < 8 and 0 <= c < 8:
                piece = board[r][c]
                if piece != "":
                    if (piece.lower() == 'r' or piece.lower() == 'q') and piece.islower() == (opponent_color == "b"):
                        return True
                    break  # Blocked by another piece

    # Check for bishop/queen attacks (diagonal)
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dr, dc in directions:
        r, c = row, col
        while 0 <= r < 8 and 0 <= c < 8:
            r += dr
            c += dc
            if 0 <= r < 8 and 0 <= c < 8:
                piece = board[r][c]
                if piece != "":
                    if (piece.lower() == 'b' or piece.lower() == 'q') and piece.islower() == (opponent_color == "b"):
                        return True
                    break  # Blocked by another piece

    # Check for king attacks (adjacent squares)
    king_moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dr, dc in king_moves:
        r, c = row + dr, col + dc
        if 0 <= r < 8 and 0 <= c < 8 and board[r][c].lower() == 'k' and board[r][c].islower() == (opponent_color == "b"):
            return True

    return False  # Square is not under attack
