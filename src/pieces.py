import pygame as p
from move import Move

class Rule():
    def get_moves(self, player, position, board):
        moves = self.generate_moves(player, position, board)
        if self.check(moves, board):
            return moves
        return []

    def check(self, move, board):
        return True

    def generate_moves(self, player, position, board):
        new_positions = self.generate_positions(player, position, board)
        return [Move(position, new_position, board) for new_position in new_positions]

class CombinedSlidingAttack(Rule):
    def __init__(self, rules):
        self.rules = rules

    def generate_positions(self, player, position, board):
        new_positions = []
        for rule in self.rules:
            new_position = rule.generate_positions(player, position, board)[0]
            if not board.state[new_position[0]][new_position[1]].is_empty():
                return [new_position]
            position = new_position
        return new_positions

class CombinedSlide(Rule):
    def __init__(self, rules):
        self.rules = rules

    def generate_positions(self, player, position, board):
        new_positions = []
        for rule in self.rules:
            new_position = rule.generate_positions(player, position, board)[0]
            if not board.state[new_position[0]][new_position[1]].is_empty():
                break
            new_positions.append(new_position)
            position = new_position
        return new_positions

class Jump(Rule):
    def __init__(self, x_hop, y_hop):
        self.x_hop = x_hop
        self.y_hop = y_hop

    def generate_positions(self,player, position, board):
        new_position = (position[0]+self.y_hop, position[1]+self.x_hop)
        if 0<new_position[0]<board.dimension and 0<new_position[1]<board.dimension:
            if board.state[new_position[0]][new_position[1]].is_empty():
                return [new_position]
        return []

class JumpAttack(Rule):
    def __init__(self, x_hop, y_hop):
        self.x_hop = x_hop
        self.y_hop = y_hop

    def generate_positions(self,player, position, board):
        new_position = (position[0]+self.y_hop, position[1]+self.x_hop)
        if 0<=new_position[0]<board.dimension and 0<=new_position[1]<board.dimension:
            if not board.state[new_position[0]][new_position[1]].is_empty():
                return [new_position]
        return []


    
class SingleSlide(Rule):
    def __init__(self, x_increment, y_increment):
        self.x_increment = x_increment
        self.y_increment = y_increment
    
    def generate_positions(self, player, position, board):
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

    def generate_positions(self,player, position, board):
        return CombinedSlide([self.rule for i in range(board.dimension)]).generate_positions(player, position, board)







class Piece():
    def __init__(self, player, image, square_size=64):
        self.player = player
        self.image = image
        self.square_size = square_size
        

    def draw(self, screen, square_size, position):
        screen.blit(self.image, p.Rect(position[1]*square_size, position[0]*square_size, square_size, square_size))

    def get_moves(self, position, board):
        result = []
        for rule in self.rules:
            result.extend(rule.get_moves(self.player, position, board))
        return result

    def is_empty(self):
        False


class Knight(Piece):
    def __init__(self, player, image):
        self.rules = [Jump(1,-2), Jump(-1,-2), Jump(1,2), Jump(-1,2)]
        super().__init__(player, image)

class Rook(Piece):
    def __init__(self, player, image):
        self.rules = [RuleStar(SingleSlide(0,1)), RuleStar(SingleSlide(0,-1)), RuleStar(SingleSlide(1,0)), RuleStar(SingleSlide(-1,0))]
        super().__init__(player, image)

class Queen(Piece):
    def __init__(self, player, image):
        self.rules = [RuleStar(SingleSlide(0,1)), RuleStar(SingleSlide(0,-1)), RuleStar(SingleSlide(1,0)), RuleStar(SingleSlide(-1,0)), RuleStar(SingleSlide(-1,-1)), RuleStar(SingleSlide(1,-1)), RuleStar(SingleSlide(1,1)), RuleStar(SingleSlide(-1,1))]
        super().__init__(player, image)

class Bishop(Piece):
    def __init__(self, player, image):
        self.rules = [RuleStar(SingleSlide(1,-1)), RuleStar(SingleSlide(-1,-1)), RuleStar(SingleSlide(1,1)), RuleStar(SingleSlide(-1,1))]
        super().__init__(player, image)

class Pawn(Piece):
    def __init__(self, player, image):
        self.rules = [SingleSlide(0,-1)]
        super().__init__(player, image)





class King(Piece):
    def __init__(self, player, image):
        self.rules = [SingleSlide(0,-1)]
        super().__init__(player, image)

class Empty_Space(Piece):
    def __init__(self):
        self.player = 0

    def draw(self, screen, square_size, position):
        pass

    def is_empty(self):
        return True

    def get_moves(self, position, board):
        return []


