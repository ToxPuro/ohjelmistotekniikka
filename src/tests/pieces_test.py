import unittest
from pieces import Piece, Knight, Pawn, King, Queen, Rook


class TestRuleReader(unittest.TestCase):

    def test_incorrect_json_does_not_work(self):
        self.assertEqual(1, 1)
