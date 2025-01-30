import pygame
from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE
from .piece import Piece

class Board:
    def __init__(self):
        # Inicializa el tablero y las variables de estado del juego
        self.board = []  # Matriz que representa el tablero
        self.red_left = self.white_left = 12  # Número de piezas rojas y blancas restantes
        self.red_kings = self.white_kings = 0  # Número de reyes rojos y blancos
        self.create_board()  # Llama a la función para crear el tablero inicial

    def draw_squares(self, win):
        # Dibuja los cuadrados del tablero en la ventana proporcionada
        win.fill(BLACK)  # Rellena la ventana con color negro
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                # Dibuja cuadrados rojos en las posiciones adecuadas
                pygame.draw.rect(win, RED, (row*SQUARE_SIZE, col *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def move(self, piece, row, col):
        # Mueve una pieza a una nueva posición en el tablero
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)  # Actualiza la posición de la pieza

        # Si la pieza llega a la última fila, se convierte en rey
        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1

    def get_piece(self, row, col):
        # Devuelve la pieza en la posición (row, col) del tablero
        return self.board[row][col]

    def create_board(self):
        # Crea el tablero inicial con las piezas en sus posiciones de inicio
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 2:
                        # Coloca piezas blancas en las primeras dos filas
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > ROWS - 3:
                        # Coloca piezas rojas en las últimas dos filas
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        # Espacios vacíos en el medio del tablero
                        self.board[row].append(0)
                else:
                    # Espacios vacíos en las posiciones alternas
                    self.board[row].append(0)

    def draw(self, win):
        # Dibuja el tablero y las piezas en la ventana
        self.draw_squares(win)  # Dibuja los cuadrados del tablero
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    # Dibuja la pieza si no es un espacio vacío
                    piece.draw(win)

    def remove(self, pieces):
        # Elimina las piezas capturadas del tablero
        for piece in pieces:
            self.board[piece.row][piece.col] = 0  # Marca la posición como vacía
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1  # Reduce el contador de piezas rojas
                else:
                    self.white_left -= 1  # Reduce el contador de piezas blancas

    def winner(self):
        # Determina si hay un ganador basado en el número de piezas restantes
        if self.red_left <= 0:
            return WHITE  # Si no quedan piezas rojas, gana el blanco
        elif self.white_left <= 0:
            return RED  # Si no quedan piezas blancas, gana el rojo
        return None  # Si no hay ganador aún

    def get_valid_moves(self, piece):
        """
        OBTIENE TODOS LOS MOVIMIENTOS VÁLIDOS PARA UNA PIEZA.
        ----------------------------------------------------
        Variables:
            - moves (dict): Diccionario que almacena {posición_final: [piezas_capturadas]}
            - left (int): Columna inicial para exploración diagonal IZQUIERDA (col - 1)
            - right (int): Columna inicial para exploración diagonal DERECHA (col + 1)
            - row (int): Fila actual de la pieza

        Límites de movimiento:
            - up_stop (int):
                * Para REYES: -1 (borde superior del tablero)
                * Para piezas NORMALES: máximo 3 filas hacia arriba (row - 3)
            - down_stop (int):
                * Para REYES: ROWS (borde inferior del tablero)
                * Para piezas NORMALES: máximo 3 filas hacia abajo (row + 3)

        Parámetros clave en _traverse_left/_traverse_right:
            - start: Fila desde donde inicia la exploración (row ± 1)
            - stop: Límite de hasta dónde explorar (up_stop/down_stop)
            - step: Dirección vertical (-1 = arriba, 1 = abajo)
            - color: Color de la pieza (para validar enemigos)
            - is_king: Si la pieza tiene movimientos de rey

        Retorna:
            - moves (dict): Posiciones válidas y piezas a capturar en cada movimiento
        """
        # Obtiene todos los movimientos válidos para una pieza dada
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        # Movimientos hacia arriba (para piezas rojas o reyes)
        if piece.color == RED or piece.king:
            up_stop = -1 if piece.king else max(row - 3, -1)
            moves.update(self._traverse_left(row - 1, up_stop, -1, piece.color, left, is_king=piece.king))
            moves.update(self._traverse_right(row - 1, up_stop, -1, piece.color, right, is_king=piece.king))
        # Movimientos hacia abajo (para piezas blancas o reyes)
        if piece.color == WHITE or piece.king:
            down_stop = ROWS if piece.king else min(row + 3, ROWS)
            moves.update(self._traverse_left(row + 1, down_stop, 1, piece.color, left, is_king=piece.king))
            moves.update(self._traverse_right(row + 1, down_stop, 1, piece.color, right, is_king=piece.king))
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[], is_king=False):
        moves = {}
        last = []
        row = start
        while self._is_within_bounds(row, step, stop):
            if left < 0:
                break
            current = self.board[row][left]
            if current == 0:
                stop_loop = self._process_empty_square(moves, row, left, last, skipped, step, color, is_king, -1)
                if stop_loop:
                    break
                if is_king:
                    row, left = self._update_position(row, step, left, -1)
                    continue
                break
            elif current.color == color:
                break
            else:
                if not self._handle_opponent_piece(moves, row, left, step, color, skipped, is_king, -1, last):
                    break
                break
            row, left = self._update_position(row, step, left, -1)
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[], is_king=False):
        moves = {}
        last = []
        row = start
        while self._is_within_bounds(row, step, stop):
            if right >= COLS:
                break
            current = self.board[row][right]
            if current == 0:
                stop_loop = self._process_empty_square(moves, row, right, last, skipped, step, color, is_king, 1)
                if stop_loop:
                    break
                if is_king:
                    row, right = self._update_position(row, step, right, 1)
                    continue
                break
            elif current.color == color:
                break
            else:
                if not self._handle_opponent_piece(moves, row, right, step, color, skipped, is_king, 1, last):
                    break
                break
            row, right = self._update_position(row, step, right, 1)
        return moves

    # Métodos auxiliares

    def _is_within_bounds(self, r, step, stop):
        return (step > 0 and r < stop) or (step < 0 and r > stop)

    def _get_new_stop(self, r, step, is_king):
        if is_king:
            return 0 if step == -1 else ROWS
        else:
            return max(r - 3, 0) if step == -1 else min(r + 3, ROWS)

    def _add_recursive_moves(self, moves, r, step, color, col, skipped, is_king):
        new_stop = self._get_new_stop(r, step, is_king)
        start_row = r + step
        moves.update(self._traverse_left(start_row, new_stop, step, color, col - 1, skipped, is_king))
        moves.update(self._traverse_right(start_row, new_stop, step, color, col + 1, skipped, is_king))

    def _process_empty_square(self, moves, r, col, last, skipped, step, color, is_king, delta_col):
        if skipped and not last:
            return True  # Break loop
        moves[(r, col)] = last + skipped if skipped else last
        if last:
            self._add_recursive_moves(moves, r + step, step, color, col, last + skipped, is_king)
            return True  # Break loop after recursion
        return False  # Continue loop

    def _update_position(self, r, step, col, delta_col):
        return r + step, col + delta_col

    def _handle_opponent_piece(self, moves, r, col, step, color, skipped, is_king, delta_col, last):
        if last:
            return False  # Break outer loop
        current = self.board[r][col]
        last.append(current)
        next_r = r + step
        next_col = col + delta_col
        if next_col < 0 or next_col >= COLS or next_r < 0 or next_r >= ROWS:
            return False  # Break outer loop
        next_current = self.board[next_r][next_col]
        if next_current == 0:
            moves[(next_r, next_col)] = last + skipped
            self._add_recursive_moves(moves, next_r, step, color, next_col, last + skipped, is_king)
        return True  # Continue processing
