import re
import numpy as np
from make_dag import *
from decimal import *
from datetime import datetime
from datetime import timedelta

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
    from timer import Timer
    nodes = []
    stack = [trace.dag]
    while stack:
	with Timer() as t:
	    cur_node = stack[0]
	    stack = stack[1:]
	    if cur_node.id not in nodes: #do not duplicate in case of sync
		nodes.append(cur_node.id)
	    for child in cur_node.get_rev_children():
		stack.insert(0, child)
	    #print "=> time of start: %s" % t.start
    return nodes 

def hashval(trace):
    """
    hashval takes the list generated by DFT and 
    creates a meaningful string for the hash value
    of each trace (stored in trace object).
    """
    lst = depth_first_traversal(trace)
    trunc = [re.search(r'....$', x).group(0) for x in lst]
    hashval = "".join(trunc)
    #hashval = "".join(re.findall(r'(\d)\.1', "".join(depth_first_traversal(trace))))
    #hashval = "".join(re.findall(r'.(\d+)', "".join(depth_first_traversal(trace))))
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

def trace_lookup(tid, tlist):
    for trace in tlist:
        if trace.traceId == tid:
            return trace
    return none

def process_groups(d, tlist):
    """
    calculates the average completion time of
    traces within a group, as well as variance 
    of each group.
    """
    group_info = {}

    for hashv, traceids in d.items():
        psum = 0
        lst = []
        numvals = len(traceids)
 
        # calculate average
        for tid in traceids:
            t = trace_lookup(tid, tlist)
            psum += float(t.response)
        avg = psum / numvals
        
        # calculate variance
        psum = 0
        for tid in traceids:
            t = trace_lookup(tid, tlist)
            curr = (float(t.response) - avg) ** 2            
            psum += curr
        if (numvals - 1) > 1:
            var = (1 / float(numvals - 1)) * psum
        else:
            var = 0

        group_info[hashv] = {'Average' : avg, 'Variance': var}
    return group_info

        


def edge_latencies(group, tlist):
    """
    creates key-value pairs of edge : [list of latencies found for edge]
    in one group;
    returns this list, a list of average latencies per edge, and a list 
    of variance per edge;
    variance calculated in microseconds
    ...
    ** assumes all traces in group have exact same structure **
    ...
    possibly, we could group the edges by label instead of tid -> tid,
    which would give us more data per edge
    """
    traces = categories[group]
    edge_latencies = {}
    edge_averages = {}
    edge_variance = {}
    for traceid in traces:
        t = trace_lookup(traceid, tlist)
        for full_edge in t.fullEdges:
            #edge = re.search(r'(\d+.* -> \d+.*) \[', full_edge).group(1)
            #time = re.search(r'label="(.*)"', full_edge).group(1)
            edge = re.search(r'(.* -> .*) \[', full_edge).group(1)
            time = re.search(r'label=\"(.+)\"', full_edge).group(1)
            if edge in edge_latencies:
                edge_latencies[edge].append(time)
            else: 
                edge_latencies[edge] = [time]

    # calculate averages
    for key, values in edge_latencies.items():

        # baseline
        psum = timedelta(hours=0, minutes=0, seconds=0, microseconds=0)
        numvals = len(values)

        for value in values:
            # sum up all latencies in this group
            dateval = datetime.strptime(value, "%H:%M:%S.%f").time()
            deltaval = timedelta(hours=dateval.hour, minutes=dateval.minute, 
                       seconds=dateval.second, microseconds=dateval.microsecond)
            psum += deltaval

        avg = psum / numvals
        edge_averages[key] = avg
        #print "edge average is: " + str(edge_averages[key])

    # calculate variance
    '''
    in microseconds
    '''
    for key, values in edge_latencies.items():
	if numvals < 2:
	    edge_variance[key] = 0
	else:
	    psum = 0
            print "now on edge " + str(key)
	    for value in values:
                print "value: " + str(value)
                dateval = datetime.strptime(value, "%H:%M:%S.%f").time()
		avg = edge_averages[key]
                print "avg:" + str(avg)
                fval = float((dateval.hour * 3600000000) + (dateval.minute * 60000000) + (dateval.second * 1000000) + dateval.microsecond)
                print "value turns into " + str(fval)
                favg = float((avg.seconds * 1000000) + avg.microseconds)
                print "avg turns into " + str(favg)
		curr = (fval - favg) ** 2
		psum += curr
                print "total is..." + str(psum)
            #edge_variance[key] = (1 / float(numvals - 1)) * psum
            edge_variance[key] = (1 / float(numvals)) * psum

        print "edge variance is: " + str(edge_variance[key]) + " microseconds\n"

    #print "edges in group: "
    #print edge_latencies

    return (edge_latencies, edge_averages, edge_variance)


def cov_matrix(e_lat_dict, tlist):
    """
    returns covariance matrix for each pair of edges within a group.
    """
    if len(tlist) == 1:
        print "\ntoo few data points to create covariance matrix \n"
    else:
        lat_array = np.array([e_lat_dict[k] for k in e_lat_dict]).astype(np.float)
        print "\n array of latencies in group per edge: \n" 
        print  lat_array
	matrix = np.cov(lat_array)
        print "\n covariance matrix for group: \n"
	print matrix
	print "\n"
        return matrix
