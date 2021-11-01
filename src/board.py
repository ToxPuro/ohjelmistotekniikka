import pygame as p

class Board():
    def __init__(self, state, dimension=8, square_size=64):
        self.state = state
        self.dimension = dimension
        self.square_size = square_size
    
    def drawGameState(self, screen):
        self.drawSquares(screen)
        self.drawPieces(screen)

    def drawSquares(self, screen):
        colors = [p.Color("white"), p.Color("gray")]
        for r in range(self.dimension):
            for c in range(self.dimension):
                color = colors[((r+c) %2)]
                p.draw.rect(screen, color, p.Rect(c*self.square_size, r*self.square_size, self.square_size, self.square_size))

    def drawPieces(self, screen):
        for piece in self.state:
            piece.draw(screen)
