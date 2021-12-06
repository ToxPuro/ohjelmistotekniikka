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

    def test_can_save_jumping_piece_correctly(self):
        self.setting.saved = [(2,1,1, False, True), (2,5,1,False, True)]
        self.setting.save_piece()
        self.assertEqual(self.setting.piece_created.rules[4].x_hop, -2)
        self.assertEqual(self.setting.piece_created.rules[5].x_hop, 2)

    def test_can_save_sliding_piece_correctly(self):
        self.setting.saved = [(2,3,1, False, False), (2,4,1, False, False)]
        self.setting.save_piece()
        self.assertEqual(self.setting.piece_created.rules[0].rules[0].y_increment, -1)
        self.assertEqual(self.setting.piece_created.rules[0].rules[1].x_increment, 1)
        self.assertEqual(len(self.setting.piece_created.rules[0].rules), 2)

    def test_increase_initial_state(self):
        self.setting.increase_initial_state()
        self.assertEqual(self.setting.initial_state,
        [
            ["empty" for i in range(10)],
            ["empty","bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR","empty"],
            ["empty","bp","bp","bp","bp","bp","bp","bp","bp","empty"],
            ["empty" for i in range(10)],
            ["empty" for i in range(10)],
            ["empty" for i in range(10)],
            ["empty"for i in range(10)],
            ["empty","wp","wp","wp","wp","wp","wp","wp","wp","empty"],
            ["empty","wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR","empty"],
            ["empty" for i in range(10)]
        ])

    def test_decrease_initial_state(self):
        self.setting.decrease_initial_state()
        self.assertEqual(self.setting.initial_state,
        [
            ["bp","bp","bp","bp","bp","bp"],
            ["empty" for i in range(6)],
            ["empty" for i in range(6)],
            ["empty" for i in range(6)],
            ["empty"for i in range(6)],
            ["wp","wp","wp","wp","wp","wp"],
        ])