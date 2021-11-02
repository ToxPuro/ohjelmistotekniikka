import pygame as p
from board import Board
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

    return initial_state
    


def load_images():
    pieces = ["wp", "wR", "wN", "wB", "wK", "wQ", "bp", "bR", "bN", "bB", "bK", "bQ"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(f"../images/{piece}.png"), (SQ_SIZE, SQ_SIZE))



def main():
    p.init()
    screen = p.display.set_mode((WIDHT, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    initial_state = generate_initial_state()
    board = Board(initial_state)
    running = True
    selected_square = ()
    player_clicks = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouset.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if selected_square == (row, col):
                    selected_square = ()
                    player_clicks = []
                else:
                    selected_square = (row, col)
                    player_clicks.append(selected_square)
                if len(player_clicks) == 2:
                    pass

        board.drawGameState(screen)
        clock.tick(MAX_FPS)
        p.display.flip()




if __name__ == "__main__":
    main()
