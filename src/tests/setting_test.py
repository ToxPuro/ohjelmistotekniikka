import unittest
from setting import Setting


class TestSetting(unittest.TestCase):
    def setUp(self):
        self.setting = Setting()

    def test_flip_slider_works(self):
        self.assertEqual(self.setting.slider, False)
        self.setting.flip_slider()
        self.assertEqual(self.setting.slider, True)

    def test_increase_index(self):
        self.assertEqual(self.setting.index, 1)
        self.setting.increase_index()
        self.assertEqual(self.setting.index, 2)

    def test_next_piece_increments_correctly(self):
        self.assertEqual(self.setting.current_piece, 0)
        self.setting.next_piece()
        self.assertEqual(self.setting.current_piece, 1)

    def test_save_jump_piece_works_correctly(self):
        self.setting.board.selected = [(2,1), (2,5)]
        self.setting.save_jump_piece()
        self.assertEqual(self.setting.piece_created.rules[0].x_hop, -2)
        self.assertEqual(self.setting.piece_created.rules[2].x_hop, 2)

    def test_save_sliding_piece_works(self):
        self.setting.board.selected = [(2,3,1), (2,4,1)]
        self.setting.save_sliding_piece()
        self.assertEqual(self.setting.piece_created.rules[0].rules[0].y_increment, -1)
        self.assertEqual(self.setting.piece_created.rules[0].rules[1].x_increment, 1)
        self.assertEqual(len(self.setting.piece_created.rules[0].rules), 2)



    