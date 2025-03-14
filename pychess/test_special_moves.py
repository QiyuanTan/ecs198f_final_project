import pytest
from logic.chess_logic import ChessLogic

@pytest.mark.parametrize("board, move, white_king_moved, black_king_moved, expected", [
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
            False,
            False,
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
            False,
            False,
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
            True,
            False,
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
            False,
            False,
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
            False,
            False,
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
            False,
            False,
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
            False,
            True,
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
            False,
            False,
            True
    ),
    # causes a check
    (
            [
                ['', '', '', '', 'k', '', '', 'r'],
                ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                ['','','','','','','',''],
                ['','','','','','','',''],
                ['','','','','','','',''],
                ['','','','','','','',''],
                ['P', 'P', 'r', 'P', 'P', 'P', 'P', 'P'],
                ['R', '', '', '', 'K', 'B', 'N', 'R'],
            ],
            'e8g8',
            False,
            False,
            False
    ),
])
def test_castling_applies(board, move, white_king_moved, black_king_moved, expected):
    from logic.chess_logic import ChessLogic
    logic = ChessLogic()
    logic.board = board
    logic.castling.white_king_moved = white_king_moved
    logic.castling.black_king_moved = black_king_moved
    assert logic.castling.applies(logic.board, move) == expected
    
def test_en_passant():
    logic = ChessLogic()
    logic.play_move("e2e4")  # White moves pawn two squares
    logic.play_move("d7d5")  # Black moves pawn two squares
    logic.play_move("e4e5")  # White advances pawn one square
    logic.play_move("d5e4")  # Black captures via En Passant
    assert logic.play_move("d5e4") == "d5xe4"
