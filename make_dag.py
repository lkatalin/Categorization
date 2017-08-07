import re
import sys
from make_nodes import *
from print_stuff import *

def dag(trace):
    #import pdb; pdb.set_trace()
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

        idnum = re.search(r'(.*) \[', node_text).group(1)
        label = re.search(r'\[label="(.*)"\]', node_text).group(1)
        
        # OLD
        #idnum = re.search(r'\d+.\d+', node_text).group(0)
  
        print label + " " + idnum
 
        new_node = Node(label)
        new_node.id = idnum

        # to find node object by its idnum
        name_to_obj[idnum] = new_node

        # node considered a root until dst for other node
        root.append(new_node) 

    for edge in trace.fullEdges:
        # extract source and dest nodes as strings
        #src_str = re.search(r'(\d+.*) ->', edge).group(1)
        #dst_str = re.search(r'-> (\d+.*) \[', edge).group(1)

        # OLD
        #dst_str = re.search(r'-> (\d+.\d+)', edge).group(1) 
        #src_str = re.search(r'(\d+.\d+) ->', edge).group(1)

        # for DOT output from json_dag.py (span -> DAG)
        dst_str = re.search(r'-> (.+) \[', edge).group(1)
        src_str = re.search(r'(.+) ->', edge).group(0)

        print "source: %s, dest: %s" % (src_str, dst_str)

        # update both node object fields, if nodes exist
        try:
	    srcnode = name_to_obj[src_str]
	    dstnode = name_to_obj[dst_str]
	    srcnode.add_child(dstnode)
	    dstnode.add_parent(srcnode)
            dstnode.latency = re.search(r'\[label="(.*)"\]', edge).group(1)

            # OLD
	    #dstnode.latency = re.search(r'R: (\d+.\d+ us)', edge).group(1)
	    
            # keep track of potential root nodes
            #import pdb; pdb.set_trace()

            #sometimes dstnode may already be removed if it showed up before as the dst for something else
            #but should switch to looking these up by ID instead of name...
            if dstnode in root:
	        root.remove(dstnode)

        except KeyError:
            print "error: source or destination node of edge not in node group"
            sys.exit()
 
    if len(root) == 1:
	#print "Trace structure for Trace %s: " % trace.traceId
	#print_tree(root[0])
        #print "\n\n"
        return root[0]
    else:
        return root[0] 
        #print "error: multiple root nodes detected in trace"
        #sys.exit()
