from pieces import Empty_Space, EnPassantSquare, Queen
from move import Move
import pygame as p

class Board():
    def __init__(self, state, pieces, dimension=8, square_size=64, player_num=2):
        self.state = state
        self.dimension = dimension
        self.square_size = square_size
        self.turn = 1
        self.king_locations = {1: (7,4), 2: (0,4)}
        self.player_num = player_num
        self.move_log = []
        self.pieces = pieces
        self.en_passant_squares = []
    
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
        

    def makeMove(self, move, simulation=False):
        self.state[move.start_row][move.start_col] = Empty_Space()
        self.state[move.end_row][move.end_col] = move.piece_moved
        
        if move.piece_moved.is_king():
            self.king_locations[self.turn] = (move.end_row, move.end_col)
        self.move_log.append(move)

        if move.is_pawn_promotion:
            if self.turn == 1:
                self.state[move.end_row][move.end_col] = self.pieces["wQ"]
            else:
                self.state[move.end_row][move.end_col] = self.pieces["bQ"]
            
        if not simulation:
            if self.en_passant_squares != []:
                en_passant_square = self.en_passant_squares.pop()
                if self.state[en_passant_square[0]][en_passant_square[1]].is_en_passant():
                    self.state[en_passant_square[0]][en_passant_square[1]] = Empty_Space()
            if move.is_double_pawn_forward:
                if self.turn == 1:
                    between_row = move.end_row+1
                else:
                    between_row = move.end_row-1
                self.state[between_row][move.end_col] = EnPassantSquare()
                self.en_passant_squares.append((between_row, move.end_col))
            move.piece_moved.set_as_moved()
            if self.turn == 1:
                self.turn = 2
            else:
                self.turn = 1

    def get_all_possible_moves(self, player):
        moves = []
        for row in range(len(self.state)):
            for col in range(len(self.state[row])):
                piece = self.state[row][col]
                if player == piece.player:
                    piece_moves = piece.get_moves((row, col), self)
                    if piece.is_pawn():
                        for move in piece_moves:
                            print(move)
                    moves.extend(piece_moves)
        return moves

    def get_all_valid_moves(self):
        moves = self.get_all_possible_moves(self.turn)
        print(self.king_locations[self.turn])
        for i in range(len(moves)-1,-1,-1):
            self.makeMove(moves[i], simulation=True)
            if self.inCheck():
                moves.remove(moves[i])
            self.undoMove(swap=False)

        return moves

    def inCheck(self):
        return self.square_under_attack(self.king_locations[self.turn])

    def undoMove(self, swap = True):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.state[move.start_row][move.start_col] = move.piece_moved
            self.state[move.end_row][move.end_col] = move.piece_captured
            if swap:
                self.switchTurnBack()
            if move.piece_moved.is_king():
                self.king_locations[self.turn] = (move.start_row, move.start_col)

    def switchTurnBack(self):
        if self.turn == 1:
            self.turn = 2
        else:
            self.turn = 1
    def square_under_attack(self, position):
        for player in range(1, self.player_num+1):
            if player != self.turn:
                opponents_moves = self.get_all_possible_moves(player)
                for move in opponents_moves:
                    if move.end_row == position[0] and move.end_col == position[1]:
                        return True
        return False

            






