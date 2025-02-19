import pygame
import time
from juego.ai import comprobarMovimientosIa
from juego.board import Board
from juego.nodos import Nodo
from juego.db import cargar_movimientos, respuesta_movimientos
from juego.constants import PINK, SQUARE_SIZE, BOARD_BORDER, BLUE, HEIGHT, TIME

from juego.constants import IA_MATCH, HEIGHT, DB_ACTIVE
from juego.loser import menu_loser
from juego.winner import menu_winner

class Game:
    def __init__(self, win, ia):
        self._init()
        self.win = win
        self.ia = ia

    def update(self):
        self.update_timer()
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        self.draw_timer()
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = PINK
        self.valid_moves = {}
        self.pink_time = TIME
        self.blue_time = TIME
        self.last_time = time.time()
        self.dbActive = DB_ACTIVE
        self.turnNumber = 0

    def winner(self):
        return self.board.winner()

    def reset(self):
        self._init()

    def select(self, row, col):
        prev_row = self.selected.row if self.selected else None
        prev_col = self.selected.col if self.selected else None
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
            else:
                self.update()
                global IA_MATCH
                IA_MATCH= self.ia
                if self.turn == BLUE and IA_MATCH:
                    nuevo_nodo = Nodo("Raiz")
                    db_move = False
                    if (self.dbActive):
                        db_move = respuesta_movimientos(prev_row, prev_col, row, col, self, self.turnNumber)
                        self.turnNumber += 1
                        if (not db_move):
                            self.dbActive = False

                    if (not self.dbActive):
                        comprobarMovimientosIa(self.board, color=self.turn, nodoActual=nuevo_nodo, game=self)
                    self.turn = PINK

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
            # print(f"cambio de turno {self.turn}")
        else:
            return False

        return True


    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, PINK, ((col * SQUARE_SIZE + SQUARE_SIZE // 2) + BOARD_BORDER,
                                                (row * SQUARE_SIZE + SQUARE_SIZE // 2) + BOARD_BORDER), 15)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == PINK:
            self.turn = BLUE
        elif self.turn == BLUE:
            self.turn = PINK

    def update_timer(self):
        current_time = time.time()
        elapsed = current_time - self.last_time  # Tiempo transcurrido desde el último frame
        self.last_time = current_time  # Actualizar el tiempo de referencia

        if self.turn == PINK:
            self.pink_time -= elapsed
            if self.pink_time <= 0:
                self.pink_time = 0  # Asegurar que no sea negativo
                self.end_game(BLUE)  # Termina el juego si el tiempo llega a 0
        else:
            self.blue_time -= elapsed
            if self.blue_time <= 0:
                self.blue_time = 0  # Asegurar que no sea negativo
                self.end_game(PINK)  # Termina el juego si el tiempo llega a 0

    def draw_timer(self):
        font = pygame.font.Font("assets/fuente/neon.ttf", 41)

        # Convertir tiempo restante a formato mm:ss
        pink_minutes, pink_seconds = divmod(int(self.pink_time), 60)
        blue_minutes, blue_seconds = divmod(int(self.blue_time), 60)

        pink_time_str = f"{pink_minutes:02}:{pink_seconds:02}"  # Formato mm:ss
        blue_time_str = f"{blue_minutes:02}:{blue_seconds:02}"  # Formato mm:ss

        pink_time = font.render(pink_time_str, True, (255, 0, 254))
        blue_time = font.render(blue_time_str, True, (23, 151, 253))

        # Opcional: si mantienes el texto rojo/blanco para más contexto
        red_text = font.render(f"Rojo: {pink_time_str}", True, (200, 0, 0))  # Rojo oscuro
        white_text = font.render(f"Blanco: {blue_time_str}", True, (0, 0, 200))  # Azul fuerte

        self.win.blit(pink_time, (HEIGHT // 4 + BOARD_BORDER // 4, 0))
        self.win.blit(blue_time, (HEIGHT // 4 * 3 + BOARD_BORDER // 4, 0))

    def end_game(self, winner):
        if winner == BLUE:
            menu_loser()
        elif winner == PINK:
            menu_winner()
