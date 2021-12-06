import pygame as p
from pieces import Queen, EmptySpace, Pawn
from configs import SQ_SIZE
IMAGES = {}

def generate_initial_state(setting):
    load_images()
    pieces = {"bQ": Queen(2, IMAGES["bQ"]), "wQ": Queen(1, IMAGES["wQ"])}
    initial_state = setting.get_initial_state()

    return initial_state, pieces


def generate_initial_state2(dimension):

    load_images()
    pieces = {"bQ": Queen(2, IMAGES["bQ"]), "wQ": Queen(1, IMAGES["wQ"])}
    initial_state = [[EmptySpace() for i in range(dimension)] for i in range(dimension)]
    initial_state[3][3] = Pawn(1, IMAGES["wp"])

    return initial_state, pieces


def load_images():
    pieces = ["wp", "wR", "wN", "wB", "wK",
              "wQ", "bp", "bR", "bN", "bB", "bK", "bQ"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(
            f"./images/{piece}.png"), (SQ_SIZE, SQ_SIZE))
