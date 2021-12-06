from pieces import EmptySpace, EnPassantSquare, SelectedSquare
from ui.board_ui import BoardUI
from configs import SQ_SIZE

class Board():
    """Class that represents the chess board and works also as our chess engine
    """
    def __init__(self, state, pieces, square_size=SQ_SIZE, player_num=2):
        self.state = state
        self.dimension = len(state)
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
        """Delegates board drawing to BoardUI

        Args:
            screen: pygame screen on which to draw
            valid_moves (list, optional): valid moves in the current state. Defaults to [].
            selected_square (tuple, optional): square that the player has selected. Defaults to ().
        """
        self.board_ui.draw_game_state(screen, valid_moves, selected_square, self)

    def make_move(self, move, simulation=False):
        """Makes a move in the board. Can be simulated when checking for valid moves

        Args:
            move (Move): The move that is performed
            simulation (bool, optional): Whether move is only simulated to check for valid moves. Defaults to False.
        """

        self.state[move.start_row][move.start_col] = EmptySpace()
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
                self.state[move.end_row][move.end_col+1] = EmptySpace()

            if move.piece_moved.is_king and move.end_col - move.start_col == -2:
                self.state[move.start_row][move.start_col -
                                           1] = self.state[move.end_row][move.end_col-2]
                self.state[move.end_row][move.end_col-2] = EmptySpace()

            self.delete_en_passant_squares()
            if move.is_double_pawn_forward:
                self.create_en_passant_square(move)
            move.piece_moved.set_as_moved()
            self.swap_turns()

    def swap_turns(self):
        """Changes the turn to the other player
        """
        self.turn = 2 if self.turn == 1 else 1

    def get_all_possible_moves(self, player, no_king=False):
        """Gets all possible moves, even those that are invalid

        Args:
            player (int): player whose moves to get
            no_king (bool, optional): Whether to get King's moves or not. Was included to sidestep infinite recursion
            Where kings check if the other king can eat them when castling which requires to check whether the other king can eat them while castling and so on. 
            Defaults to False.

        Returns:
            [type]: [description]
        """
        moves = []
        for row, _ in enumerate(self.state):
            for col, _ in enumerate(self.state[row]):
                piece = self.state[row][col]
                # ugly implementation to sidestep infinite recursion where
                if not (piece.is_king() and no_king and not piece.is_empty()) and player == piece.player:
                    piece_moves = piece.get_moves((row, col), self)
                    for move in piece_moves:
                        if move not in moves:
                            moves.append(move)
        return moves

    def get_all_valid_moves(self):
        """Returns the valid subset of all moves

        Returns:
            moves [Move]: all valid moves 
        """
        moves = self.get_all_possible_moves(self.turn)
        for i in range(len(moves)-1, -1, -1):
            self.make_move(moves[i], simulation=True)
            if self.in_check():
                moves.remove(moves[i])
            self.undo_move(swap=False)

        return moves

    def checkmate(self):
        """Returns whether the current state is checkmate

        Returns:
            checkmate bool: Whether it is checkmate
        """
        return len(self.get_all_valid_moves()) == 0 and self.in_check()

    def stalemate(self):
        """Returns whether the current state is stalemate 
        """ 
        return len(self.get_all_valid_moves()) == 0 and not self.in_check()

    def in_check(self):
        """Returns whether the the current player is in check

        Returns:
            returns True if is in check and False if not
        """
        return self.square_under_attack(self.king_locations[self.turn])

    def undo_move(self, swap=True):
        """Undoes the last move. swap is included since we don't want to swap the player when simulating

        Args:
            swap (bool, optional): Whether to swap the player after undoing the move. Defaults to True.
        """
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
        """Returns whether the square is under attack

        Args:
            position ([(row, col)]): the position to check if is under attack

        Returns:
            Returns True if under attack and false otherwise
        """
        for player in range(1, self.player_num+1):
            if player != self.turn:
                opponents_moves = self.get_all_possible_moves(
                    player, no_king=True)
                for move in opponents_moves:
                    if move.end_row == position[0] and move.end_col == position[1]:
                        return True
        return False

    def delete_en_passant_squares(self):
        """Removes the single en passant square if one exists
        """
        if self.en_passant_squares:
            en_passant_square = self.en_passant_squares.pop()
            if self.state[en_passant_square[0]][en_passant_square[1]].is_en_passant():
                self.state[en_passant_square[0]
                           ][en_passant_square[1]] = EmptySpace()

    def create_en_passant_square(self, move):
        """Creates an en passant square which pawns can eat

        Args:
            move (Move): The move that generated the en passant square
        """
        if self.turn == 1:
            between_row = move.end_row+1
        else:
            between_row = move.end_row-1
        self.state[between_row][move.end_col] = EnPassantSquare()
        self.en_passant_squares.append((between_row, move.end_col))

    def promote(self, move):
        """Promote a pawn to a Queen. TODO: other pieces

        Args:
            move (Move): The move that pushed the pawn to the end of the board
        """
        if self.turn == 1:
            self.state[move.end_row][move.end_col] = self.pieces["wQ"]
        else:
            self.state[move.end_row][move.end_col] = self.pieces["bQ"]

    def set_selected(self, row, col, index, is_attack, is_jump):
        """Sets a square in selected when creating piece movements

        Args:
            row (int): Row of the selected square
            col (int): Column of the selected square
            index (int): Which index the square belongs, is required to create sliding moves
            is_attack (bool): Whether the square is selected for attack move
            is_jump (bool): Whether the square is selected for jump move
        """
        if self.state[row][col].is_empty():
            self.state[row][col] = SelectedSquare(is_attack)
            self.selected.append((row, col, index, is_attack, is_jump))
        else:
            self.selected.remove((row, col, index, is_attack, is_jump))
            self.state[row][col] = EmptySpace()

    def delete_old_selected_squares(self):
        """Delete all selected squares
        """
        for square in self.selected:
            self.state[square[0]][square[1]] = EmptySpace()
        self.selected = []
