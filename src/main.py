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
        self.saved = []
        self.flash_box = None
        self.pieces = {"bR": lambda: Rook(2, IMAGES["bR"]), "bN": lambda: Knight(2, IMAGES["bN"]), "bB": lambda: Bishop(2, IMAGES["bB"]) , "bQ": lambda: Queen(2, IMAGES["bQ"]) ,"bK": lambda: King(2, IMAGES["bK"]),
                        "wR": lambda: Rook(1, IMAGES["wR"]), "wN": lambda: Knight(1, IMAGES["wN"]), "wB": lambda: Bishop(1, IMAGES["wB"]) , "wQ": lambda: Queen(1, IMAGES["wQ"]) ,"wK": lambda: King(1, IMAGES["wK"]),
                        "bp": lambda: Pawn(2, IMAGES["bp"]), "wp": lambda: Pawn(1, IMAGES["wp"]), "empty": lambda: Empty_Space()
                    }

        self.current_piece = 0
        self.time = 0

        self.initial_state = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bp" for i in range(8)],
            ["empty" for i in range(8)],
            ["empty" for i in range(8)],
            ["empty" for i in range(8)],
            ["empty"for i in range(8)],
            ["wp" for i in range(8)],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]
        ]

    def get_initial_state(self):
        initial_state= []
        for row in self.initial_state:
            initial_state.append([self.pieces[piece]()for piece in row])
        return initial_state

    def set_current_piece(self, rules):

        is_king = (self.current_piece == 5)

        white_piece_name = self.get_piece_name_from_index(self.current_piece)
        self.pieces[white_piece_name] = lambda: Piece(1, IMAGES[white_piece_name], rules, is_king)

        black_piece_name = self.get_piece_name_from_index(self.current_piece + 6)
        self.pieces[black_piece_name] = lambda: Piece(2, IMAGES[black_piece_name], rules, is_king)
        self.piece_created = Piece(1, IMAGES[white_piece_name], rules, is_king)


    def flip_slider(self):
        self.slider = not self.slider
        initial_state, pieces = generate_initial_state2()
        self.board = Board(initial_state, pieces)
        self.piece_created = None
        self.index = 1

    def increase_index(self):
        self.index += 1
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
        self.current_piece = (1+ self.current_piece) % 6
    
    def next_piece(self):
        self.increment_current_piece()
        next_piece = self.pieces[self.get_piece_name_from_index(self.current_piece)]()
        self.board.state[3][3] = next_piece

    def flash_text(self, screen):
        if self.time > 0:
            self.flash_box.draw(screen)

def generate_initial_state(gs):
    load_images()
    pieces = {"bQ": Queen(2, IMAGES["bQ"]), "wQ": Queen(1, IMAGES["wQ"])}
    initial_state = gs.get_initial_state()
        

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

def drawText(screen, text):
    font = p.font.SysFont("Helvitca", 32, True, False)
    rendered_text = font.render(text, 0, p.Color("Gray"))
    text_location = p.Rect(0,0,WIDHT, HEIGHT).move(WIDHT/2 - rendered_text.get_width()/2, HEIGHT/2 - rendered_text.get_height()/2)
    screen.blit(rendered_text, text_location)
    text_shadow = font.render(text, 0, p.Color("Black"))
    screen.blit(text_shadow, text_location.move(2,2))

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
    game_over = False
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN and not game_over: 
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
        board.drawGameState(screen, valid_moves, selected_square)

        if board.checkmate():
            game_over = True
            if board.turn == 1:
                drawText(screen, "Black wins by checkmate")
            else:
                drawText(screen, "White wins by checkmate")

        if board.stalemate():
            game_over = True
            drawText(screen, "Stalemate")

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
    gs.increase_index()
    gs.index = 1
    for i in range(1, gs.index+1):
        index_rules = []
        
        index_coordinates = [x for x in gs.saved if x[2] == i]
        current_coordinates = (3,3)
        while index_coordinates != []:
            new_coordinates = [
                (current_coordinates[0]+1, current_coordinates[1], i),
                (current_coordinates[0]-1, current_coordinates[1], i),
                (current_coordinates[0], current_coordinates[1]+1, i),
                (current_coordinates[0], current_coordinates[1]-1, i),
                (current_coordinates[0]-1, current_coordinates[1]-1, i),
                (current_coordinates[0]+1, current_coordinates[1]-1, i),
                (current_coordinates[0]-1, current_coordinates[1]+1, i),
                (current_coordinates[0]+1, current_coordinates[1]+1, i),
                ]

            for coordinate in new_coordinates:
                if coordinate in index_coordinates:
                    difference = (coordinate[0] - current_coordinates[0] , coordinate[1] - current_coordinates[1] )
                    current_coordinates = (coordinate[0], coordinate[1])
                    index_rules.append(SingleSlide(difference[1], difference[0]))
                    index_coordinates.remove(coordinate)
                    break
        
        rules.append(CombinedSlide(index_rules))
    gs.set_current_piece(rules)
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
    boxes = [ClickBox(0,0,140,height, lambda: True, text="Back")]
    for i, piece in enumerate(pieces):
        rules = [rule_reader.json_to_rule(rule) for rule in piece["rules"]]
        def fun():
            gs.set_current_piece(rules)
            return True
        
        boxes.append(ClickBox(0,(i+1)*height,140,height, fun, text=piece["name"]))

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
    name_box = ClickBox(0, 0, 140, 40, lambda: None, "Name")
    input_box = InputBox(0, 40, 140, 32)
    boxes = [input_box, name_box]

    done = False

    while not done:
        for event in p.event.get():
            if event.type == p.QUIT:
                done = True
            name = input_box.handle_event(event)
            if name is not None and name != '':
                done = True
                upload_piece(name, gs.piece_created.rules)

        input_box.update()
        for box in boxes:
            box.draw(screen)

        p.display.flip()
        clock.tick(30)

def customize_board(gs, screen):
    done = False
    gs.clear_initial_state()
    initial_state, pieces = generate_initial_state(gs)
    gs.board = Board(initial_state, pieces)
    box1 = ClickBox(WIDHT-140, 0, 140, 40, lambda: gs.increment_current_piece(), "Next piece")
    def fun():
        nonlocal done
        done = True
    
    box2 = ClickBox(WIDHT-140, 40, 140, 40, fun, "Done")
    boxes = [box1, box2]
    while not done:

        for e in p.event.get():
            location = p.mouse.get_pos()
            
            if e.type == p.MOUSEBUTTONDOWN and (WIDHT-140 > location[0] or location[1]>80):
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                opposite_row = 3-(row-4) if row>=4 else 4+(3-row)
                gs.initial_state[row][col] = gs.get_piece_name_from_index(gs.current_piece)
                gs.initial_state[opposite_row][col] = gs.get_piece_name_from_index(gs.current_piece+6)
                initial_state, pieces = generate_initial_state(gs)
                gs.board = Board(initial_state, pieces)

            else:
                for box in boxes:
                    box.handle_event(e)



        gs.board.drawGameState(screen)
        for box in boxes:
            box.draw(screen)
        p.display.flip()
    
    initial_state, pieces = generate_initial_state2()
    gs.board = Board(initial_state, pieces)
    

def create_piece():
    screen = p.display.set_mode((WIDHT, HEIGHT))
    gs = GameState()


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
        box8 = ClickBox(WIDHT-140, 240, 140, 40, lambda: customize_board(gs, screen), "Customize board")
        box2 = ClickBox(WIDHT-140, 40, 140, 40, gs.flip_slider, "Slider" if gs.slider else "Jumper")
        boxes = [box, box2, box3, box5, box6, box7, box8]
        for e in p.event.get():
            location = p.mouse.get_pos()
            if e.type == p.QUIT:
                running = False
            
            elif e.type == p.MOUSEBUTTONDOWN and (WIDHT-140 > location[0] or location[1]>280):
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if gs.slider:
                    if col == 3 and row == 3:
                        gs.increase_index()
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
    menu = pygame_menu.Menu('Bizarro Chess', 400, 300,
                       theme=pygame_menu.themes.THEME_BLUE)

    menu.add.button('Play', start_the_game)
    menu.add.button("Settings", create_piece)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(screen)
    
    





if __name__ == "__main__":
    main()
