from pieces import Empty_Space, EnPassantSquare, SelectedJumpSquare, SelectedSlideSquare
from ui.board_ui import BoardUI

class Board():
    def __init__(self, state, pieces, dimension=8, square_size=64, player_num=2):
        self.state = state
        self.dimension = dimension
        self.square_size = square_size
        self.turn = 1
        self.king_locations = {1: (7, 4), 2: (0, 4)}
        self.player_num = player_num
        self.move_log = []
        self.pieces = pieces
        self.en_passant_squares = []
        self.selected = []
        self.board_ui = BoardUI()


    def draw_game_state(self, screen, valid_moves=[], selected_square=()):
        self.board_ui.draw_game_state(screen, valid_moves, selected_square, self)

    def make_move(self, move, simulation=False):

        self.state[move.start_row][move.start_col] = Empty_Space()
        self.state[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)

        if move.piece_moved.is_king():
            self.king_locations[self.turn] = (move.end_row, move.end_col)

        if move.is_pawn_promotion:
            self.promote(move)

        if not simulation:
            if move.piece_moved.is_king and move.end_col - move.start_col == 2:
                self.state[move.start_row][move.start_col +
                                           1] = self.state[move.end_row][move.end_col+1]
                self.state[move.end_row][move.end_col+1] = Empty_Space()

            if move.piece_moved.is_king and move.end_col - move.start_col == -2:
                self.state[move.start_row][move.start_col -
                                           1] = self.state[move.end_row][move.end_col-2]
                self.state[move.end_row][move.end_col-2] = Empty_Space()

            self.delete_en_passant_squares()
            if move.is_double_pawn_forward:
                self.create_en_passant_square(move)
            move.piece_moved.set_as_moved()
            self.swap_turns()

    def swap_turns(self):
        self.turn = 2 if self.turn == 1 else 1

    def get_all_possible_moves(self, player, no_king=False):
        moves = []
        for row, _ in enumerate(self.state):
            for col, _ in enumerate(self.state[row]):
                piece = self.state[row][col]
                # ugly implementation to sidestep infinite recursion where
                if not (piece.is_king() and no_king) and player == piece.player:
                    piece_moves = piece.get_moves((row, col), self)
                    moves.extend(piece_moves)
        return moves

    def get_all_valid_moves(self):
        moves = self.get_all_possible_moves(self.turn)
        for i in range(len(moves)-1, -1, -1):
            self.make_move(moves[i], simulation=True)
            if self.in_check():
                moves.remove(moves[i])
            self.undo_move(swap=False)

        return moves

    def checkmate(self):
        return len(self.get_all_valid_moves()) == 0 and self.in_check()

    def stalemate(self):
        return len(self.get_all_valid_moves()) == 0 and not self.in_check()

    def in_check(self):
        return self.square_under_attack(self.king_locations[self.turn])

    def undo_move(self, swap=True):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.state[move.start_row][move.start_col] = move.piece_moved
            self.state[move.end_row][move.end_col] = move.piece_captured
            if swap:
                self.swap_turns()
            if move.piece_moved.is_king():
                self.king_locations[self.turn] = (
                    move.start_row, move.start_col)

    def square_under_attack(self, position):
        for player in range(1, self.player_num+1):
            if player != self.turn:
                opponents_moves = self.get_all_possible_moves(
                    player, no_king=True)
                for move in opponents_moves:
                    if move.end_row == position[0] and move.end_col == position[1]:
                        print("under attack")
                        return True
        return False

    def delete_en_passant_squares(self):
        if self.en_passant_squares:
            en_passant_square = self.en_passant_squares.pop()
            if self.state[en_passant_square[0]][en_passant_square[1]].is_en_passant():
                self.state[en_passant_square[0]
                           ][en_passant_square[1]] = Empty_Space()

    def create_en_passant_square(self, move):
        if self.turn == 1:
            between_row = move.end_row+1
        else:
            between_row = move.end_row-1
        self.state[between_row][move.end_col] = EnPassantSquare()
        self.en_passant_squares.append((between_row, move.end_col))

    def promote(self, move):
        if self.turn == 1:
            self.state[move.end_row][move.end_col] = self.pieces["wQ"]
        else:
            self.state[move.end_row][move.end_col] = self.pieces["bQ"]

    def set_jump_selected(self, row, col, is_attack):
        if self.state[row][col].is_empty():
            self.state[row][col] = SelectedJumpSquare()
            self.selected.append((row, col, is_attack))
        else:
            self.selected.remove((row, col, is_attack))
            self.state[row][col] = Empty_Space()

    def set_slide_selected(self, row, col, index, is_attack):
        if self.state[row][col].is_empty():
            self.state[row][col] = SelectedSlideSquare(index)
            self.selected.append((row, col, index, is_attack))
        else:
            self.selected.remove((row, col, index, is_attack))
            self.state[row][col] = Empty_Space()

    def delete_old_selected_squares(self):
        for square in self.selected:
            self.state[square[0]][square[1]] = Empty_Space()
        self.selected = []
