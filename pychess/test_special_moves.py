import pytest
from logic.chess_logic import ChessLogic

@pytest.mark.parametrize("board, move, white_castling_allowed, black_castling_allowed, expected", [
    # allowed
    (
        [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', '', '', '', 'K', 'B', 'N', 'R'],
        ],
        'e1c1',
        True,
        True,
        True
    ),
    # blocked
    (
        [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', '', 'B', '', 'K', '', 'N', 'R'],
        ],
        'e1c1',
        True,
        True,
        False
    ),
    # king moved
    (
        [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', '', '', '', 'K', 'B', 'N', 'R'],
        ],
        'e1c1',
        False,
        True,
        False
    ),
    # not a castling move
    (
        [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', '', '', '', 'K', 'B', 'N', 'R'],
        ],
        'e2e4',
        True,
        True,
        False
    ),
    # valid black castling
    (
        [
            ['r', '', '', '', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', '', 'B', 'N', 'R'],
        ],
        'e8c8',
        True,
        True,
        True
    ),
    # blocked black castling
    (
        [
            ['r', '', 'b', '', 'k', '', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', '', 'B', 'N', 'R'],
        ],
        'e8c8',
        True,
        True,
        False
    ),
    # black king moved
    (
        [
            ['r', '', '', '', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', '', 'B', 'N', 'R'],
        ],
        'e8c8',
        True,
        False,
        False
    ),
    # black castling king side
    (
        [
            ['r', '', '', '', 'k', '', '', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', '', 'B', 'N', 'R'],
        ],
        'e8g8',
        True,
        True,
        True
    ),
    # causes a check
    (
        [
            ['', '', '', '', 'k', '', '', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'R', 'p'],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', '', '', '', 'K', 'B', 'N', 'R'],
        ],
        'e8g8',
        True,
        True,
        False
    ),
])
def test_castling_applies(board, move, white_castling_allowed, black_castling_allowed, expected):
    from logic.chess_logic import ChessLogic
    logic = ChessLogic()
    logic.board = board
    logic.castling.white_castling_allowed = white_castling_allowed
    logic.castling.back_castling_allowed = black_castling_allowed
    assert logic.castling.applies(logic.board, move) == expected
    
def test_en_passant():
    logic = ChessLogic()
    logic.play_move("e2e4")  # White moves pawn two squares
    logic.play_move("d7d5")  # Black moves pawn two squares
    logic.play_move("e4e5")  # White advances pawn one square
    logic.play_move("d5e4")  # Black captures via En Passant
    assert logic.play_move("d5e4") == "d5xe4"
