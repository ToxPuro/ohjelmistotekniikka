import unittest
from rules import Castling, CombinedSlide, CombinedSlidingAttack, Jump, JumpAttack, SingleSlide, EnPassant
from pieces import EnPassantSquare, Piece
from setting import Setting
from generate import generate_initial_state
from board import Board
from move import Move


class TestRules(unittest.TestCase):
    def setUp(self):
        setting = Setting()
        setting.initial_state = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["wR", "wN", "wB", "wQ", "empty", "wB", "wN", "wR"],
            ["wR", "wN", "wB", "bQ", "wK", "wB", "wN", "wR"],
            ["wR", "wN", "wB", "wQ", "empty", "wB", "wN", "wR"],
            ["empty" for i in range(8)],
            ["empty"for i in range(8)],
            ["wp" for i in range(8)],
            ["wR", "wN", "wB", "wQ", "wK", "empty", "empty", "wR"]
        ]
        initial_state, pieces = generate_initial_state(setting)
        self.white_piece = Piece(1,None, [])
        self.black_piece = Piece(2, None, [])
        self.board = Board(initial_state, pieces)
        self.board.state[2][2] = EnPassantSquare()

    def test_combinded_sliding_gives_correct_squares(self):
        single_slide_up = CombinedSlide([SingleSlide(0,-1)])
        white_positions = single_slide_up.generate_moves(1,(3,3),self.board, self.white_piece)
        self.assertEqual(white_positions, [])
        black_positions = single_slide_up.generate_moves(2,(3,3),self.board, self.black_piece)
        self.assertEqual(black_positions, [Move((3,3), (4,3),self.board)])

    def test_combined_sliding_attack_gives_correct_squares(self):
        single_slide_up = CombinedSlidingAttack([SingleSlide(0,-1)])
        white_positions = single_slide_up.generate_moves(1,(3,3),self.board, self.white_piece)
        self.assertEqual(white_positions, [Move((3,3), (2,3),self.board)])
        black_positions = single_slide_up.generate_moves(2,(3,3),self.board, self.black_piece)
        self.assertEqual(black_positions, [])

    def test_jump_gives_correct_squares(self):
        jump = Jump(1,-2)
        white_positions = jump.get_moves(1,(3,3), self.board, self.white_piece)
        self.assertEqual(white_positions, [Move((3,3), (1,4),self.board)])
        black_positions = jump.generate_moves(2,(3,3), self.board, self.black_piece)
        self.assertEqual(black_positions, [Move((3,3), (5,4),self.board)])

    def test_jump_attack_gives_correct_squares(self):
        jump = JumpAttack(0,-1)
        white_positions = jump.get_moves(1,(3,3), self.board, self.white_piece)
        self.assertEqual(white_positions, [Move((3,3), (2,3),self.board)])
        black_positions = jump.generate_moves(2,(3,3), self.board, self.black_piece)
        self.assertEqual(black_positions, [])

    def test_en_passant_works(self):
        en_passant = EnPassant()
        white_positions = en_passant.get_moves(1, (3,3), self.board, self.white_piece)
        self.assertEqual(white_positions, [Move((3,3), (2,2),self.board)])
        black_positions = en_passant.get_moves(2, (3,3), self.board, self.black_piece)
        self.assertEqual(black_positions, [])

    def test_can_castle(self):
        castling = Castling()
        white_positions = castling.get_moves(1, (7,4), self.board, self.white_piece)
        self.assertEqual(white_positions, [Move((7,4), (7,6), self.board)])

    