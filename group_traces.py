import re
from simple_dag import *
from decimal import *

#this is the dictionary of traces
#key is structure based on hashval below
categories = {}

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

# DFT of trace's DAG structure (lossy)
#
def depth_first_traversal(trace):
    #keep track of nodes seen and don't duplicate

    def dft_helper(root):
        nodes = []
        stack = [root]
        while stack:
            cur_node = stack[0]
	    stack = stack[1:]
            if cur_node.name not in nodes:
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

# HASHVAL: forms hash value of all paths in DAG
# to be used with grouping; uses DFT
#
def hashval(trace):
    hashval = "".join(re.findall(r'(\d)\.1', "".join(depth_first_traversal(trace))))
    return hashval

# GROUP_TRACES: based on structure
#
def group_traces(trace):
    #has this trace's structure been seen before?
    maybe_key = categories.get(trace.hashval)
    if maybe_key:
        categories[trace.hashval].append(trace.traceId)
    else:
        categories[trace.hashval] = [trace.traceId]

# PROCESS_GROUPS: calculates avg latency and
# variance of a group
#
def process_groups(d, tlist):
    group_info = {}
    for key, values in d.items():
        psum = 0
        lst = []
        l = len(values)
 
        # calculate average
        for value in values:
            psum += float(tlist[value - 1].response)
        avg = psum / l
        
        # calculate variance
        psum = 0
        for value in values:
            curr = (float(tlist[value - 1].response) - avg) ** 2
            
            psum += curr
        if (l - 1) > 1:
            var = (1 / float(l - 1)) * psum
        else:
            var = 0

        group_info[key] = {'Average' : avg, 'Variance': var}
    return group_info
