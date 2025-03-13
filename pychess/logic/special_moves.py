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

        # check if the move is a castling move
        if move == 'e1g1' or move == 'e1c1':
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