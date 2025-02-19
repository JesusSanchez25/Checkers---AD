from juego.database import jsonletras

def formatear_row_to_db(row):
    letras = ["a", "b", "c", "d", "e", "f", "g", "h"]
    return (letras[row]).upper()

def formatear_col_to_db(col):
    """
    Convierte una columna de 0 a 7 a un numero de 1 a 8.
    """
    return 8 - col

def formatear_col_from_db(col):
    letras = ["a", "b", "c", "d", "e", "f", "g", "h"]
    return letras.index(col.lower())

def formatear_row_from_db(row):
    return 8 - int(row)

def cargar_movimientos():
    """
    Convierte el JSON de la base de datos en una lista de secuencias de movimientos.
    """
    json_data = jsonletras
    movimientos = []

    for entry in json_data["movements"]:
        secuencia = entry["secuencia"]
        movimientos_procesados = []

        # Separar cada jugada dentro de la secuencia
        jugadas = secuencia.split("; ")
        for jugada in jugadas:
            partida, llegada = jugada.split("-")
            inicio = tuple(map(str, partida.split(",")))
            destino = tuple(map(str, llegada.split(",")))
            movimientos_procesados.append(inicio)
            movimientos_procesados.append(destino)

        movimientos.append(movimientos_procesados)

    return movimientos

def respuesta_movimientos(col_inicial, row_inicial, col_final, row_final, game,  turno=0):
    row_inicial, row_final = formatear_row_to_db(row_inicial), formatear_row_to_db(row_final)
    col_inicial, col_final = formatear_col_to_db(col_inicial), formatear_col_to_db(col_final)
    if (turno >= 2):
        return False

    for entry in jsonletras["movements"]:
        secuencia = entry["secuencia"]
        jugadas = secuencia.split("; ")
        primer_movimiento = jugadas[turno].split("-")[0]
        primer_movimiento_ejecutad = f"{row_inicial}{col_inicial}{row_final}{col_final}"
        if (primer_movimiento_ejecutad == primer_movimiento):
            print("MOVIMIENTO RESPUESTA", jugadas[0].split("-")[1])
            movimientoRespuesta = ""
            col = -1
            for i, posicion in enumerate(jugadas[0].split("-")[1]):
                if (i % 2 == 0):
                    col = formatear_col_from_db(posicion)
                else:
                    row = formatear_row_from_db(posicion)
                    game.select(row, col)
            print(movimientoRespuesta)
            return True
        # for jugada in jugadas:
        #     partida, llegada = jugada.split("-")
        #     inicio = tuple(map(int, partida.split(",")))
        #     destino = tuple(map(int, llegada.split(",")))
        #     if inicio == (row_inicial, col_inicial) and destino == (row_final, col_final):
        #         return entry["respuesta"]
    # """
    # Convierte el JSON de la base de datos en una lista de respuestas de movimientos.
    # """
    # json_data = json
    # respuestas = []

    # for entry in json_data["movements"]:
    #     respuestas.append(entry["respuesta"])

    # for respuesta in respuestas:
    #     print(respuesta, end="\n\n")
    # return respuestas
