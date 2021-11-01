import pygame as p

class Piece():
    def __init__(self, player, image, position, square_size=64):
        self.player = player
        self.image = image
        self.position = position
        self.square_size = square_size

    def draw(self, screen):
        screen.blit(self.image, p.Rect(self.position["column"]*self.square_size, self.position["row"]*self.square_size, self.square_size, self.square_size))


class Knight(Piece):
    def __init__(self, player, image, position):
        super().__init__(player, image, position)

class Rook(Piece):
    def __init__(self, player, image, position):
        super().__init__(player, image, position)

class Queen(Piece):
    def __init__(self, player, image, position):
        super().__init__(player, image, position)

class Bishop(Piece):
    def __init__(self, player, image, position):
        super().__init__(player, image, position)

class Pawn(Piece):
    def __init__(self, player, image, position):
        super().__init__(player, image, position)

class King(Piece):
    def __init__(self, player, image, position):
        super().__init__(player, image, position)

class Empty_Space(Piece):
    def __init__(self, position):
        self.position = position

    def draw(self, screen):
        pass



