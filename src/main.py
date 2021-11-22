from os import WIFSIGNALED
import pygame as p
from board import Board, Move
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
        self.extra_rules = []

    def add_extra_rules(self, rules):
        self.extra_rules.append(rules)

def generate_initial_state(gs):
    load_images()
    pieces = {"bQ": Queen(2, IMAGES["bQ"]), "wQ": Queen(1, IMAGES["wQ"])}
    initial_state = [
            [Rook(2, IMAGES["bR"]), Knight(2, IMAGES["bN"]), Bishop(2, IMAGES["bB"]), Queen(2, IMAGES["bQ"]), King(2, IMAGES["bK"]), Bishop(2, IMAGES["bB"]), Knight(2, IMAGES["bN"]), Rook(2, IMAGES["bR"])],
            [Pawn(2, IMAGES["bp"]) for i in range(8)],
            [Empty_Space() for i in range(8)],
            [Empty_Space() for i in range(8)],
            [Empty_Space() for i in range(8)],
            [Empty_Space() for i in range(8)],
            [Pawn(1, IMAGES["wp"]) for i in range(8)],
            [Rook(1, IMAGES["wR"]), Knight(1, IMAGES["wN"]), Bishop(1, IMAGES["wB"]), Queen(1, IMAGES["wQ"]), King(1, IMAGES["wK"]), Bishop(1, IMAGES["wB"]), Knight(1, IMAGES["wN"]), Rook(1, IMAGES["wR"])]
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

def save_jump_piece(board, gs):
    rules = []
    for selected_square in board.selected:
        rules.append(Jump(selected_square[1]-3, selected_square[0]-3))
        print(selected_square[1]-3, selected_square[0]-3)
        rules.append(JumpAttack(selected_square[1]-3, selected_square[0]-3))
    gs.add_extra_rules(rules)
    return gs

def save_sliding_piece(board, index, gs):
    rules = []
    for i in range(1, index+1):
        index_rules = []
        index_coordinates = [x for x in board.selected if x[2] == i]
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


def load_pieces(screen, gs):
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
                    upload_piece(name, gs.extra_rules[0])


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
    index = 1
    slider = False
    hello = lambda : print("Hello")
    box = ClickBox(WIDHT-140, 0, 140, 40, hello, "Back")
    box2 = ClickBox(WIDHT-140, 40, 140, 40, hello, "Slider" if slider else "Jumper")
    box3 = ClickBox(WIDHT-140, 80, 140, 40, hello, "Save")
    box4 = ClickBox(WIDHT-140, 120, 140, 40, hello, "Play")
    box5 = ClickBox(WIDHT-140, 120, 140, 40, hello, "Upload")
    box6 = ClickBox(WIDHT-140, 160, 140, 40, hello, "Download")
    boxes = [box, box2, box3, box4, box5, box6]

    # screen.blit(text , (WIDHT-140+50,0))
    # screen.blit(status_text , (WIDHT-140+50,40))
    # screen.blit(save_text , (WIDHT-140+50,80))
    # screen.blit(play_text , (WIDHT-140+50,120))
    # screen.blit(upload_text, (WIDHT-140+50,160))


    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    initial_state, pieces = generate_initial_state2()
    board = Board(initial_state, pieces)
    running = True
    selected_square = ()
    player_clicks = []
    while running:
        for e in p.event.get():
            location = p.mouse.get_pos()
            if e.type == p.QUIT:
                running = False
            
            elif e.type == p.MOUSEBUTTONDOWN and (WIDHT-140 > location[0] or location[1]>200):
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if slider:
                    if col == 3 and row == 3:
                        index = index+1
                    else:
                        board.set_slide_selected(row, col, index)
                else:
                    board.set_jump_selected(row, col)
                if selected_square == (row, col):
                    selected_square = ()
                    player_clicks = []
                else:
                    selected_square = (row, col)
                    player_clicks.append(selected_square)

            else:
                for box in boxes:
                    box.handle_event(e)

        board.drawGameState(screen)
        for box in boxes:
            box.draw(screen)
        clock.tick(MAX_FPS)
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
