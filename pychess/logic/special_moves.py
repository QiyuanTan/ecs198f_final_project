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
        raise NotImplementedError

    def handle(self, board, move):
        raise NotImplementedError

class Promotion(MoveHandler):
    def applies(self, board, move):
        raise NotImplementedError

    def handle(self, board, move):
        raise NotImplementedError