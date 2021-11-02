import pygame as p

class Piece():
    def __init__(self, player, image, square_size=64):
        self.player = player
        self.image = image
        self.square_size = square_size

    def draw(self, screen, square_size, position):
        screen.blit(self.image, p.Rect(position[1]*square_size, position[0]*square_size, square_size, square_size))


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
        super().__init__(player, image)

class King(Piece):
    def __init__(self, player, image):
        super().__init__(player, image)

class Empty_Space(Piece):
    def __init__(self):
        pass

    def draw(self, screen, square_size, position):
        pass



