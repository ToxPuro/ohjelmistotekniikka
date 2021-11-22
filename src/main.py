from os import WIFSIGNALED
import pygame as p
from board import Board, Move
from rule_reader import RuleReader
from rules import CombinedSlide, Jump, JumpAttack, SingleSlide
from input_box import ClickBox, InputBox
import db
import pygame_menu

WIDHT = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
SQ_SIZE = 64
from pieces import Rook, Pawn, Empty_Space, Knight, Bishop, Queen, King, Piece
class GameState():
    def __init__(self):
        self.piece_created = None
        self.slider = False
        initial_state, pieces = generate_initial_state2()
        self.board = Board(initial_state, pieces)
        self.index=1
        self.flash_box = None
        self.pieces = {"bR": lambda: Rook(2, IMAGES["bR"]), "bN": lambda: Knight(2, IMAGES["bN"]), "bB": lambda: Bishop(2, IMAGES["bB"]) , "bQ": lambda: Queen(2, IMAGES["bQ"]) ,"bK": lambda: King(2, IMAGES["bK"]),
                        "wR": lambda: Rook(1, IMAGES["wR"]), "wN": lambda: Knight(1, IMAGES["wN"]), "wB": lambda: Bishop(1, IMAGES["wB"]) , "wQ": lambda: Queen(1, IMAGES["wQ"]) ,"wK": lambda: King(1, IMAGES["wK"]),
                        "bp": lambda: Pawn(2, IMAGES["bp"]), "wp": lambda: Pawn(1, IMAGES["wp"])
                    }

        self.current_piece = 0
        self.time = 0

    def set_current_piece(self, rules):
        

        is_king = (self.current_piece == 5)

        white_piece_name = self.get_piece_name_from_index(self.current_piece)
        self.pieces[white_piece_name] = lambda: Piece(1, IMAGES[white_piece_name], rules, is_king)

        black_piece_name = self.get_piece_name_from_index(self.current_piece + 6)
        self.pieces[black_piece_name] = lambda: Piece(2, IMAGES[black_piece_name], rules, is_king)
        self.piece_created = Piece(1, IMAGES[white_piece_name], rules, is_king)


    def add_extra_rules(self, rules):
        self.extra_rules.append(rules)


    def flip_slider(self):
        self.slider = not self.slider
        initial_state, pieces = generate_initial_state2()
        self.board = Board(initial_state, pieces)
        self.extra_rules = None
        self.index = 1

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

    def next_piece(self):
        self.current_piece = (1+ self.current_piece) % 6
        print(self.current_piece)
        next_piece = self.pieces[self.get_piece_name_from_index(self.current_piece)]()
        self.board.state[3][3] = next_piece

    def flash_text(self, screen):
        if self.time > 0:
            self.flash_box.draw(screen)

def generate_initial_state(gs):
    load_images()
    pieces = {"bQ": Queen(2, IMAGES["bQ"]), "wQ": Queen(1, IMAGES["wQ"])}
    initial_state = [
            [gs.pieces["bR"](), gs.pieces["bN"](), gs.pieces["bB"](), gs.pieces["bQ"](), gs.pieces["bK"](), gs.pieces["bB"](), gs.pieces["bN"](), gs.pieces["bR"]()],
            [gs.pieces["bp"]() for i in range(8)],
            [Empty_Space() for i in range(8)],
            [Empty_Space() for i in range(8)],
            [Empty_Space() for i in range(8)],
            [Empty_Space() for i in range(8)],
            [gs.pieces["wp"]() for i in range(8)],
            [gs.pieces["wR"](), gs.pieces["wN"](), gs.pieces["wB"](), gs.pieces["wQ"](), gs.pieces["wK"](), gs.pieces["wB"](), gs.pieces["wN"](), gs.pieces["wR"]()]
        ]

    if gs.extra_rules != []:
        for rule in gs.extra_rules:
            initial_state[6] = [Piece(1, IMAGES["wR"], rule) for i in range(8)]
        

    return initial_state, pieces

def generate_initial_state2():
    load_images()
    pieces = {"bQ": Queen(2, IMAGES["bQ"]), "wQ": Queen(1, IMAGES["wQ"])}
    initial_state = [
            [Empty_Space() for i in range(8)],
            [Empty_Space() for i in range(8)],
            [Empty_Space() for i in range(8)],
            [Empty_Space(), Empty_Space(), Empty_Space(), Pawn(1, IMAGES["wp"]), Empty_Space(), Empty_Space(), Empty_Space(), Empty_Space()],
            [Empty_Space() for i in range(8)],
            [Empty_Space() for i in range(8)],
            [Empty_Space() for i in range(8)],
            [Empty_Space() for i in range(8)],
        ]

    return initial_state, pieces
    


def load_images():
    pieces = ["wp", "wR", "wN", "wB", "wK", "wQ", "bp", "bR", "bN", "bB", "bK", "bQ"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(f"../images/{piece}.png"), (SQ_SIZE, SQ_SIZE))


def start_the_game(gs=None):
    screen = p.display.set_mode((WIDHT, HEIGHT))
    if gs == None:
        gs = GameState()
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    initial_state, pieces = generate_initial_state(gs)
    board = Board(initial_state, pieces)
    running = True
    selected_square = ()
    player_clicks = []
    valid_moves = board.get_all_valid_moves()
    move_made = False
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if selected_square == (row, col):
                    selected_square = ()
                    player_clicks = []
                else:
                    selected_square = (row, col)
                    player_clicks.append(selected_square)
                if len(player_clicks) == 2:
                    move = Move(player_clicks[0], player_clicks[1], board)
                    for i in range(len(valid_moves)):
                        if move == valid_moves[i]:
                            move_made = True
                            board.makeMove(move)
                            selected_square = ()
                            player_clicks = []

                    
                    if not move_made:
                        player_clicks = [selected_square]
        
        if move_made:
            valid_moves = board.get_all_valid_moves()
            move_made = False
        board.drawGameState(screen)
        clock.tick(MAX_FPS)
        p.display.flip()

def save_piece(gs):
    gs.flash_box = ClickBox(0, 0, 140, 40, lambda: 1, "Saved")
    gs.time = 2000
    if gs.slider:
        save_sliding_piece(gs)
    else:
        save_jump_piece(gs)

def save_jump_piece(gs):
    rules = []
    for selected_square in gs.board.selected:
        rules.append(Jump(selected_square[1]-3, selected_square[0]-3))
        rules.append(JumpAttack(selected_square[1]-3, selected_square[0]-3))
    gs.set_current_piece(rules)

def save_sliding_piece(gs):
    rules = []
    for i in range(1, gs.index+1):
        index_rules = []
        index_coordinates = [x for x in gs.board.selected if x[2] == i]
        current_coordinates = (3,3)
        while index_coordinates != []:
            if (current_coordinates[0], current_coordinates[1]+1, i) in index_coordinates:
                index_rules.append(SingleSlide(1,0))
                current_coordinates = (current_coordinates[0], current_coordinates[1]+1)
                index_coordinates.remove((current_coordinates[0], current_coordinates[1], i))
            if (current_coordinates[0]-1, current_coordinates[1], i) in index_coordinates:
                index_rules.append(SingleSlide(0,-1))
                current_coordinates = (current_coordinates[0]-1, current_coordinates[1])
                index_coordinates.remove((current_coordinates[0], current_coordinates[1], i))
        rules.append(CombinedSlide(index_rules))
    gs.add_extra_rules(rules)
    return gs

def upload_piece(name, rules):
    json = {
        "name": name
    }
    json["rules"] = [rule.to_json() for rule in rules]
    db.insert_piece_to_db(json)

def download(screen, gs):
    rule_reader = RuleReader()
    pieces = db.get_db_pieces()
    clock = p.time.Clock()
    done = False
    height = 30
    boxes = []
    for i, piece in enumerate(pieces):
        rules = [rule_reader.json_to_rule(rule) for rule in piece["rules"]]
        def fun():
            gs.set_current_piece(rules)
            return True
        
        boxes.append(ClickBox(0,i*height,140,height, fun, text=piece["name"]))

    while not done:
        for event in p.event.get():
            if event.type == p.QUIT:
                done = True
            for box in boxes:
                clicked = box.handle_event(event)
                if not done: done = clicked

        for box in boxes:
            box.draw(screen)

        p.display.flip()
        clock.tick(30)

def upload(screen, gs):
    clock = p.time.Clock()
    input_box1 = InputBox(100, 100, 140, 32)
    input_boxes = [input_box1]
    done = False

    while not done:
        for event in p.event.get():
            if event.type == p.QUIT:
                done = True
            for box in input_boxes:
                name = box.handle_event(event)
                if name is not None and name != '':
                    done = True
                    upload_piece(name, gs.piece_created.rules)


        for box in input_boxes:
            box.update()

        screen.fill((30, 30, 30))
        for box in input_boxes:
            box.draw(screen)

        p.display.flip()
        clock.tick(30)



def create_piece():
    screen = p.display.set_mode((WIDHT, HEIGHT))
    gs = GameState()

    

    # screen.blit(text , (WIDHT-140+50,0))
    # screen.blit(status_text , (WIDHT-140+50,40))
    # screen.blit(save_text , (WIDHT-140+50,80))
    # screen.blit(play_text , (WIDHT-140+50,120))
    # screen.blit(upload_text, (WIDHT-140+50,160))


    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    running = True
    selected_square = ()
    player_clicks = []

    while running:
        box = ClickBox(WIDHT-140, 0, 140, 40, lambda: start_the_game(gs), "Play")
        box3 = ClickBox(WIDHT-140, 80, 140, 40, lambda: save_piece(gs), "Save")
        box5 = ClickBox(WIDHT-140, 120, 140, 40, lambda: upload(screen, gs), "Upload")
        box6 = ClickBox(WIDHT-140, 160, 140, 40, lambda: download(screen, gs), "Download")
        box7 = ClickBox(WIDHT-140, 200, 140, 40, lambda: gs.next_piece(), "Next piece")
        box2 = ClickBox(WIDHT-140, 40, 140, 40, gs.flip_slider, "Slider" if gs.slider else "Jumper")
        boxes = [box, box2, box3, box5, box6, box7]
        for e in p.event.get():
            location = p.mouse.get_pos()
            if e.type == p.QUIT:
                running = False
            
            elif e.type == p.MOUSEBUTTONDOWN and (WIDHT-140 > location[0] or location[1]>240):
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if gs.slider:
                    if col == 3 and row == 3:
                        gs.index = gs.index+1
                    else:
                        gs.board.set_slide_selected(row, col, gs.index)
                else:
                    gs.board.set_jump_selected(row, col)
                if selected_square == (row, col):
                    selected_square = ()
                    player_clicks = []
                else:
                    selected_square = (row, col)
                    player_clicks.append(selected_square)

            else:
                for box in boxes:
                    box.handle_event(e)

        gs.board.drawGameState(screen)
        for box in boxes:
            box.draw(screen)
        gs.time -= clock.tick(MAX_FPS)
        gs.flash_text(screen)

        p.display.flip()


def main():
    p.init()
    screen = p.display.set_mode((WIDHT, HEIGHT))
    menu = pygame_menu.Menu('Welcome', 400, 300,
                       theme=pygame_menu.themes.THEME_BLUE)

    menu.add.text_input('Name :', default='John Doe')
    menu.add.button('Play', start_the_game)
    menu.add.button("Create a new piece", create_piece)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(screen)
    
    





if __name__ == "__main__":
    main()
