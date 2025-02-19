import copy
from juego.board import Board
from juego.constants import PROFUNDIDAD, BLUE, PINK, CAPTURA_OBLIGATORIA
from juego.nodos import Nodo, min_max, arbol_a_json
import pyperclip
import torch

def comprobarMovimientosIa(board: Board, color, profundidad=PROFUNDIDAD, nodoActual=Nodo("Raiz"), game = None):
    hay_capturas = False
    if (CAPTURA_OBLIGATORIA):
        hay_capturas = any(
            any(capturas for _, capturas in board.get_valid_moves(pieza).items())
            for fila in board.board for pieza in fila
            if str(pieza) == str(color)
        )

    # --- 1. Recorrer el tablero ---
    # Itera sobre cada fila y columna del tablero para encontrar piezas del color de la IA.
    for i, fila in enumerate(board.board):
        for j, pieza in enumerate(fila):
            if str(pieza) == str(color):
                # Obtiene los movimientos válidos para la pieza actual.
                moves = board.get_valid_moves(pieza)

                if (hay_capturas and CAPTURA_OBLIGATORIA):
                    moves = {m: c for m, c in moves.items() if c}
                    if not moves: continue

                # Si hay movimientos válidos, procesa cada uno.
                if len(moves) > 0:
                    # --- 2. Procesar cada movimiento válido ---
                    for movimiento, capturas in moves.items():
                        # Desempaqueta la nueva posición (fila y columna).
                        nuevaRow, nuevaCol = movimiento

                        # Crea un nodo hijo en el árbol con la información del movimiento.
                        nodoHijo = Nodo(
                            f"{pieza.row},{pieza.col}-{nuevaRow},{nuevaCol}-{capturas}")

                        # --- 3. Simular el movimiento ---
                        # Guarda la posición original de la pieza para restaurarla después.
                        fila_original, col_original = pieza.row, pieza.col

                        # Clona el tablero para simular el movimiento sin afectar el estado real.
                        board_copia: Board =board
                        pieza_copia = board_copia.get_piece(
                            fila_original, col_original)

                        crowned_original = pieza.queen
                        # Mueve la pieza en el tablero clonado a la nueva posición.
                        board_copia.move(pieza_copia, nuevaRow, nuevaCol)
                        board_copia.remove(capturas)

                        # board_copia.print_board()
                        # if capturas != []:
                        #     board_copia.print_board()

                        # --- 4. Evaluar el tablero si se alcanza la profundidad 0 ---
                        # Si se alcanza la profundidad 0, evalúa el tablero resultante.
                        if  profundidad == 0 or es_estado_terminal(board_copia, PINK):
                            # Evalúa el tablero.
                            nodoHijo.puntuacion = evaluate_board(
                                board_copia, player_color=BLUE)
                        # --- 5. Explorar movimientos futuros (recursión) ---
                        # Si no se ha alcanzado la profundidad máxima, sigue explorando.
                        elif profundidad > 0:
                            # Cambia al color del oponente para simular su turno.
                            nuevaProfundidad = profundidad - 1
                            nuevoColor = PINK if str(color) == str(BLUE) else BLUE
                            # board_copia.print_board()
                            comprobarMovimientosIa(board, nuevoColor, nuevaProfundidad, nodoHijo)
                        nodoActual.agregar_hijo(nodoHijo)



                        # --- 6. Restaurar la posición original de la pieza ---
                        # Restaura la posición original de la pieza en el tablero real.
                        # pieza.row, pieza.col = fila_original, col_original
                        board.move(pieza, fila_original, col_original)
                        pieza.queen = crowned_original
                        board.add(capturas)


    # --- 7. Imprimir el árbol (solo para el nodo raíz) ---
    # Si es el nodo raíz, imprime el árbol (para depuración).
    if nodoActual.valor == "Raiz":
        siguienteMove = min_max(nodoActual, profundidad + 1)

        if (siguienteMove.valor == "Raiz"):
            return
        move_origen, move_destino, capturas = siguienteMove.valor.split("-")

        row_origen = int(move_origen.split(",")[0])
        col_origen = int(move_origen.split(",")[1])

        row_destino = int(move_destino.split(",")[0])
        col_destino = int(move_destino.split(",")[1])

        game.select(row_origen, col_origen)
        game.select(row_destino, col_destino)
        arbol_json = str(arbol_a_json(nodoActual))
        arbol_json = arbol_json.replace("'", '"')
        pyperclip.copy(arbol_json)



def eval_capture_options(piece, board):
    """
    Evalúa si la pieza tiene opciones de captura.
    Retorna 5 si existe al menos una opción de captura, o 0 en caso contrario.
    """
    moves = board.get_valid_moves(piece)
    for move, captured in moves.items():
        if captured:  # Si hay alguna captura posible
            return 5
    return 0

def eval_piece_risk(piece, board, row, col):
    """
    Evalúa si la pieza está en riesgo de ser capturada.
    Recorre las direcciones diagonales y, si detecta un enemigo con la posibilidad
    de saltar (con casilla de aterrizaje vacía), retorna -4; si no, 0.
    """
    rows = len(board.board)
    cols = len(board.board[0])
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dx, dy in directions:
        new_row = row + dx
        new_col = col + dy
        landing_row = row + 2 * dx
        landing_col = col + 2 * dy
        if 0 <= new_row < rows and 0 <= new_col < cols:
            neighbor = board.get_piece(new_row, new_col)
            if neighbor != 0 and neighbor.color != piece.color:
                if 0 <= landing_row < rows and 0 <= landing_col < cols:
                    landing_piece = board.get_piece(landing_row, landing_col)
                    if landing_piece == 0:
                        return -4
    return 0

def eval_chain_defense(piece, board, row, col):
    """
    Evalúa si la pieza está protegida por otra pieza amiga en una posición adyacente.
    Retorna 2 si está protegida, o 0 si no lo está.
    """
    rows = len(board.board)
    cols = len(board.board[0])
    protected = False
    if piece.queen:
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    else:
        # Para piezas normales, se asume que la protección proviene "detrás" según su color
        if piece.color == BLUE:
            directions = [(-1, -1), (-1, 1)]
        else:
            directions = [(1, -1), (1, 1)]
    for dx, dy in directions:
        new_row = row + dx
        new_col = col + dy
        if 0 <= new_row < rows and 0 <= new_col < cols:
            neighbor = board.get_piece(new_row, new_col)
            if neighbor != 0 and neighbor.color == piece.color:
                protected = True
                break
    return 2 if protected else 0

def eval_center_control(piece, board, row, col):
    """
    Evalúa el control del centro.
    Se considera centro la franja central del tablero; retorna 3 si la pieza se encuentra allí, o 0 si no.
    """
    rows = len(board.board)
    cols = len(board.board[0])
    center_row_start = rows // 4
    center_row_end = center_row_start + rows // 2
    center_col_start = cols // 4
    center_col_end = center_col_start + cols // 2
    if center_row_start <= row < center_row_end and center_col_start <= col < center_col_end:
        return 3
    return 0

def eval_edge_pieces(piece, board, row, col):
    """
    Evalúa si la pieza está en una casilla de borde (columna 0 o última columna).
    Retorna 2 si está en el borde, o 0 si no.
    """
    cols = len(board.board[0])
    if col == 0 or col == cols - 1:
        return 2
    return 0

def eval_advanced_pieces(piece, board, row, col):
    """
    Evalúa cuánto ha avanzado la pieza.
    Para piezas no coronadas, a mayor avance (dependiendo del color) se asigna un valor mayor.
    Retorna un bonus multiplicado por 3; las damas no se evalúan en este criterio.
    """
    rows = len(board.board)
    if piece.queen:
        return 0
    if piece.color == BLUE:
        # Para WHITE, se asume que avanzar significa estar en filas de mayor índice
        return 4 * row
    else:
        # Para RED, se asume que avanzar significa estar en filas de menor índice
        return 4 * (rows - 1 - row)

def eval_piece_count(piece, board, row, col):
    """
    Evalúa cuánto ha avanzado la pieza.
    Para piezas no coronadas, a mayor avance (dependiendo del color) se asigna un valor mayor.
    Retorna un bonus multiplicado por 3; las damas no se evalúan en este criterio.
    """
    rows = len(board.board)
    if piece.queen:
        return 20 + (4 * 8)
    return 10

def evaluate_board(board, player_color):
    """
    Itera una sola vez por todo el tablero y, para cada pieza encontrada,
    aplica las funciones de valoración auxiliares:
      - eval_capture_options
      - eval_piece_risk
      - eval_chain_defense
      - eval_center_control
      - eval_edge_pieces
      - eval_advanced_pieces

    Si la pieza pertenece al jugador (player_color), su valoración se suma;
    si es del oponente, se resta.
    Retorna el score total del tablero.
    """
    total_score = 0
    rows = len(board.board)
    cols = len(board.board[0])
    for row in range(rows):
        for col in range(cols):
            piece = board.get_piece(row, col)
            if piece == 0:
                continue

            # Suma de la valoración de esta pieza según cada criterio
            piece_score = 0
            # piece_score += eval_capture_options(piece, board)
            piece_score += eval_piece_risk(piece, board, row, col)
            piece_score += eval_chain_defense(piece, board, row, col)
            piece_score += eval_center_control(piece, board, row, col)
            # piece_score += eval_edge_pieces(piece, board, row, col)
            piece_score += eval_advanced_pieces(piece, board, row, col)
            piece_score += eval_piece_count(piece, board, row, col)

            # Si la pieza es del jugador, se suma; si es del oponente, se resta.
            if piece.color == player_color:
                total_score += piece_score
            else:
                total_score -= piece_score
    # print(total_score)
    return total_score


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

def es_estado_terminal(board: Board, color_jugador) -> bool:
    """Verifica si el jugador no tiene movimientos posibles (juego terminado)"""
    for fila in board.board:
        for pieza in fila:
            if str(pieza) == str(color_jugador) and board.get_valid_moves(pieza):
                return False
    return True
