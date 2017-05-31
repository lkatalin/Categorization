import re
from make_tree import *

# COMPARE_NODES: if same node, keeps n2
#"same" means the node is a source in one 
# edge but a destination in another
# a.k.a. not a root or leaf
#
def compare_nodes(n1, n2):
    if n1.name == n2.name:
        for child in n1.children:
            n2.add_child(child)
        for parent in n1.parents:
            n2.add_parent(parent)
        n1.name = 'remove'
        return n2

# COMPARE_TREES: iterator to compare nodes
# returns value only if match was found
#
def compare_trees(t1, t2):
    maybe_tree = compare_nodes(t1, t2)
    if maybe_tree:
        return maybe_tree
    else:
        for child2 in t2.children:
            compare_nodes(t1, child2)
        for child1 in t1.children:
            for child2 in t2.children:
                compare_nodes(child1, child2)

# COMBINE_TREES: iterator to compare trees
# compares each node in a tree to all nodes
# of all other trees in the list;
# keeps only trees that are not duplicates
# once combined
#
def combine_trees(tree_list): 
    l = len(tree_list)
    if l < 1:
        print "cannot process empty list"
    elif l == 1:
        return tree_list
    else:
        for tree in tree_list:
            other_trees = [x for x in tree_list if x != tree]
            for other_tree in other_trees:
                maybe_tree = compare_trees(tree, other_tree)
                if maybe_tree:
                    tree_list[:] = [maybe_tree if tree.name == tree else t for t in tree_list]
        tree_list = [t for t in tree_list if (t.name != 'remove' and t.name != 'root')]
        return tree_list

# DAG takes a trace object and uses its list of edges to 
# construct a directed acyclic graph; attempts to check
# that all nodes connect and returns graph if so
#
def dag(trace):
    trees = []

    #FIRST, add all edges into tree list, connecting where possible
    for edge in trace.edges:
        #extract source and dest nodes
        src = re.search(r'(\d+.\d+) ->', edge).group(1)
        dst = re.search(r'-> (\d+.\d+)', edge).group(1)

        #find if these nodes are already in tree list
        #returns the *first* tree in which the node is present
        def search_trees(node):
            for tree in trees:
                maybe_found = find_b(tree, node)
                return maybe_found

        srcnode = search_trees(src)
        dstnode = search_trees(dst)
         
        #ADD_NEW
        #if neither is in the tree, make new linked trees
        if not srcnode and not dstnode:
            new_src_tree = Tree(src)
            new_dst_tree = Tree(dst)
            
            new_src_tree.add_child(new_dst_tree)
            new_dst_tree.add_parent(new_src_tree)

            #add only src tree into list
            trees.append(new_src_tree)

        #CONNECT_EXISTING
        #if they're both in the tree already, connect them
        elif srcnode and dstnode:
            srcenode.add_child(dstnode)
            dstnode.add_parent(srcnode)
            
        #ADD PARENT OR CHILD
        #if only one is present, add the other
        elif srcnode and not dstnode:
            new_dst_tree = Tree(dst)
            new_dst_tree.add_parent(srcnode)
            srcnode.add_child(new_dst_tree)

        elif dstnode and not srcenode:
            new_src_tree = Tree(src)
            new_src_tree.add_child(dstnode)
            dstnode.add_parent(new_src_tree) 

    #NEXT, combine trees if possible
    combined = combine_trees(trees)

    if len(combined) > 1:
        print "malformed DAG, some nodes do not connect"
    elif len(combined) < 1:
        print "no graph exists"
    else:
         return combined[0]
