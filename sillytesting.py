from make_tree import *
from print_tree import *
from hashval import *

t = Tree('*', [Tree('1'), Tree('2'), Tree('+', [Tree('3'), Tree('4')])])

t1 = Tree('a', [Tree('b'), Tree('c')])

t2 = Tree('c', [Tree('d')])

t3 = Tree('d', [Tree('f')])

lst = [t1, t2, t3]

result = combine_trees(lst)

print "our resulting tree list is "
print result

print "\n and our trees are "
for tree in result:
    print_tree(tree)
