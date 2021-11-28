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

    def to_json(self):
        pass


class CombinedSlidingAttack(Rule):
    def __init__(self, rules):
        self.rules = rules

    def generate_positions(self, player, position, board, piece):
        new_positions = []
        for rule in self.rules:
            new_position = rule.generate_positions(
                player, position, board, piece)[0]
            if not board.state[new_position[0]][new_position[1]].is_empty():
                if board.state[new_position[0]][new_position[1]].player != piece.player:
                    return [new_position]
                return []
            position = new_position
        return new_positions

    def to_json(self):
        return {
            "type": "combined_slide_attack",
            "slides": [rule.to_json() for rule in self.rules]
        }


class CombinedSlide(Rule):
    def __init__(self, rules):
        self.rules = rules

    def generate_positions(self, player, position, board, piece):
        new_positions = []
        for rule in self.rules:
            new_position = rule.generate_positions(
                player, position, board, piece)[0]
            if not board.state[new_position[0]][new_position[1]].is_empty():
                return new_positions
            new_positions.append(new_position)
            position = new_position
        return new_positions

    def to_json(self):
        return {
            "type": "combined_slide",
            "slides": [rule.to_json() for rule in self.rules]
        }


class Jump(Rule):
    def __init__(self, x_hop, y_hop):
        self.x_hop = x_hop
        self.y_hop = y_hop

    def generate_positions(self, player, position, board, piece):
        y_hop = self.y_hop if player == 1 else -self.y_hop
        new_position = (position[0]+y_hop, position[1]+self.x_hop)
        if 0 < new_position[0] < board.dimension and 0 < new_position[1] < board.dimension:
            if board.state[new_position[0]][new_position[1]].is_empty():
                return [new_position]
        return []

    def to_json(self):
        return {
            "type": "jump",
            "x_hop": self.x_hop,
            "y_hop": self.y_hop
        }

    def __str__(self):
        return f"x_hop: {self.x_hop}, y_hop {self.y_hop}"


class JumpAttack(Rule):
    def __init__(self, x_hop, y_hop):
        self.x_hop = x_hop
        self.y_hop = y_hop

    def generate_positions(self, player, position, board, piece):
        y_hop = self.y_hop if player == 1 else -self.y_hop
        new_position = (position[0]+y_hop, position[1]+self.x_hop)
        if 0 <= new_position[0] < board.dimension and 0 <= new_position[1] < board.dimension:
            if not board.state[new_position[0]][new_position[1]].is_empty() and board.state[new_position[0]][new_position[1]].player != piece.player:
                return [new_position]
        return []

    def to_json(self):
        return {
            "type": "jump_attack",
            "x_hop": self.x_hop,
            "y_hop": self.y_hop
        }


class SingleSlide(Rule):
    def __init__(self, x_increment, y_increment):
        self.x_increment = x_increment
        self.y_increment = y_increment

    def generate_positions(self, player, position, board, piece):
        if player == 1:
            new_position = (position[0]+self.y_increment,
                            position[1]+self.x_increment)
        else:
            new_position = (position[0]-self.y_increment,
                            position[1]+self.x_increment)
        if 0 <= new_position[0] < board.dimension and 0 <= new_position[1] < board.dimension:
            return [new_position]
        return [position]

    def to_json(self):
        return {
            "type": "single_slide",
            "x_increment": self.x_increment,
            "y_increment": self.y_increment
        }


class RuleStar(Rule):
    def __init__(self, rule):
        self.rule = rule

    def generate_positions(self, player, position, board, piece):
        return CombinedSlide([self.rule for i in range(board.dimension)]).generate_positions(player, position, board, piece)

    def to_json(self):
        return {
            "type": "RuleStar",
            "rule": self.rule.to_json()

        }


class RuleStarAttacks(Rule):
    def __init__(self, rule):
        self.rule = rule

    def generate_positions(self, player, position, board, piece):
        return CombinedSlidingAttack([self.rule for i in range(board.dimension)]).generate_positions(player, position, board, piece)

    def to_json(self):
        return {
            "type": "RuleStarAttacks",
            "rule": self.rule.to_json()

        }


class EnPassant(Rule):
    def generate_positions(self, player, position, board, piece):
        if player == 1:
            new_positions = [(position[0]-1, position[1]-1),
                             (position[0]-1, position[1]+1)]
        else:
            new_positions = [(position[0]+1, position[1]-1),
                             (position[0]+1, position[1]+1)]

        for new_position in new_positions:
            if 0 <= new_position[0] < board.dimension and 0 <= new_position[1] < board.dimension:
                if board.state[new_position[0]][new_position[1]].is_en_passant():
                    return [new_position]

        return []


class Castling(Rule):
    def get_moves(self, player, position, board, piece):
        moves = []
        if piece.moved:
            return []

        if board.inCheck():
            return []

        can_castle_left = True
        if (board.state[position[0]][position[1]-1].is_empty() and board.state[position[0]][position[1]-2].is_empty() and board.state[position[0]][position[1]-3].moved == False) is False:
            can_castle_left = False
        if board.square_under_attack((position[0], position[1]-1)) or board.square_under_attack((position[0], position[1]-2)):
            can_castle_left = False
        if can_castle_left:
            moves.append(Move(position, (position[0], position[1]-2), board))

        can_castle_right = True
        if (board.state[position[0]][position[1]+1].is_empty() and board.state[position[0]][position[1]+2].is_empty() and board.state[position[0]][position[1]+3].moved == False) is False:
            can_castle_right = False
        if board.square_under_attack((position[0], position[1]+1)) or board.square_under_attack((position[0], position[1]+2)):
            can_castle_right = False
        if can_castle_right:
            moves.append(Move(position, (position[0], position[1]+2), board))
        print(moves)
        return moves
