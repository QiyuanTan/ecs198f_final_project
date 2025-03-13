from pickle import FALSE

import pytest

import pytest
from logic.chess_logic import ChessLogic

@pytest.mark.parametrize("board, move, king_moved,expected", [
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
            'e1g1',
            False,
            False
    )
])

def test_is_castling(board, move, king_moved, expected):
    logic = ChessLogic()
    logic.board = board
    logic.castling.white_king_moved = king_moved
    assert logic.castling.applies(logic.board, move) == expected



def test_get_piece():
    from logic.chess_logic import ChessLogic
    logic = ChessLogic()
    logic.board = [
        ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
    ]
    assert logic._get_piece('a1') == 'R'
    assert logic._get_piece('h8') == 'r'
    assert logic._get_piece('e4') ==  ''
    assert logic._get_piece('a2') == 'P'

