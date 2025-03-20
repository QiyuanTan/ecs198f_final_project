import copy
from .board_utils import *
from .special_moves import Castling, EnPassant, Promotion

class ChessLogic:
    def __init__(self):
        """
        Initalize the ChessLogic Object. External fields are board and result

        board -> Two Dimensional List of string Representing the Current State of the Board
            P, R, N, B, Q, K - White Pieces

            p, r, n, b, q, k - Black Pieces

            '' - Empty Square

        result -> The current result of the game
            w - White Win

            b - Black Win

            d - Draw

            '' - Game In Progress
        """
        self.board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
        ]
        self.result = ""
        self.turn = 'w'
        self.castling = Castling()
        self.en_passant = EnPassant()
        self.promotion = Promotion()
        self.white_king_index = (7, 4)
        self.black_king_index = (0, 4)

    def play_move(self, move: str) -> str:
        """
        Function to make a move if it is a valid move. This function is called everytime a move in made on the board

        Args:
            move (str): The move which is proposed. The format is the following: starting_sqaure}{ending_square}

            i.e. e2e4 - This means that whatever piece is on E2 is moved to E4

        Returns:
            str: Extended Chess Notation for the move, if valid. Empty str if the move is invalid
        """
        starting = move[:2]
        ending = move[2:]
        starting_piece = get_piece(self.board, starting)
        ending_piece = get_piece(self.board, ending)

        print(f'{self.turn}\'s turn')
        print(self.en_passant.last_move)

        # skip if the starting piece is invalid
        if self._invalid_starting_piece(starting_piece):
            print("Invalid starting square")
            return ""

        # handle special moves
        if self.castling.applies(self.board, move):
            print("castling")
            result = self.castling.handle(self.board, move)
        elif self.en_passant.applies(self.board, move):
            print("en passant")
            result =  self.en_passant.handle(self.board, move)
        else:
            # handle normal moves
            if self._invalid_move(move):
                print("Invalid move")
                return ""
            # move the piece
            print("normal move")
            result = self._handle_move_capture(starting, ending)

        if starting_piece == 'k':
            self.black_king_index = str2index(ending)
            self.castling.back_castling_allowed = False
        if starting_piece == 'K':
            self.white_king_index = str2index(ending)
            self.castling.white_castling_allowed = False
        if starting_piece == 'r':
            self.castling.back_castling_allowed = False
        if starting_piece == 'R':
            self.castling.white_castling_allowed = False
        self.en_passant.last_move = move

        # switch the move
        self.turn = 'w' if self.turn == 'b' else 'b'

        if self.promotion.applies(self.board, move):
            print("promotion")
            result =  self.promotion.handle(self.board, move)

        # determine if the game is over
        self.result = self._game_over()

        print(result)
        return result

    def _invalid_starting_piece(self, starting_piece):
        """
        @brief: Function to check if the starting piece is invalid
        @param starting_piece: The piece at the starting square
        @return: True if the starting piece is invalid, False otherwise
        """
        return starting_piece == '' or (self.turn == 'w' and starting_piece.islower()) or (
                    self.turn == 'b' and starting_piece.isupper())

    def move_causes_check(self, move, side):
        """
            Function to check if move causes a check
            Args:
                side: the side that is making the move
                move: the move that the player is making
            Returns:
                True if move causes a check, else False
        """
        board = copy.deepcopy(self.board)
        move_piece(board, move[:2], move[2:])
        king_index = self.white_king_index if side == 'w' else self.black_king_index
        return is_square_attacked(board, king_index if not get_piece(board, move[2:]).lower() == 'k' else move[2:], side)

    def _invalid_move(self, move) -> bool:
        """
            Function to check if move is valid
            Args:
                move: the move that the player is making
            Returns:
                True if move is invalid, else False
        """
        return self.invalid_move(self.board, move, self.turn)

    def invalid_move(self, board, move, side) -> bool:
        """
            Function to check if move is valid for white
            Args:
                board:
                side:
                move: the move that the player is making
            Returns:
                True if move is invalid, else False
        """
        # set side
        is_self = lambda p: p.isupper() if side == 'w' else p.islower()

        if self.castling.applies(board, move) or self.en_passant.applies(board, move):
            return False

        # check to make sure you're not moving on top of another white piece
        dest_piece = get_piece(board, move[2:])
        if is_self(dest_piece):
            print("moving on top of another piece")
            return True

        causes_check = self.move_causes_check(move, side)
        invalid_move = invalid_move_for_piece(board, move, side)

        if causes_check:
            print("causes check")
        if invalid_move:
            print("invalid move for piece")

        return causes_check or invalid_move

    def _handle_move_capture(self, starting, ending):
        chess_notation = (f"{get_piece(self.board, starting).lower() if get_piece(self.board, starting).lower() != 'p' else ''}"
                          f"{starting}"
                          f"{'x' if get_piece(self.board, ending) != '' else ''}"
                          f"{ending}")
        move_piece(self.board, starting, ending)
        return chess_notation

    def white_king_checked(self, board, white_king_index) -> bool:
        """
            Function to check if Black King is in check
            Args:
                board: 2D object representing board
            Returns:
                True or False if king is in check
        """
        # Convert the numeric coordinates to chess notation
        row = str(8 - white_king_index[0])
        col = chr(ord('a') + white_king_index[1])
        square = col + row
        print(f"White king is at square: {square}")
        return is_square_attacked(board, square, "w")

    def black_king_checked(self, board, black_king_index) -> bool:
        """
            Function to check if Black King is in check
            Args:
                board: 2D object representing board
            Returns:
                True or False if king is in check
        """
        # Convert the numeric coordinates to chess notation
        row = str(8 - black_king_index[0])
        col = chr(ord('a') + black_king_index[1])
        square = col + row
        print(f"Black king is at square: {square}")
        return is_square_attacked(board, square, "b")

    def _game_over(self) -> str:
        """
        Function to determine if the game is over.
        This function is called after every move

        Returns:
            str: The result of the game
                w - White Win

                b - Black Win

                d - Draw

                '' - Game In Progress
        """
        is_king_checked = self.white_king_checked(self.board, self.white_king_index) if self.turn == 'w' else self.black_king_checked(self.board, self.black_king_index)
        no_valid_moves = self._no_valid_moves(self.turn)
        print(f'{self.turn}: is_king_checked: {is_king_checked}, no_valid_moves: {no_valid_moves}')
        if is_king_checked and no_valid_moves:
            return 'w' if self.turn == 'b' else 'b'
        elif (not is_king_checked) and no_valid_moves:
            return 'd'
        return ''

    def _no_valid_moves(self, side):
        """
        Function to check if there are no valid moves for a side
        Args:
            side: The side to check for
        Returns:
            True if there are no valid moves, else False
        """
        is_self = lambda p: p.isupper() if side == 'w' else p.islower()
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece == "" or not is_self(piece):
                    continue

                piece = piece.lower()
                if piece == 'p':
                    move_set = pawn_moves(self.board, i, j, side)
                elif piece == 'r':
                    move_set = rook_moves(self.board, i, j, side)
                elif piece == 'n':
                    move_set = knight_moves(self.board, i, j, side)
                elif piece == 'b':
                    move_set = bishop_moves(self.board, i, j, side)
                elif piece == 'q':
                    move_set = queen_moves(self.board, i, j, side)
                elif piece == 'k':
                    move_set = king_moves(self.board, i, j, side)
                else:
                    raise Exception("Unhandled piece")

                for move in move_set:
                    if not self.invalid_move(self.board, index2str((i, j)) + index2str(move), side):
                        print(f'valid move: {index2str((i, j)) + index2str(move)}')
                        return False

        if side == 'w':
            if self.castling.applies(self.board, "e1g1") or self.castling.applies(self.board, "e1c1"):
                return False
        elif side == 'b':
            if self.castling.applies(self.board, "e8g8") or self.castling.applies(self.board, "e8c8"):
                return False

        return True
