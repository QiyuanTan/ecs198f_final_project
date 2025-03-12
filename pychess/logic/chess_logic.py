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
		self.move = "w"

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
		starting_piece = self._get_piece(starting)
		ending_piece = self._get_piece(ending)

		# skip if the starting piece is invalid
		if self._invalid_starting_piece(starting_piece):
			return ""

		# handle special moves
		if self._is_castling(move):
			return self._handle_castling(move)
		elif self._is_en_passant(move):
			return self._handle_en_passant(move)
		elif self._is_promotion(move):
			return self._handle_promotion(move)

		return ""


	def _get_piece(self, square:str) -> str:
			"""
			@brief: Function to get the piece at the given move
			@param square: The square to get the piece from, e.g. e4
			@return: The piece at the square
			"""
			col = ord(square[0]) - ord('a')
			row = 8 - int(square[1])
			return self.board[row][col]

	def _invalid_starting_piece(self, starting_piece):
		return starting_piece == '' or (self.move == 'w' and starting_piece.islower()) or (self.move == 'b' and starting_piece.isupper())

	def _is_castling(self, move):
		raise NotImplementedError

	def _handle_castling(self, move):
		raise NotImplementedError

	def _is_en_passant(self, move):
		raise NotImplementedError

	def _handle_en_passant(self, move):
		raise NotImplementedError

	def _is_promotion(self, move):
		raise NotImplementedError

	def _handle_promotion(self, move):
		raise NotImplementedError