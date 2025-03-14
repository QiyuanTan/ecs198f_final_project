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

