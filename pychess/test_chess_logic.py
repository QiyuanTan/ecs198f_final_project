import unittest


class TestCases(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)  # add assertion here

class TestUtils(unittest.TestCase):
    def test_get_piece(self):
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
        self.assertEqual(logic._get_piece('a1'), 'R')
        self.assertEqual(logic._get_piece('h8'), 'r')
        self.assertEqual(logic._get_piece('e4'), '')
        self.assertEqual(logic._get_piece('a2'), 'P')


if __name__ == '__main__':
    unittest.main()
