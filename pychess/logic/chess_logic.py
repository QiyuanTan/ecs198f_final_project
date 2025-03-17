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
		self.white_king_index = (7,4)
		self.black_king_index = (0,4)

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
		if self._invalid_move(move):
			return ""

		# move the piece
		result = self._handle_move_capture(starting, ending)

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


	def move_causes_check():
		pass


	def _invalid_move(self, move) -> bool:
		"""
			Function to check if move is valid
			Args:
				move: the move that the player is making
			Returns:
				True if move is invalid, else False
		"""
		#check if destination is valid
		#get the piece
		cur_piece:str = get_piece(self.board, move[:2])
		#validate piece
		if self._invalid_starting_piece(cur_piece):
			return True

		#check if destination is in its path, if not return false
		if self.turn == 'w':
			#return invalid_move_for_white(move, cur_piece)
			print('whites turn')
		#return invalid_move_for_black(move, cur_piece)
			
		pass

	def invalid_move_for_white(self, move, piece) -> bool:
		"""
			Function to check if move is valid for white
			Args:
				move: the move that the player is making
				piece: the current piece selected
			Returns:
				True if move is invalid, else False
		"""
		#check to make sure youre not moving on top of another white piece
		dest_piece = get_piece(self.board, move[2:])
		if not (dest_piece.islower() or dest_piece == ""):
			return True
		#check if pieces blocking it, if not return false
		#check if causing a check, if so then return false TBD ADD SOON
		#else return true
		#ex move: e2e3
		is_horizontal = is_horizontal_move(move[:2], move[2:])
		is_diagonal = is_diagonal_move(move[:2], move[2:])
		is_vertical = is_vertical_move(move[:2], move[2:])
		srow, scol = str2index(move[:2])
		erow, ecol = str2index(move[2:])
		
		if piece == "P": #if the piece is a pawn

			if( not is_vertical):
				return True

			if((srow) == 2): # this means its at the starting row i.e "e2,a2"
				if ((erow) !=  srow+1 or  erow != srow+2): #if ending square is not 1 or 2 spaces above start
					return True
				else:
					if empty_between_vertical(self.board, move[:2], move[2:]) and not self.move_causes_check(): #make sure nothing is in front of pawn
						return False
					else:
						return True
			else:
				if ((erow) != srow+1): #if ending square is not 1 above 
					return True
				else:
					if empty_between_vertical(self.board, move[:2], move[2:]) and not self.move_causes_check(): #make sure nothing is in front of pawn
						return False
					else:
						return True
		elif piece == "R":
			if is_diagonal:
				return True
			if is_horizontal:
				if empty_between_horizontal(self.board, move[0:2], move[2:0]) and not self.move_causes_check():
					return False
				else:
					return True
			if is_vertical:
				if empty_between_vertical(self.board, move[0:2], move[2:0]) and not self.move_causes_check():
					return False
				else:
					return True
		elif piece == "B":
			if not is_diagonal:
				return True

			if empty_between_diagonal(self.board, move[0:2], move[2:0]) and not self.move_causes_check():
				return False
			else:
				return True
		elif piece == "N":
			if is_vertical or is_horizontal or is_diagonal:
				return True

			if erow == srow+2 and ecol == scol + 1 and not self.move_causes_check(): #up two, one right
				return False
			
			if erow == srow+2 and ecol == scol - 1 and not self.move_causes_check():#up two, one left
				return False
			
			if erow == srow-2 and ecol == scol - 1 and not self.move_causes_check():#down two, one left
				return False
			
			if erow == srow-2 and ecol == scol + 1 and not self.move_causes_check():#up two, one right
				return False
			
			if erow == srow+1 and ecol == scol + 2 and not self.move_causes_check(): #up one two right
				return False

			if erow == srow+1 and ecol == scol - 2 and not self.move_causes_check(): #up one two left
				return False

			if erow == srow-1 and ecol == scol + 2 and not self.move_causes_check(): #down one two right
				return False

			if erow == srow-1 and ecol == scol - 2 and not self.move_causes_check(): #down one two left
				return False
			
			return True
		elif piece == "Q":
			if not(is_horizontal and is_diagonal and is_vertical):
				return True
			if is_horizontal:
				if empty_between_horizontal(move[0:2], move[2:]) and not self.move_causes_check():
					return False

			if is_vertical:
				if empty_between_vertical(move[0:2], move[2:]) and not self.move_causes_check():
					return False
			
			if is_diagonal:
				if empty_between_diagonal(move[0:2], move[2:]) and not self.move_causes_check():
					return False
				
			return True
		else:
			if not(is_horizontal and is_diagonal and is_vertical):
				return True	

			if is_vertical:

				if ((erow) != srow+1 or erow != srow-1): #if ending square is not 1 verticla 
						return True
				else:
					if empty_between_vertical(self.board, move[:2], move[2:]) and not self.move_causes_check(): #make sure nothing is in front of pawn
						return False
					else:
						return True

			if is_horizontal:

				if ((ecol) != scol+1 or ecol != scol-1): #if ending square is not 1 horizontal 
						return True
				else:
					if empty_between_horizontal(self.board, move[:2], move[2:]) and not self.move_causes_check(): #make sure nothing is in front of pawn
						return False
					else:
						return True
			if is_diagonal:

				if ((ecol) == scol+1  and erow != erow-1): #bottom right
						if empty_between_diagonal(self.board, move[:2], move[2:]) and not self.move_causes_check(): #make sure nothing is in front of pawn
							return False
				
				if ((ecol) == scol-1  and erow != erow-1): #bottom left 
						if empty_between_diagonal(self.board, move[:2], move[2:]) and not self.move_causes_check(): #make sure nothing is in front of pawn
							return False
				
				if ((ecol) == scol+1  and erow != erow-1): #top left 
						if empty_between_diagonal(self.board, move[:2], move[2:]) and not self.move_causes_check(): #make sure nothing is in front of pawn
							return False
				if ((ecol) == scol+1  and erow != erow+1): #top right
						if empty_between_diagonal(self.board, move[:2], move[2:]) and not self.move_causes_check(): #make sure nothing is in front of pawn
							return False
				
				return True

			

	def _handle_move_capture(self, starting, ending):
		chess_notation = (f"{get_piece(self.board, starting) if get_piece(self.board, starting).lower != 'p' else ''}"
						  f"{starting}"
						  f"{'x' if get_piece(self.board, ending) != '' else ''}"
						  f"{ending}")
		self.board = move_piece(self.board, starting, ending)
		return chess_notation

	def white_king_checked(self, board) -> bool:
		"""
			Function to check if Black King is in check
			Args:
				board: 2D object representing board
			Returns:
				True or False if king is in check
		"""
		# Convert the numeric coordinates to chess notation
		row = str(8 - self.white_king_index[0])
		col = chr(ord('a') + self.white_king_index[1])
		square = col + row
		print(f"White king is at square: {square}")
		return is_square_attacked(board, square, "w")
	
	def black_king_checked(self, board) -> bool:
		"""
			Function to check if Black King is in check
			Args:
				board: 2D object representing board
			Returns:
				True or False if king is in check
		"""
				# Convert the numeric coordinates to chess notation
		row = str(8 - self.black_king_index[0])
		col = chr(ord('a') + self.black_king_index[1])
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
		if self.check_king_path_for_check(self.board):
			return 'w' if self.turn == 'b' else 'b'
		elif self._stalemate():
			return 'd'
		else:
			return ''
		

	