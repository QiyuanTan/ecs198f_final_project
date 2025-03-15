from pychess.logic.special_moves import Castling, EnPassant, Promotion
from pychess.logic.board_utils import *
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
			['','','','','','','',''],
			['','','','','','','',''],
			['','','','','','','',''],
			['','','','','','','',''],
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
		self. white_king_index = (7,4)
		self. black_king_index = (0,4)

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

		# skip if the starting piece is invalid
		if self._invalid_starting_piece(starting_piece):
			print("Invalid starting square")
			return ""

		# handle special moves
		if self.castling.applies(self.board, move):
			return self.castling.handle(self.board, move)
		elif self.en_passant.applies(self.board, move):
			return self.en_passant.handle(self.board, move)

		# handle normal moves
		if self._invalid_move():
			return ""

		# move the piece
		result =  self._handle_move(starting, ending)

		if self.promotion.applies(self.board, move):
			return self.promotion.handle(self.board, move)

		# determine if the game is over
		self.result =  self._game_over()

		# switch the move
		self.turn = 'w' if self.turn == 'b' else 'b'

		print(result)
		return result

	def _invalid_starting_piece(self, starting_piece):
		"""
		@brief: Function to check if the starting piece is invalid
		@param starting_piece: The piece at the starting square
		@return: True if the starting piece is invalid, False otherwise
		"""
		return starting_piece == '' or (self.turn == 'w' and starting_piece.islower()) or (self.turn == 'b' and starting_piece.isupper())


	def _invalid_move(self, move) -> bool:
		#check if destination is valid
		#get the piece
		cur_piece:str = get_piece(self.board, move[:2])
		#check if destination is in its path, if not return false
		#check if pieces blocking it, if not return false
		#check if causing a check, if so then return false
		#else return true
		pass

	def _handle_move(self, starting, ending):
		raise NotImplementedError

	def check_king_path_for_check(self, board) -> bool:
		"""
		check horizontal/vertical path from king(opposing queen/rook)
		check diagonal path from king (opposing queen/bishop)
		check knight path from king
		"""
		pass

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
		if self.check_king_path_for_check(self.board):
			return 'w' if self.turn == 'b' else 'b'
		elif self._stalemate():
			return 'd'
		else:
			return ''