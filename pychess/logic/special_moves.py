from .board_utils import *

class MoveHandler:
    def applies(self, board, move):
        raise  NotImplementedError

    def handle(self, board, move):
        raise NotImplementedError

class Castling(MoveHandler):
    def __init__(self):
        self.white_king_moved = False
        self.black_king_moved = False

    def applies(self, board, move):
        # check if the king has moved
        if self.white_king_moved and get_piece(board, move[:2]).isupper():
            return False
        if self.black_king_moved and get_piece(board, move[:2]).islower():
            return False

        # check if the path is clear
        if move == "e1g1" or move == "e1h1":
            # check for the king side white
            if not empty_between_horizontal(board, "e1", "g1"):
                return False
        elif move == "e1c1" or move == "e1a1":
            # check for the queen side white
            if not empty_between_horizontal(board, "e1", "b1"):
                return False
        elif move == "e8g8" or move == "e8h8":
            # check for the king side black
            if not empty_between_horizontal(board, "e8", "g8"):
                return False
        elif move == "e8c8" or move == "e8a8":
            # check for the queen side black
            if not empty_between_horizontal(board, "e8", "b8"):
                return False
        else:
            # not a valid castling move
            return False

        # Get the color of the king
        king_color = 'w' if get_piece(board, move[:2]).isupper() else 'b'
        
        # Check if the king is in check
        if is_square_attacked(board, move[:2], king_color):
            return False
            
        # Check the squares the king passes through
        if move in ["e1g1", "e8g8"]:  # King side castling
            # Check f1/f8 (intermediate) and g1/g8 (final) squares
            intermediate = "f" + move[1]
            final = "g" + move[1]
            if is_square_attacked(board, intermediate, king_color) or \
               is_square_attacked(board, final, king_color):
                return False
        elif move in ["e1c1", "e8c8"]:  # Queen side castling
            # Check d1/d8 (intermediate) and c1/c8 (final) squares
            intermediate = "d" + move[1]
            final = "c" + move[1]
            if is_square_attacked(board, intermediate, king_color) or \
               is_square_attacked(board, final, king_color):
                return False

        return True

    def handle(self, board, move):
        if move == "e1g1":
            board[7][4], board[7][7] = "", ""
            board[7][6], board[7][5] = "K", "R"
            self.white_king_moved = True
        elif move == "e1c1":
            board[7][4], board[7][0] = "", ""
            board[7][2], board[7][3] = "K", "R"
            self.white_king_moved = True
        elif move == "e8g8":
            board[0][4], board[0][7] = "", ""
            board[0][6], board[0][5] = "k", "r"
            self.black_king_moved = True
        elif move == "e8c8":
            board[0][4], board[0][0] = "", ""
            board[0][2], board[0][3] = "k", "r"
            self.black_king_moved = True
        return "O-O" if "g" in move else "O-O-O"


class EnPassant(MoveHandler):
    def __init__(self):
        # Stores last move for en passant validation
        self.last_move = None  

    def applies(self, board, move):
        """ Check if the en passant move is valid. """
        start, end = move[:2], move[2:]
        start_col, start_row = ord(start[0]) - ord('a'), 8 - int(start[1])
        end_col, end_row = ord(end[0]) - ord('a'), 8 - int(end[1])
        piece = board[start_row][start_col]

        # Ensure it's a pawn moving diagonally
        if piece.lower() != "p" or abs(start_col - end_col) != 1 or abs(start_row - end_row) != 1:
            return False

        # Check last move to see if en passant is possible
        if self.last_move:
            last_start, last_end = self.last_move[:2], self.last_move[2:]
            last_start_col, last_start_row = ord(last_start[0]) - ord('a'), 8 - int(last_start[1])
            last_end_col, last_end_row = ord(last_end[0]) - ord('a'), 8 - int(last_end[1])

            # Opponent's pawn must have moved two squares forward to be capturable
            if (last_start_row == (6 if piece == "p" else 1) and 
                last_end_row == (4 if piece == "p" else 3) and 
                last_start_col == last_end_col and 
                last_end_col == end_col):

                return True

        return False

    def handle(self, board, move):
        """ Execute the en passant move. """
        start, end = move[:2], move[2:]
        start_col, start_row = ord(start[0]) - ord('a'), 8 - int(start[1])
        end_col, end_row = ord(end[0]) - ord('a'), 8 - int(end[1])

        # Remove opponent's captured pawn
        captured_pawn_row = start_row
        board[captured_pawn_row][end_col] = ""

        # Move the current player's pawn
        board[start_row][start_col] = ""
        board[end_row][end_col] = "P" if start_row == 3 else "p"

        return f"{start}x{end}"


class Promotion(MoveHandler):
    def applies(self, board, move):
        return move[1] == "7" and move[3] == "8" and board[1][ord(move[0]) - ord('a')].lower() == "p"

    def handle(self, board, move):
        end_col, end_row = ord(move[2]) - ord('a'), 8 - int(move[3])
        board[end_row][end_col] = "Q" if board[end_row][end_col].isupper() else "q"
        return f"{move}=Q"

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
        if 0 <= r < 8 and 0 <= c < 8:
            piece = board[r][c]
            if piece.lower() == 'p' and piece.islower() == (opponent_color == "b"):
                return True

    # Check for knight attacks
    knight_moves = [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2)]
    for dr, dc in knight_moves:
        r, c = row + dr, col + dc
        if 0 <= r < 8 and 0 <= c < 8:
            piece = board[r][c]
            if piece.lower() == 'n' and piece.islower() == (opponent_color == "b"):
                return True

    # Check for rook/queen attacks (horizontal/vertical)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in directions:
        r, c = row + dr, col + dc
        while 0 <= r < 8 and 0 <= c < 8:
            piece = board[r][c]
            if piece != "":
                if (piece.lower() in ['r', 'q']) and piece.islower() == (opponent_color == "b"):
                    return True
                break  # Blocked by any piece
            r += dr
            c += dc

    # Check for bishop/queen attacks (diagonal)
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dr, dc in directions:
        r, c = row + dr, col + dc
        while 0 <= r < 8 and 0 <= c < 8:
            piece = board[r][c]
            if piece != "":
                if (piece.lower() in ['b', 'q']) and piece.islower() == (opponent_color == "b"):
                    return True
                break  # Blocked by any piece
            r += dr
            c += dc

    # Check for king attacks (adjacent squares)
    king_moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dr, dc in king_moves:
        r, c = row + dr, col + dc
        if 0 <= r < 8 and 0 <= c < 8:
            piece = board[r][c]
            if piece.lower() == 'k' and piece.islower() == (opponent_color == "b"):
                return True

    return False

