import re
import sys
from make_nodes import *
from print_stuff import *

def dag(trace):
    """
    creates treelike structure of nodes in trace linked to
    their parents and children. returns root node of structure.
    """
    name_to_obj = {}
    root = []

    for node_text in trace.fullNodes:
        # even though the name/identity of the node is based
        # on the label, the hash map keys are the idnums because
        # this will make lookup easy when processing edges
        idnum = re.search(r'\d+.\d+', node_text).group(0)
        label = re.search(r'\[label="(.*)"\]', node_text).group(1)
        new_node = Node(label)
        new_node.id = idnum
        name_to_obj[idnum] = new_node
        root.append(new_node)

    for edge in trace.fullEdges:
        # extract source and dest nodes as strings
        src_str = re.search(r'(\d+.\d+) ->', edge).group(1)
        dst_str = re.search(r'-> (\d+.\d+)', edge).group(1)

        # update both node object fields, if nodes exist
        try:
	    srcnode = name_to_obj[src_str]
	    dstnode = name_to_obj[dst_str]
	    srcnode.add_child(dstnode)
	    dstnode.add_parent(srcnode)
	    dstnode.latency = re.search(r'R: (\d+.\d+ us)', edge).group(1)
	    
            # keep track of potential root nodes
	    root.remove(dstnode)
        except KeyError:
            print "error: source or destination node of edge not in node group"
            sys.exit()
 
    if len(root) == 1:
	print "Trace structure for Trace %s: " % trace.traceId
	print_tree(root[0])
        print "\n\n"
        return root[0]
    else: 
        print "error: multiple root nodes detected in trace"
        sys.exit()
