import re
from make_dag import *
from decimal import *

# groups of traces based on structure
categories = {}

def depth_first_traversal(trace):
    """
    the DFT traverses DAG dict starting with 
    root node; returns a list indicating all
    nodes seen in order. no duplicates are
    kept in case of sync and full paths are 
    not kept.
    """
    nodes = []
    stack = [trace.dag]
    while stack:
	cur_node = stack[0]
	stack = stack[1:]
	if cur_node.name not in nodes: #do not duplicate in case of sync
	    nodes.append(cur_node.name)
	for child in cur_node.get_rev_children():
	    stack.insert(0, child)
    return nodes 

def hashval(trace):
    """
    hashval takes the list generated by DFT and 
    creates a meaningful string for the hash value
    of each trace (stored in trace object).
    """
    hashval = "".join(re.findall(r'(\d)\.1', "".join(depth_first_traversal(trace))))
    return hashval

def group_traces(trace):
    """
    traces with the same hash value (determined by
    hashval function) are in the same group. keys are
    hashvalues, values are lists of trace ids in that
    group.
    """
    maybe_key = categories.get(trace.hashval)
    if maybe_key is not None:
        categories[trace.hashval].append(trace.traceId)
    else:
        categories[trace.hashval] = [trace.traceId]

def process_groups(d, tlist):
    """
    calculates the average completion time of
    traces within a group, as well as variance 
    of each group. to do: calculate variance of
    edges.
    """
    group_info = {}
    for key, values in d.items():
        psum = 0
        lst = []
        numvals = len(values)
 
        # calculate average
        for value in values:
            psum += float(tlist[value - 1].response)
        avg = psum / numvals
        
        # calculate variance
        psum = 0
        for value in values:
            curr = (float(tlist[value - 1].response) - avg) ** 2            
            psum += curr
        if (numvals - 1) > 1:
            var = (1 / float(numvals - 1)) * psum
        else:
            var = 0

        group_info[key] = {'Average' : avg, 'Variance': var}
    return group_info

def edge_latencies(group, tlist):
    """
    assumes all traces in group have exact same structure
    """
    traces = categories[group]
    edge_latencies = {}
    edge_averages = {}
    edge_variance = {}
    for traceid in traces:
        for full_edge in tlist[traceid - 1].fullEdges:
            edge = re.search(r'\d+.\d+ -> \d+.\d+', full_edge).group(0)
            time = re.search(r'(\d+.\d+) us', full_edge).group(1)
            if edge in edge_latencies:
                 edge_latencies[edge].append(time)
            else: 
                edge_latencies[edge] = [time]

    # calculate averages
    for key, values in edge_latencies.items():
        psum = 0
        numvals = len(values)
        for value in values:
            psum += float(value)
        edge_averages[key] = psum / numvals

    # calculate variance
    for key, values in edge_latencies.items():
	if numvals <= 2:
	    edge_variance[key] = 0
	else:
	    psum = 0
	    for value in values:
		avg = edge_averages[key]
		curr = (float(value) - avg) ** 2
		psum += curr
            edge_variance[key] = (1 / float(numvals - 1)) * psum

    print "edges: "
    print edge_latencies

    print "edge averages: "
    print edge_averages

    print "edge variances: "
    print edge_variance
