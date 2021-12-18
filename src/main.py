import pygame_menu
import pygame as p
from pygame.constants import (
    MOUSEBUTTONDOWN, QUIT
)
from board import Board
from move import Move
from rule_reader import RuleReader
from ui.input_box import ClickBox, InputBox
import db
from setting import Setting
from generate import generate_initial_state, generate_initial_state2
from configs import WIDHT, HEIGHT, SQ_SIZE, MAX_FPS

"""The application entrypoint where the actual game is run
"""






def draw_text(screen, text):
    """Helper function to draw text

    Args:
        screen: Pygame screen to draw on
        text (string): Text to draw
    """
    font = p.font.SysFont("Helvitca", 32, True, False)
    rendered_text = font.render(text, 0, p.Color("Gray"))
    text_location = p.Rect(0, 0, WIDHT, HEIGHT).move(
        WIDHT/2 - rendered_text.get_width()/2, HEIGHT/2 - rendered_text.get_height()/2)
    screen.blit(rendered_text, text_location)
    text_shadow = font.render(text, 0, p.Color("Black"))
    screen.blit(text_shadow, text_location.move(2, 2))


def start_the_game(setting=None):
    """Function to actually run the game

    Args:
        setting (Setting, optional): The settings the player has chosen. Defaults to None.
    """
    setting = Setting() if setting is None else setting
    screen = p.display.set_mode((setting.width, setting.height))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    initial_state, pieces = generate_initial_state(setting)
    board = Board(initial_state, pieces)
    running = True
    selected_square = ()
    player_clicks = []
    valid_moves = board.get_all_valid_moves()
    move_made = False
    game_over = False
    while running:
        for event in p.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN and not game_over:
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
                    for valid_move in valid_moves:
                        if move == valid_move:
                            move_made = True
                            board.make_move(move)
                            selected_square = ()
                            player_clicks = []

                    if not move_made:
                        player_clicks = [selected_square]

        if move_made:
            valid_moves = board.get_all_valid_moves()
            move_made = False
        board.draw_game_state(screen, valid_moves, selected_square)

        if board.checkmate():
            game_over = True
            if board.turn == 1:
                draw_text(screen, "Black wins by checkmate")
            else:
                draw_text(screen, "White wins by checkmate")

        if board.stalemate():
            game_over = True
            draw_text(screen, "Stalemate")

        clock.tick(MAX_FPS)
        p.display.flip()











def download(screen, setting):
    """Helper function to choose which piece to download. Sets the current piece to be the downloaded piece

    Args:
        screen: Pygame screen to draw on
        setting (Setting): Settings the player has currently chosen
        
    """
    rule_reader = RuleReader()
    pieces = db.get_db_pieces()
    clock = p.time.Clock()
    done = False
    height = 30
    boxes = [ClickBox(0, 0, 140, height, lambda: True, text="Back")]
    for i, piece in enumerate(pieces):
        rules = [rule_reader.json_to_rule(rule) for rule in piece["rules"]]

        def fun():
            setting.set_current_piece(rules)
            return True

        boxes.append(ClickBox(0, (i+1)*height, 140,
                     height, fun, text=piece["name"]))

    while not done:
        for event in p.event.get():
            if event.type == QUIT:
                done = True
            for box in boxes:
                clicked = box.handle_event(event)
                if not done:
                    done = clicked

        for box in boxes:
            box.draw(screen)

        p.display.flip()
        clock.tick(30)


def input_phase(screen, func, input_name):
    """Helper function to get user input

    Args:
        screen: Pygame screen to draw on
        func (function): Function that gets the user's input and is run
        input_name (string): What to draw over input box
    """
    clock = p.time.Clock()
    name_box = ClickBox(0, 0, 140, 40, lambda: None, input_name)
    input_box = InputBox(0, 40, 140, 32)
    boxes = [input_box, name_box]

    done = False

    while not done:
        for event in p.event.get():
            if event.type == QUIT:
                done = True
            name = input_box.handle_event(event)
            if name is not None and name != '':
                done = True
                func(name)
        input_box.update()
        for box in boxes:
            box.draw(screen)

        p.display.flip()
        clock.tick(30)


def customize_board(setting, screen):
    """Customize the piece positions

    Args:
        setting (Setting): Settings the player has currently chosen
        screen: Pygame screen to draw on
    """
    done = False
    clock = p.time.Clock()
    setting.clear_initial_state()
    initial_state, pieces = generate_initial_state(setting)
    setting.board = Board(initial_state, pieces)
    box1 = ClickBox(WIDHT-140, 0, 140, 40,
                    lambda: setting.increment_current_piece(), "Next piece")

    def fun():
        nonlocal done
        kings = 0
        for row, _ in enumerate(setting.board.state):
            for col, _ in enumerate(setting.board.state[row]):
                piece = setting.board.state[row][col]
                if piece.is_king():
                    kings += 1
        if kings==2:
            done = True
        else:
            setting.set_flash_box("One king")

    box2 = ClickBox(WIDHT-140, 40, 140, 40, fun, "Done")
    boxes = [box1, box2]
    while not done:

        for event in p.event.get():
            location = p.mouse.get_pos()

            if event.type == MOUSEBUTTONDOWN and (WIDHT-140 > location[0] or location[1] > 80):
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                opposite_row = 3-(row-4) if row >= 4 else 4+(3-row)
                setting.initial_state[row][col] = setting.get_piece_name_from_index(
                    setting.current_piece)
                setting.initial_state[opposite_row][col] = setting.get_piece_name_from_index(
                    setting.current_piece+6)
                initial_state, pieces = generate_initial_state(setting)
                setting.board = Board(initial_state, pieces)

            else:
                for box in boxes:
                    box.handle_event(event)

        setting.board.draw_game_state(screen)
        for box in boxes:
            box.draw(screen)
        setting.time -= clock.tick(MAX_FPS)
        setting.flash_text(screen)
        p.display.flip()


def settings():
    """Player chooses settingss
    """
    setting = Setting()
    old_width = setting.width
    screen = p.display.set_mode((setting.width, setting.height))
    screen.fill(p.Color("white"))
    clock = p.time.Clock()
    
    running = True

    while running:


        if old_width != setting.width:
            screen = p.display.set_mode((setting.width, setting.height))
            old_width = setting.width

        box = ClickBox(WIDHT-140, 0, 140, 40,
                       lambda: start_the_game(setting), "Play")
        box11 = ClickBox(WIDHT-140, 40, 140, 40, setting.toggle_menu, "Menu")
        box12 = ClickBox(WIDHT-140, 400, 140, 40, setting.toggle_menu, "Hide")
        box3 = ClickBox(WIDHT-140, 80, 140, 40, setting.save_piece, "Save")
        upload_func = lambda name: db.upload_piece(name, setting.piece_created.rules)
        box5 = ClickBox(WIDHT-140, 120, 140, 40,
                        lambda: input_phase(screen, upload_func, "Name" ), "Upload")
        box6 = ClickBox(WIDHT-140, 160, 140, 40,
                        lambda: download(screen, setting), "Download")
        box7 = ClickBox(WIDHT-140, 200, 140, 40,
                        lambda: setting.next_piece(), "Next piece")
        box8 = ClickBox(WIDHT-140, 240, 140, 40,
                        lambda: customize_board(setting, screen), "Customize board")
        box2 = ClickBox(WIDHT-140, 40, 140, 40, setting.flip_slider,
                        "Slider" if setting.slider else "Jumper")
        box4 = ClickBox(WIDHT-140, 280, 140, 40, setting.flip_attack, "Attack" if setting.attack else "Movement")
        box9 = ClickBox(WIDHT-140, 320, 140, 40, setting.copy_to_other, "Copy")
        box10 = ClickBox(WIDHT-140, 360, 140, 40, setting.reset, "Reset")
        set_dimension_func = lambda dimension: setting.set_board_dimension(int(dimension))
        box13 = ClickBox(WIDHT-140, 440, 140, 40, lambda: input_phase(screen, set_dimension_func, "Dimension"), "Dimension")
        boxes = [box, box2, box3, box4, box5, box6, box7, box8, box9, box10, box12, box13] if setting.menu else [box, box11]
        for event in p.event.get():
            location = p.mouse.get_pos()
            if event.type == QUIT:
                running = False

            elif event.type == MOUSEBUTTONDOWN and (WIDHT-140 > location[0] or location[1] > (480 if setting.menu else 80)):
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if col == 3 and row == 3:
                    if setting.slider and col == 3:
                        setting.increase_index()
                        setting.save_rules()
                else:
                    setting.board.set_selected(row, col, setting.index, setting.attack, not setting.slider)

            else:
                for box in boxes:
                    box.handle_event(event)

        setting.board.draw_game_state(screen)
        for box in boxes:
            box.draw(screen)
        setting.time -= clock.tick(MAX_FPS)
        setting.flash_text(screen)

        p.display.flip()


def main():
    """Displays the menu to the player
    """
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
