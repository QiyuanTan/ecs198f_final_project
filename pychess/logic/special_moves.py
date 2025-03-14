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

        # check if the move is causing a check
        # TODO: implement this

        return True

    def handle(self, board, move):
        raise NotImplementedError

class EnPassant(MoveHandler):
    def applies(self, board, move):
        start, end = move[:2], move[2:]
        start_col, start_row = ord(start[0]) - ord('a'), 8 - int(start[1])
        end_col, end_row = ord(end[0]) - ord('a'), 8 - int(end[1])
        piece = board[start_row][start_col]
        return piece.lower() == "p" and abs(start_col - end_col) == 1 and board[start_row][end_col].lower() == "p"

    def handle(self, board, move):
        start, end = move[:2], move[2:]
        start_col, start_row = ord(start[0]) - ord('a'), 8 - int(start[1])
        end_col, end_row = ord(end[0]) - ord('a'), 8 - int(end[1])
        board[start_row][start_col] = ""
        board[start_row][end_col] = ""
        board[end_row][end_col] = "P" if start_row == 3 else "p"
        return f"{start}x{end}"

class Promotion(MoveHandler):
    def applies(self, board, move):
        return move[1] == "7" and move[3] == "8" and board[1][ord(move[0]) - ord('a')].lower() == "p"

    def handle(self, board, move):
        end_col, end_row = ord(move[2]) - ord('a'), 8 - int(move[3])
        board[end_row][end_col] = "Q" if board[end_row][end_col].isupper() else "q"
        return f"{move}=Q"
