import re
import sys
from make_nodes import *
from print_stuff import *

def dag(trace):
    """
    creates treelike structure of nodes in trace linked to
    their parents and children. returns root node of structure.
    """
    # mapping of node names to actual node objects
    id_to_obj = {}
    # root node for a trace's DAG structure
    root = []

    for node_text in trace.fullNodes:
        '''
        even though node is named with "trace name,"
        hash map's keys for name_to_obj are the idnums
        to ensure uniqueness
        '''

        idnum = re.search(r'(.*) \[', node_text).group(1)
        label = re.search(r'\[label="(.*)"\]', node_text).group(1)
         
        new_node = Node(label)
        new_node.id = idnum

        # update hash map
        id_to_obj[idnum] = new_node

        # keep track of potential root nodes
        root.append(new_node.id)

    for edge in trace.fullEdges:
        # extract source and dest nodes as strings
        # below works for DOT output from json_dag.py (span -> DAG)
        try:
            dst_str = re.search(r'-> (.+) \[', edge).group(1)
        except AttributeError:
            dst_str = re.search(r'\d+ -> (\d+)', edge).group(1)
        src_str = re.search(r'(.+) ->', edge).group(1)

        # update both node object fields, if nodes successfully created
        try:
	    srcnode = id_to_obj[src_str]
        except KeyError:
            print "error: source node %s of edge not in node group" % src_str
            for n in id_to_obj.iteritems():
                print n
            sys.exit()
        try:
	    dstnode = id_to_obj[dst_str]
        except KeyError:
            print "error: dest node of edge not in node group" % dst_str
            for n in id_to_obj.iteritems():
                print n
            sys.exit()

        # update node relationships
	srcnode.add_child(dstnode)
	dstnode.add_parent(srcnode)
        dstnode.latency = re.search(r'\[label="(.*)"\]', edge).group(1)

        # remove from root if is dst
        if dstnode.id in root:
            root.remove(dstnode.id)
 
    if len(root) == 1:
        return id_to_obj[root[0]]
    else:
        print "error: no root node or multiple root nodes detected in trace"
        print "root: " + str([root])
        sys.exit()
