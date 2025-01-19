from graphics import *

class Tree:
    '''
    CS61A implementation of Tree.
    '''
    def __init__(self, label, branches=[]):
        for b in branches:
            assert isinstance(b, Tree)
        self.label = label
        self.branches = list(branches)
    def is_leaf(self):
        return not self.branches
    def __repr__(self):
        if self.branches:
            branch_str = ', ' + repr(self.branches)
        else:
            branch_str = ''
        return 'Tree({0}{1})'.format(self.label, branch_str)
    def __str__(self):
        def print_tree(t, indent=0):
            tree_str = '  ' * indent + str(t.label) + "\n"
            for b in t.branches:
                tree_str += print_tree(b, indent + 1)
            return tree_str
        return print_tree(self).rstrip()

class WinsizeError(Exception):
    '''
    Handles errors when the tree or repr's visual representation does not fit the window.
    '''
    pass

def set_all(vtree, width, height, radius, h_offset, v_offset):

    def set_levels(t, level=0):
        '''
        t: Should be an entire tree, including the root node by default

        Set the level attribute for every node within t. The row containing just the root
        has level 0, trees within its branches have level 1, and so on.
        '''
        t.level = level
        for b in t.branches:
            set_levels(b, level + 1)

    def set_parents(t, parent=None):
        '''
        t: Should be an entire tree, including the root node by default

        Set the parent attribute for every node within t. The root node is assigned parent = None
        by default; all other nodes' parents point to their parent node.
        '''
        t.parent = parent
        for b in t.branches:
            set_parents(b, t)

    def set_repr_occurrences(t):
        '''
        t: Should be an entire tree, including the root node

        Set the repr_occurrence attribute for every node within t.
        This attribute is an integer tracking the node's __repr__'s
        occurrence within the entire tree t's __repr__.

        For example, if t = Tree(1, [Tree(2), Tree(2)]), t.branches[0].repr_occurrence = 0 and
        t.branches[1].repr_occurrence = 1, since 'Tree(2)' shows up twice in 'Tree(1, [Tree(2), Tree(2)])'
        '''
        d = {t.__repr__(): 0}
        t.repr_occurrence = d[t.__repr__()]

        def helper(st):
            for b in st.branches:
                if b.__repr__() in d.keys():
                    d[b.__repr__()] += 1
                else:
                    d[b.__repr__()] = 0
                b.repr_occurrence = d[b.__repr__()]
                helper(b)

        helper(t)

    def set_coords(tree, x, y, radius, h_offset, v_offset):
        '''
        tree: An entire tree, including the root node
        x: x-coordinate of tree's root node
        y: y-coordinate of tree's root node
        radius: Radius of each node
        h_offset: Minimum horizontal distance between each node
        v_offset: Vertical distance between parent and children nodes

        Assign instance attributes x and y to every node within tree, representing
        the coordinates of that node's center, with the following constraints:

        (1) each node has a radius 'radius'
        (2) there is a minimum of h_offset between nodes on the same level
        (3) there is v_offset between nodes on successive levels
        '''
        tree.x, tree.y = x, y

        def rows(t):
            '''
            t: An entire tree, including the root node

            Returns a dictionary with keys equal to the level and values equal to lists of
            trees within t having that level.
            '''
            d = {0: [t]}

            def helper(st):
                for b in st.branches:
                    if b.level in d.keys():
                        d[b.level].append(b)
                    else:
                        d[b.level] = [b]
                    helper(b)

            helper(t)
            return d

        layers = rows(tree)

        def intersect(p1, p2):
            '''
            p1: Tree
            p2: Tree

            Determines if the spaces occupied by the branches of p1 and p2 overlap.
            If they do, return the minimum distance to shift p1 and p2 both by such that the spaces no longer overlap.
            Otherwise return 0.
            '''
            if p1.branches and p2.branches:
                p1_space = (p1.branches[0].x - radius - h_offset, p1.branches[-1].x + radius + h_offset)
                p2_space = (p2.branches[0].x - radius - h_offset, p2.branches[-1].x + radius + h_offset)
                is_intersect = max(p1_space[0], p2_space[0]) < min(p1_space[1], p2_space[1])

                if is_intersect:
                    if p1_space[0] <= p2_space[0]:
                        return (p1_space[1] - p2_space[0]) / 2
                    else:
                        return (p2_space[1] - p1_space[0]) / 2
            return 0

        def node_counter(length):
            '''
            length: length of some tree's branches

            Returns a generator used for determining the horizontal positions of each node.
            These positions are based on whether length is even or odd.
            '''
            if length % 2 == 0:
                ctr = min(0, -(length - 1))
                while ctr <= length:
                    yield ctr * (h_offset / 2 + radius)
                    ctr += 2
            else:
                ctr = -(length // 2)
                while ctr <= length // 2:
                    yield ctr * (2 * radius + h_offset)
                    ctr += 1

        def shift_tree_left(row_index, tree_index, dist):
            '''
            row_index: key value in layers corresponding to current row
            tree_index: index of tree within layers[row_index]
            dist: how much we want to shift the tree left or right

            Shift all elements to the left of and including layers[row_index][tree_index]
            within layers[row_index] to the left and all elements to the right of it to the right by dist.
            Then, recursively repeat this process using the parent of layers[row_index][tree_index] and its
            row, until the root node is reached.
            '''
            parent = layers[row_index][tree_index].parent

            if parent is None:
                return

            parent_index = layers[row_index - 1].index(parent)

            if len(layers[row_index]) > 1:
                for i in range(tree_index + 1):
                    layers[row_index][i].x -= dist

                for i in range(tree_index + 1, len(layers[row_index])):
                    layers[row_index][i].x += dist

            shift_tree_left(row_index - 1, parent_index, dist)

        def set_lower(level):
            '''
            level: the level of some row within tree

            While the rightmost tree at the current level has not had its coordinates
            assigned yet, keep setting the coordinates for each tree on the current level by
            accessing the parent level.

            Once the rightmost tree has been assigned coordinates, check for
            overlap on the current level by using intersect on parents from the previous level.
            If overlap is detected, apply shift_tree_left.

            Iteratively repeat this process until the last level of tree is reached.
            '''
            while level in layers.keys():
                current_row = layers[level]
                prev_row = layers[level - 1]

                while not hasattr(current_row[-1], 'x'):
                    for parent in prev_row:
                        spacings = node_counter(len(parent.branches))
                        for child in parent.branches:
                            child.x, child.y = parent.x + next(spacings), parent.y + v_offset

                for i in range(len(prev_row)):
                    for j in range(i + 1, len(prev_row)):
                        overlap = intersect(prev_row[i], prev_row[j])
                        if overlap:
                            rightmost_child_index = current_row.index(prev_row[i].branches[-1])
                            shift_tree_left(level, rightmost_child_index, overlap)

                level += 1

        set_lower(1)

        def fits_screen(t):
            '''
            Makes sure that t fits on the window, otherwise throw a WinsizeError
            '''
            # if t.x - 16 <= 0 or t.x + 16 >= width or t.y - 16 <= 0:
            #     raise WinsizeError("Tree is too big to fit on window.")
            for b in t.branches:
                fits_screen(b)

        fits_screen(tree)

    def set_circles(t, r):
        '''
        t: Should be an entire tree, including the root node
        r: Radius of each circle

        Set the circle attribute for every node within t. The circle attribute is a Circle
        object from the graphics library, centered about the x and y attributes
        of the node and having radius 'r'.
        '''
        t.circle = Circle(Point(t.x, t.y), r)
        for b in t.branches:
            set_circles(b, r)

    def set_texts(t):
        '''
        t: Should be an entire tree, including the root node

        Set the text attribute for every node within t. The text attribute is a Text
        object from the graphics library, centered about the x and y attributes and
        having string = str(t.label)
        '''
        t.text = Text(Point(t.x, t.y), str(t.label))
        for b in t.branches:
            set_texts(b)

    set_levels(vtree)
    set_parents(vtree)
    set_repr_occurrences(vtree)
    set_coords(vtree, width*0.5, height*0.75, radius, h_offset, v_offset)
    set_circles(vtree, radius)
    set_texts(vtree)


