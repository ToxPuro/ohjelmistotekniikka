import unittest
from move import Move
from setting import Setting
from board import Board
from generate import generate_initial_state


class TestMove(unittest.TestCase):
    def setUp(self):
        setting = Setting()
        initial_state, pieces = generate_initial_state(setting)
        self.board = Board(initial_state, pieces)

    def test_equality_works(self):
        move1 = Move((1,1), (2,2), self.board)
        move2 = Move((1,1), (2,2), self.board)
        move3 = Move((2,2), (1,1), self.board)
        move4 = "Trust me I am a move"
        self.assertEqual(move1 == move2, True)
        self.assertEqual(move1 == move3, False)
        self.assertEqual(move1 == move4, False)

    def test_double_pawn_forward_works(self):
        move = Move((1,1), (3,1), self.board)
        self.assertEqual(move.is_double_pawn_forward, True)

    def test_pawn_promotion_works(self):
        move = Move((6,6), (7,6), self.board)
        self.assertEqual(move.is_pawn_promotion, True)

    def test_str_is_correct(self):
        move = Move((6,6), (7,6), self.board)
        self.assertEqual(str(move), "6, 6, 6, 7")
