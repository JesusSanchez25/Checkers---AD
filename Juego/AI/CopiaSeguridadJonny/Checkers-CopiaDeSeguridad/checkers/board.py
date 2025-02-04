import pygame
from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE
from .piece import Piece


class Board:
    def __init__(self):
        # Inicializa el tablero y las variables de estado del juego
        self.board = []  # Matriz que representa el tablero
        # Número de piezas rojas y blancas restantes
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0  # Número de reyes rojos y blancos
        self.create_board()  # Llama a la función para crear el tablero inicial

    def draw_squares(self, win):
        # Dibuja los cuadrados del tablero en la ventana proporcionada
        win.fill(BLACK)  # Rellena la ventana con color negro
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                # Dibuja cuadrados rojos en las posiciones adecuadas
                pygame.draw.rect(win, RED, (row*SQUARE_SIZE,
                                 col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def move(self, piece, row, col):
        # Mueve una pieza a una nueva posición en el tablero
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece._move(row, col)  # Actualiza la posición de la pieza

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
            # Marca la posición como vacía
            self.board[piece.row][piece.col] = 0
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
            moves.update(self._traverse_left(row - 1, up_stop, -
                         1, piece.color, left, is_king=piece.king))
            moves.update(self._traverse_right(row - 1, up_stop, -
                         1, piece.color, right, is_king=piece.king))
            print(moves)
        # Movimientos hacia abajo (para piezas blancas o reyes)
        if piece.color == WHITE or piece.king:
            down_stop = ROWS if piece.king else min(row + 3, ROWS)
            moves.update(self._traverse_left(row + 1, down_stop,
                         1, piece.color, left, is_king=piece.king))
            moves.update(self._traverse_right(row + 1, down_stop,
                         1, piece.color, right, is_king=piece.king))
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[], is_king=False):
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
        last = []   # Lista para guardar la última pieza capturada
        r = start   # Fila actual de exploración

        # Bucle principal: recorre la diagonal izquierda
        while (step > 0 and r < stop) or (step < 0 and r > stop):
            # Verificar límite izquierdo del tablero
            if left < 0:
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
                    if is_king:
                        new_stop = 0 if step == -1 else ROWS  # Reyes: hasta bordes
                    else:
                        new_stop = max(r - 3, 0) if step == -1 else min(r + 3, ROWS)  # Piezas normales: 3 filas

                    # Explorar en ambas direcciones después de la captura
                    moves.update(self._traverse_left(
                        r + step, new_stop, step, color, left - 1, skipped=last + skipped, is_king=is_king
                    ))
                    moves.update(self._traverse_right(
                        r + step, new_stop, step, color, left + 1, skipped=last + skipped, is_king=is_king
                    ))

                    if is_king:
                        step = -step
                        new_stop = 0 if step == -1 else ROWS
                        moves.update(self._traverse_left(
                        r + step, new_stop, step, color, left - 1, skipped=last + skipped,is_king=is_king))


                else:
                    # Si es rey, continuar explorando
                    if is_king:
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
                    if is_king:
                        new_stop = 0 if step == -1 else ROWS
                    else:
                        new_stop = max(next_r - 3, 0) if step == -1 else min(next_r + 3, ROWS)

                    # Explorar en ambas direcciones después de la captura
                    moves.update(self._traverse_left(
                        next_r + step, new_stop, step, color, next_left - 1, skipped=last + skipped, is_king=is_king
                    ))
                    moves.update(self._traverse_right(
                        next_r + step, new_stop, step, color, next_left + 1, skipped=last + skipped, is_king=is_king
                    ))
                else:
                    break  # No se puede saltar sobre dos piezas

            # Actualizar posición para siguiente iteración
            r += step
            left -= 1

        return moves


    def _traverse_right(self, start, stop, step, color, right, skipped=[], is_king=False):
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
        last = []   # Lista para guardar la última pieza capturada
        r = start   # Fila actual de exploración

        # Bucle principal: recorre la diagonal derecha
        while (step > 0 and r < stop) or (step < 0 and r > stop):
            # Verificar límite derecho del tablero
            if right >= COLS:
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
                    if is_king:
                        new_stop = 0 if step == -1 else ROWS  # Reyes: hasta bordes
                    else:
                        new_stop = max(r - 3, 0) if step == -1 else min(r + 3, ROWS)  # Piezas normales: 3 filas

                    # Explorar en ambas direcciones después de la captura
                            # Movimientos hacia arriba (para piezas rojas o reyes)


                    moves.update(self._traverse_right(
                        r + step, new_stop, step, color, right + 1, skipped=last + skipped, is_king=is_king
                    ))

                    if is_king:
                        step = -step
                        new_stop = 0 if step == -1 else ROWS
                        moves.update(self._traverse_left(
                        r + step, new_stop, step, color, right - 1, skipped=last + skipped, is_king=is_king
                    ))
                        moves.update(self._traverse_right(
                            r + step, new_stop, step, color, right + 1, skipped=last + skipped, is_king=is_king
                        ))

                    break  # Detener exploración en esta dirección
                else:
                    # Si es rey, continuar explorando
                    if is_king:
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
                    if is_king:
                        new_stop = 0 if step == -1 else ROWS
                    else:
                        new_stop = max(next_r - 3, 0) if step == -1 else min(next_r + 3, ROWS)

                    # Explorar en ambas direcciones después de la captura
                    moves.update(self._traverse_left(
                        next_r + step, new_stop, step, color, next_right - 1, skipped=last + skipped, is_king=is_king
                    ))
                    moves.update(self._traverse_right(
                        next_r + step, new_stop, step, color, next_right + 1, skipped=last + skipped, is_king=is_king
                    ))
                else:
                    break  # No se puede saltar sobre dos piezas

            # Actualizar posición para siguiente iteración
            r += step
            right += 1

        return moves
