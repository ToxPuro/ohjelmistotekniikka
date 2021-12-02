import pygame as p



class BoardUI():

    def __init__(self):
        pass

    def highlight_squares(self, screen, valid_moves, selected_square, state, square_size, turn):
        if selected_square != ():
            row, column = selected_square
            if state[row][column].player == turn:
                square = p.Surface((square_size, square_size))
                square.set_alpha(100)
                square.fill(p.Color("blue"))
                screen.blit(square, (column*square_size, row*square_size))
                square.fill(p.Color("yellow"))
                for move in valid_moves:
                    if move.start_row == row and move.start_col == column:
                        screen.blit(square, (move.end_col*square_size,
                                    move.end_row*square_size))

    def draw_game_state(self, screen, valid_moves, selected_square, board):
        self.draw_squares(screen, board.dimension, board.square_size)
        self.highlight_squares(screen, valid_moves, selected_square, board.state, board.square_size, board.turn)
        self.draw_pieces(screen, board.state, board.square_size)

    def draw_squares(self, screen, dimension, square_size):
        colors = [p.Color("white"), p.Color("gray")]
        for row in range(dimension):
            for column in range(dimension):
                color = colors[((row+column) % 2)]
                p.draw.rect(screen, color, p.Rect(
                    column*square_size, row*square_size, square_size, square_size))

    def draw_pieces(self, screen, state, square_size):
        for row, _ in enumerate(state):
            for col, _ in enumerate(state[row]):
                state[row][col].draw(screen, square_size, (row, col))
