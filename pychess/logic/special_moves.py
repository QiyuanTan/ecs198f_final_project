from .board_utils import *

class MoveHandler:
    def applies(self, board, move):
        raise  NotImplementedError

    def handle(self, board, move):
        raise NotImplementedError

class Castling(MoveHandler):
    def __init__(self):
        self.white_castling_allowed = True
        self.black_castling_allowed = True
        self.white_king_moved = False
        self.white_kingside_rook_moved = False
        self.white_queenside_rook_moved = False
        self.black_king_moved = False
        self.black_kingside_rook_moved = False
        self.black_queenside_rook_moved = False

    def applies(self, board, move):
        """
        Check if castling is allowed
        
        Args:
            board: The current board state
            move: The move string (e.g. 'e1g1' for white kingside castling)
            
        Returns:
            bool: True if castling is allowed, False otherwise
        """
        # Check if the king has moved
        if self.white_king_moved and get_piece(board, move[:2]).isupper():
            return False
        if self.black_king_moved and get_piece(board, move[:2]).islower():
            return False

        # Check if the path is clear and safe
        if move == "e1g1":  # White kingside
            if self.white_kingside_rook_moved:
                return False
            # Check if squares between king and rook are empty and not attacked
            return (empty_between_horizontal(board, "e1", "h1") and
                   not is_square_attacked(board, "e1", "w") and
                   not is_square_attacked(board, "f1", "w") and
                   not is_square_attacked(board, "g1", "w"))
        elif move == "e1c1":  # White queenside
            if self.white_queenside_rook_moved:
                return False
            # Check if squares between king and rook are empty and not attacked
            return (empty_between_horizontal(board, "e1", "a1") and
                   not is_square_attacked(board, "e1", "w") and
                   not is_square_attacked(board, "d1", "w") and
                   not is_square_attacked(board, "c1", "w"))
        elif move == "e8g8":  # Black kingside
            if self.black_kingside_rook_moved:
                return False
            # Check if squares between king and rook are empty and not attacked
            return (empty_between_horizontal(board, "e8", "h8") and
                   not is_square_attacked(board, "e8", "b") and
                   not is_square_attacked(board, "f8", "b") and
                   not is_square_attacked(board, "g8", "b"))
        elif move == "e8c8":  # Black queenside
            if self.black_queenside_rook_moved:
                return False
            # Check if squares between king and rook are empty and not attacked
            return (empty_between_horizontal(board, "e8", "a8") and
                   not is_square_attacked(board, "e8", "b") and
                   not is_square_attacked(board, "d8", "b") and
                   not is_square_attacked(board, "c8", "b"))
        else:
            # Not a valid castling move
            return False

    def handle(self, board, move):
        """
        Execute the castling move
        
        Args:
            board: The current board state
            move: The move string (e.g. 'e1g1' for white kingside castling)
            
        Returns:
            str: The chess notation for the move ('O-O' for kingside, 'O-O-O' for queenside)
        """
        if move == "e1g1":  # White kingside
            board[7][4], board[7][7] = "", ""  # Remove king and rook
            board[7][6], board[7][5] = "K", "R"  # Place king and rook
            self.white_king_moved = True
            self.white_kingside_rook_moved = True
        elif move == "e1c1":  # White queenside
            board[7][4], board[7][0] = "", ""  # Remove king and rook
            board[7][2], board[7][3] = "K", "R"  # Place king and rook
            self.white_king_moved = True
            self.white_queenside_rook_moved = True
        elif move == "e8g8":  # Black kingside
            board[0][4], board[0][7] = "", ""  # Remove king and rook
            board[0][6], board[0][5] = "k", "r"  # Place king and rook
            self.black_king_moved = True
            self.black_kingside_rook_moved = True
        elif move == "e8c8":  # Black queenside
            board[0][4], board[0][0] = "", ""  # Remove king and rook
            board[0][2], board[0][3] = "k", "r"  # Place king and rook
            self.black_king_moved = True
            self.black_queenside_rook_moved = True
            
        return "O-O" if "g" in move else "O-O-O"

    def update(self, board, move):
        """
        Update the castling flags based on piece movements
        
        Args:
            board: The current board state
            move: The move string (e.g. 'e2e4')
        """
        start, end = move[:2], move[2:]
        piece = get_piece(board, start)
        
        # King moves
        if start == "e1":
            self.white_king_moved = True
        elif start == "e8":
            self.black_king_moved = True
            
        # Rook moves
        if start == "a1":
            self.white_queenside_rook_moved = True
        elif start == "h1":
            self.white_kingside_rook_moved = True
        elif start == "a8":
            self.black_queenside_rook_moved = True
        elif start == "h8":
            self.black_kingside_rook_moved = True


class EnPassant(MoveHandler):
    def __init__(self):
        # Stores last move for en passant validation
        self.last_move = None  

    def applies(self, board, move):
        """ Check if the en passant move is valid. """
        # 处理带有 'x' 的捕获符号
        if 'x' in move:
            capture_index = move.index('x')
            start = move[:capture_index]
            end = move[capture_index+1:]
        else:
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

        return f"P{start}x{end}"


class Promotion(MoveHandler):
    def applies(self, board, move):
        """
        Check if a pawn promotion is valid
        
        Args:
            board: The current board state
            move: The move string (e.g. 'e7e8')
            
        Returns:
            bool: True if the move is a valid promotion
        """
        # Ensure move has correct length
        if len(move) < 4:
            return False
            
        start, end = move[:2], move[2:4]
        start_row, start_col = str2index(start)
        end_row, end_col = str2index(end)
        piece = board[start_row][start_col]
        
        # Check if this is a pawn
        if piece.lower() != 'p':
            return False
            
        # Check if white pawn reaches 8th rank or black pawn reaches 1st rank
        if (piece == 'P' and end_row == 0) or (piece == 'p' and end_row == 7):
            return True
            
        return False

    def handle(self, board, move):
        """
        Execute a pawn promotion
        
        Args:
            board: The current board state
            move: The move string (e.g. 'e7e8=Q')
            
        Returns:
            str: The chess notation for the move
        """
        start, end = move[:2], move[2:4]
        start_row, start_col = str2index(start)
        end_row, end_col = str2index(end)
        
        # 获取原始棋子是白棋还是黑棋
        is_white = board[start_row][start_col].isupper()
        
        # Get the piece type to promote to (Q by default)
        promotion_piece = 'Q'
        if '=' in move:
            promotion_piece = move.split('=')[1][0]
            
        # Determine if it's a white or black piece
        piece_case = promotion_piece.upper() if is_white else promotion_piece.lower()
        
        # Move the pawn and replace with promoted piece
        move_piece(board, start, end)
        board[end_row][end_col] = piece_case
        
        # Return the appropriate notation - 根据棋子颜色设置前缀
        pawn_prefix = 'P' if is_white else 'p'
        return f"{pawn_prefix}{start}{end}={promotion_piece.upper()}"  # 升变后的棋子总是大写
