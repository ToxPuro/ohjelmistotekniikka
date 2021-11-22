from rules import CombinedSlide, Jump, JumpAttack, SingleSlide, CombinedSlidingAttack, RuleStar, RuleStarAttacks

class RuleReader():

    def json_to_rule(self,json):
        if json["type"] == "single_slide":
            return SingleSlide(json["x_increment"], json["y_increment"])

        elif json["type"] == "jump":
            return Jump(json["x_hop"], json["y_hop"])

        elif json["type"] == "jump_attack":
            return JumpAttack(json["x_hop"], json["y_hop"])

        elif json["type"] == "combined_slide":
            return CombinedSlide([self.json_to_rule(rule) for rule in json["slides"]])

        elif json["type"] == "combined_slide_attack":
            return CombinedSlidingAttack([self.json_to_rule(rule) for rule in json["slides"]])

        elif json["type"] == "RuleStar":
            return RuleStar(self.json_to_rule(json["rule"]))

        elif json["type"] == "RuleStarAttacks":
            return RuleStarAttacks(self.json_to_rule(json["rule"]))
        
        return "incorrect type"

