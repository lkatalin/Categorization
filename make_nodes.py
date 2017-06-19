#credit: https://stackoverflow.com/questions/2358045/how-can-i-implement-a-tree-in-python-are-there-any-built-in-data-structures-in
from print_stuff import *

"""
class of node objects in a doubly linked list to 
represent DOT edges in a treelike form. source
nodes are parents and destination nodes are children.
info from edge labels resides in destination nodes/
children.
"""
class Node(object):
    def __init__(self, name='root', children=None, parents=None):
        self.name = name
        self.children = []
        self.parents = []
        self.id = ""
        self.latency = ""
        if children is not None:
            for child in children:
                self.add_child(child)
        if parents is not None:
            for parent in parents:
                self.add_parent(parent)
    def __repr__(self):
        return self.name
    def __eq__(self, other):
        return (self.name == other.name)
    def __hash__(self):
        return hash(self.name)
    def get_name(self):
        return self.name
    def get_children(self):
        return self.children
    def get_parents(self):
        return self.parents
    def get_rev_children(self):
        children = self.children[:]
        children.reverse()
        return children 
    def add_child(self, child):
        assert isinstance(child, Node)
        self.children.append(child)
    def add_parent(self, parent):
        assert isinstance(parent, Node)
        self.parents.append(parent)

# breadth first search of tree for element
def find_b(tree, elm):
    if not tree or not elm:
        return None
    if tree.name == elm:
        return tree
    else:
        for child in tree.children:
            find_b(child, elm)

# use:
# t = Tree('*', [Tree('1'),
#                Tree('2'),
#                Tree('+', [Tree('3'),
#                           Tree('4')])])
