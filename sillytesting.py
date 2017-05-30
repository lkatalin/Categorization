from make_tree import *
from print_tree import *
from hashval import *

t = Tree('*', [Tree('1'), Tree('2'), Tree('+', [Tree('3'), Tree('4')])])

t1 = Tree('a', [Tree('b'), Tree('c')])

t2 = Tree('c', [Tree('d')])

t3 = Tree('e', [Tree('f')])

lst = [t1, t2, t3]

combine_trees(lst)
