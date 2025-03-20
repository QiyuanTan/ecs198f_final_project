from .board_utils import *

class MoveHandler:
    def applies(self, board, move):
        raise  NotImplementedError

    def handle(self, board, move):
        raise NotImplementedError

class Castling(MoveHandler):
    def __init__(self):
        self.white_castling_allowed = True
        self.back_castling_allowed = True

    def applies(self, board, move):
        # check if the king has moved
        if (not self.white_castling_allowed) and get_piece(board, move[:2]).isupper():
            return False
        if (not self.back_castling_allowed) and get_piece(board, move[:2]).islower():
            return False

        # check if the path is clear
        if move == "e1g1" or move == "e1h1":
            # check for the king side white
            return empty_between_horizontal(board, "e1", "h1") and not is_square_attacked(board, "g1", "w")
        elif move == "e1c1" or move == "e1a1":
            # check for the queen side white
            return empty_between_horizontal(board, "e1", "a1") and not is_square_attacked(board, "c1", "w")
        elif move == "e8g8" or move == "e8h8":
            # check for the king side black
            return empty_between_horizontal(board, "e8", "h8") and not is_square_attacked(board, "g8", "b")
        elif move == "e8c8" or move == "e8a8":
            # check for the queen side black
            return empty_between_horizontal(board, "e8", "a8") and not is_square_attacked(board, "c8", "b")
        else:
            # not a valid castling move
            return False

    def handle(self, board, move):
        if move == "e1g1":
            board[7][4], board[7][7] = "", ""
            board[7][6], board[7][5] = "K", "R"
            self.white_castling_allowed = True
        elif move == "e1c1":
            board[7][4], board[7][0] = "", ""
            board[7][2], board[7][3] = "K", "R"
            self.white_castling_allowed = True
        elif move == "e8g8":
            board[0][4], board[0][7] = "", ""
            board[0][6], board[0][5] = "k", "r"
            self.back_castling_allowed = True
        elif move == "e8c8":
            board[0][4], board[0][0] = "", ""
            board[0][2], board[0][3] = "k", "r"
            self.back_castling_allowed = True
        return "O-O" if "g" in move else "O-O-O"

    def update(self, move):
        if move[2:] == "e1" or move[2:] == "a1" or move[:2] == "h8":
            self.white_castling_allowed = False
        elif move[2:] == "e8" or move[2:] == "a8" or move[:2] == "h8":
            self.back_castling_allowed = False


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
            if ((last_start_row == (6 if piece == "p" else 1) and
                last_end_row == (4 if piece == "p" else 3) and
                last_end_col == end_col) and
                get_piece(board, last_end).upper() == "P"):

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
        return (move[1] == "7" and move[3] == "8" and board[1][ord(move[0]) - ord('a')].lower() == "p") or \
                (move[1] == "2" and move[3] == "1" and board[6][ord(move[0]) - ord('a')].lower() == "P")

    def handle(self, board, move):
        # end_col, end_row = ord(move[2]) - ord('a'), 8 - int(move[3])
        # board[end_row][end_col] = "Q" if board[end_row][end_col].isupper() else "q"
        # return f"{move}=Q"
        color = 'Q' if get_piece(board, move[2:]) == 'P' else 'q'
        return f"{move}={color}"
