import re
from simple_dag import *

# ALL_PATHS: finds all paths in DAG based on 
# ppath pushed from parent to child in each 
# node object
#

def all_paths(trace):
    all_paths = []
    thegraph = dag(trace)
    #find leaves and dump their path info
    for key, values in thegraph.items():
        for node in values:
            if node.children == []:
                all_paths.append(node.ppath)
    all_paths = "||".join(["->".join(x) for x in all_paths])
    #print "all paths from the allpaths fxn: "
    #print all_paths
    return all_paths 


# HASHVAL: forms hash value of all paths in DAG
# to be used with grouping; currently uses 
# all_paths function rather than DFT
#
def hashval(trace):
    trace.allpaths = all_paths(trace)
    #print "paths: " 
    #print trace.allpaths
    #paths = '2586230574222222.1->2586230574555555.1->2586230574111111.1->2586230574888888.1||2586230574222222.1->2586230574555555.1->2586230574111111.1->2586230574999999.1||2586230574222222.1->2586230574555555.1->2586230574666666.1'
    hashval = "".join(re.findall(r'(\d)\.1', trace.allpaths))
    return hashval
