from juego.database import jsonletras

def formatear_row(row):
    letras = ["a", "b", "c", "d", "e", "f", "g", "h"]
    return (letras[row - 1]).upper()

def formatear_col(col):
    return 7 - col

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

    for movimiento in movimientos:
        print(movimiento, end="\n\n")
    return movimientos

def respuesta_movimientos(row_inicial, col_inicial, row_final, col_final):
    print(row_inicial, col_inicial, row_final, col_final)
    row_inicial, row_final = formatear_row(row_inicial), formatear_row(row_final)
    col_inicial, col_final = formatear_col(col_inicial), formatear_col(col_final)

    for entry in jsonletras["movements"]:
        secuencia = entry["secuencia"]
        jugadas = secuencia.split("; ")
        primer_movimiento = jugadas[0].split("-")[0]
        primer_movimiento_ejecutad = f"{row_inicial}{col_inicial}{row_final}{col_final}"
        if (primer_movimiento_ejecutad == primer_movimiento):
            print("MOVIMIENTO BD", primer_movimiento)
            print("MOVIMIENTO EJECUTADO", primer_movimiento_ejecutad)
            print("hola")
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
