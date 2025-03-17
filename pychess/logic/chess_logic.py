from logic.board_utils import *
from logic.special_moves import Castling, EnPassant, Promotion


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
        self.white_king_moved = False
        self.black_king_moved = False
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
        # Handle capture notation with 'x'
        promotion_piece = ""
        if 'x' in move:
            capture_index = move.index('x')
            starting = move[:capture_index]
            ending = move[capture_index+1:]
            if '=' in ending:
                eq_index = ending.index('=')
                promotion_piece = ending[eq_index:]
                ending = ending[:eq_index]
        else:
            # Regular move format
            starting = move[:2]
            if '=' in move:
                eq_index = move.index('=')
                promotion_piece = move[eq_index:]
                ending = move[2:eq_index]
            else:
                ending = move[2:]
            
        starting_piece = get_piece(self.board, starting)
        ending_piece = get_piece(self.board, ending)

        # skip if the starting piece is invalid
        if self._invalid_starting_piece(starting_piece):
            print("Invalid starting square")
            return ""

        # handle special moves
        if self.castling.applies(self.board, starting + ending):
            return self.castling.handle(self.board, starting + ending)
        elif self.en_passant.applies(self.board, starting + ending):
            return self.en_passant.handle(self.board, starting + ending)

        # handle normal moves
        if self._invalid_move(starting + ending):
            return ""

        # 检查是否是升变
        if promotion_piece and starting_piece.lower() == 'p':
            # 检查目标位置是否是第1/8行
            end_row = 8 - int(ending[1])
            if (starting_piece.isupper() and end_row == 0) or (starting_piece.islower() and end_row == 7):
                # 移动棋子并处理升变
                result = self.promotion.handle(self.board, starting + ending + promotion_piece)
                
                # determine if the game is over
                self.result = self._game_over()
                
                # switch the move
                self.turn = 'w' if self.turn == 'b' else 'b'
                
                return result

        # 普通棋子移动
        result = self._handle_move_capture(starting, ending)

        # determine if the game is over
        self.result = self._game_over()

        # switch the move
        self.turn = 'w' if self.turn == 'b' else 'b'

        return result

    def _invalid_starting_piece(self, starting_piece):
        """
        @brief: Function to check if the starting piece is invalid
        @param starting_piece: The piece at the starting square
        @return: True if the starting piece is invalid, False otherwise
        """
        return starting_piece == '' or (self.turn == 'w' and starting_piece.islower()) or (
                    self.turn == 'b' and starting_piece.isupper())

    def move_causes_check(self):
        """
        Check if a move causes a check (king is under attack).
        
        Returns:
            bool: True if the move causes check, False otherwise
        """
        # 获取当前方的国王位置
        king_piece = 'K' if self.turn == 'w' else 'k'
        king_pos = None
        
        # 扫描棋盘找到国王
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == king_piece:
                    king_pos = (row, col)
                    break
            if king_pos:
                break
                
        # 如果找不到国王（在有效的游戏中不应该发生），返回False
        if not king_pos:
            return False
            
        # 转换为代数记号
        king_square = chr(king_pos[1] + ord('a')) + str(8 - king_pos[0])
        
        # 检查国王是否正在被攻击
        return is_square_attacked(self.board, king_square, self.turn)

    def check_king_path_for_check(self, board):
        """
        Check if the king is in check
        
        Args:
            board: The current board state
            
        Returns:
            bool: True if the king is in check, False otherwise
        """
        # 确定当前方
        king_piece = 'K' if self.turn == 'w' else 'k'
        king_pos = None
        
        # 扫描棋盘找到国王
        for row in range(8):
            for col in range(8):
                if board[row][col] == king_piece:
                    king_pos = (row, col)
                    break
            if king_pos:
                break
                
        # 如果找不到国王（在有效的游戏中不应该发生），返回False
        if not king_pos:
            return False
            
        # 转换为代数记号
        king_square = chr(king_pos[1] + ord('a')) + str(8 - king_pos[0])
        
        # 检查国王是否正在被攻击
        return is_square_attacked(board, king_square, self.turn)

    def _invalid_move(self, move) -> bool:
        """
        Function to check if move is valid
        Args:
            move: the move that the player is making
        Returns:
            True if move is invalid, else False
        """
        # 检查格式错误
        if '=' not in move and 'x' not in move:
            # 标准格式应该是4个字符，如"e2e4"
            if len(move) != 4:
                return True
                
        # 处理带有 'x' 的捕获符号
        if 'x' in move:
            capture_index = move.index('x')
            starting = move[:capture_index]
            ending = move[capture_index+1:]
            # 确保起始位置和目标位置格式正确
            if len(starting) != 2 or len(ending) != 2:
                return True
        else:
            # 正常格式提取
            starting = move[:2]
            ending = move[2:] if '=' not in move else move[2:].split('=')[0]
            # 确保终点位置格式正确
            if '=' not in move and len(ending) != 2:
                return True
            
        # 检查是否是王车易位
        if (starting == 'e1' and (ending == 'g1' or ending == 'c1')) or \
           (starting == 'e8' and (ending == 'g8' or ending == 'c8')):
            # 验证王车易位条件
            castle_allowed = self.castling.applies(self.board, starting + ending)
            # 如果王车易位不允许，返回True表示这是一个无效的移动
            return not castle_allowed
        
        # 正常的移动检查
        return self.invalid_move(self.board, starting + ending, self.turn)

    def invalid_move(self, board, move, side) -> bool:
        """
            Function to check if move is valid for white
            Args:
                move: the move that the player is making
            Returns:
                True if move is invalid, else False
        """
        # 处理带有 'x' 的捕获符号
        if 'x' in move:
            capture_index = move.index('x')
            starting = move[:capture_index]
            ending = move[capture_index+1:]
        else:
            # 确保我们总是使用不带"="的移动格式
            if '=' in move:
                eq_index = move.index('=')
                move = move[:eq_index]
            starting = move[:2]
            ending = move[2:]
            
        starting_piece = get_piece(board, starting)  # 起始位置的棋子
        ending_piece = get_piece(board, ending)      # 目标位置的棋子
        
        # set side
        to_self = lambda p: p.upper() if side == 'w' else p.lower()
        is_self = lambda p: p.isupper() if side == 'w' else p.islower()
        delta = -1 if side == 'w' else 1
        pawn_base = 6 if side == 'w' else 1

        # check to make sure youre not moving on top of another white piece
        if is_self(ending_piece):
            return True
            
        # check if pieces blocking it, if not return false
        # check if causing a check, if so then return false TBD ADD SOON
        # else return true
        # ex move: e2e3
        is_horizontal = is_horizontal_move(starting, ending)
        is_diagonal = is_diagonal_move(starting, ending)
        is_vertical = is_vertical_move(starting, ending)
        srow, scol = str2index(starting)
        erow, ecol = str2index(ending)

        piece_type = starting_piece.lower()
        
        if piece_type == "p":  # if the piece is a pawn
            # check if it's a capture (diagonal move)
            if is_diagonal:
                if abs(erow - srow) == 1 and abs(ecol - scol) == 1:
                    # 确保对角线移动是为了捕获
                    if ending_piece != '' or (self.en_passant and self.en_passant.applies(board, starting + ending)):
                        return False
                return True
                
            if not is_vertical:
                return True
                
            # 处理向后移动
            if (side == 'w' and erow > srow) or (side == 'b' and erow < srow):
                return True  # 不允许向后移动

            if srow == pawn_base:  # this means its at the starting row i.e "e2,a2"
                if abs(erow - srow) > 2:  # 不能移动超过两格
                    return True
                if empty_between_vertical(board, starting, ending) and not self.move_causes_check():
                    # make sure nothing is in front of pawn
                    return False
                else:
                    return True
            else:
                if abs(erow - srow) > 1:  # 非起始位置只能移动一格
                    return True
                if empty_between_vertical(board, starting, ending) and not self.move_causes_check():
                    # make sure nothing is in front of pawn
                    return False
                else:
                    return True
        elif piece_type == "r":  # Rook
            if is_diagonal:
                return True
            if not (is_horizontal or is_vertical):
                return True
                
            if is_horizontal:
                if empty_between_horizontal(board, starting, ending) and not self.move_causes_check():
                    return False
            elif is_vertical:
                if empty_between_vertical(board, starting, ending) and not self.move_causes_check():
                    return False
            return True
            
        elif piece_type == "b":  # Bishop
            if not is_diagonal:
                return True

            if empty_between_diagonal(board, starting, ending) and not self.move_causes_check():
                return False
            return True
            
        elif piece_type == "n":  # Knight
            # 确保移动是L形的
            knight_moves = [
                (2, 1), (2, -1), (-2, 1), (-2, -1),
                (1, 2), (1, -2), (-1, 2), (-1, -2)
            ]
            if (erow - srow, ecol - scol) in knight_moves and not self.move_causes_check():
                return False
            return True
            
        elif piece_type == "q":  # Queen
            if not (is_horizontal or is_diagonal or is_vertical):
                return True
                
            if is_horizontal:
                if empty_between_horizontal(board, starting, ending) and not self.move_causes_check():
                    return False
            elif is_vertical:
                if empty_between_vertical(board, starting, ending) and not self.move_causes_check():
                    return False
            elif is_diagonal:
                if empty_between_diagonal(board, starting, ending) and not self.move_causes_check():
                    return False
            return True
            
        elif piece_type == "k":  # King
            # 检查是否是一步移动（横向、纵向或对角线）
            if abs(erow - srow) <= 1 and abs(ecol - scol) <= 1:
                # 确保国王不走入被攻击的方格
                king_square = ending
                if not is_square_attacked(board, king_square, side) and not self.move_causes_check():
                    return False
            
            # 检查王车易位
            if starting == "e1" and side == "w":
                if ending == "g1" or ending == "c1":
                    return False
            elif starting == "e8" and side == "b":
                if ending == "g8" or ending == "c8":
                    return False
                    
            return True
        
        # 如果没有处理的棋子类型
        return True

    def _handle_move_capture(self, starting, ending):
        """
        Function to handle a normal move and generate the correct chess notation
        
        Args:
            starting (str): Starting square (e.g. 'e2')
            ending (str): Ending square (e.g. 'e4')
            
        Returns:
            str: Extended Chess Notation for the move
        """
        # Get the piece and determine notation
        starting_piece = get_piece(self.board, starting)
        ending_piece = get_piece(self.board, ending)
        
        # Create the chess notation with the piece prefix
        # Use uppercase letters for piece types: P (pawn), N (knight), B (bishop), R (rook), Q (queen), K (king)
        piece_prefix = starting_piece.upper() if starting_piece.lower() != 'p' else 'P'
        capture_symbol = 'x' if ending_piece != '' else ''
        
        chess_notation = f"{piece_prefix}{starting}{capture_symbol}{ending}"
        
        # Move the piece on the board
        move_piece(self.board, starting, ending)
        
        # Update the last move for en passant detection
        self.en_passant.last_move = f"{starting}{ending}"
        
        return chess_notation

    def has_legal_moves(self, side):
        """
        Check if the given side has any legal moves
        
        Args:
            side: 'w' for white, 'b' for black
            
        Returns:
            bool: True if the side has any legal moves, False otherwise
        """
        for start_row in range(8):
            for start_col in range(8):
                piece = self.board[start_row][start_col]
                # Skip empty squares and opponent's pieces
                if piece == '' or (side == 'w' and piece.islower()) or (side == 'b' and piece.isupper()):
                    continue
                # Try all possible moves for this piece
                for end_row in range(8):
                    for end_col in range(8):
                        start = chr(start_col + ord('a')) + str(8 - start_row)
                        end = chr(end_col + ord('a')) + str(8 - end_row)
                        # If this is a legal move
                        if not self._invalid_move(start + end):
                            return True
        return False

    def _game_over(self):
        """
        Check if the game is over.
        
        Returns:
            str: 'w' if white wins, 'b' if black wins, 'd' if draw, '' if game is not over
        """
        # First check if kings exist
        white_king_exists = False
        black_king_exists = False
        
        # Scan the board for kings
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == 'K':
                    white_king_exists = True
                elif self.board[row][col] == 'k':
                    black_king_exists = True
                    
        # If a king is missing, that side loses
        if not white_king_exists:
            return 'b'  # Black wins
        elif not black_king_exists:
            return 'w'  # White wins
        
        # Check for checkmate and stalemate
        # First, save the current turn
        current_turn = self.turn
        
        # Check both sides
        for side in ['w', 'b']:
            self.turn = side
            # If the king is in check
            if self.check_king_path_for_check(self.board):
                # If no legal moves exist and king is in check, it's checkmate
                if not self.has_legal_moves(side):
                    # Restore the original turn
                    self.turn = current_turn
                    return 'b' if side == 'w' else 'w'
            else:
                # If king is not in check but no legal moves exist, it's stalemate
                if not self.has_legal_moves(side):
                    # Restore the original turn
                    self.turn = current_turn
                    return 'd'
        
        # Restore the original turn
        self.turn = current_turn
        return ''  # Game not over
