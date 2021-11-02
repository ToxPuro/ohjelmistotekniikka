from pieces import Empty_Space
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
        for row in range(len(self.state)):
            for col in range(len(self.state[row])):
                self.state[row][col].draw(screen, self.square_size, (row, col))
        

    def makeMove(self, move):
        self.board[move.start_row][move.start_col] = Empty_Space()
        self.board[move.end_row][move.end_col] = move.piece_moved

class Move():
    def __init__(self, startSq, endSq, board):
        self.start_row = startSq[0]
        self.start_col = startSq[1]
        self.end_row = endSq[0]
        self.end_col = endSq[1]
        self.piece_moved = board.state[self.start_row][self.start_col]
        self.pieceCaptured = board.state[self.end_row][self.end_col]
