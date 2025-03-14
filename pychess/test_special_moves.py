import pytest

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
            False
    ),
])
def test_is_castling(board, move, king_moved, expected):
    from logic.chess_logic import ChessLogic
    logic = ChessLogic()
    logic.board = board
    logic.castling.white_king_moved = king_moved
    assert logic.castling.applies(logic.board, move) == expected