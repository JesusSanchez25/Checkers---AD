import random

PROFUNDIDAD = 7
class Nodo:
	def __init__(self, valor):
		self.valor = valor
		self.hijos = []

	def agregar_hijo(self, hijo):
		self.hijos.append(hijo)

def imprimir_arbol(nodo, nivel=0):
	print("  " * nivel + f"=={nodo.valor}")
	for hijo in nodo.hijos:
		imprimir_arbol(hijo, nivel + 1)


def crear_arbol(profundidad: int = 0, nodoActual: Nodo = None):
	if (profundidad == 0):
		return
	for i in range(4):
		hijo = Nodo(f"Nodo {i}")
		if (profundidad == 1):
			hijo = Nodo(random.randint(-9, 9))
			print(hijo.valor, end=",")
			nodoActual.agregar_hijo(hijo)
		else:
			nodoActual.agregar_hijo(hijo=hijo)
		crear_arbol(profundidad - 1, hijo)



def min_max_TEST(nodoActual: Nodo, profundidad: int, maximo: bool = True):
    # Caso base: si es una hoja, devuelve su valor
    if profundidad == 0 or not nodoActual.hijos:
        return nodoActual.valor

    # Recursión para los hijos
    valores = []
    for hijo in nodoActual.hijos:
        valor = min_max(hijo, profundidad - 1, not maximo)
        valores.append(valor)

    # Devuelve el máximo o mínimo según el turno
    return max(valores) if maximo else min(valores)

def min_max(nodoActual, profundidad, maximo: bool = True):
	if (profundidad == 0):
		return nodoActual.valor
	hijos = []

	if (maximo):
		for hijo in nodoActual.hijos:
			hijos.append(min_max(hijo, profundidad - 1, False))
			# print(hijos)
		return max(hijos)
	else:
		for hijo in nodoActual.hijos:
			hijos.append(min_max(hijo, profundidad - 1))
			# print(hijos)
		return min(hijos)

if __name__ == "__main__":
	arbol = Nodo("Raiz")
	crear_arbol(PROFUNDIDAD, arbol)

	imprimir_arbol(arbol)
	print(min_max(arbol, PROFUNDIDAD))
	print(min_max_TEST(arbol, PROFUNDIDAD))


