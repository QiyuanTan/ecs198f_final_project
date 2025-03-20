import pytest
from logic.chess_logic import ChessLogic
from logic.special_moves import Promotion
from logic.special_moves import EnPassant
from logic.special_moves import Castling
from logic.board_utils import get_piece

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
# def test_castling_applies(board, move, white_castling_allowed, black_castling_allowed, expected):
#     from logic.chess_logic import ChessLogic
#     logic = ChessLogic()
#     logic.board = board
#     logic.castling.white_castling_allowed = white_castling_allowed
#     logic.castling.back_castling_allowed = black_castling_allowed
#     assert logic.castling.applies(logic.board, move) == expected
    
# def test_en_passant():
#     logic = ChessLogic()
#     logic.play_move("e2e4")  # White moves pawn two squares
#     logic.play_move("d7d5")  # Black moves pawn two squares
#     logic.play_move("e4e5")  # White advances pawn one square
#     logic.play_move("d5e4")  # Black captures via En Passant
#     assert logic.play_move("d5e4") == "d5xe4"

def test_castling():
    castling = Castling()
    board = [
        ["r", "", "", "", "k", "", "", "r"],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["R", "", "", "", "K", "", "", "R"],
    ]
    assert castling.applies(board, "e1g1") is True
    castling.handle(board, "e1g1")
    assert get_piece(board, "g1") == "K"
    assert get_piece(board, "f1") == "R"

def test_en_passant():
    en_passant = EnPassant()
    en_passant.last_move = "e7e5"  
    board = [
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "p", "", "", ""],  
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "P", "", "", ""], 
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
    ]
    assert en_passant.applies(board, "e4d5") is True 
    en_passant.handle(board, "e4d5")
    assert get_piece(board, "e5") == "" 

def test_promotion():
    promotion = Promotion()
    board = [
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "P", "", "", ""], 
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
    ]
    assert promotion.applies(board, "a7a8") is True
    promotion.handle(board, "a7a8")
    assert get_piece(board, "a8") == "Q"