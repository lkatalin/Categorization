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


# HASHVAL: forms hash value of all paths in DAG
# to be used with grouping; currently uses 
# all_paths function rather than DFT
#
def hashval(trace):
    hashval = "".join(re.findall(r'(\d)\.1', trace.allpaths))
    return hashval

#.........................
#OTHER POSSIBLE GROUPINGS|
#.........................
#by total time between nodes
#def hashval(trace):
    hashval = 0
    for edge in trace.fullEdges:
        curr = float(re.search(r'R: (\d+.\d+) us', edge).group(1))
        print "curr is %s" % curr
        hashval += curr 
    return hashval

#by number of calls

#by number of nodes

#by R vs. W
