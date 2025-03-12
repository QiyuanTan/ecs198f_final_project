class MoveHandler:
    @staticmethod
    def applies(board, move):
        raise NotImplementedError

    @staticmethod
    def handle(board, move):
        raise NotImplementedError

class Castling(MoveHandler):
    @staticmethod
    def applies(board, move):
        raise NotImplementedError

    @staticmethod
    def handle(board, move):
        raise NotImplementedError

class EnPassant(MoveHandler):
    @staticmethod
    def applies(board, move):
        raise NotImplementedError

    @staticmethod
    def handle(board, move):
        raise NotImplementedError

class Promotion(MoveHandler):
    @staticmethod
    def applies(board, move):
        raise NotImplementedError

    @staticmethod
    def handle(board, move):
        raise NotImplementedError