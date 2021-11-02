import pygame as p
from move import Move

class Rule():
    def get_move(self, player, position, board):
        move = self.generate_move(player, position, board)
        if self.check(move, board):
            return move
        return []

    def check(self, move, board):
        return True

class CombinedSlidingAttack(Rule):
    def __init__(self, rules):
        self.rules = rules

    def generate_move(self,player, position, board):
        new_position = self.generate_positions(player, position, board)
        if new_position == []:
            return []
        return [Move(position, new_position[0] ,board)]

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

    def generate_move(self, player, position, board):
        new_positions = self.generate_positions(player, position, board)
        return [Move(position, new_position, board) for new_position in new_positions]
    def generate_positions(self, player, position, board):
        new_positions = []
        for rule in self.rules:
            new_position = rule.generate_positions(player, position, board)[0]
            if not board.state[new_position[0]][new_position[1]].is_empty():
                break
            new_positions.append(new_position)
            position = new_position
        return new_positions


class JoinedRule():
    def __init__(self, rules):
        self.rules = rules
    
    def generate_positions(self, player, position, board):
        new_positions = []
        for rule in self.rules:
            new_positions.extend(rule.generate_positions(player, position, board))
        return new_positions

class Jump(Rule):
    def __init__(self, x_hop, y_hop):
        self.x_hop = x_hop
        self.y_hop = y_hop

    def generate_move(self,player, position, board):
        new_position = (position[0]+self.y_hop, position[1]+self.x_hop)
        if 0<new_position[0]<board.dimension and 0<new_position[1]<board.dimension:
            if board.state[new_position[0]][new_position[1]].is_empty():
                return [Move(position, new_position ,board)]
        return []


    


class Up(Rule):
    def generate_move(self,player, position, board):
        new_position = self.generate_positions(player, position, board)[0]
        if board.state[new_position[0]][new_position[1]].is_empty():
            return [Move(position, new_position ,board)]
        return []

    def generate_positions(self, player, position, board):
        if player==1:
            return [(position[0]-1, position[1])]
        else:
            return  [(position[0]+1, position[1])]

class Left(Rule):
    def generate_move(self,player, position, board):
        new_position = self.generate_positions(player, position, board)[0]
        if board.state[new_position[0]][new_position[1]].is_empty():
            return [Move(position, new_position ,board)]
        return []

    def generate_positions(self, player, position, board):
            return  [(position[0], position[1]-1)]

class UpStar(Rule):
    def generate_move(self,player, position, board):
        moves = []
        if player==1:
            for i in range(position[0]-1,-1,-1):
                new_position = (i, position[1])
                if board.state[new_position[0]][new_position[1]].is_empty():
                    moves.append(Move(position, new_position, board))
        else:
            for i in range(position[0]-1,-1,-1):
                new_position = (i, position[1])
                if board.state[new_position[0]][new_position[1]].is_empty():
                    moves.append(Move(position, new_position, board))
        return moves





class Piece():
    def __init__(self, player, image, square_size=64):
        self.player = player
        self.image = image
        self.square_size = square_size
        

    def draw(self, screen, square_size, position):
        screen.blit(self.image, p.Rect(position[1]*square_size, position[0]*square_size, square_size, square_size))

    def get_moves(self, position, board):
        return []

    def is_empty(self):
        False


class Knight(Piece):
    def __init__(self, player, image):
        super().__init__(player, image)

class Rook(Piece):
    def __init__(self, player, image):
        super().__init__(player, image)

class Queen(Piece):
    def __init__(self, player, image):
        super().__init__(player, image)

class Bishop(Piece):
    def __init__(self, player, image):
        super().__init__(player, image)

class Pawn(Piece):
    def __init__(self, player, image):
        self.moves = [CombinedSlidingAttack([Up(), Up(), Left()]),  CombinedSlide([Up(), Up(), Left()])]
        super().__init__(player, image)

    def get_moves(self, position, board):
        result = []
        for move in self.moves:
            result.extend(move.get_move(self.player, position, board))
        return result



class King(Piece):
    def __init__(self, player, image):
        super().__init__(player, image)

class Empty_Space(Piece):
    def __init__(self):
        self.player = 0

    def draw(self, screen, square_size, position):
        pass

    def is_empty(self):
        return True


