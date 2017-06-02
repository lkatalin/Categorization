import re
from make_tree import *
from print_tree import *

#parent nodes are keys, children are values (as list)
nodes_seen = {}

#this is given a trace object
def dag(trace):
    for edge in trace.edges:
        #extract source and dest nodes
        src = re.search(r'(\d+.\d+) ->', edge).group(1)
        dst = re.search(r'-> (\d+.\d+)', edge).group(1)

        #create new nodes and update their pointers
        src_tree = Tree(src)
        dst_tree = Tree(dst)
            
        src_tree.add_child(dst_tree)
        dst_tree.add_parent(src_tree)

        #this is a dict, but since the pointers are updated
        #we could just use a list instead?
        if src_tree in nodes_seen:
            nodes_seen[src_tree].append(dst_tree)
        else: 
            nodes_seen[src_tree] = [dst_tree]
    return nodes_seen
