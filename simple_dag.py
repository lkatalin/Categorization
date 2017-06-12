import re
from make_tree import *
from print_tree import *

#given trace object, returns dict of parent/children pairs
#
def dag(trace):
    #parent nodes are keys, children are values (as list)
    nodes_seen = {}

    #sees if node called "name" is in dict already
    #returns "k" if already key, "v" if already value
    #or "x" if already both
    def lookup(dictionary, name):
        returnval = None
        for key, values in dictionary.items():
            if key.name == name:
                returnval = (key, "k")
	    for value in values:
		if value.name == name:
                    if returnval and returnval[1] == "k":
		        returnval = (value, "x")
                    else:
                        returnval = (value, "v")
        if returnval:
            return returnval
        return False
  
    def push_ppath(node):
        for child in node.children:
            child.add_parent(node)
            push_ppath(child)

    for edge in trace.fullEdges:
        #extract source and dest nodes as strings
        src = re.search(r'(\d+.\d+) ->', edge).group(1)
        dst = re.search(r'-> (\d+.\d+)', edge).group(1)

        #extract label info to push into dst node
        label = re.search(r'R: (\d+.\d+ us)', edge).group(1)

        #check whether src in dict already
        src_present = lookup(nodes_seen, src)
        dst_present = lookup(nodes_seen, dst)

        if src_present:
            srcnode = src_present[0]
            srcnodetype = src_present[1]

        if dst_present:
            #if present as a value == multi-parent scenario
            dstnode = dst_present[0]
            dstnodetype = dst_present[1]

        #POSSIBLE COMBINATIONS OF EXISTENCE
        #both present
        if src_present and dst_present:
            #include checks to make sure != cycle
            #TO DO
        
            srcnode.add_child(dstnode)
            dstnode.add_parent(srcnode)
            push_ppath(dstnode)
            dstnode.labelinfo = label   
            nodes_seen[srcnode] = [dstnode]
 
        #only src present
        if src_present and not dst_present:
	    #create a dst tree and link them
	    dst_tree = Tree(dst)
	    srcnode.add_child(dst_tree)
	    dst_tree.add_parent(srcnode)
            dst_tree.labelinfo = label
            push_ppath(dst_tree)
            #src is already a key

            if srcnodetype == "k" or srcnodetype == "x":
                nodes_seen[srcnode].append(dst_tree)
            
            #this src is a value/dst somewhere else
            elif srcnodetype == "v":
                nodes_seen[srcnode] = [dst_tree]
           
        #only dst present
        if dst_present and not src_present:
	    src_tree = Tree(src)
	    src_tree.add_child(dstnode)
	    dstnode.add_parent(src_tree)
            push_ppath(dstnode)
            dstnode.labelinfo = label
	    nodes_seen[src_tree] = [dstnode] 
 
        #neither present
        if not dst_present and not src_present:
            src_tree = Tree(src)
            dst_tree = Tree(dst)
            src_tree.add_child(dst_tree)
            dst_tree.add_parent(src_tree)
            push_ppath(dst_tree)
            dst_tree.labelinfo = label
            nodes_seen[src_tree] = [dst_tree]
 
    return nodes_seen
