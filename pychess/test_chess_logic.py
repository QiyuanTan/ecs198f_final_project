import pytest
from logic.chess_logic import ChessLogic
from logic.board_utils import is_square_attacked

@pytest.fixture
def new_game():
    """Initialize a new chess game"""
    return ChessLogic()

# ========================== Basic Move Tests ========================== #
@pytest.mark.parametrize("move, expected", [
    ("e2e4", "Pe2e4"),  # Normal pawn move
    ("g1f3", "Ng1f3"),  # Normal knight move
    ("f1c4", "Bf1c4"),  # Diagonal bishop move
    ("d1h5", "Qd1h5"),  # Horizontal queen move
    ("a1a3", "Ra1a3"),  # Vertical rook move
])
def test_valid_moves(new_game, move, expected):
    """Test valid piece movements"""
    assert new_game.play_move(move) == expected

# ========================== Invalid Move Tests ========================== #
@pytest.mark.parametrize("move", [
    "e2e5",  # Pawn moving too far
    "g1g3",  # Knight non-L move
    "f1b5",  # Bishop non-diagonal move
    "d1d4",  # Queen moving through pieces
    "a1a4",  # Rook moving through pieces
])
def test_invalid_moves(new_game, move):
    """Test invalid piece movements"""
    assert new_game.play_move(move) == ""

# ========================== _invalid_move Method Tests ========================== #
@pytest.mark.parametrize("move, expected", [
    # Invalid starting pieces
    ("e3e4", True),  # Empty square
    ("a7a6", True),  # Black piece (White's turn)
    
    # Invalid pawn moves
    ("e2e5", True),  # Pawn moving more than two squares
    ("e2d3", True),  # Pawn diagonal move (without capture)
    ("e2e3e4", True),  # Format error
    
    # Invalid rook moves
    ("a1b2", True),  # Rook diagonal move
    ("a1a4", True),  # Rook moving through other pieces
    
    # Invalid bishop moves
    ("c1d2e3", True),  # Format error
    ("c1e2", True),  # Bishop non-diagonal move
    
    # Invalid knight moves
    ("b1b3", True),  # Knight straight move
    ("b1c4", True),  # Knight move not in L-shape
    
    # Invalid queen moves
    ("d1d3", True),  # Queen moving through other pieces
    ("d1f3", True),  # Queen moving through other pieces
    
    # Invalid king moves
    ("e1e3", True),  # King moving more than one square
    ("e1c1", False),  # Castling (should be handled by Castling class, should return False)
])
def test_invalid_move_method(new_game, move, expected):
    """Test the _invalid_move method"""
    assert new_game._invalid_move(move) == expected

# ========================== Specific Piece Invalid Move Tests ========================== #
def test_pawn_invalid_moves():
    """Test invalid pawn moves"""
    logic = ChessLogic()
    # Set up a simple board
    logic.board = [
        ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','P','','','',''],
        ['P', 'P', 'P', '', 'P', 'P', 'P', 'P'],
        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
    ]
    
    # Pawn moving backward
    assert logic._invalid_move("d3d4") == True
    
    # Pawn diagonal move (without capture)
    assert logic._invalid_move("d3c4") == True
    assert logic._invalid_move("d3e4") == True
    
    # Pawn moving more than one square (not from starting position)
    assert logic._invalid_move("d3d1") == True

def test_knight_invalid_moves():
    """Test invalid knight moves"""
    logic = ChessLogic()
    
    # Knight straight move
    assert logic._invalid_move("g1g3") == True
    
    # Knight diagonal move
    assert logic._invalid_move("g1e3") == True
    
    # Knight move not in L-shape
    assert logic._invalid_move("g1h4") == True

def test_bishop_invalid_moves():
    """Test invalid bishop moves"""
    logic = ChessLogic()
    
    # Bishop straight move
    assert logic._invalid_move("f1f3") == True
    
    # Bishop non-diagonal move
    assert logic._invalid_move("f1e4") == True
    
    # Bishop moving through other pieces
    assert logic._invalid_move("f1a6") == True

def test_rook_invalid_moves():
    """Test invalid rook moves"""
    logic = ChessLogic()
    
    # Rook diagonal move
    assert logic._invalid_move("a1b2") == True
    
    # Rook moving through other pieces
    assert logic._invalid_move("a1a6") == True

def test_queen_invalid_moves():
    """Test invalid queen moves"""
    logic = ChessLogic()
    
    # Queen moving through other pieces (straight)
    assert logic._invalid_move("d1d6") == True
    
    # Queen moving through other pieces (diagonal)
    assert logic._invalid_move("d1h5") == True
    
    # Queen illegal move (neither straight nor diagonal)
    assert logic._invalid_move("d1e3") == True

def test_king_invalid_moves():
    """Test invalid king moves"""
    logic = ChessLogic()
    
    # King moving more than one square
    assert logic._invalid_move("e1e3") == True
    assert logic._invalid_move("e1c3") == True
    
    # King moving to an attacked square
    logic.board = [
        ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
        ['p', 'p', 'p', 'p', '', 'p', 'p', 'p'],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','r','','',''],
        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
    ]
    assert logic._invalid_move("e1e2") == True  # King moving to a square attacked by a rook

# ========================== Capture Tests ========================== #
def test_capture():
    """Test piece capture"""
    logic = ChessLogic()
    # Set up a simple capture scenario
    logic.board = [
        ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
        ['p', 'p', 'p', '', 'p', 'p', 'p', 'p'],
        ['','','','','','','',''],
        ['','','','p','','','',''],
        ['','','','P','','','',''],
        ['','','','','','','',''],
        ['P', 'P', 'P', '', 'P', 'P', 'P', 'P'],
        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
    ]
    # White captures black pawn
    assert logic.play_move("d4xd5") == "Pd4xd5"
    # Confirm black pawn is captured
    assert logic.board[3][3] == "P"
    assert logic.board[4][3] == ""

# ========================== Castling Tests ========================== #

def test_queenside_castling():
    """Test queenside castling (long castling)"""
    logic = ChessLogic()
    # Set up a board suitable for queenside castling
    logic.board = [
        ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
        ['R', '', '', '', 'K', 'B', 'N', 'R'],
    ]
    # Execute queenside castling
    assert logic.play_move("e1c1") == "O-O-O"
    # Verify king and rook new positions
    assert logic.board[7][2] == "K"  # King moved to c1
    assert logic.board[7][3] == "R"  # Rook moved to d1
    assert logic.board[7][4] == ""   # e1 is empty
    assert logic.board[7][0] == ""   # a1 is empty

def test_castling_invalid_when_king_moved():
    """Test castling is invalid after king has moved"""
    logic = ChessLogic()
    # Set up the board
    logic.board = [
        ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
        ['R', '', '', '', 'K', '', '', 'R'],
    ]
    # Set king has moved
    logic.castling.white_castling_allowed = False
    # Attempt castling
    assert logic.play_move("e1g1") == ""
    # Verify board hasn't changed
    assert logic.board[7][4] == "K"
    assert logic.board[7][7] == "R"

# ========================== Pawn Promotion Tests ========================== #
def test_pawn_promotion_white():
    """Test white pawn promotion"""
    logic = ChessLogic()
    # Set up a white pawn about to promote
    logic.board = [
        ['r', 'n', 'b', '', 'k', 'b', 'n', 'r'],
        ['p', 'p', 'p', 'p', 'P', 'p', 'p', 'p'],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['P', 'P', 'P', 'P', '', 'P', 'P', 'P'],
        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
    ]
    # Execute promotion
    assert logic.play_move("e7e8=Q") == "Pe7e8=Q"
    # Confirm e8 now has a white queen
    assert logic.board[0][4] == "Q"

def test_pawn_promotion_black():
    """Test black pawn promotion"""
    logic = ChessLogic()
    # Set up a black pawn about to promote
    logic.board = [
        ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
        ['p', 'p', 'p', 'p', '', 'p', 'p', 'p'],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['P', 'P', 'P', 'P', 'p', 'P', 'P', 'P'],
        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
    ]
    logic.turn = 'b'  # Set black's turn
    # Execute promotion
    assert logic.play_move("e2e1=Q") == "pe2e1=Q"
    # Confirm e1 now has a black queen
    assert logic.board[7][4] == "q"

# ========================== En Passant Tests ========================== #
def test_en_passant():
    """Test en passant capture"""
    logic = ChessLogic()
    # Set up board state
    logic.board = [
        ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
        ['p', 'p', 'p', '', 'p', 'p', 'p', 'p'],
        ['','','','','','','',''],
        ['','','','p','P','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['P', 'P', 'P', 'P', '', 'P', 'P', 'P'],
        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
    ]
    # Record last move for en_passant class to check
    logic.en_passant.last_move = "d7d5"
    
    # White captures en passant
    assert logic.play_move("e5d6") == "Pe5xd6"
    # Confirm black pawn is captured
    assert logic.board[3][3] == ""  # d5 should be empty
    # Confirm white pawn moved to correct position
    assert logic.board[2][3] == "P"  # d6 should have white pawn


# ========================== Check Detection Tests ========================== #
def test_check_detection_extended():
    game = ChessLogic()
    game.board = [
        ['', '', '', '', 'k', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', 'R', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', 'K', '', '', '']
    ]
    assert is_square_attacked(game.board, "e8", "b") == True 
  
    game.board = [
        ['', '', '', '', 'k', '', '', ''],
        ['', 'b', '', '', '', '', '', ''],
        ['', '', 'P', '', '', '', '', ''],  
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', 'K', '', '', ''],  
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '']
    ]
    assert is_square_attacked(game.board, "e1", "w") == False  

    game.board = [
        ['', '', '', '', 'k', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['R', '', '', '', 'K', '', '', 'R'], 
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '']
    ]
    assert is_square_attacked(game.board, "e5", "b") == True  


    game.board = [
        ['', '', '', '', '', '', '', ''],
        ['', '', '', 'n', '', 'b', '', ''], 
        ['', '', '', '', 'k', '', '', ''],    
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', 'K', '', '', ''],   
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '']
    ]
    assert is_square_attacked(game.board, "e4", "w") == True 

def test_edge_case_checks():

    game = ChessLogic()
    game.board = [
        ['k', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', 'Q', '', '']  
    ]
    assert is_square_attacked(game.board, "a8", "b") == True 

    game.board = [
        ['', '', '', '', 'k', '', '', ''],
        ['', '', '', '', '', '', '', 'p'], 
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', 'K', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['P', '', '', '', '', '', '', ''], 
        ['', '', '', '', '', '', '', '']
    ]

    assert is_square_attacked(game.board, "e4", "w") == False 
    assert is_square_attacked(game.board, "g8", "b") == True 

def test_complex_check_scenarios():

    game = ChessLogic()
    game.board = [
        ['', '', '', '', '', '', '', 'k'],
        ['', '', '', 'q', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', 'r', '', '', '', 'b', '', ''],  
        ['', '', '', '', 'K', '', '', ''], 
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '']
    ]
    assert is_square_attacked(game.board, "e4", "w") == True

    game.board = [
        ['', '', '', '', 'k', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', 'B', '', '', '', '', ''], 
        ['', '', '', 'p', '', '', '', ''],  
        ['', '', '', '', 'K', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '']
    ]
    assert is_square_attacked(game.board, "e8", "b") == False 

def test_special_check_cases():

    game = ChessLogic()
    game.board = [
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', 'k', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', 'K', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '']
    ]

    assert is_square_attacked(game.board, "e4", "w") == True

    game.board = [
        ['', '', '', '', 'k', '', '', 'Q'],  
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', 'K', '', '', ''], 
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '']
    ]
    assert is_square_attacked(game.board, "e8", "b") == True  



# ========================== Invalid Starting Piece Tests ========================== #
@pytest.mark.parametrize("piece, turn, expected", [
    ('r', 'w', True),   # White's turn, black rook is invalid starting piece
    ('r', 'b', False),  # Black's turn, black rook is valid starting piece
    ('R', 'w', False),  # White's turn, white rook is valid starting piece
    ('R', 'b', True),   # Black's turn, white rook is invalid starting piece
    ('p', 'w', True),   # White's turn, black pawn is invalid starting piece
    ('p', 'b', False),  # Black's turn, black pawn is valid starting piece
    ('P', 'w', False),  # White's turn, white pawn is valid starting piece
    ('P', 'b', True),   # Black's turn, white pawn is invalid starting piece
    ('', 'w', True),    # Empty square is always invalid starting piece
    ('', 'b', True),    # Empty square is always invalid starting piece
])
def test_invalid_starting_piece(piece, turn, expected):
    """Test invalid starting piece check"""
    logic = ChessLogic()
    logic.turn = turn
    assert logic._invalid_starting_piece(piece) == expected

def test_no_valid_moves():
    logic = ChessLogic()
    logic.black_king_index = (4, 3)
    logic.board = [
        ['','','','R','','','',''],
        ['','','','','','','',''],
        ['','B','','r','','B','',''],
        ['','','','','','','',''],
        ['','R','','k','','','',''],
        ['','R','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','','']
    ]
    assert logic._no_valid_moves('b') == True

    logic.board = [
        ['','' ,'','','','','',''],
        ['','K','','R','','K','',''],
        ['','' ,'','r','','','',''],
        ['','', '','','','','',''],
        ['','', '','k','','','',''],
        ['','R','','','','','',''],
        ['','', '','','','','',''],
        ['','', 'R','','R','','','']
    ]
    assert logic._no_valid_moves('b') == False


def test_invalid_move():
    logic = ChessLogic()
    logic.board = [
        ['','' ,'','','','','',''],
        ['','K','','R','','K','',''],
        ['','' ,'','r','','','',''],
        ['','', '','','','','',''],
        ['','', '','k','','','',''],
        ['','R','','','','','',''],
        ['','', '','','','','',''],
        ['','', 'R','','R','','','']
    ]
    logic.black_king_index = (4, 3)
    assert logic.invalid_move(logic.board, 'd6d5', 'b') == False
    assert logic.invalid_move(logic.board, 'd6d7', 'b') == False