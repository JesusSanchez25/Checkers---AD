from trees import * 

width, height = 1280, 640
radius = 16
h_offset = 16
v_offset = -64
window = GraphWin("Tree Visualizer", width, height, autoflush=False)
window.setCoords(0, 0, width, height)

def visualize(tree, animate=False):
	'''
	Provide the full visualization of the tree and its __repr__. Can highlight both the circular nodes
	and their corresponding __repr__()'s by clicking.
	'''
	def draw_tree(t):
		'''
		Draw the circle for the current node and its label in the center of the circle.
		If the current node is not the root node, draw a line connecting the top of the current node to the root node,
		ensuring the line does not cross into either circle. 
		'''
		t.circle.draw(window)
		t.text.draw(window)
		
		if t.parent:
			distance = ((t.parent.x - t.x)**2 + (t.parent.y-t.y)**2 ) ** 0.5
			parent_dx = (t.parent.x - t.x) / distance * radius
			parent_dy = (t.parent.y - t.y) / distance * radius
			Line(Point(t.x, t.y + radius), Point(t.parent.x - parent_dx, t.parent.y - parent_dy)).draw(window)

		for b in t.branches:
			draw_tree(b)

	def draw_repr(t, h=0.95*height, max_ppr=0.75*width, space=7):
		'''
		Draw t.__repr__() onto the window, making sure no overlap occurs.
		Return a dictionary mapping each character's index within t.__repr__() to its corresponding
		Text object (useful for coloring the Text object later).
		'''
		strindex_to_textobj = {}

		def draw_text(text, color="black", size=14, font="courier"):
			text.setSize(size)
			text.setFace(font)
			text.setFill(color)
			text.draw(window)
			
		draw_text(Text(Point((width - max_ppr)/2 - 24, h), 't = ')) 

		def draw_baserepr(string):
			'''
			Draw the string onto the window by creating and drawing a Text object for each character inside.
			Each character has 'space' number of pixels between. The string is separated into rows beginning at height
			'h' and each of width 'max_ppr'.
			'''
			px_start, px_end = (width - max_ppr)/2, (width + max_ppr)/2
			y = h
			i = 0
			
			while i < len(string):
				text = Text(Point(px_start, y), string[i])
				draw_text(text)
				strindex_to_textobj[i] = text

				px_start += space
				i += 1
				
				if px_start > px_end:
					px_start = (width - max_ppr)/ 2
					y -= 16
					if y - t.y <= 16:
						raise WinsizeError("Repr overlaps with Tree")

		draw_baserepr(tree.__repr__())

		return strindex_to_textobj

	def fill_loop(t):
		'''
		Loop that allows user to click the nodes on the visual tree, highlighting subtrees and their corresponding
		text within the __repr__ green. 
		'''
		def search_tree(st, point):
			'''
			Detect if the point is within st.circle's radius, returning st if it is. 
			'''
			if (st.x - 16 <= point.getX() <= st.x + 16) and (st.y - 16 <= point.getY() <= st.y + 16):
				return st
			for b in st.branches:
				if search_tree(b, point) is not None:
					return search_tree(b, point)

		def fill_tree(st, color):
			'''
			Fill st and all of its children's circles to be color.
			'''
			st.circle.setFill(color)
			for b in st.branches:
				fill_tree(b, color)

		def find_highlight_index(st):
			'''
			Find the index inside of t.__repr__() where st's __repr__ occurs, accounting
			for duplicates by using st.repr_occurrence. 
			'''
			substring = st.__repr__()
			copy = t.__repr__()
			occurrence = 0
			while True:
				if substring in copy:
					if occurrence == st.repr_occurrence:
						return copy.index(substring)
					else:
						copy = copy.replace(substring, ' '*len(substring), 1)
					occurrence += 1

		d = draw_repr(tree)
		if animate:
			window.autoflush = True
		draw_tree(tree)
		window.autoflush = False

		while not window.isClosed():
			click_pt = window.getMouse()

			fill_this = search_tree(t, click_pt)
			
			#highlight both the circles and the text
			if fill_this is not None:
				fill_tree(fill_this, 'green')
				repr_index = find_highlight_index(fill_this)
				for index in d.keys():
					if index in range(repr_index, repr_index + len(fill_this.__repr__())):
						d[index].setFill('green')

			window.getMouse()

			#second click resets circles to white and text to black
			fill_tree(t, 'white')
			for index in d.keys():
				d[index].setFill('black')

	fill_loop(tree)





