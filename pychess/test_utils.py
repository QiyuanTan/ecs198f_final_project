import pytest

def get_initial_board():
    return [
        ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
        ['','','','X','','','',''],
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
    assert get_piece(board, 'd6') == 'X'

def test_str2index():
    from logic.board_utils import str2index
    assert str2index('a1') == (7, 0)
    assert str2index('h8') == (0, 7)
    assert str2index('e4') == (4, 4)
    assert str2index('a2') == (6, 0)

def test_index2str():
    from logic.board_utils import index2str
    assert index2str((7, 0)) == 'a1'
    assert index2str((0, 7)) == 'h8'
    assert index2str((4, 4)) == 'e4'
    assert index2str((6, 0)) == 'a2'
    # assert index2str("a1") == "a1"

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
    from logic.board_utils import empty_between_horizontal, str2index
    board = get_initial_board()
    index = str2index('e4')
    board[index[0]][index[1]] = "p"
    assert empty_between_horizontal(board, 'a1', 'h1') == False
    assert empty_between_horizontal(board, 'c3', 'g3') == True
    assert empty_between_horizontal(board, 'b4', 'd4') == True
    assert empty_between_horizontal(board, 'e4', 'g4') == True
    try:
        empty_between_horizontal(board, 'a1', 'h1')
    except Exception as e:
        assert isinstance(e, ValueError)

def test_empty_between_vertical():
    from logic.board_utils import empty_between_vertical
    board = get_initial_board()
    assert empty_between_vertical(board, 'a1', 'a8') == False
    assert empty_between_vertical(board, 'c3', 'c6') == True
    assert empty_between_vertical(board, 'b4', 'b6') == True
    assert empty_between_vertical(board, 'b2', 'b6') == True
    try:
        empty_between_vertical(board, 'a1', 'h1')
    except Exception as e:
        assert isinstance(e, ValueError)

def test_empty_between_diagonal():
    from logic.board_utils import empty_between_diagonal
    board = get_initial_board()
    assert empty_between_diagonal(board, 'a1', 'h8') == False
    assert empty_between_diagonal(board, 'c3', 'f6') == True
    assert empty_between_diagonal(board, 'b4', 'd2') == False
    assert empty_between_diagonal(board, 'b4', 'c3') == True
    try:
        empty_between_diagonal(board, 'a1', 'h1')
    except Exception as e:
        assert isinstance(e, ValueError)

@pytest.mark.parametrize("board, square, color, expected", [
    (
        [
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','K','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','','']
        ],
        'e4',
        'w',
        False
    ),
    (
        [
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','r','','K','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','','']
        ],
        'e4',
        'w',
        True
    ),
    (
        [
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','q','','','','',''],
            ['','','','','','','',''],
            ['','','','','K','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','','']
        ],
        'e4',
        'w',
        True
    ),
    (
        [
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','p','','','',''],
            ['','','','','K','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','','']
        ],
        'e4',
        'w',
        True
    ),
    (
        [
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','k','','',''],
            ['','','','','','P','',''],
            ['','','','','','','',''],
            ['','','','','','','','']
        ],
        'e4',
        'b',
        True
    ),
    (
        [
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','n','','','','',''],
            ['','','','','K','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','','']
        ],
        'e4',
        'w',
        True
    ),
    (
        [
            ['','','','','','','',''],
            ['','b','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','K','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','','']
        ],
        'e4',
        'w',
        True
    ),
    (
        [
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','r','p','','K','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','','']
        ],
        'e4',
        'w',
        False
    ),
    (
        [
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','q','n','K','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','','']
        ],
        'e4',
        'w',
        False
    ),
    (
        [
            ['','','','','','','',''],
            ['','b','','','','','',''],
            ['','','Q','','','','',''],
            ['','','','','','','',''],
            ['','','','','K','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','','']
        ],
        'e4',
        'w',
        False
    ),
    (
        [
            ['','','','','','','',''],
            ['','b','','','','','',''],
            ['','','Q','','','','',''],
            ['','','','','p','','',''],
            ['','','','','K','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','','']
        ],
        'e4',
        'w',
        False
    ),
    (
        [
            ['','','','','','','',''],
            ['','b','','','','','',''],
            ['','','Q','','','','',''],
            ['','','','','','','',''],
            ['','','','','K','','',''],
            ['','','n','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','','']
        ],
        'e4',
        'w',
        True
    ),
    (
        [
            ['','','','','','','',''],
            ['','b','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','k','','',''],
            ['','','','','','','',''],
            ['','','','','','N','',''],
            ['','','','','','','','']
        ],
        'e4',
        'b',
        True
    ),
])
def test_is_square_attacked(board, square, color, expected):
    from logic.board_utils import is_square_attacked
    assert is_square_attacked(board, square, color) == expected

def test_pawn_moves():
    from logic.board_utils import pawn_moves
    board = [
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','X','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','','']
    ]
    assert set(pawn_moves(board, 4, 3, 'w')) == {(3, 3), (3, 2), (3, 4)}
    assert set(pawn_moves(board, 4, 3, 'b')) == {(5,3), (5,2), (5,4)}

    board = [
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','X','','','',''],
        ['','','','','','','','']
    ]
    assert set(pawn_moves(board, 6, 3, 'w')) == {(5,3), (5,2), (5,4), (4, 3)}

def test_rook_moves():
    from logic.board_utils import rook_moves
    board = [
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','X','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','','']
    ]

    for move in rook_moves(board, 4, 3, 'w'):
        board[move[0]][move[1]] = 'x'

    assert board == [
        ['','','','x','','','',''],
        ['','','','x','','','',''],
        ['','','','x','','','',''],
        ['','','','x','','','',''],
        ['x','x','x','X','x','x','x','x'],
        ['','','','x','','','',''],
        ['','','','x','','','',''],
        ['','','','x','','','','']
    ]

def test_bis_moves():
    from logic.board_utils import bishop_moves
    board = [
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','X','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','','']
    ]

    for move in bishop_moves(board, 4, 3, 'w'):
        board[move[0]][move[1]] = 'x'

    assert board == [
        ['','','','','','','','x'],
        ['x','','','','','','x',''],
        ['','x','','','','x','',''],
        ['','','x','','x','','',''],
        ['','','','X','','','',''],
        ['','','x','','x','','',''],
        ['','x','','','','x','',''],
        ['x','','','','','','x','']
    ]

def test_knight_moves():
    from logic.board_utils import knight_moves
    board = [
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','X','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','','']
    ]

    for move in knight_moves(board, 4, 3, 'w'):
        board[move[0]][move[1]] = 'x'

    assert board == [
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','x','','x','','',''],
        ['','x','','','','x','',''],
        ['','','','X','','','',''],
        ['','x','','','','x','',''],
        ['','','x','','x','','',''],
        ['','','','','','','','']
    ]

def test_queen_moves():
    from logic.board_utils import queen_moves
    board = [
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','X','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','','']
    ]

    for move in queen_moves(board, 4, 3, 'w'):
        board[move[0]][move[1]] = 'x'

    assert board == [
        ['', '', '', 'x','','','','x'],
        ['x', '', '', 'x','','','x',''],
        ['', 'x', '', 'x','','x','',''],
        ['', '', 'x', 'x','x','','',''],
        ['x','x','x','X','x','x','x','x'],
        ['', '', 'x', 'x','x','','',''],
        ['', 'x', '', 'x','','x','',''],
        ['x', '', '', 'x','','','x','']
    ]

def test_king_moves():
    from logic.board_utils import king_moves
    board = [
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','X','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','','']
    ]

    for move in king_moves(board, 4, 3, 'w'):
        board[move[0]][move[1]] = 'x'

    assert board == [
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','x','x','x','','',''],
        ['','','x','X','x','','',''],
        ['','','x','x','x','','',''],
        ['','','','','','','',''],
        ['','','','','','','','']
    ]