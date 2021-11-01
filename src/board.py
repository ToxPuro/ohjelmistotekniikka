import pygame as p

class Board():
    def __init__(self, images, dimension=8, square_size=64):
        self.state = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp" for i in range(8)],
            ["--" for i in range(8)],
            ["--" for i in range(8)],
            ["--" for i in range(8)],
            ["--" for i in range(8)],
            ["wp" for i in range(8)],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.dimension = dimension
        self.square_size = square_size
        self.images = images
    
    def drawBoard(self, screen):
        colors = [p.Color("white"), p.Color("gray")]
        for r in range(self.dimension):
            for c in range(self.dimension):
                color = colors[((r+c) %2)]
                p.draw.rect(screen, color, p.Rect(c*self.square_size, r*self.square_size, self.square_size, self.square_size))

    def drawPieces(self, screen):
        for r in range(self.dimension):
            for c in range(self.dimension):
                piece = self.state[r][c]
                if piece != "--":
                    screen.blit(self.images[piece], p.Rect(c*self.square_size, r*self.square_size, self.square_size, self.square_size))