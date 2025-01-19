from draw import *
import random

def make_tree(n, max_branches=4):
	'''
	Returns a Tree object with 'n' nodes and at most max_branches branches per node. Labels are integers.

	Entering a large 'n' (around 35 or greater) or a large 'max_branches' (around 7 or greater) will likely
	result in error since the tree will not fit on the window.
	'''
	assert n > 0, 'A Tree must have at least 1 node.'
	assert max_branches > 0, 'Cannot have max_branches <= 0.'

	t = Tree(n)
	n = n - 1
	d = {0: [t]}
	level = 1

	while n > 0:
		d[level] = []
		for tree in d[level - 1]:
			i = max_branches - random.randint(0, max_branches)
			while i < max_branches or d[level] == []:
				i = i + 1
				a = Tree(n)
				tree.branches.append(a)
				d[level].append(a)
				n = n - 1
				if n <= 0:
					break
			if n <= 0:
				break
		level += 1

	return t

import random

PROFUNDIDAD_BUSQUEDA = 2
class Nodo:
	def __init__(self, valor):
		self.label = valor
		self.branches = []

	def agregar_hijo(self, hijo):
		self.branches.append(hijo)

def imprimir_arbol(nodo, nivel=0):
	print("  " * nivel + f"=={nodo.valor}")
	for hijo in nodo.hijos:
		imprimir_arbol(hijo, nivel + 1)

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

def crear_arbol(profundidad: int = 0, nodoActual: Nodo = None):
	if (profundidad == 0):
		return
	for i in range(4):
		hijo = Nodo(f"Nodo {i}")
		if (profundidad == 1):
			hijo = Nodo(random.randint(-9, 9))
			nodoActual.agregar_hijo(hijo)
		else:
			nodoActual.agregar_hijo(hijo=hijo)
		crear_arbol(profundidad - 1, hijo)



# if __name__ == "__main__":


# 	imprimir_arbol(arbol)
# 	print(min_max(arbol, 4))




#reassign tree to any tree you want to draw, or use make_tree() to create a random tree
tree = Nodo("Raiz")
crear_arbol(3, tree)

#DO NOT CHANGE THIS LINE
set_all(tree, width, height, radius, h_offset, v_offset)

#set animate to True if you want to see the tree drawn step-by-step
visualize(tree, animate=True)












