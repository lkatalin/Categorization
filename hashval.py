import re
from simple_dag import *

# ALL_PATHS: finds all paths in DAG based on 
# ppath pushed from parent to child in each 
# node object
#

def all_paths(trace):
    all_paths = []
    #find leaves and dump their path info
    for key, values in trace.dag.items():
        for node in values:
            if node.children == []:
                all_paths.append(node.ppath)
    all_paths = "||".join(["->".join(x) for x in all_paths])
    return all_paths 


def depth_first_traversal(trace):
    #keep track of nodes seen and don't duplicate

    def dft_helper(root):
        nodes = []
        stack = [root]
        while stack:
            cur_node = stack[0]
            stack = stack[1:]
            nodes.append(cur_node.name)        
            for child in cur_node.get_rev_children():
                stack.insert(0, child)
        return nodes
            
    start = []
    for node in trace.dag:
        if node.parents == []:
            start.append(node)

    if len(start) > 1:
        print "ERROR: more than one start node: "
        print start

    return dft_helper(start[0])

#def hashval(trace):
#    return "".join(depth_first_traversal(trace))
   

# HASHVAL: forms hash value of all paths in DAG
# to be used with grouping; currently uses 
# all_paths function rather than DFT
#
def hashval(trace):
    hashval = "".join(re.findall(r'(\d)\.1', "".join(depth_first_traversal(trace))))
    return hashval

#.........................
#OTHER POSSIBLE GROUPINGS|
#.........................
#by total time between nodes
#def hashval(trace):
#    hashval = 0
#    for edge in trace.fullEdges:
#        curr = float(re.search(r'R: (\d+.\d+) us', edge).group(1))
#        print "curr is %s" % curr
#        hashval += curr 
#    return hashval
