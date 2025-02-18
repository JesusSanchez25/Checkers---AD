import random  # Importa la librería random para generar valores aleatorios.

# Define la profundidad máxima del árbol.
PROFUNDIDAD = 7

# Clase Nodo que representa un nodo en el árbol.


class Nodo:
	def __init__(self, valor):
		# Inicializa el nodo con un valor y una lista vacía de hijos.
		self.valor = valor
		self.puntuacion = 0
		self.hijos = []

	def agregar_hijo(self, hijo):
		# Agrega un nodo hijo a la lista de hijos del nodo actual.
		self.hijos.append(hijo)

# Función para imprimir el árbol de manera jerárquica.
def arbol_a_json(nodo):
    """
    Convierte el árbol a un diccionario en formato JSON.
    """
    return {
        "valor": nodo.valor,
        "puntuacion": nodo.puntuacion,
        "hijos": [arbol_a_json(hijo) for hijo in nodo.hijos]
    }

def imprimir_arbol(nodo, nivel=0):
	# Imprime el valor del nodo con una indentación basada en el nivel.
	print("  " * nivel + f"=={nodo.valor} + ({nodo.puntuacion}) ==")
	for hijo in nodo.hijos:  # Recorre los hijos del nodo actual.
		# Llama recursivamente para imprimir los hijos.
		imprimir_arbol(hijo, nivel + 1)

# Función recursiva para crear el árbol.
def crear_arbol(profundidad: int = 0, nodoActual: Nodo = None):
	# Caso base: si la profundidad es 0, se detiene la recursión.
	if (profundidad == 0):
		return
	for i in range(4):  # Cada nodo tendrá 4 hijos.
		hijo = Nodo(f"Nodo {i}")  # Crea un hijo con un nombre genérico.
		if (profundidad == 1):
			# Si es el último nivel, asigna un valor aleatorio entre -9 y 9 al hijo.
			hijo = Nodo(random.randint(-9, 9))
			print(hijo.valor, end=",")  # Imprime el valor del nodo hoja.
			nodoActual.agregar_hijo(hijo)  # Agrega el nodo hoja como hijo.
		else:
			nodoActual.agregar_hijo(hijo=hijo)  # Agrega el hijo intermedio.
		# Llama recursivamente para crear el subárbol del hijo.
		crear_arbol(profundidad - 1, hijo)

# Función alternativa para aplicar el algoritmo Min-Max (estructura similar a min_max).




# Función principal que implementa el algoritmo Min-Max.
def min_max(nodoActual, profundidad, maximo: bool = True):
	if (len(nodoActual.hijos) == 0):
		# Caso base: si la profundidad es 0, devuelve el valor del nodo actual.
		return nodoActual
	hijos = []  # Lista para almacenar los valores calculados de los hijos.

	if (maximo):
		# Si es el turno del maximizador:
		for hijo in nodoActual.hijos:
			# Calcula recursivamente los valores de los hijos alternando al minimizador.
			next_max_node = min_max(hijo, profundidad - 1, False)
			hijos.append(next_max_node)
			nodoActual.puntuacion = max(hijos, key=lambda item: item.puntuacion).puntuacion
		if nodoActual.valor == "Raiz":
			return max(nodoActual.hijos, key=lambda item: item.puntuacion)
		return max(hijos, key=lambda item: item.puntuacion)
	else:
		# Si es el turno del minimizador:
		for hijo in nodoActual.hijos:
			# Calcula recursivamente los valores de los hijos alternando al maximizador.
			next_max_node = min_max(hijo, profundidad - 1, True)
			hijos.append(next_max_node)
			nodoActual.puntuacion = min(hijos, key=lambda item: item.puntuacion).puntuacion
		return min(hijos, key=lambda item: item.puntuacion)

# Bloque principal del programa.
if __name__ == "__main__":
	arbol = Nodo("Raiz")  # Crea el nodo raíz con el valor "Raiz".
	# Llama a la función para construir el árbol.
	crear_arbol(PROFUNDIDAD, arbol)

	imprimir_arbol(arbol)  # Imprime el árbol completo en forma jerárquica.
	# Aplica el algoritmo Min-Max y muestra el resultado.
	# print(min_max(arbol, PROFUNDIDAD))


"""movimientos_valores = {
    "mover_seguro": 1,
    "mover_amenazado": -5,
    "comer_ficha_normal": 10,
    "comer_fichas_cadena": 15,
    "comer_ficha_protegida": 20,
    "promocion_a_dama": 50,
    "proteger_promocion": 30,
    "posicion_central": 5,
    "formar_pared": 10,
    "ficha_aislada": -10,
    "proteger_ficha_amenazada": 15,
    "cubrir_dama": 20,
    "formacion_mutua": 10,
    "perder_dama": -50,
    "perder_ficha_normal": -10,
    "ignorar_captura": -15
}
"""

"""Definir las reglas de captura:

Establecer cómo la IA determina qué fichas puede capturar.
Por ejemplo: si la IA está evaluando un estado, debe poder identificar qué fichas del oponente son vulnerables.✅✅✅


Agregar información al árbol:

Añadir propiedades a los nodos que representen el estado del tablero.
Cada nodo deberá reflejar una posición actual del tablero, fichas disponibles y cuáles pueden ser capturadas.
Modificar la generación del árbol:

Hacer que los hijos de un nodo reflejen los movimientos posibles, incluida la captura de fichas.
Asegurarnos de que las capturas alteren el estado del tablero de forma adecuada.
Actualizar el algoritmo Min-Max:

Evaluar el valor de un nodo basado no solo en las fichas capturadas, sino también en las posibilidades futuras de la IA y el oponente.
Usar una función heurística para evaluar qué tan ventajosa es una captura en un determinado estado."""
