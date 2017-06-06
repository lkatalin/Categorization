from simple_dag import *

#path = []
#path_list = []

#traversal - this is passed a list of nodes
        

# HASHVAL: uses depth-first traversal of dag to form
# value to be used with grouping
#
def hashval(trace):
    all_paths = []
    thegraph = dag(trace)
    for key, values in thegraph.items():
        print "in hashval key:"
        print key
        for node in values:
            if node.children == []: #it's a leaf
                all_paths.append(node.ppath)
    print "all paths: "
    print all_paths
    return all_paths
