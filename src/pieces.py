import pygame as p
from rules import CombinedSlidingAttack, CombinedSlide, EnPassant, SingleSlide, JumpAttack, Jump, RuleStarAttacks, RuleStar









class Piece():
    def __init__(self, player, image, square_size=64):
        self.player = player
        self.image = image
        self.square_size = square_size
        self.moved = False
        

    def draw(self, screen, square_size, position):
        screen.blit(self.image, p.Rect(position[1]*square_size, position[0]*square_size, square_size, square_size))

    def get_moves(self, position, board):
        result = []
        for rule in self.rules:
            result.extend(rule.get_moves(self.player, position, board, self))
        return result

    def is_empty(self):
        return False

    def is_king(self):
        return False

    def is_pawn(self):
        return False

    def set_as_moved(self):
        self.moved = True

    def is_en_passant(self):
        return False


class Knight(Piece):
    def __init__(self, player, image):
        self.rules = [Jump(1,-2), Jump(-1,-2), Jump(1,2), Jump(-1,2), Jump(2,-1), Jump(2,1), Jump(-2,-1), Jump(-2,1)]
        self.rules.extend([JumpAttack(1,-2), JumpAttack(-1,-2), JumpAttack(1,2), JumpAttack(-1,2), JumpAttack(2,-1), JumpAttack(2,1), JumpAttack(-2,-1), JumpAttack(-2,1)])
        super().__init__(player, image)

class Rook(Piece):
    def __init__(self, player, image):
        self.rules = [RuleStar(SingleSlide(0,1)), RuleStar(SingleSlide(0,-1)), RuleStar(SingleSlide(1,0)), RuleStar(SingleSlide(-1,0))]
        self.rules.extend([RuleStarAttacks(SingleSlide(0,1)), RuleStarAttacks(SingleSlide(0,-1)), RuleStarAttacks(SingleSlide(1,0)), RuleStarAttacks(SingleSlide(-1,0))])
        super().__init__(player, image)

class Queen(Piece):
    def __init__(self, player, image):
        self.rules = [RuleStar(SingleSlide(0,1)), RuleStar(SingleSlide(0,-1)), RuleStar(SingleSlide(1,0)), RuleStar(SingleSlide(-1,0)), RuleStar(SingleSlide(-1,-1)), RuleStar(SingleSlide(1,-1)), RuleStar(SingleSlide(1,1)), RuleStar(SingleSlide(-1,1))]
        self.rules.extend([RuleStarAttacks(SingleSlide(0,1)), RuleStarAttacks(SingleSlide(0,-1)), RuleStarAttacks(SingleSlide(1,0)), RuleStarAttacks(SingleSlide(-1,0)), RuleStarAttacks(SingleSlide(-1,-1)), RuleStarAttacks(SingleSlide(1,-1)), RuleStarAttacks(SingleSlide(1,1)), RuleStarAttacks(SingleSlide(-1,1))])
        super().__init__(player, image)

class Bishop(Piece):
    def __init__(self, player, image):
        self.rules = [RuleStar(SingleSlide(1,-1)), RuleStar(SingleSlide(-1,-1)), RuleStar(SingleSlide(1,1)), RuleStar(SingleSlide(-1,1))]
        self.rules = [RuleStarAttacks(SingleSlide(1,-1)), RuleStarAttacks(SingleSlide(-1,-1)), RuleStarAttacks(SingleSlide(1,1)), RuleStarAttacks(SingleSlide(-1,1))]
        super().__init__(player, image)

class Pawn(Piece):
    def __init__(self, player, image):
        self.rules = [CombinedSlide([SingleSlide(0,-1), SingleSlide(0,-1)]), CombinedSlidingAttack([SingleSlide(1,-1)]), CombinedSlidingAttack([SingleSlide(-1,-1)]), EnPassant() ]
        super().__init__(player, image)
    
    def is_pawn(self):
        return True

    def __str__(self):
        return "Pawn"

    def set_as_moved(self):
        self.rules = [CombinedSlide([SingleSlide(0,-1)]), CombinedSlidingAttack([SingleSlide(1,-1)]), CombinedSlidingAttack([SingleSlide(-1,-1)]), EnPassant() ]
        super().set_as_moved()





class King(Piece):
    def __init__(self, player, image):
        self.rules = [CombinedSlide([SingleSlide(0,-1)]), CombinedSlide([SingleSlide(1,-1)]), CombinedSlide([SingleSlide(-1,-1)]), CombinedSlide([SingleSlide(1,0)]), CombinedSlide([SingleSlide(-1,0)]), CombinedSlide([SingleSlide(0,1)]), CombinedSlide([SingleSlide(1,1)]), CombinedSlide([SingleSlide(-1,-1)])]
        self.rules.extend([CombinedSlidingAttack([SingleSlide(0,-1)]), CombinedSlidingAttack([SingleSlide(1,-1)]), CombinedSlidingAttack([SingleSlide(-1,-1)]), CombinedSlidingAttack([SingleSlide(1,0)]), CombinedSlidingAttack([SingleSlide(-1,0)]), CombinedSlidingAttack([SingleSlide(0,1)]), CombinedSlidingAttack([SingleSlide(1,1)]), CombinedSlidingAttack([SingleSlide(-1,-1)])])
        super().__init__(player, image)

    def is_king(self):
        return True

class Empty_Space(Piece):
    def __init__(self):
        self.player = 0

    def draw(self, screen, square_size, position):
        pass

    def is_empty(self):
        return True

    def get_moves(self, position, board):
        return []

class EnPassantSquare(Empty_Space):
    def is_en_passant(self):
        return True

    def draw(self, screen, square_size, position):
        p.draw.rect(screen, p.Color("black"), p.Rect(position[1]*square_size, position[0]*square_size, square_size, square_size))


