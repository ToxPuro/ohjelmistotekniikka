import pygame as p
from pieces import Queen, EmptySpace, Pawn
from configs import SQ_SIZE
IMAGES = {}

"""Functions to generate initial states
"""

def generate_initial_state(setting):
    """Generates initial state for game board

    Args:
        setting (Setting): chosen settings from which to generate initial state

    Returns:
        initial state for game board
    """
    load_images()
    pieces = {"bQ": Queen(2, IMAGES["bQ"]), "wQ": Queen(1, IMAGES["wQ"])}
    initial_state = setting.get_initial_state()

    return initial_state, pieces


def generate_initial_state2(dimension):
    """Generates initial state for settings

    Args:
        dimension (int): The dimension of state to generate

    Returns:
        initial state for setting board
    """

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
