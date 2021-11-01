import pygame as p
from board import Board

WIDHT = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def load_images():
    pieces = ["wp", "wR", "wN", "wB", "wK", "wQ", "bp", "bR", "bN", "bB", "bK", "bQ"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(f"../images/{piece}.png"), (SQ_SIZE, SQ_SIZE))

def main():
    p.init()
    screen = p.display.set_mode((WIDHT, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    load_images()
    gs = Board(IMAGES)
    running = True
    drawGameState(screen, gs)
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, gs):
    gs.drawBoard(screen)
    gs.drawPieces(screen)


if __name__ == "__main__":
    main()
