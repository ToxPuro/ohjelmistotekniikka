import pygame as p
from rules import CombinedSlidingAttack, CombinedSlide, EnPassant, SingleSlide, JumpAttack, Jump, RuleStarAttacks, RuleStar, Castling


class Piece():
    """Super class for all pieces. Is used for custom pieces
    """
    def __init__(self, player, image, rules, is_king=False, square_size=64):
        self.player = player
        self.image = image
        self.square_size = square_size
        self.moved = False
        self.rules = rules
        self._is_king = is_king

    def draw(self, screen, square_size, position):
        """Draw the piece on the board

        Args:
            screen: the pygame screen to draw on
            square_size: how large should the piece be drawn
            position: Where the piece should be drawn on
        """
        screen.blit(self.image, p.Rect(
            position[1]*square_size, position[0]*square_size, square_size, square_size))

    def get_moves(self, position, board):
        """Returns the moves that the piece can make, doesn't check validity

        Args:
            position: the pieces current position
            board: the current state of the board

        Returns:
            moves [Move]: Possible moves for the piece
        """
        result = []
        for rule in self.rules:
            result.extend(rule.get_moves(self.player, position, board, self))
        return result

    def is_empty(self):
        """Whether the square is empty

        Returns:
            Always false since pieces aren't empty
        """
        return False

    def is_king(self):
        """Returns info whether the piece is king

        Returns:
            returns the param given in init
        """
        return self._is_king

    def is_pawn(self):
        """Returns whether the current piece is a pawn

        Returns:
            Superclass returns False, Pawn class overwrites this
        """
        return False

    def set_as_moved(self):
        """Set the piece as moved
        """
        self.moved = True

    def is_en_passant(self):
        """Whether the square is en passant square

        Returns:
            Returns always false as pieces aren't en passant squares
        """
        return False


class Knight(Piece):
    """Helper class for Knight piece
    """
    def __init__(self, player, image):
        rules = [Jump(1, -2), Jump(-1, -2), Jump(1, 2), Jump(-1, 2),
                 Jump(2, -1), Jump(2, 1), Jump(-2, -1), Jump(-2, 1)]
        rules.extend([JumpAttack(1, -2), JumpAttack(-1, -2), JumpAttack(1, 2), JumpAttack(-1, 2),
                     JumpAttack(2, -1), JumpAttack(2, 1), JumpAttack(-2, -1), JumpAttack(-2, 1)])
        super().__init__(player, image, rules)


class Rook(Piece):
    """Helper class for Rook piece
    """
    def __init__(self, player, image):
        rules = [RuleStar(SingleSlide(0, 1)), RuleStar(SingleSlide(
            0, -1)), RuleStar(SingleSlide(1, 0)), RuleStar(SingleSlide(-1, 0))]
        rules.extend([RuleStarAttacks(SingleSlide(0, 1)), RuleStarAttacks(SingleSlide(
            0, -1)), RuleStarAttacks(SingleSlide(1, 0)), RuleStarAttacks(SingleSlide(-1, 0))])
        super().__init__(player, image, rules)


class Queen(Piece):
    """Helper class for Queen piece
    """
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
    """Helper class for Bishop piece
    """
    def __init__(self, player, image):
        rules = [RuleStar(SingleSlide(-1, -1)), RuleStar(SingleSlide(1, -1)),
                 RuleStar(SingleSlide(1, 1)), RuleStar(SingleSlide(-1, 1))]
        rules.extend([RuleStarAttacks(SingleSlide(-1, -1)), RuleStarAttacks(SingleSlide(1, -1)),
                     RuleStarAttacks(SingleSlide(1, 1)), RuleStarAttacks(SingleSlide(-1, 1))])
        super().__init__(player, image, rules)


class Pawn(Piece):
    """Helper class for Pawn piece
    """
    def __init__(self, player, image):
        rules = [CombinedSlide([SingleSlide(0, -1), SingleSlide(0, -1)]), CombinedSlidingAttack(
            [SingleSlide(1, -1)]), CombinedSlidingAttack([SingleSlide(-1, -1)]), EnPassant()]
        super().__init__(player, image, rules)

    def is_pawn(self):
        """Overwrite superclass

        Returns:
            Returns True as the piece is a pawn
        """
        return True

    def set_as_moved(self):
        """Removes double forward from the piece rules after moving
        """
        self.rules = [CombinedSlide([SingleSlide(0, -1)]), CombinedSlidingAttack(
            [SingleSlide(1, -1)]), CombinedSlidingAttack([SingleSlide(-1, -1)]), EnPassant()]
        super().set_as_moved()


class King(Piece):
    """Helper class for King piece
    """
    def __init__(self, player, image):
        rules = [Castling(), CombinedSlide([SingleSlide(0, -1)]),
                CombinedSlide([SingleSlide(1, -1)]),
                CombinedSlide([SingleSlide(-1, -1)]), CombinedSlide([SingleSlide(1, 0)]),
                 CombinedSlide([SingleSlide(-1, 0)]), CombinedSlide([SingleSlide(0, 1)]),
                 CombinedSlide([SingleSlide(1, 1)]), CombinedSlide([SingleSlide(-1, 1)])]

        rules.extend([CombinedSlidingAttack([SingleSlide(0, -1)]),
                    CombinedSlidingAttack([SingleSlide(1, -1)]),
                    CombinedSlidingAttack([SingleSlide(-1, -1)]),
                    CombinedSlidingAttack([SingleSlide(1, 0)]),
                    CombinedSlidingAttack([SingleSlide(-1, 0)]),
                    CombinedSlidingAttack([SingleSlide(0, 1)]),
                    CombinedSlidingAttack([SingleSlide(1, 1)]),
                    CombinedSlidingAttack([SingleSlide(-1, 1)])])

        super().__init__(player, image, rules)

    def is_king(self):
        """Whether piece is king

        Returns:
            returns always True as the piece is King
        """
        return True

class EmptySpace():
    """Class that represents an empty square
    """
    def __init__(self):
        self.player = 0
        self.moved = False
        self._is_king = False

    def draw(self, screen, square_size, position):
        """Draw the empty square i.e. do nothing

        Args:
            screen: screen to draw on
            square_size: How large square to draw
            position: Where to draw
        """
        pass

    def is_empty(self):
        return True

    def is_king(self):
        return False

    def is_en_passant(self):
        return False

    def is_pawn(self):
        return False

class EnPassantSquare(EmptySpace):
    def is_en_passant(self):
        return True

    def draw(self, screen, square_size, position):
        pass


class SelectedSquare(EmptySpace):
    def __init__(self, is_attack):
        self.moved = False
        self.is_attack = is_attack

    def is_empty(self):
        return False

    def draw(self, screen, square_size, position):
        p.draw.rect(screen, p.Color("red" if self.is_attack else "green"), p.Rect(
            position[1]*square_size, position[0]*square_size, square_size, square_size))
