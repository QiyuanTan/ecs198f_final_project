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
        raise NotImplementedError

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