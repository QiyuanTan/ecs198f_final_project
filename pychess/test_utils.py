import pytest

def test_get_piece():
    from logic.board_utils import get_piece
    board = [
        ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
    ]
    assert get_piece(board, 'a1') == 'R'
    assert get_piece(board, 'h8') == 'r'
    assert get_piece(board, 'e4') ==  ''
    assert get_piece(board, 'a2') == 'P'

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

def test_str2index():
    from logic.board_utils import str2index
    assert str2index('a1') == (7, 0)
    assert str2index('h8') == (0, 7)
    assert str2index('e4') == (4, 4)
    assert str2index('a2') == (6, 0)

def test_move_piece():
    from logic.board_utils import move_piece
    board = [
        ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
    ]
    move_piece(board, 'a2', 'a4')
    assert board[6][0] == ''
    assert board[4][0] == 'P'
    move_piece(board, 'e1', 'e2')
    assert board[7][4] == ''
    assert board[6][4] == 'K'