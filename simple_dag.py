import re
import sys
from make_tree import *
from print_stuff import *

def dag(trace):
    """
    given trace object, returns dict of parent/[children]
    for key/[values] pairs. these are also a linked list.
    """
    nodes_seen = {}

    def lookup(dictionary, name):
        """
        if "name" is in dict, return tuple ("name" obj, 
        "type") where type refers to key (k), value (v),
        or both (x)
        """
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
        return returnval

    for edge in trace.fullEdges:
        # extract source and dest nodes as strings
        src = re.search(r'(\d+.\d+) ->', edge).group(1)
        dst = re.search(r'-> (\d+.\d+)', edge).group(1)

        # cannot add same edge twice
        # but should we keep track that it showed up again?
        for key, values in nodes_seen.items():
            if key.name == src:
                for value in values:
                    if value.name == dst:
                        print "error: attempted addition of edge %s -> %s redundant" % (src, dst)
                        sys.exit()

        # extract label info to push into dst node
        label = re.search(r'R: (\d+.\d+ us)', edge).group(1)

        # check whether src in dict already
        src_present = lookup(nodes_seen, src)
        dst_present = lookup(nodes_seen, dst)

        if src_present:
            srcnode = src_present[0]
            srcnodetype = src_present[1]

        if dst_present:
            # if present as a value == multi-parent scenario
            dstnode = dst_present[0]
            dstnodetype = dst_present[1]

        # POSSIBLE COMBINATIONS
        # both present
        if src_present and dst_present:
            # include checks to make sure != cycle
            # TO DO
        
            srcnode.add_child(dstnode)
            dstnode.add_parent(srcnode)
            dstnode.labelinfo = label   
            nodes_seen[srcnode] = [dstnode]
 
        # only src present
        if src_present and not dst_present:
	    # create a dst tree and link them
	    dst_tree = Tree(dst)
	    srcnode.add_child(dst_tree)
	    dst_tree.add_parent(srcnode)
            dst_tree.labelinfo = label

            # if src is already a key, append
            if srcnodetype == "k" or srcnodetype == "x":
                nodes_seen[srcnode].append(dst_tree)
            
            # if src is a value/dst somewhere else, create new key
            elif srcnodetype == "v":
                nodes_seen[srcnode] = [dst_tree]
           
        # only dst present
        if dst_present and not src_present:
	    src_tree = Tree(src)
	    src_tree.add_child(dstnode)
	    dstnode.add_parent(src_tree)
            dstnode.labelinfo = label
	    nodes_seen[src_tree] = [dstnode] 
 
        # neither present
        if not dst_present and not src_present:
            src_tree = Tree(src)
            dst_tree = Tree(dst)
            src_tree.add_child(dst_tree)
            dst_tree.add_parent(src_tree)
            dst_tree.labelinfo = label
            nodes_seen[src_tree] = [dst_tree]
 
    return nodes_seen
