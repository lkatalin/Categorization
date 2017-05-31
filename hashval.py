import re
from make_tree import *

def compare_nodes(n1, n2, orig_lst):
    #print "comparing nodes now for % s and %s" % (n1.name, n2.name)
    #this keeps the first tree in case of same node
    if n1.name == n2.name:
        for child in n1.children:
            n2.add_child(child)
        for parent in n1.parents:
            n2.add_parent(parent)
        #orig_lst = orig_lst.remove(n2)
        n1.name = 'remove'
        #print "updated a tree. %s now has children : " % n2.name
        #for child in n2.children:
        #    print child
        return n2
    else: 
        return False

def compare_trees(t1, t2, orig_list):
    print "comparing trees now"
    maybe_tree = compare_nodes(t1, t2, orig_list)
    if not maybe_tree:
        for child2 in t2.children:
            compare_nodes(t1, child2, orig_list)
        for child1 in t1.children:
            for child2 in t2.children:
                compare_nodes(child1, child2, orig_list)
    else:
        return maybe_tree 

def combine_trees(tree_list):
    print "our starting tree list is " 
    print tree_list
    l = len(tree_list)
    if l < 1:
        print "cannot process empty list"
    elif l == 1:
        return tree_list[0]
    else:
        for tree in tree_list:
            other_trees = [x for x in tree_list if x != tree]
            for other_tree in other_trees:
                maybe_tree = compare_trees(tree, other_tree, tree_list)
                if maybe_tree:
                    tree_list.replace(tree, maybe_tree)
    tree_list = [t for t in tree_list if t.name != 'remove']
    #for tree in tree_list:
    #    if tree.name == 'remove':
    #        print "we should remove %s" % tree.name
            #tree_list.remove(tree)
    return tree_list

def dag(trace):
    tree = Tree()
    trees = [tree]

    for edge in trace.edges:
        #extract source and dest nodes
        src = re.search(r'(\d+.\d+) ->', edge).group(1)
        dst = re.search(r'-> (\d+.\d+)', edge).group(1)

       #all you're doing here is updating pointers in the nodes
       #this first bit should return the first tree in which the node is present
        for tree in trees:
            srcnode = find_b(tree, src)
            dstnode = find_b(tree, dst)
         
            #if neither is in the tree, make new populated tree structure
            if not srcnode and not dstnode:
                new_src_tree = Tree(src)
                new_dst_tree = Tree(dst)
            
                new_src_tree.add_child(dst)
                new_dst_tree.add_parent(src)

                #add only src tree into list
                trees.append(new_src_tree)

            #if they're both there, just connect them
            elif srcnode and dstnode:
                srcenode.add_child(dstnode)
                dstnode.add_parent(srcnode)
            
            #if only one is present, add the other
            elif srcnode and not dstnode:
                new_dst_tree = Tree(dst)
                new_dst_tree.add_parent(srcnode)
                srcnode.add_child(new_dst_tree)

            elif dstnode and not srcenode:
                #add the src as a tree (with dstnode child) to dst's parents
                new_src_tree = Tree(src)
                new_src_tree.add_child(dstnode)
                dstnode.add_parent(new_src_tree)

#def hashval(trace):

#for trace in tracelist:
#    hashval = ""
#    for edge in trace.edges:
#        n1 = re.search(r'(\d{5}) ->', edge).group(1)
#        n2 = re.search(r'.*?(\d{5})$', edge).group(1)
#        partial = '-'.join([re.search(r'(\d{5}) ->',
#            edge).group(1), re.search(r'.*?(\d{5})$', edge).group(1)])
#        hashval += (partial + '|')
#    trace.hashval = hashval

