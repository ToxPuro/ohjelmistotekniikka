import pygame as p
from board import Board, Move
from rule_reader import RuleReader
from ui.input_box import ClickBox, InputBox
import db
import pygame_menu
from setting import Setting
from generate import generate_initial_state, generate_initial_state2


WIDHT = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15

SQ_SIZE = 64







def drawText(screen, text):
    font = p.font.SysFont("Helvitca", 32, True, False)
    rendered_text = font.render(text, 0, p.Color("Gray"))
    text_location = p.Rect(0, 0, WIDHT, HEIGHT).move(
        WIDHT/2 - rendered_text.get_width()/2, HEIGHT/2 - rendered_text.get_height()/2)
    screen.blit(rendered_text, text_location)
    text_shadow = font.render(text, 0, p.Color("Black"))
    screen.blit(text_shadow, text_location.move(2, 2))


def start_the_game(gs=None):
    screen = p.display.set_mode((WIDHT, HEIGHT))
    gs = Setting() if gs == None else gs
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
        gs.save_sliding_piece()
    else:
        gs.save_jump_piece()











def download(screen, gs):
    rule_reader = RuleReader()
    pieces = db.get_db_pieces()
    clock = p.time.Clock()
    done = False
    height = 30
    boxes = [ClickBox(0, 0, 140, height, lambda: True, text="Back")]
    for i, piece in enumerate(pieces):
        rules = [rule_reader.json_to_rule(rule) for rule in piece["rules"]]

        def fun():
            gs.set_current_piece(rules)
            return True

        boxes.append(ClickBox(0, (i+1)*height, 140,
                     height, fun, text=piece["name"]))

    while not done:
        for event in p.event.get():
            if event.type == p.QUIT:
                done = True
            for box in boxes:
                clicked = box.handle_event(event)
                if not done:
                    done = clicked

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
                db.upload_piece(name, gs.piece_created.rules)

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
    box1 = ClickBox(WIDHT-140, 0, 140, 40,
                    lambda: gs.increment_current_piece(), "Next piece")

    def fun():
        nonlocal done
        done = True

    box2 = ClickBox(WIDHT-140, 40, 140, 40, fun, "Done")
    boxes = [box1, box2]
    while not done:

        for e in p.event.get():
            location = p.mouse.get_pos()

            if e.type == p.MOUSEBUTTONDOWN and (WIDHT-140 > location[0] or location[1] > 80):
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                opposite_row = 3-(row-4) if row >= 4 else 4+(3-row)
                gs.initial_state[row][col] = gs.get_piece_name_from_index(
                    gs.current_piece)
                gs.initial_state[opposite_row][col] = gs.get_piece_name_from_index(
                    gs.current_piece+6)
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


def settings():
    screen = p.display.set_mode((WIDHT, HEIGHT))
    gs = Setting()

    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    running = True
    selected_square = ()
    player_clicks = []

    while running:
        box = ClickBox(WIDHT-140, 0, 140, 40,
                       lambda: start_the_game(gs), "Play")
        box3 = ClickBox(WIDHT-140, 80, 140, 40, lambda: save_piece(gs), "Save")
        box5 = ClickBox(WIDHT-140, 120, 140, 40,
                        lambda: upload(screen, gs), "Upload")
        box6 = ClickBox(WIDHT-140, 160, 140, 40,
                        lambda: download(screen, gs), "Download")
        box7 = ClickBox(WIDHT-140, 200, 140, 40,
                        lambda: gs.next_piece(), "Next piece")
        box8 = ClickBox(WIDHT-140, 240, 140, 40,
                        lambda: customize_board(gs, screen), "Customize board")
        box2 = ClickBox(WIDHT-140, 40, 140, 40, gs.flip_slider,
                        "Slider" if gs.slider else "Jumper")
        boxes = [box, box2, box3, box5, box6, box7, box8]
        for e in p.event.get():
            location = p.mouse.get_pos()
            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN and (WIDHT-140 > location[0] or location[1] > 280):
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
    menu.add.button("Settings", settings)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(screen)


if __name__ == "__main__":
    main()
