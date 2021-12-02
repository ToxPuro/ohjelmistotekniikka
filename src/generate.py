import pygame as p
from pieces import Queen, Empty_Space, Pawn
WIDHT = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15

SQ_SIZE = 64
IMAGES = {}

def generate_initial_state(setting):
    load_images()
    pieces = {"bQ": Queen(2, IMAGES["bQ"]), "wQ": Queen(1, IMAGES["wQ"])}
    initial_state = setting.get_initial_state()

    return initial_state, pieces


def generate_initial_state2():
    load_images()
    pieces = {"bQ": Queen(2, IMAGES["bQ"]), "wQ": Queen(1, IMAGES["wQ"])}
    initial_state = [
        [Empty_Space() for i in range(8)],
        [Empty_Space() for i in range(8)],
        [Empty_Space() for i in range(8)],
        [Empty_Space(), Empty_Space(), Empty_Space(), Pawn(1, IMAGES["wp"]),
         Empty_Space(), Empty_Space(), Empty_Space(), Empty_Space()],
        [Empty_Space() for i in range(8)],
        [Empty_Space() for i in range(8)],
        [Empty_Space() for i in range(8)],
        [Empty_Space() for i in range(8)],
    ]

    return initial_state, pieces


def load_images():
    pieces = ["wp", "wR", "wN", "wB", "wK",
              "wQ", "bp", "bR", "bN", "bB", "bK", "bQ"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(
            f"./images/{piece}.png"), (SQ_SIZE, SQ_SIZE))
