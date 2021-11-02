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

class Up(Rule):
    def generate_move(self,player, position, board):
        if player==1:
            return [Move(position, (position[0]-1, position[1]),board)]
        return [Move(position, (position[0]+1, position[1]),board)]

class UpStar(Rule):
    def generate_move(self,player, position, board):
        if player==1:
            return [Move(position, (i, position[1]),board) for i in range(position[0]-1,-1,-1)]
        [Move(position, (i, position[1]),board) for i in range(position[0]+1,board.dimension)]





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
        self.moves = [UpStar()]
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


