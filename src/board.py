from pieces import Empty_Space
from move import Move
import pygame as p

class Board():
    def __init__(self, state, dimension=8, square_size=64):
        self.state = state
        self.dimension = dimension
        self.square_size = square_size
        self.turn = 1
    
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
        self.state[move.start_row][move.start_col] = Empty_Space()
        self.state[move.end_row][move.end_col] = move.piece_moved

    def get_all_possible_moves(self):
        moves = []
        for row in range(len(self.state)):
            for col in range(len(self.state[row])):
                piece = self.state[row][col]
                if self.turn == piece.player:
                    piece_moves = piece.get_moves((row, col), self)
                    if piece_moves != []:
                        for move in piece_moves:
                            print(f"piece move {move}")
                    moves.extend(piece_moves)
        return moves

    def get_all_valid_moves(self):
        return self.get_all_possible_moves()




