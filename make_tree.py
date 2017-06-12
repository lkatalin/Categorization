#credit: https://stackoverflow.com/questions/2358045/how-can-i-implement-a-tree-in-python-are-there-any-built-in-data-structures-in
from print_tree import *

class Tree(object):
    def __init__(self, name='root', children=None, parents=None):
        self.name = name
        self.children = []
        self.parents = []
        self.labelinfo = ""
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
        assert isinstance(child, Tree)
        self.children.append(child)
    def add_parent(self, parent):
        assert isinstance(parent, Tree)
        self.parents.append(parent)

def find_b(tree, elm):
    if not tree or not elm:
        return None
    if tree.name == elm:
        #print "found"
        return tree
    else:
        #print "not found in node %s" % tree.name
        for child in tree.children:
            find_b(child, elm)

# use:
# t = Tree('*', [Tree('1'),
#                Tree('2'),
#                Tree('+', [Tree('3'),
#                           Tree('4')])])

#print_tree(t)
#find_b(t, "4")
