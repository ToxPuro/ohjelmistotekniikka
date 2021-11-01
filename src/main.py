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
            Rook(2, IMAGES["bR"], {"column": 0, "row": 0}), Knight(2, IMAGES["bN"], {"column": 1, "row": 0}), Bishop(2, IMAGES["bB"], {"column": 2, "row": 0}), Queen(2, IMAGES["bQ"], {"column": 3, "row": 0}), King(2, IMAGES["bK"], {"column": 4, "row": 0}), Bishop(2, IMAGES["bB"], {"column": 5, "row": 0}), Knight(2, IMAGES["bN"], {"column": 6, "row": 0}), Rook(2, IMAGES["bR"], {"column": 7, "row": 0}),
            Rook(1, IMAGES["wR"], {"column": 0, "row": 7}), Knight(1, IMAGES["wN"], {"column": 1, "row": 7}), Bishop(1, IMAGES["wB"], {"column": 2, "row": 7}), Queen(1, IMAGES["wQ"], {"column": 3, "row": 7}), King(1, IMAGES["wK"], {"column": 4, "row": 7}), Bishop(1, IMAGES["wB"], {"column": 5, "row": 7}), Knight(1, IMAGES["wN"], {"column": 6, "row": 7}), Rook(1, IMAGES["wR"], {"column": 7, "row": 7})
        ]
    initial_state.extend(Pawn(2, IMAGES["bp"], {"column": i, "row": 1}) for i in range(8))
    initial_state.extend(Empty_Space({"column": i, "row": 2}) for i in range(8))
    initial_state.extend(Empty_Space({"column": i, "row": 3}) for i in range(8))
    initial_state.extend(Empty_Space({"column": i, "row": 4}) for i in range(8))
    initial_state.extend(Empty_Space({"column": i, "row": 5}) for i in range(8))
    initial_state.extend(Pawn(1, IMAGES["wp"], {"column": i, "row": 6}) for i in range(8))
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
    board.drawGameState(screen)
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        
        clock.tick(MAX_FPS)
        p.display.flip()




if __name__ == "__main__":
    main()
