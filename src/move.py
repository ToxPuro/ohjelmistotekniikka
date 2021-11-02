class Move():
    def __init__(self, startSq, endSq, board):
        self.start_row = startSq[0]
        self.start_col = startSq[1]
        self.end_row = endSq[0]
        self.end_col = endSq[1]
        self.piece_moved = board.state[self.start_row][self.start_col]
        self.piece_captured = board.state[self.end_row][self.end_col]


        self.is_double_pawn_forward = False
        if self.piece_moved.is_pawn():
            between_row = max(self.start_row, self.end_row) - min(self.start_row, self.end_row)
            if between_row > 1:
                self.is_double_pawn_forward = True



        self.is_pawn_promotion = False
        if self.piece_moved.is_pawn() and (self.end_row == 0 or self.end_row == 7):
            self.is_pawn_promotion = True

    def __eq__(self, other):
        if not isinstance(other, Move):
            return False
        
        return other.start_row == self.start_row and other.start_col == self.start_col and other.end_row == self.end_row and self.end_col == other.end_col

    def __str__(self):
        return f"{self.start_col}, {self.start_row}, {self.end_col}, {self.end_row}"