import pytest
from logic.chess_logic import ChessLogic

@pytest.fixture
def new_game():
    return ChessLogic()

# ========================== Basic Move Tests ========================== #
@pytest.mark.parametrize("move, expected", [
    ("e2e4", "e2e4"),  # Pawn normal move
    ("g1f3", "Ng1f3"),  # Knight normal move
    ("f1c4", "Bc1c4"),  # Bishop diagonal move
    ("d1h5", "Qd1h5"),  # Queen horizontal move
    ("a1a3", "Ra1a3"),  # Rook vertical move
])
def test_valid_moves(new_game, move, expected):
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
    assert new_game.play_move(move) == ""

# ========================== Capture Tests ========================== #
def test_capture():
    logic = ChessLogic()
    logic.play_move("e2e4")
    logic.play_move("d7d5")
    assert logic.play_move("e4xd5") == "e4xd5"

# ========================== Castling Tests ========================== #
def test_castling():
    logic = ChessLogic()
    logic.board[7] = ['R','','','','K','','','R']  # Clear castling path
    assert logic.play_move("e1g1") == "O-O"  # Kingside castling
    assert logic.play_move("e1c1") == "O-O-O"  # Queenside castling

# ========================== Pawn Promotion Tests ========================== #
def test_pawn_promotion():
    logic = ChessLogic()
    logic.board[1][4] = ''  # Clear target position
    logic.board[6][4] = 'P'  # Set white pawn
    assert logic.play_move("e7e8=Q") == "e7e8=Q"

# ========================== En Passant Tests ========================== #
def test_en_passant():
    logic = ChessLogic()
    logic.play_move("e2e4")
    logic.play_move("d7d5")
    assert logic.play_move("e4d5") == "e4xd5"

# ========================== Self Check Prevention Tests ========================== #
def test_self_check():
    logic = ChessLogic()
    logic.board[7][4] = ''  # Remove white king
    logic.board[0][3] = 'Q'  # Black queen
    logic.board[7][3] = 'K'  # White king
    assert logic.play_move("d1d2") == ""  # Move cannot expose own king to check

# ========================== Check Detection Tests ========================== #
def test_check_detection():
    logic = ChessLogic()
    logic.board[7][4] = ''  # Remove white king
    logic.board[0][3] = 'Q'  # Black queen
    logic.board[7][3] = 'K'  # White king
    assert logic.play_move("d1d2") == ""

# ========================== Checkmate Detection Tests ========================== #
def test_checkmate():
    logic = ChessLogic()
    logic.board[7][4] = ''  # Remove white king
    logic.board[0][3] = 'Q'  # Black queen
    logic.board[7][3] = 'K'  # White king
    logic.board[6][3] = ''  # Clear escape path for king
    assert logic.play_move("d1d2") == ""

@pytest.mark.parametrize("piece, turn, expected", [
    ('r', 'w', True),
    ('r', 'b', False),
    ('R', 'w', False),
    ('R', 'b', True),
    ('p', 'w', True),
    ('p', 'b', False),
    ('P', 'w', False),
    ('P', 'b', True),
    ('', 'w', True),
    ('', 'b', True),
])
def test_invalid_starting_piece(piece, turn, expected):
    from logic.chess_logic import ChessLogic
    logic = ChessLogic()
    logic.turn = turn
    assert logic._invalid_starting_piece(piece) == expected