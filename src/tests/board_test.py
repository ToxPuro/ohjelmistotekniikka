import unittest
from board import Board
from setting import Setting
from generate import generate_initial_state

class TestBoard(unittest.TestCase):

    def setUp(self):
        setting = Setting()
        initial_state, pieces = generate_initial_state(setting)
        self.board = Board(initial_state, pieces)

    def test_swap_turns_works(self):
        self.assertEqual(self.board.turn, 1)
        self.board.swap_turns()
        self.assertEqual(self.board.turn, 2)
        self.board.swap_turns()
        self.assertEqual(self.board.turn, 1)

    def test_correctly_notices_checkmate(self):
        setting = Setting()
        setting.initial_state = [
              ["bK", "bR", "bR", "bR", "bR", "bR", "bR", "bR"],
              ["empty" for i in range(8)],
              ["empty" for i in range(8)],
              ["empty" for i in range(8)],
              ["empty" for i in range(8)],
              ["empty"for i in range(8)],
              ["empty" for i in range(8)],
              ["empty", "empty", "empty", "wp", "wK", "wp", "empty", "empty"]
        ]
        initial_state, pieces = generate_initial_state(setting)
        check_mate_board = Board(initial_state, pieces)
        self.assertEqual(check_mate_board.checkmate(), True)

    def test_correctly_notices_stalemate(self):
        setting = Setting()
        setting.initial_state = [
              ["bK", "bR", "bR", "bR", "empty", "bR", "bR", "bR"],
              ["empty" for i in range(8)],
              ["empty" for i in range(8)],
              ["empty" for i in range(8)],
              ["empty" for i in range(8)],
              ["empty"for i in range(8)],
              ["bR", "empty", "empty", "empty", "empty", "empty", "empty", "empty"],
              ["bR", "empty", "empty", "wp", "wK", "wp", "empty", "bR"]
        ]
        initial_state, pieces = generate_initial_state(setting)
        check_mate_board = Board(initial_state, pieces)
        self.assertEqual(check_mate_board.stalemate(), True)


