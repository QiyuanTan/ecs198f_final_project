import pytest

def get_initial_board():
    return [
        ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
    ]

def test_get_piece():
    from logic.board_utils import get_piece
    board = get_initial_board()
    assert get_piece(board, 'a1') == 'R'
    assert get_piece(board, 'h8') == 'r'
    assert get_piece(board, 'e4') ==  ''
    assert get_piece(board, 'a2') == 'P'

def test_str2index():
    from logic.board_utils import str2index
    assert str2index('a1') == (7, 0)
    assert str2index('h8') == (0, 7)
    assert str2index('e4') == (4, 4)
    assert str2index('a2') == (6, 0)

def test_move_piece():
    from logic.board_utils import move_piece
    board = get_initial_board()
    move_piece(board, 'a2', 'a4')
    assert board[6][0] == ''
    assert board[4][0] == 'P'
    move_piece(board, 'e1', 'e2')
    assert board[7][4] == ''
    assert board[6][4] == 'K'

def test_is_horizontal_move():
    from logic.board_utils import is_horizontal_move
    assert is_horizontal_move('a1', 'h1') == True
    assert is_horizontal_move('a1', 'a8') == False
    assert is_horizontal_move('a1', 'h8') == False
    assert is_horizontal_move('a1', 'b1') == True

def test_is_vertical_move():
    from logic.board_utils import is_vertical_move
    assert is_vertical_move('a1', 'a8') == True
    assert is_vertical_move('a1', 'h1') == False
    assert is_vertical_move('h5', 'h8') == True
    assert is_vertical_move('a1', 'b1') == False

def test_is_diagonal_move():
    from logic.board_utils import is_diagonal_move
    assert is_diagonal_move('a1', 'h8') == True
    assert is_diagonal_move('b2', 'c1') == True
    assert is_diagonal_move('a1', 'h1') == False
    assert is_diagonal_move('a1', 'a8') == False

def test_empty_between_horizontal():
    from logic.board_utils import empty_between_horizontal
    board = get_initial_board()
    assert empty_between_horizontal(board, 'a1', 'h1') == False
    assert empty_between_horizontal(board, 'c3', 'g3') == True
    try:
        empty_between_horizontal(board, 'a1', 'h1')
    except Exception as e:
        assert isinstance(e, ValueError)

def test_empty_between_vertical():
    from logic.board_utils import empty_between_vertical
    board = get_initial_board()
    assert empty_between_vertical(board, 'a1', 'a8') == False
    assert empty_between_vertical(board, 'c3', 'c6') == True
    try:
        empty_between_vertical(board, 'a1', 'h1')
    except Exception as e:
        assert isinstance(e, ValueError)

def test_empty_between_diagonal():
    from logic.board_utils import empty_between_diagonal
    board = get_initial_board()
    assert empty_between_diagonal(board, 'a1', 'h8') == False
    assert empty_between_diagonal(board, 'c3', 'f6') == True
    try:
        empty_between_diagonal(board, 'a1', 'h1')
    except Exception as e:
        assert isinstance(e, ValueError)