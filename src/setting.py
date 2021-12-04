from board import Board
from generate import generate_initial_state2, IMAGES
from pieces import Rook, Knight, Empty_Space, Bishop, King, Pawn, Piece, Queen
from rules import Jump, JumpAttack, CombinedSlide, CombinedSlidingAttack, SingleSlide
WIDHT = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
SQ_SIZE = 64

class Setting():
    def __init__(self):
        self.piece_created = None
        self.slider = False
        self.attack = False
        initial_state, pieces = generate_initial_state2()
        self.board = Board(initial_state, pieces)
        self.index = 1
        self.saved = []
        self.flash_box = None
        self.pieces = {"bR": lambda: Rook(2, IMAGES["bR"]), "bN": lambda: Knight(2, IMAGES["bN"]), "bB": lambda: Bishop(2, IMAGES["bB"]), "bQ": lambda: Queen(2, IMAGES["bQ"]), "bK": lambda: King(2, IMAGES["bK"]),
                       "wR": lambda: Rook(1, IMAGES["wR"]), "wN": lambda: Knight(1, IMAGES["wN"]), "wB": lambda: Bishop(1, IMAGES["wB"]), "wQ": lambda: Queen(1, IMAGES["wQ"]), "wK": lambda: King(1, IMAGES["wK"]),
                       "bp": lambda: Pawn(2, IMAGES["bp"]), "wp": lambda: Pawn(1, IMAGES["wp"]), "empty": lambda: Empty_Space()
                       }

        self.current_piece = 0
        self.time = 0

        self.initial_state = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp" for i in range(8)],
            ["empty" for i in range(8)],
            ["empty" for i in range(8)],
            ["empty" for i in range(8)],
            ["empty"for i in range(8)],
            ["wp" for i in range(8)],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]

    def get_initial_state(self):
        initial_state = []
        for row in self.initial_state:
            initial_state.append([self.pieces[piece]()for piece in row])
        return initial_state

    def set_current_piece(self, rules):

        is_king = (self.current_piece == 5)

        white_piece_name = self.get_piece_name_from_index(self.current_piece)
        self.pieces[white_piece_name] = lambda: Piece(
            1, IMAGES[white_piece_name], rules, is_king)

        black_piece_name = self.get_piece_name_from_index(
            self.current_piece + 6)
        self.pieces[black_piece_name] = lambda: Piece(
            2, IMAGES[black_piece_name], rules, is_king)
        self.piece_created = Piece(1, IMAGES[white_piece_name], rules, is_king)

    def flip_slider(self):
        self.slider = not self.slider
        initial_state, pieces = generate_initial_state2()
        self.board = Board(initial_state, pieces)
        self.piece_created = None
        self.index = 1

    def flip_attack(self):
        self.attack = not self.attack
        self.increase_index()


    def increase_index(self):
        self.index += 1
        self.saved.extend(self.board.selected)
        print(self.saved)
        self.board.delete_old_selected_squares()

    def clear_initial_state(self):
        self.initial_state = [
            ["empty" for i in range(8)],
            ["empty" for i in range(8)],
            ["empty" for i in range(8)],
            ["empty" for i in range(8)],
            ["empty" for i in range(8)],
            ["empty" for i in range(8)],
            ["empty" for i in range(8)],
            ["empty" for i in range(8)]
        ]

    def get_piece_name_from_index(self, index):
        index_to_pieces = {
            0: "wp",
            1: "wR",
            2: "wN",
            3: "wB",
            4: "wQ",
            5: "wK",

            6: "bp",
            7: "bR",
            8: "bN",
            9: "bB",
            10: "bQ",
            11: "bK",

        }
        return index_to_pieces[index]

    def increment_current_piece(self):
        self.current_piece = (1 + self.current_piece) % 6

    def next_piece(self):
        self.increment_current_piece()
        next_piece = self.pieces[self.get_piece_name_from_index(
            self.current_piece)]()
        self.board.state[3][3] = next_piece

    def flash_text(self, screen):
        if self.time > 0:
            self.flash_box.draw(screen)

    def generate_sliding_rules(self, index, is_attack):
        coordinates = [x for x in self.saved if x[2] == index and x[3] == is_attack]
        rules = []
        current_coordinates = (3, 3)
        while coordinates != []:
            new_coordinates = [
                (current_coordinates[0]+1, current_coordinates[1], index, is_attack),
                (current_coordinates[0]-1, current_coordinates[1], index, is_attack),
                (current_coordinates[0], current_coordinates[1]+1, index, is_attack),
                (current_coordinates[0], current_coordinates[1]-1, index, is_attack),
                (current_coordinates[0]-1, current_coordinates[1]-1, index, is_attack),
                (current_coordinates[0]+1, current_coordinates[1]-1, index, is_attack),
                (current_coordinates[0]-1, current_coordinates[1]+1, index, is_attack),
                (current_coordinates[0]+1, current_coordinates[1]+1, index, is_attack),
            ]

            for coordinate in new_coordinates:
                if coordinate in coordinates:
                    difference = (
                        coordinate[0] - current_coordinates[0], coordinate[1] - current_coordinates[1])
                    current_coordinates = (coordinate[0], coordinate[1])
                    rules.append(SingleSlide(
                        difference[1], difference[0]))
                    coordinates.remove(coordinate)
                    break

        return rules

    def save_sliding_piece(self):
        print(self.saved)
        rules = []
        self.increase_index()
        rules = [CombinedSlide(self.generate_sliding_rules(i, False)) for i in range(1, self.index+1)]
        rules.extend([CombinedSlidingAttack(self.generate_sliding_rules(i, True)) for i in range(1, self.index+1)])
        self.set_current_piece(rules)

    def save_jump_piece(self):
        rules = [Jump(selected_square[1]-3, selected_square[0]-3) for selected_square in self.saved if selected_square[2]==False]
        rules.extend([JumpAttack(selected_square[1]-3, selected_square[0]-3) for selected_square in self.saved if selected_square[2] == True])
        self.set_current_piece(rules)
