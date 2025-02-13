import copy

import pygame

from juego.board import Board
from juego.constants import WIDTH, BOARD_BORDER, HEIGHT, SQUARE_SIZE, PINK, BLUE
from juego.game import Game

FPS = 60

WIN = pygame.display.set_mode((WIDTH + BOARD_BORDER * 2, HEIGHT + BOARD_BORDER * 2))
pygame.display.set_caption('Checkers')


def get_position_from_mouse(pos):  # la posicion conssiste en (cordenada_x, cordenada_y)
    x, y = pos  # dividimos pos en (x, y)
    row = (y - BOARD_BORDER) // SQUARE_SIZE
    col = (x - BOARD_BORDER) // SQUARE_SIZE

    if row > 7:
        print("row fuera del tablero")
        row = -1


    if col > 7:
        print("col fuera del tablero")
        col = -1

    return row, col


def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        if game.winner() is not None:
            print(game.winner())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_position_from_mouse(pos)
                print(row, col)
                if  row >= 0 and  col >= 0:
                    game.select(row, col)
                else: print("Has seleccionado el borde del tablero")

                # comprobarMovimientosIa(game.board)

        game.update()

    pygame.quit()

main()
