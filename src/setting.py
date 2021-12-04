from board import Board
from generate import generate_initial_state2, IMAGES
from pieces import Rook, Knight, EmptySpace, Bishop, King, Pawn, Piece, Queen
from rules import Jump, JumpAttack, CombinedSlide, CombinedSlidingAttack, SingleSlide
from ui.input_box import ClickBox

class Setting():
    def __init__(self):
        self.piece_created = None
        self.slider = False
        self.attack = False
        self.menu = False
        initial_state, pieces = generate_initial_state2()
        self.board = Board(initial_state, pieces)
        self.index = 1
        self.saved = []
        self.flash_box = None
        self.pieces = {"bR": lambda: Rook(2, IMAGES["bR"]), "bN": lambda: Knight(2, IMAGES["bN"]), "bB": lambda: Bishop(2, IMAGES["bB"]), "bQ": lambda: Queen(2, IMAGES["bQ"]), "bK": lambda: King(2, IMAGES["bK"]),
                       "wR": lambda: Rook(1, IMAGES["wR"]), "wN": lambda: Knight(1, IMAGES["wN"]), "wB": lambda: Bishop(1, IMAGES["wB"]), "wQ": lambda: Queen(1, IMAGES["wQ"]), "wK": lambda: King(1, IMAGES["wK"]),
                       "bp": lambda: Pawn(2, IMAGES["bp"]), "wp": lambda: Pawn(1, IMAGES["wp"]), "empty": lambda: EmptySpace()
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


    def reset(self):
        initial_state, pieces = generate_initial_state2()
        self.board = Board(initial_state, pieces)
        self.piece_created = None
        self.index = 1

    def flip_slider(self):
        self.slider = not self.slider
        self.increase_index()

    def flip_attack(self):
        self.attack = not self.attack
        self.increase_index()

    def toggle_menu(self):
        self.menu = not self.menu


    def increase_index(self):
        self.index += 1
        self.save_chosen_squares()

    def save_chosen_squares(self):
        self.saved.extend(self.board.selected)
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

    def get_index_rules(self, index, is_attack):
        coordinates = [x for x in self.saved if x[2] == index and x[3] is is_attack and x[4] is False]
        rules = []
        current_coordinates = (3, 3)
        while coordinates != []:

            ## This boolean flag exists to notice when there are only incorrect leftover squares left
            leftovers = True
            new_coordinates = [
                (current_coordinates[0]+1, current_coordinates[1], index, is_attack, False),
                (current_coordinates[0]-1, current_coordinates[1], index, is_attack, False),
                (current_coordinates[0], current_coordinates[1]+1, index, is_attack, False),
                (current_coordinates[0], current_coordinates[1]-1, index, is_attack, False),
                (current_coordinates[0]-1, current_coordinates[1]-1, index, is_attack, False),
                (current_coordinates[0]+1, current_coordinates[1]-1, index, is_attack, False),
                (current_coordinates[0]-1, current_coordinates[1]+1, index, is_attack, False),
                (current_coordinates[0]+1, current_coordinates[1]+1, index, is_attack, False),
            ]

            for coordinate in new_coordinates:
                if coordinate in coordinates:
                    leftovers = False
                    difference = (
                        coordinate[0] - current_coordinates[0], coordinate[1] - current_coordinates[1])
                    current_coordinates = (coordinate[0], coordinate[1])
                    rules.append(SingleSlide(
                        difference[1], difference[0]))
                    coordinates.remove(coordinate)
                    break
            if leftovers:
                coordinates.pop(0)
        return rules

    def set_flash_box(self, string):
        self.flash_box = ClickBox(0, 0, 140, 40, lambda: None, string)
        self.time = 2000

    def save_piece(self):
        print(self.saved)
        self.set_flash_box("Saved")
        rules = self.generate_sliding_rules()
        rules.extend(self.generate_jump_rules())
        self.set_current_piece(rules)

    def generate_sliding_rules(self):
        self.increase_index()
        rules = [CombinedSlide(self.get_index_rules(i, False)) for i in range(1, self.index+1)]
        rules.extend([CombinedSlidingAttack(self.get_index_rules(i, True)) for i in range(1, self.index+1)])
        return rules

    def generate_jump_rules(self):
        self.save_chosen_squares()
        rules = [Jump(x[1]-3, x[0]-3) for x in self.saved if x[3] is False and x[4] is True]
        rules.extend([JumpAttack(x[1]-3, x[0]-3) for x in self.saved if x[3] is True and x[4] is True])
        return rules

    def copy_to_other(self):
        array_to_copy = [x for x in self.saved if x[3] == self.attack]
        array_to_copy.extend([(x[0], x[1], x[2], not x[3]) for x in array_to_copy])
        self.saved = array_to_copy
        self.save_piece()


