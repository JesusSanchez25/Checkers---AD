import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.game import Game
from checkers.nodos import Nodo, imprimir_arbol
from checkers.board import Board
import copy

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        if game.winner() != None:
            print(game.winner())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

                comprobarMovimientosIa(game.board)


        game.update()

    pygame.quit()


def comprobarMovimientosIa(board: Board, color=RED, profundidad=2, nodoActual=Nodo("Raiz")):

    for i, fila in enumerate(board.board):
        for j, pieza in enumerate(fila):
            # odio python
            if (str(pieza) == str(color)):
                moves = board.get_valid_moves(pieza)
                if (len(moves) > 0):
                    for movimiento, capturas in moves.items():
                        nuevaRow, nuevaCol = movimiento  # Desempaquetar la posición
                        nodoHijo = Nodo(f"Movimiento a ({nuevaRow}, {nuevaCol}) - Capturas: {capturas}")
                        nodoActual.agregar_hijo(nodoHijo)

                        # Guardar la posición actual de la pieza para restaurarla luego
                        fila_original, col_original = pieza.row, pieza.col

                        # Mover la pieza a la nueva posición
                        board_copia: Board = copy.deepcopy(board)
                        pieza_copia = board_copia.get_piece(fila_original, col_original)
                        board_copia.move(pieza_copia, nuevaRow, nuevaCol)

                        # Mover la pieza en el tablero copiado
                        board_copia.print_board()

                        # Si no hemos alcanzado la profundidad máxima, seguir explorando
                        if profundidad > 0 and color == RED:
                            color = RED if color == WHITE else WHITE
                            comprobarMovimientosIa(board_copia, color, profundidad - 1, nodoHijo)

                        # Restaurar la posición original de la pieza
                        pieza.row, pieza.col = fila_original, col_original

                    # Si es el nodo raíz, imprimir el árbol
                    # print(moves)
                    if(nodoActual.valor == "Raiz"):
                        print()
                        # imprimir_arbol(nodoActual)
                else:
                    print()
    # # Obtener movimientos válidos para la pieza
    # moves = game.board.get_valid_moves(pieza)
    # print(f"Movimientos válidos para la pieza en ({pieza.row}, {pieza.col}): {moves}")

    # # Explorar cada movimiento
    # for movimiento, capturas in moves.items():
    #     nuevaRow, nuevaCol = movimiento  # Desempaquetar la posición
    #     nodoHijo = Nodo(f"Movimiento a ({nuevaRow}, {nuevaCol}) - Capturas: {capturas}")
    #     nodoActual.agregar_hijo(nodoHijo)

    #     # Guardar la posición actual de la pieza para restaurarla después
    #     fila_original, col_original = pieza.row, pieza.col

    #     # Mover la pieza a la nueva posición
    #     pieza.row, pieza.col = nuevaRow, nuevaCol

    #     # Si no hemos alcanzado la profundidad máxima, seguir explorando
    #     if profundidad > 0:
    #         comprobarMovimientosIa(game, pieza, profundidad - 1, nodoHijo)

    #     # Restaurar la posición original de la pieza
    #     pieza.row, pieza.col = fila_original, col_original

    # # Si es el nodo raíz, imprimir el árbol
    # if nodoActual.valor == "Raiz":
    #     imprimir_arbol(nodoActual)

    # # Actualizar el estado del juego (si es necesario)
    # game.update()

main()
