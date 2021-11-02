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

class EnPassant(Rule):
    def generate_positions(self,player, position, board, piece):
        if player == 1:
            new_positions = [(position[0]-1, position[1]-1), (position[0]-1, position[1]+1)]
        else:
            new_positions = [(position[0]+1, position[1]-1), (position[0]+1, position[1]+1)]

        for new_position in new_positions:
            if 0<=new_position[0]<board.dimension and 0<=new_position[1]<board.dimension:
                if board.state[new_position[0]][new_position[1]].is_en_passant():
                    return [new_position]
        
        return []
        