class Move():
    """Class for moves in the chess board.
    Has the moved piece, starting and end position and the possibly captured piece
    """
    def __init__(self, start_square, end_square, board):
        self.start_row = start_square[0]
        self.start_col = start_square[1]
        self.end_row = end_square[0]
        self.end_col = end_square[1]
        self.piece_moved = board.state[self.start_row][self.start_col]
        self.piece_captured = board.state[self.end_row][self.end_col]

        self.is_double_pawn_forward = False
        if self.piece_moved.is_pawn():
            between_row = max(self.start_row, self.end_row) - \
                min(self.start_row, self.end_row)
            if between_row > 1:
                self.is_double_pawn_forward = True

        self.is_pawn_promotion = False
        if self.piece_moved.is_pawn() and (self.end_row in (0,7)):
            self.is_pawn_promotion = True

    def __eq__(self, other):
        if not isinstance(other, Move):
            return False

        return other.start_row == self.start_row and other.start_col == self.start_col and other.end_row == self.end_row and self.end_col == other.end_col

    def __str__(self):
        return f"{self.start_col}, {self.start_row}, {self.end_col}, {self.end_row}"
