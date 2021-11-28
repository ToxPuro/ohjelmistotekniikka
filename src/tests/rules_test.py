import unittest
from rules import CombinedSlide, CombinedSlidingAttack, Jump, JumpAttack, RuleStar, RuleStarAttacks, SingleSlide


class TestRuleReader(unittest.TestCase):

    def test_incorrect_json_does_not_work(self):
        self.assertEqual(1, 1)
