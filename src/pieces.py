import pygame as p
from rules import CombinedSlidingAttack, CombinedSlide, EnPassant, SingleSlide, JumpAttack, Jump, RuleStarAttacks, RuleStar, Castling


class Piece():
    def __init__(self, player, image, rules, is_king=False, square_size=64):
        self.player = player
        self.image = image
        self.square_size = square_size
        self.moved = False
        self.rules = rules
        self._is_king = is_king

    def draw(self, screen, square_size, position):
        screen.blit(self.image, p.Rect(
            position[1]*square_size, position[0]*square_size, square_size, square_size))

    def get_moves(self, position, board):
        result = []
        for rule in self.rules:
            result.extend(rule.get_moves(self.player, position, board, self))
        return result

    def is_empty(self):
        return False

    def is_king(self):
        return self._is_king

    def is_pawn(self):
        return False

    def set_as_moved(self):
        self.moved = True

    def is_en_passant(self):
        return False


class Knight(Piece):
    def __init__(self, player, image):
        rules = [Jump(1, -2), Jump(-1, -2), Jump(1, 2), Jump(-1, 2),
                 Jump(2, -1), Jump(2, 1), Jump(-2, -1), Jump(-2, 1)]
        rules.extend([JumpAttack(1, -2), JumpAttack(-1, -2), JumpAttack(1, 2), JumpAttack(-1, 2),
                     JumpAttack(2, -1), JumpAttack(2, 1), JumpAttack(-2, -1), JumpAttack(-2, 1)])
        super().__init__(player, image, rules)


class Rook(Piece):
    def __init__(self, player, image):
        rules = [RuleStar(SingleSlide(0, 1)), RuleStar(SingleSlide(
            0, -1)), RuleStar(SingleSlide(1, 0)), RuleStar(SingleSlide(-1, 0))]
        rules.extend([RuleStarAttacks(SingleSlide(0, 1)), RuleStarAttacks(SingleSlide(
            0, -1)), RuleStarAttacks(SingleSlide(1, 0)), RuleStarAttacks(SingleSlide(-1, 0))])
        super().__init__(player, image, rules)


class Queen(Piece):
    def __init__(self, player, image):
        rules = [RuleStar(SingleSlide(0, 1)), RuleStar(SingleSlide(0, -1)),
                RuleStar(SingleSlide(1, 0)), RuleStar(SingleSlide(-1, 0)),
                RuleStar(SingleSlide(-1, -1)), RuleStar(SingleSlide(1, -1)),
                RuleStar(SingleSlide(1, 1)), RuleStar(SingleSlide(-1, 1))]
        rules.extend([RuleStarAttacks(SingleSlide(0, 1)), RuleStarAttacks(SingleSlide(0, -1)),
                      RuleStarAttacks(SingleSlide(1, 0)), RuleStarAttacks(SingleSlide(-1, 0)),
                     RuleStarAttacks(SingleSlide(-1, -1)), RuleStarAttacks(SingleSlide(1, -1)),
                     RuleStarAttacks(SingleSlide(1, 1)), RuleStarAttacks(SingleSlide(-1, 1))])
        super().__init__(player, image, rules)


class Bishop(Piece):
    def __init__(self, player, image):
        rules = [RuleStar(SingleSlide(-1, -1)), RuleStar(SingleSlide(1, -1)),
                 RuleStar(SingleSlide(1, 1)), RuleStar(SingleSlide(-1, 1))]
        rules.extend([RuleStarAttacks(SingleSlide(-1, -1)), RuleStarAttacks(SingleSlide(1, -1)),
                     RuleStarAttacks(SingleSlide(1, 1)), RuleStarAttacks(SingleSlide(-1, 1))])
        super().__init__(player, image, rules)


class Pawn(Piece):
    def __init__(self, player, image):
        rules = [CombinedSlide([SingleSlide(0, -1), SingleSlide(0, -1)]), CombinedSlidingAttack(
            [SingleSlide(1, -1)]), CombinedSlidingAttack([SingleSlide(-1, -1)]), EnPassant()]
        super().__init__(player, image, rules)

    def is_pawn(self):
        return True

    def set_as_moved(self):
        self.rules = [CombinedSlide([SingleSlide(0, -1)]), CombinedSlidingAttack(
            [SingleSlide(1, -1)]), CombinedSlidingAttack([SingleSlide(-1, -1)]), EnPassant()]
        super().set_as_moved()


class King(Piece):
    def __init__(self, player, image):
        rules = [Castling(), CombinedSlide([SingleSlide(0, -1)]),
                CombinedSlide([SingleSlide(1, -1)]),
                CombinedSlide([SingleSlide(-1, -1)]), CombinedSlide([SingleSlide(1, 0)]),
                 CombinedSlide([SingleSlide(-1, 0)]), CombinedSlide([SingleSlide(0, 1)]),
                 CombinedSlide([SingleSlide(1, 1)]), CombinedSlide([SingleSlide(-1, -1)])]

        rules.extend([CombinedSlidingAttack([SingleSlide(0, -1)]),
                    CombinedSlidingAttack([SingleSlide(1, -1)]),
                    CombinedSlidingAttack([SingleSlide(-1, -1)]),
                    CombinedSlidingAttack([SingleSlide(1, 0)]),
                    CombinedSlidingAttack([SingleSlide(-1, 0)]),
                    CombinedSlidingAttack([SingleSlide(0, 1)]),
                    CombinedSlidingAttack([SingleSlide(1, 1)]),
                    CombinedSlidingAttack([SingleSlide(-1, -1)])])

        super().__init__(player, image, rules)

    def is_king(self):
        return True


class Empty_Space(Piece):
    def __init__(self):
        self.player = 0
        self.moved = False
        self._is_king = False

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
        pass


class SelectedJumpSquare(Piece):
    def __init__(self):
        self.moved = False

    def draw(self, screen, square_size, position):
        p.draw.rect(screen, p.Color("green"), p.Rect(
            position[1]*square_size, position[0]*square_size, square_size, square_size))


class SelectedSlideSquare(Piece):
    def __init__(self, num):
        self.num = num

    def draw(self, screen, square_size, position):
        p.draw.rect(screen, p.Color("red"), p.Rect(
            position[1]*square_size, position[0]*square_size, square_size, square_size))
        smallfont = p.font.SysFont('Corbel', 35)
        text = smallfont.render(f"{self.num}", True, p.Color("black"))
        screen.blit(text, p.Rect(
            position[1]*square_size, position[0]*square_size, square_size, square_size))
