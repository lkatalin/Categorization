# 2017 Massachusetts Open Cloud Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the
# License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS
# IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied.  See the License for the specific language
# governing permissions and limitations under the License.

import re
from make_dag import dag
from memory_profiler import profile

# groups of traces based on structure
categories = {}
anomaly_types = {'anomalous_groups': {}, 'anomalous_edges': {}, 'high_covar_edges': {}}

def add_to_categories(key, rtime, dag, traceid, edges):
    """
    keys are: hash values of traces.
    values are: a DAG in that group, followed by another
    dict of a trace_id key with a list of edge latencies as 
    values.
    """
    if categories.get(key) is not None:
        categories[key][1].append(rtime)
	categories[key][3][traceid] = edges
    else:
        categories[key] = [dag, [rtime], { traceid : edges}]

def depth_first_traversal(trace):
    """
    The function will traverse the single trace using DFT and create a directed
    acyclic graph with events in order.
    """
    # FIXME: The ordering of events are not identified by logical clock but time
    # stamps kept by osprofler. This means we are dealing potential clock skews.

    #the DFT traverses DAG dict starting with
    #root node; returns a list indicating all
    #nodes seen in order. no duplicates are
    #kept in case of sync and full paths are
    #not kept.

    #from timer import Timer
    nodes = []
    edge_latencies = []
    stack = [trace.dag]
    while stack:
        #with Timer() as t:
        cur_node = stack[0]
        #print "DFT cur node: " + str(cur_node)
        stack = stack[1:]
        #print "rest of stack: " + str(stack)
        if cur_node.name not in nodes: #do not duplicate in case of sync
            nodes.append(cur_node.name)
            if cur_node.latency is not '':
	        edge_latencies.append(cur_node.latency)
            for child in cur_node.get_rev_children():
                stack.insert(0, child)
                #print "=> time of start: %s" % t.start
                
    return (nodes, edge_latencies)

def hashval(trace):
    """
    hashval takes the list generated by DFT and
    creates a string for the hash value
    of each trace (stored in trace object).
    """
    (hashlst, edgelst) = depth_first_traversal(trace)
    trunc = [re.search(r'....$', x).group(0) if len(x) > 3 else x for x in hashlst]

    hashval = "".join(trunc)

    return (hashval, edgelst)

def group_traces(trace):
    add_to_dict(categories, trace.hashval, trace.traceId)

def trace_lookup(tid, tlist):
    for trace in tlist:
        if trace.traceId == tid:
            return trace
    return None

def process_groups(d, tlist):
    """
    calculates the average completion time of
    traces within a group, as well as variance
    of each group.
    """
    group_info = {}

    for hashv, traceids in d.items():
        psum = 0
        #lst = []
        numvals = len(traceids)

        # count edges (uses first trace in group as representative)
        t = trace_lookup(traceids[0], tlist)
        num_edges = len(t.fullEdges)

        # calculate average
        for tid in traceids:
            t = trace_lookup(tid, tlist)
            psum += float(t.response)
            if numvals != 0:
                avg = psum / numvals
            else:
                #throw an error
                pass

        # calculate variance
        psum = 0
        if numvals < 2:
            var = 0
        else:
            for tid in traceids:
                t = trace_lookup(tid, tlist)
                curr = (float(t.response) - avg) ** 2
                psum += curr
                if numvals != 1:
                    var = (1 / float(numvals - 1)) * psum
                else:
                    #throw an error
                    pass
        # random value, can be changed
        if var > 5:
            add_to_dict(anomaly_types["anomalous_groups"], "Groups:", hashv)

        group_info[hashv] = {'Number of edges': num_edges, 'Trace total time average' : avg, 'Trace total time variance': var}
    return group_info
