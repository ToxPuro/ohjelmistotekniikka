import pygame as p
from board import Board, Move
import generate

WIDHT = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15

IMAGES = {}
SQ_SIZE = 64
from pieces import Rook, Pawn, Empty_Space, Knight, Bishop, Queen, King

def generate_initial_state():
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

    return initial_state, pieces
    


def load_images():
    pieces = ["wp", "wR", "wN", "wB", "wK", "wQ", "bp", "bR", "bN", "bB", "bK", "bQ"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(f"../images/{piece}.png"), (SQ_SIZE, SQ_SIZE))



def main():
    p.init()
    screen = p.display.set_mode((WIDHT, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    initial_state, pieces = generate_initial_state()
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




if __name__ == "__main__":
    main()
