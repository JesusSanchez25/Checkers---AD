import pygame
from pygame.time import set_timer
import time


from juego.constants import ROWS, COLS, PINK, BLACK, WHITE, SQUARE_SIZE, BOARD_BORDER, COLOR_STROKE, HEIGHT, \
    numeros_neon, letras_neon, BLUE
from juego.piece import Piece

from juego.constants import IA_MATCH


def draw_gradient(surface, rect, start_color, end_color):
    start_r, start_g, start_b = start_color
    end_r, end_g, end_b = end_color

    for x in range(rect.width):
        r = start_r + (end_r - start_r) * x / rect.width
        g = start_g + (end_g - start_g) * x / rect.width
        b = start_b + (end_b - start_b) * x / rect.width
        pygame.draw.line(surface, (int(r), int(g), int(b)), (rect.x + x, rect.y),
                         (rect.x + x, rect.y + rect.height))


class Board:
    def __init__(self):
        self.board = []
        self.blue_pieces = self.pink_pieces = 12
        self.blue_queens = self.pink_queens = 0
        self.create_board()

    def print_board(self):
        """
        Imprime el tablero en consola con colores y símbolos para las piezas.
        - 🔴: Pieza roja normal
        - ⚪: Pieza blanca normal
        - ♔: Rey (se añade a los símbolos anteriores)
        """
        for row in range(ROWS):
            # Crear línea horizontal entre filas
            print("-" * (COLS * 5 + 1))

            # Construir línea de fichas
            line = "|"
            for col in range(COLS):
                piece = self.board[row][col]
                if piece == 0:
                    line += "    |"
                else:
                    color_code = "\033[91m" if piece.color == PINK else "\033[97m"
                    symbol = "🩷" if piece.color == PINK else "🔵"
                    if piece.queen:
                        symbol += "♔"
                    line += f"{color_code} {symbol} \033[0m|"
            print(line)

        print("-" * (COLS * 5 + 1))
        print("\n\n\n")

    # def draw_squares(self, win):  # win --> window
    #     for row in range(ROWS):
    #         for col in range(ROWS):
    #             # Determinar el color del cuadrado
    #             color = BLACK if (row + col) % 2 != 0 or (row == 9 or col == 0) else WHITE
    #             square_rect = pygame.Rect(row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
    #             # Dibujar el cuadrado
    #             pygame.draw.rect(win, color, square_rect)
    #             # Dibujar el contorno (stroke) para destacar
    #             pygame.draw.rect(win, COLOR_STROKE, square_rect, width=1)  # Grosor del borde: 1 píxel



    def draw_squares(self, win):
        # font = pygame.font.SysFont("Arial", 24,True)  # Fuente para coordenadas
        win.fill(BLACK)  # Rellena la ventana con color negro
        pygame.font.init()
        font = pygame.font.Font(None, 41)

        for row in range(ROWS):
            for col in range(ROWS):
                # Determinar el color del cuadrado
                color = BLACK if (row + col) % 2 != 0 else WHITE
                square_rect = pygame.Rect(col * SQUARE_SIZE + BOARD_BORDER, row * SQUARE_SIZE + BOARD_BORDER,
                                          SQUARE_SIZE, SQUARE_SIZE)
                square_rect2 = pygame.Rect(col * SQUARE_SIZE + BOARD_BORDER, row * SQUARE_SIZE + BOARD_BORDER,
                                          SQUARE_SIZE, SQUARE_SIZE - 1)

                if color == BLACK: # dibujar cuadrado negro
                    pygame.draw.rect(win, color, square_rect)
                else: # dibujar cuadrado con radieante
                    draw_gradient(win, square_rect2, (128, 0, 128), (255, 165, 0))

                #dibujar reborde cuadrado
                pygame.draw.rect(win, COLOR_STROKE, square_rect, width=1)




                # placeholder marcador
                time_text = font.render(f"{"00:00"}", True, (255, 255, 255))
                blue_time = font.render(f"{"00:00"}", True, (23, 151, 253))

                if row == 0:
                    if IA_MATCH:
                        win.blit(time_text, (HEIGHT // 2 + BOARD_BORDER // 4, SQUARE_SIZE // 6))
                    # else:
                    #     # win.blit(pink_time, (HEIGHT // 4 + BOARD_BORDER // 4, SQUARE_SIZE // 6))
                    #     win.blit(blue_time, (HEIGHT // 4 * 3 + BOARD_BORDER // 4, SQUARE_SIZE // 6))




                if col == 0:  # dibujar nuemros cuando sea la primera columna
                    for i, numero in enumerate(numeros_neon): # recorre el array con los numeros
                        # va pintando los numeros en orden, en la posicion i * el tamaño del cuadrado
                        win.blit(numero, (5, i * SQUARE_SIZE + SQUARE_SIZE // 4 + BOARD_BORDER))

                if row == ROWS - 1:  # dibujar letras cuando sea la ultima fila 8 - 1 = 7 (ultima fila)
                    for i, letra in enumerate(letras_neon): #dibuajr las letras en la posicion correspondiente
                        win.blit(letra, (i * SQUARE_SIZE + BOARD_BORDER + SQUARE_SIZE // 4, 5 + HEIGHT + BOARD_BORDER))



    def move(self, piece, row, col):
        # Mueve una pieza a una nueva posición en el tablero
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)  # Actualiza la posición de la pieza

        # Si la pieza llega a la última fila, se convierte en rey
        if row == ROWS - 1 or row == 0:
            piece.crowning()
            if piece.color == BLUE:
                self.blue_queens += 1
            else:
                self.pink_queens += 1

    def get_piece(self, row, col):
        # Devuelve la pieza en la posición (row, col) del tablero
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 2:
                        self.board[row].append(Piece(row, col, BLUE))
                    elif row > 5:
                        self.board[row].append(Piece(row, col, PINK))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        # Elimina las piezas capturadas del tablero
        for piece in pieces:
            self.board[piece.row][piece.col] = 0  # Marca la posición como vacía
            if piece != 0:
                if piece.color == PINK:
                    self.pink_pieces -= 1  # Reduce el contador de piezas rojas
                else:
                    self.blue_pieces -= 1  # Reduce el contador de piezas blancas

    def winner(self):
        # Determina si hay un ganador basado en el número de piezas restantes
        if self.pink_pieces <= 0:
            return WHITE  # Si no quedan piezas rojas, gana el blanco
        elif self.blue_pieces <= 0:
            return PINK  # Si no quedan piezas blancas, gana el rojo
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
        if piece.color == PINK or piece.queen:
            up_stop = -1 if piece.queen else max(row - 3, -1)
            moves.update(self._traverse_left(row - 1, up_stop, -1, piece.color, left, is_queen=piece.queen))
            moves.update(self._traverse_right(row - 1, up_stop, -1, piece.color, right, is_queen=piece.queen))
        # Movimientos hacia abajo (para piezas blancas o reyes)
        if piece.color == BLUE or piece.queen:
            down_stop = ROWS if piece.queen else min(row + 3, ROWS)
            moves.update(self._traverse_left(row + 1, down_stop, 1, piece.color, left, is_queen=piece.queen))
            moves.update(self._traverse_right(row + 1, down_stop, 1, piece.color, right, is_queen=piece.queen))
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[], is_queen=False):
        """
        Recorre el tablero hacia la izquierda para encontrar movimientos válidos.

        Parámetros:
            start (int): Fila inicial de exploración.
            stop (int): Límite vertical máximo/mínimo (depende de step).
            step (int): Dirección vertical (-1 = arriba, 1 = abajo).
            color (str): Color de la pieza actual.
            left (int): Columna inicial para exploración izquierda.
            skipped (list): Piezas capturadas en saltos previos.
            is_king (bool): Indica si es una pieza rey.

        Retorna:
            dict: Movimientos válidos con estructura {posicion: piezas_capturadas}.
        """
        moves = {}  # Diccionario para almacenar movimientos válidos
        last = []  # Lista para guardar la última pieza capturada
        r = start  # Fila actual de exploración

        # Bucle principal: recorre la diagonal izquierda
        while (step > 0 and r < stop) or (step < 0 and r > stop):
            # Verificar límite izquierdo del tablero
            if left < 0 or (self.get_piece(r, left)) in skipped:
                break

            # Obtener la pieza en la posición actual
            current = self.board[r][left]

            # Caso 1: Casilla vacía
            if current == 0:
                # Si hay capturas previas pero ninguna actual, detener
                if skipped and not last:
                    break

                # Registrar movimiento
                if skipped:
                    moves[(r, left)] = last + skipped  # Captura múltiple
                else:
                    moves[(r, left)] = last  # Movimiento simple

                # Si hay una captura reciente, buscar saltos adicionales
                if last:
                    # Calcular nuevo límite vertical
                    if is_queen:
                        new_stop = 0 if step == -1 else ROWS  # Reyes: hasta bordes
                    else:
                        # Piezas normales: 3 filas
                        new_stop = max(r - 3, 0) if step == - \
                            1 else min(r + 3, ROWS)

                    # Explorar en ambas direcciones después de la captura
                    moves.update(self._traverse_left(
                        r + step, new_stop, step, color, left - 1, skipped=last + skipped, is_queen=is_queen
                    ))
                    moves.update(self._traverse_right(
                        r + step, new_stop, step, color, left + 1, skipped=last + skipped, is_queen=is_queen
                    ))

                    if is_queen:
                        step = -step
                        new_stop = 0 if step == -1 else ROWS
                        moves.update(self._traverse_left(
                            r + step, new_stop, step, color, left - 1, skipped=last + skipped, is_queen=is_queen))

                else:
                    # Si es rey, continuar explorando
                    if is_queen:
                        r += step
                        left -= 1
                        continue
                    else:
                        break  # Piezas normales: solo un movimiento

            # Caso 2: Pieza aliada (mismo color)
            elif current.color == color:
                break  # Bloquear movimiento

            # Caso 3: Pieza enemiga
            else:
                # Si ya hay una captura en este salto, detener
                if last:
                    break

                # Guardar la pieza enemiga para captura
                last = [current]

                # Calcular posición post-salto
                next_r = r + step
                next_left = left - 1

                # Verificar límites del tablero
                if next_left < 0 or next_r < 0 or next_r >= ROWS:
                    break

                # Verificar si la posición post-salto está vacía
                next_current = self.board[next_r][next_left]
                if next_current == 0:
                    # Registrar captura
                    moves[(next_r, next_left)] = last + skipped

                    # Calcular nuevo límite vertical
                    if is_queen:
                        new_stop = 0 if step == -1 else ROWS
                    else:
                        new_stop = max(next_r - 3, 0) if step == - \
                            1 else min(next_r + 3, ROWS)

                    # Explorar en ambas direcciones después de la captura
                    moves.update(self._traverse_left(
                        next_r + step, new_stop, step, color, next_left - 1, skipped=last + skipped, is_queen=is_queen
                    ))
                    moves.update(self._traverse_right(
                        next_r + step, new_stop, step, color, next_left + 1, skipped=last + skipped, is_queen=is_queen
                    ))
                else:
                    break  # No se puede saltar sobre dos piezas

            # Actualizar posición para siguiente iteración
            r += step
            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[], is_queen=False):
        """
        Recorre el tablero hacia la derecha para encontrar movimientos válidos.

        Parámetros:
            start (int): Fila inicial de exploración.
            stop (int): Límite vertical máximo/mínimo (depende de step).
            step (int): Dirección vertical (-1 = arriba, 1 = abajo).
            color (str): Color de la pieza actual.
            right (int): Columna inicial para exploración derecha.
            skipped (list): Piezas capturadas en saltos previos.
            is_king (bool): Indica si es una pieza rey.

        Retorna:
            dict: Movimientos válidos con estructura {posicion: piezas_capturadas}.
        """
        moves = {}  # Diccionario para almacenar movimientos válidos
        last = []  # Lista para guardar la última pieza capturada
        r = start  # Fila actual de exploración

        # Bucle principal: recorre la diagonal derecha
        while ((step > 0 and r < stop) or (step < 0 and r > stop) and last == []):
            # Verificar límite derecho del tablero
            if right >= COLS or (self.get_piece(r, right)) in skipped:
                break

            # Obtener la pieza en la posición actual
            current = self.board[r][right]

            # Caso 1: Casilla vacía
            if current == 0:
                # Si hay capturas previas pero ninguna actual, detener
                if skipped and not last:
                    break

                # Registrar movimiento
                if skipped:
                    moves[(r, right)] = last + skipped  # Captura múltiple
                else:
                    moves[(r, right)] = last  # Movimiento simple

                # Si hay una captura reciente, buscar saltos adicionales
                if last:
                    # Calcular nuevo límite vertical
                    if is_queen:
                        new_stop = 0 if step == -1 else ROWS  # Reyes: hasta bordes
                    else:
                        # Piezas normales: 3 filas
                        new_stop = max(r - 3, 0) if step == - \
                            1 else min(r + 3, ROWS)

                    # Explorar en ambas direcciones después de la captura
                    # Movimientos hacia arriba (para piezas rojas o reyes)

                    moves.update(self._traverse_right(
                        r + step, new_stop, step, color, right + 1, skipped=last + skipped, is_queen=is_queen
                    ))
                    moves.update(self._traverse_left(
                        r + step, new_stop, step, color, right - 1, skipped=last + skipped, is_queen=is_queen
                    ))

                    if is_queen:
                        step = -step
                        new_stop = 0 if step == -1 else ROWS

                        moves.update(self._traverse_right(
                            r + step, new_stop, step, color, right + 1, skipped=last + skipped, is_queen=is_queen
                        ))

                    break  # Detener exploración en esta dirección
                else:
                    # Si es rey, continuar explorando
                    if is_queen:
                        r += step
                        right += 1
                        continue
                    else:
                        break  # Piezas normales: solo un movimiento

            # Caso 2: Pieza aliada (mismo color)
            elif current.color == color:
                break  # Bloquear movimiento

            # Caso 3: Pieza enemiga
            else:
                # Si ya hay una captura en este salto, detener
                if last:
                    break

                # Guardar la pieza enemiga para captura
                last = [current]

                # Calcular posición post-salto
                next_r = r + step
                next_right = right + 1

                # Verificar límites del tablero
                if next_right >= COLS or next_r < 0 or next_r >= ROWS:
                    break

                # Verificar si la posición post-salto está vacía
                next_current = self.board[next_r][next_right]
                if next_current == 0:
                    # Registrar captura
                    moves[(next_r, next_right)] = last + skipped

                    # Calcular nuevo límite vertical
                    if is_queen:
                        new_stop = 0 if step == -1 else ROWS
                    else:
                        new_stop = max(next_r - 3, 0) if step == - \
                            1 else min(next_r + 3, ROWS)

                    # Explorar en ambas direcciones después de la captura
                    moves.update(self._traverse_left(
                        next_r + step, new_stop, step, color, next_right - 1, skipped=last + skipped, is_queen=is_queen
                    ))
                    moves.update(self._traverse_right(
                        next_r + step, new_stop, step, color, next_right + 1, skipped=last + skipped, is_queen=is_queen
                    ))
                else:
                    break  # No se puede saltar sobre dos piezas

            # Actualizar posición para siguiente iteración
            r += step
            right += 1

        return moves

    # # Métodos auxiliares
    #
    # def _is_within_bounds(self, r, step, stop):
    #     return (step > 0 and r < stop) or (step < 0 and r > stop)
    #
    # def _get_new_stop(self, r, step, is_queen):
    #     if is_queen:
    #         return 0 if step == -1 else ROWS
    #     else:
    #         return max(r - 3, 0) if step == -1 else min(r + 3, ROWS)
    #
    # def _add_recursive_moves(self, moves, r, step, color, col, skipped, is_queen):
    #     new_stop = self._get_new_stop(r, step, is_queen)
    #     start_row = r + step
    #     moves.update(self._traverse_left(start_row, new_stop, step, color, col - 1, skipped, is_queen))
    #     moves.update(self._traverse_right(start_row, new_stop, step, color, col + 1, skipped, is_queen))
    #
    # def _process_empty_square(self, moves, r, col, last, skipped, step, color, is_queen, delta_col):
    #     """
    #     PROCESA UNA CASILLA VACÍA Y ACTUALIZA MOVIMIENTOS POSIBLES.
    #     ----------------------------------------------------------
    #     Variables:
    #         - moves (dict): Diccionario que almacena {posición_final: [piezas_capturadas]}
    #         - r (int): Fila actual donde se encuentra la casilla vacía
    #         - col (int): Columna actual donde se encuentra la casilla vacía
    #         - last (list): Última pieza capturada en el recorrido
    #         - skipped (list): Piezas previamente capturadas en el recorrido
    #         - step (int): Dirección vertical (-1 = arriba, 1 = abajo)
    #         - color: Color de la pieza que está explorando los movimientos
    #         - is_king (bool): Indica si la pieza en cuestión es un rey
    #         - delta_col (int): Dirección horizontal (-1 = izquierda, 1 = derecha)
    #
    #     Lógica de control:
    #         - Si hay piezas capturadas en `skipped` pero `last` está vacío, detiene la exploración.
    #         - Si `last` contiene una pieza capturada, añade movimientos recursivos para continuar la captura si es posible.
    #         - Si no hay piezas en skipped o last, continua la exploración pero se detiene en la función traverse si detecta que la pieza no es reina.
    #         - Si la pieza es rey continua y hace otra vuelta del bucle para explorar el tablero.
    #
    #     Retorna:
    #         - (bool): Indica si se debe detener la exploración o continuar
    #     """
    #     if skipped and not last:
    #         return True  # Break loop
    #     moves[(r, col)] = last + skipped if skipped else last
    #     if last:
    #         self._add_recursive_moves(moves, r + step, step, color, col, last + skipped, is_queen)
    #         return True  # Break loop after recursion
    #     return False  # Continue loop
    #
    # def _update_position(self, r, step, col, delta_col):
    #     return r + step, col + delta_col
    #
    # def _handle_opponent_piece(self, moves, row, col, step, color, skipped, is_queen, delta_col, last):
    #     """
    #     MANEJA UNA PIEZA OPONENTE DURANTE LA EXPLORACIÓN.
    #     -------------------------------------------------
    #     Variables:
    #         - moves (dict): Diccionario que almacena {posición_final: [piezas_capturadas]}
    #         - r (int): Fila actual de exploración
    #         - col (int): Columna actual de exploración
    #         - step (int): Dirección vertical de la exploración (-1 = arriba, 1 = abajo)
    #         - color (str): Color de la pieza en movimiento (para detectar enemigos)
    #         - skipped (list): Lista de piezas previamente capturadas en la secuencia
    #         - is_king (bool): Indica si la pieza en movimiento es un rey
    #         - delta_col (int): Dirección horizontal de la exploración (-1 = izquierda, 1 = derecha)
    #         - last (list): Lista temporal que almacena la última pieza oponente detectada
    #
    #     Proceso de validación:
    #         1. Se obtiene la pieza actual en la posición `(r, col)`.
    #         2. Se añade a `last` como una posible pieza a capturar.
    #         3. Se calcula la posición siguiente (`next_r`, `next_col`), donde la pieza en movimiento aterrizaría.
    #         4. Se verifica si la siguiente casilla está dentro de los límites del tablero.
    #         5. Si la casilla siguiente está vacía, se almacena la jugada con las piezas capturadas.
    #         6. Si no hay espacio después de la casilla termina la ejecución y devuelve true.
    #
    #     Retorna:
    #         - True si se debe detener explorando la captura.
    #         - False si se debe continuar la exploración en esta dirección.
    #     """
    #     current = self.board[row][col]
    #     last.append(current)
    #     next_r = row + step
    #     next_col = col + delta_col
    #     if next_col < 0 or next_col >= COLS or next_r < 0 or next_r >= ROWS:
    #         return False  # Break outer loop
    #     next_current = self.board[next_r][next_col]
    #     # Si esta casilla es vacía, se almacena la jugada con las piezas capturadas
    #     # e intenta buscar otra posible ficha para comer
    #     if next_current == 0:
    #         moves[(next_r, next_col)] = last + skipped
    #         self._add_recursive_moves(moves, next_r, step, color, next_col, last + skipped, is_queen)
    #     return True  # Stop processing
