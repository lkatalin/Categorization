from simple_dag import *

# HASHVAL: uses depth-first traversal of dag to form
# value to be used with grouping
#
def hashval(trace):
    all_paths = []
    thegraph = dag(trace)
    #find leaves and dump their path info
    for key, values in thegraph.items():
        for node in values:
            if node.children == []:
                all_paths.append(node.ppath)
    lst = ["->".join(x) for x in all_paths]
    return "||".join(lst)
