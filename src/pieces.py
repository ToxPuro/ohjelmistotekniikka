import pygame as p
from move import Move

class Rule():
    def get_moves(self, player, position, board, piece):
        moves = self.generate_moves(player, position, board, piece)
        if self.check(moves, board):
            return moves
        return []

    def check(self, move, board):
        return True

    def generate_moves(self, player, position, board, piece):
        new_positions = self.generate_positions(player, position, board, piece)
        return [Move(position, new_position, board) for new_position in new_positions]

class CombinedSlidingAttack(Rule):
    def __init__(self, rules):
        self.rules = rules

    def generate_positions(self, player, position, board, piece):
        new_positions = []
        for rule in self.rules:
            new_position = rule.generate_positions(player, position, board, piece)[0]
            if not board.state[new_position[0]][new_position[1]].is_empty() and board.state[new_position[0]][new_position[1]].player != piece.player:
                return [new_position]
            position = new_position
        return new_positions

class CombinedSlide(Rule):
    def __init__(self, rules):
        self.rules = rules

    def generate_positions(self, player, position, board, piece):
        new_positions = []
        for rule in self.rules:
            new_position = rule.generate_positions(player, position, board, piece)[0]
            if not board.state[new_position[0]][new_position[1]].is_empty():
                break
            new_positions.append(new_position)
            position = new_position
        return new_positions

class Jump(Rule):
    def __init__(self, x_hop, y_hop):
        self.x_hop = x_hop
        self.y_hop = y_hop

    def generate_positions(self,player, position, board, piece):
        new_position = (position[0]+self.y_hop, position[1]+self.x_hop)
        if 0<new_position[0]<board.dimension and 0<new_position[1]<board.dimension:
            if board.state[new_position[0]][new_position[1]].is_empty():
                return [new_position]
        return []

class JumpAttack(Rule):
    def __init__(self, x_hop, y_hop):
        self.x_hop = x_hop
        self.y_hop = y_hop

    def generate_positions(self,player, position, board, piece):
        new_position = (position[0]+self.y_hop, position[1]+self.x_hop)
        if 0<=new_position[0]<board.dimension and 0<=new_position[1]<board.dimension:
            if not board.state[new_position[0]][new_position[1]].is_empty() and board.state[new_position[0]][new_position[1]].player != piece.player:
                return [new_position]
        return []


    
class SingleSlide(Rule):
    def __init__(self, x_increment, y_increment):
        self.x_increment = x_increment
        self.y_increment = y_increment
    
    def generate_positions(self, player, position, board, piece):
        if player == 1:
            new_position = (position[0]+self.y_increment, position[1]+self.x_increment)
        else:
            new_position = (position[0]-self.y_increment, position[1]+self.x_increment)
        if 0<=new_position[0]<board.dimension and 0<=new_position[1]<board.dimension:
            return [new_position]
        return [position]


class RuleStar(Rule):
    def __init__(self, rule):
        self.rule = rule

    def generate_positions(self,player, position, board, piece):
        return CombinedSlide([self.rule for i in range(board.dimension)]).generate_positions(player, position, board, piece)

class RuleStarAttacks(Rule):
    def __init__(self, rule):
        self.rule = rule

    def generate_positions(self,player, position, board, piece):
        return CombinedSlidingAttack([self.rule for i in range(board.dimension)]).generate_positions(player, position, board, piece)







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
        self.rules = [CombinedSlide([SingleSlide(0,-1), SingleSlide(0,-1)]), CombinedSlidingAttack([SingleSlide(1,-1)]), CombinedSlidingAttack([SingleSlide(-1,-1)]) ]
        super().__init__(player, image)
    
    def is_pawn(self):
        return True

    def __str__(self):
        return "Pawn"

    def set_as_moved(self):
        self.rules = [CombinedSlide([SingleSlide(0,-1)]), CombinedSlidingAttack([SingleSlide(1,-1)]), CombinedSlidingAttack([SingleSlide(-1,-1)]) ]
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


