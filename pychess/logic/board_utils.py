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

def index2str(index) -> str:
    """
    Function to convert board index to algebraic notation
    Args:
        index: tuple of the row and column index

    Returns: a string notation of the square (e.g. 'e2')

    """
    if isinstance(index, str):
        return index

    try:
        col = chr(index[1] + ord('a'))
        row = str(8 - index[0])
        return col + row
    except (TypeError, IndexError):
        raise TypeError("Invalid index format. Must be a tuple of the row and column index")

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
        square (str) or (tuple): The square to check (e.g., "e1", (1, 1)).
        color (str): The color of the player ("w" or "b").

    Returns:
        bool: True if the square is attacked, False otherwise.
    """
    opponent_color = "b" if color == "w" else "w"
    row, col = str2index(square)

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

def invalid_move_for_piece(board, move, side) -> bool:
    """
        Function to check if move is valid for white
        Args:
            board:
            side:
            move: the move that the player is making
        Returns:
            True if move is invalid, else False
    """
    piece = get_piece(board, move[:2])
    # set side
    to_self = lambda p: p.upper() if side == 'w' else p.lower()
    delta = -1 if side == 'w' else 1
    pawn_base = 6 if side == 'w' else 1

    # check if pieces blocking it, if not return false
    # check if causing a check, if so then return false TBD ADD SOON
    # else return true
    # ex move: e2e3
    is_horizontal = is_horizontal_move(move[:2], move[2:])
    is_diagonal = is_diagonal_move(move[:2], move[2:])
    is_vertical = is_vertical_move(move[:2], move[2:])
    srow, scol = str2index(move[:2])
    erow, ecol = str2index(move[2:])

    if piece == to_self("P"):  # if the piece is a pawn

        if not is_vertical:
            return True

        if is_diagonal:
            if erow == srow + delta and get_piece(board, move[:2]) != '':
                return False
            else:
                return True

        if srow == pawn_base:  # this means its at the starting row i.e "e2,a2"
            if erow != srow + delta and erow != srow + 2 * delta:  # if ending square is not 1 or 2 spaces above start
                return True
            else:
                if empty_between_vertical(board, move[:2], move[2:]):
                    # make sure nothing is in front of pawn
                    return False
                else:
                    return True
        else:
            if erow != srow + delta:  # if ending square is not 1 above
                return True
            else:
                if empty_between_vertical(board, move[:2], move[2:]):
                    # make sure nothing is in front of pawn
                    return False
                else:
                    return True
    elif piece == to_self("R"):
        if is_diagonal:
            return True
        if is_horizontal:
            if empty_between_horizontal(board, move[:2], move[2:]):
                return False
            else:
                return True
        if is_vertical:
            if empty_between_vertical(board, move[:2], move[2:]):
                return False
            else:
                return True
    elif piece == to_self("B"):
        if not is_diagonal:
            return True

        if empty_between_diagonal(board, move[:2], move[2:]):
            return False
        else:
            return True
    elif piece == to_self("N"):
        if is_vertical or is_horizontal or is_diagonal:
            return True

        if erow == srow + 2 and ecol == scol + 1:  # up two, one right
            return False

        if erow == srow + 2 and ecol == scol - 1:  # up two, one left
            return False

        if erow == srow - 2 and ecol == scol - 1:  # down two, one left
            return False

        if erow == srow - 2 and ecol == scol + 1:  # up two, one right
            return False

        if erow == srow + 1 and ecol == scol + 2:  # up one two right
            return False

        if erow == srow + 1 and ecol == scol - 2:  # up one two left
            return False

        if erow == srow - 1 and ecol == scol + 2:  # down one two right
            return False

        if erow == srow - 1 and ecol == scol - 2:  # down one two left
            return False

        return True
    elif piece == to_self("Q"):
        if not (is_horizontal and is_diagonal and is_vertical):
            return True
        if is_horizontal:
            if empty_between_horizontal(board, move[:2], move[2:]):
                return False

        if is_vertical:
            if empty_between_vertical(board, move[:2], move[2:]):
                return False

        if is_diagonal:
            if empty_between_diagonal(board, move[:2], move[2:]):
                return False

        return True
    else:
        if not (is_horizontal and is_diagonal and is_vertical):
            return True

        if is_vertical:

            if erow != srow + 1 or erow != srow - 1:  # if ending square is not 1 vertical
                return True
            else:
                if empty_between_vertical(board, move[:2], move[2:]):
                    # make sure nothing is in front of pawn
                    return False
                else:
                    return True

        if is_horizontal:

            if ecol != scol + 1 or ecol != scol - 1:  # if ending square is not 1 horizontal
                return True
            else:
                if empty_between_horizontal(board, move[:2], move[2:]):
                    # make sure nothing is in front of pawn
                    return False
                else:
                    return True
        if is_diagonal:

            if ecol == scol + 1 and erow != erow - 1:  # bottom right
                if empty_between_diagonal(board, move[:2], move[2:]):
                    # make sure nothing is in front of pawn
                    return False

            if ecol == scol - 1 and erow != erow - 1:  # bottom left
                if empty_between_diagonal(board, move[:2], move[2:]):
                    # make sure nothing is in front of pawn
                    return False

            if ecol == scol + 1 and erow != erow - 1:  # top left
                if empty_between_diagonal(board, move[:2], move[2:]):
                    # make sure nothing is in front of pawn
                    return False
            if ecol == scol + 1 and erow != erow + 1:  # top right
                if empty_between_diagonal(board, move[:2], move[2:]):
                    # make sure nothing is in front of pawn
                    return False

            return True

    raise ValueError("Move not handled")

def pawn_moves(board, i, j, side) -> list[tuple[int, int]]:
    """
    Gets the possible moves for a pawn
    Args:
        board:
        i:
        j:
        side:

    Returns:
    """
    moves = []
    direction = -1 if side == 'w' else 1
    # move one square forward
    if board[i + direction][j] == '':
        moves.append((i + direction, j))
        # move two squares forward
        if (i == 1 and side == 'b') or (i == 6 and side == 'w'):
            if board[i + 2 * direction][j] == '':
                moves.append((i + 2 * direction, j))
    # capture diagonally
    if j > 0:
        moves.append((i + direction, j - 1))
    if j < 7:
        moves.append((i + direction, j + 1))
    return moves

def rook_moves(board, i, j, side) -> list[tuple[int, int]]:
    """
    Gets the possible moves for a rook
    Args:
        board:
        i:
        j:
        side:

    Returns:
    """
    moves = []
    for direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        for k in range(1, 8):
            new_i = i + k * direction[0]
            new_j = j + k * direction[1]
            if not (0 <= new_i < 8 and 0 <= new_j < 8):
                break
            if board[new_i][new_j] == '':
                moves.append((new_i, new_j))
            elif board[new_i][new_j].isupper() != side.isupper():
                moves.append((new_i, new_j))
                break
            else:
                break
    return moves

def knight_moves(board, i, j, side) -> list[tuple[int, int]]:
    """
    Gets the possible moves for a knight
    Args:
        board:
        i:
        j:
        side:

    Returns:
    """
    moves = []
    for direction in [(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]:
        new_i = i + direction[0]
        new_j = j + direction[1]
        if 0 <= new_i < 8 and 0 <= new_j < 8:
            if board[new_i][new_j] == '' or board[new_i][new_j].isupper() != side.isupper():
                moves.append((new_i, new_j))
    return moves

def bishop_moves(board, i, j, side) -> list[tuple[int, int]]:
    """
    Gets the possible moves for a bishop
    Args:
        board:
        i:
        j:
        side:

    Returns:
    """
    moves = []
    for direction in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
        for k in range(1, 8):
            new_i = i + k * direction[0]
            new_j = j + k * direction[1]
            if not (0 <= new_i < 8 and 0 <= new_j < 8):
                break
            if board[new_i][new_j] == '':
                moves.append((new_i, new_j))
            elif board[new_i][new_j].isupper() != side.isupper():
                moves.append((new_i, new_j))
                break
            else:
                break
    return moves

def queen_moves(board, i, j, side) -> list[tuple[int, int]]:
    """
    Gets the possible moves for a queen
    Args:
        board:
        i:
        j:
        side:

    Returns:
    """
    moves = rook_moves(board, i, j, side) + bishop_moves(board, i, j, side)
    return moves

def king_moves(board, i, j, side) -> list[tuple[int, int]]:
    """
    Gets the possible moves for a king
    Args:
        board:
        i:
        j:
        side:

    Returns:
    """
    moves = []
    for direction in [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]:
        new_i = i + direction[0]
        new_j = j + direction[1]
        if 0 <= new_i < 8 and 0 <= new_j < 8:
            if board[new_i][new_j] == '' or board[new_i][new_j].isupper() != side.isupper():
                moves.append((new_i, new_j))
    return moves