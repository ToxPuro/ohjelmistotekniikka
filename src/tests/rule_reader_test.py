import unittest
from rule_reader import RuleReader
from rules import CombinedSlide, CombinedSlidingAttack, Jump, JumpAttack, RuleStar, RuleStarAttacks, SingleSlide

class TestRuleReader(unittest.TestCase):
    def setUp(self):
        self.rule_reader = RuleReader()

    
    def test_reads_combined_sliding_attack_correct(self):
        json = {
            "type": "combined_slide_attack",
        }
        json["rules"] =  [
                    {
                        "type": "single_slide",
                        "x_increment": 1,
                        "y_increment": -1
                    },
                    {
                        "type": "single_slide",
                        "x_increment": -1,
                        "y_increment": 1
                    }
                ]

        rule = self.rule_reader.json_to_rule(json)
        self.assertEqual(isinstance(rule, CombinedSlidingAttack), True)
        self.assertEqual(isinstance(rule.rules[1], SingleSlide), True)
        self.assertEqual((rule.rules[0].x_increment, rule.rules[0].y_increment), (1,-1))
        self.assertEqual((rule.rules[1].x_increment, rule.rules[1].y_increment), (-1,1))

    def test_reads_jump_rule_correct(self):
        json = {
            "type": "jump",
            "x_hop": 2,
            "y_hop": 2
        }
        rule = self.rule_reader.json_to_rule(json)
        self.assertEqual(isinstance(rule, Jump), True)
        self.assertEqual(rule.x_hop, 2)
        self.assertEqual(rule.y_hop, 2)

    def test_reads_jump_attack_correct(self):
        json = {
            "type": "jump_attack",
            "x_hop": 2,
            "y_hop": 2
        }
        rule = self.rule_reader.json_to_rule(json)
        self.assertEqual(isinstance(rule, JumpAttack), True)
        self.assertEqual(rule.x_hop, 2)
        self.assertEqual(rule.y_hop, 2)

    def test_reads_single_slide_correct(self):
        json = {
            "type": "single_slide",
            "x_increment": 2,
            "y_increment": 2
        }
        rule = self.rule_reader.json_to_rule(json)
        self.assertEqual(isinstance(rule, SingleSlide), True)
        self.assertEqual(rule.x_increment, 2)
        self.assertEqual(rule.y_increment, 2)

    def test_reads_combined_slide_correct(self):
        json = {
            "type": "combined_slide",
        }
        json["rules"] =  [
                    {
                        "type": "single_slide",
                        "x_increment": 1,
                        "y_increment": -1
                    },
                    {
                        "type": "single_slide",
                        "x_increment": -1,
                        "y_increment": 1
                    }
                ]

        rule = self.rule_reader.json_to_rule(json)
        self.assertEqual(isinstance(rule, CombinedSlide), True)
        self.assertEqual(isinstance(rule.rules[1], SingleSlide), True)
        self.assertEqual((rule.rules[0].x_increment, rule.rules[0].y_increment), (1,-1))
        self.assertEqual((rule.rules[1].x_increment, rule.rules[1].y_increment), (-1,1))

    
    def test_reads_rulestar_correct(self):
        json = {
            "type": "RuleStar",
            "rule": {
                "type": "single_slide",
                "x_increment": 0,
                "y_increment": -1
            }
        }

        rule = self.rule_reader.json_to_rule(json)
        self.assertEqual(isinstance(rule, RuleStar), True)
        self.assertEqual(isinstance(rule.rule, SingleSlide), True)
        self.assertEqual((rule.rule.x_increment, rule.rule.y_increment), (0,-1))

    def test_reads_rulestar_attack_correct(self):
        json = {
            "type": "RuleStarAttacks",
            "rule": {
                "type": "single_slide",
                "x_increment": 0,
                "y_increment": -1
            }
        }

        rule = self.rule_reader.json_to_rule(json)
        self.assertEqual(isinstance(rule, RuleStarAttacks), True)
        self.assertEqual(isinstance(rule.rule, SingleSlide), True)
        self.assertEqual((rule.rule.x_increment, rule.rule.y_increment), (0,-1))
