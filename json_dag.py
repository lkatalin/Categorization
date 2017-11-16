import json
import sys
import os
from datetime import datetime
from make_nodes import *

# TO DO:
# - control for two sequential concurrent batches
# - handle two starting elements (fan out at beginning)
# - only toggle or only pass check_join?
# - what's up with negative latencies?

def json_dag(file):
    '''
    converts a span-model, JSON-format trace into
    a DAG-model, DOT-format trace showing concurrency
    '''
    with open(file, 'r') as data_file:
        json_data = json.load(data_file)

        # edge list as [traceid -> traceid]
        edge_list = []

        # node list as [(traceid, name, service)]
        node_list = []
 
        def extract_timestamp(element):
            for key in element["info"].keys():
                if 'meta.raw_payload' in key:
                    if 'start' in key:
                        start = element["info"][key]["timestamp"]
                        if 'stop' in locals():
                            return (start, stop)
                    elif 'stop' in key:
                        stop = element["info"][key]["timestamp"]
                        if 'start' in locals():
                            return (start, stop)

        def is_earlier(fst, snd):
            t1 = datetime.strptime(fst, "%Y-%m-%dT%H:%M:%S.%f")
            t2 = datetime.strptime(snd, "%Y-%m-%dT%H:%M:%S.%f")
            return(t1 < t2)
        
        def find_latency(fst, snd):
            t1 = datetime.strptime(fst, "%Y-%m-%dT%H:%M:%S.%f")
            t2 = datetime.strptime(snd, "%Y-%m-%dT%H:%M:%S.%f")
            return(t2 - t1)

        def find_earliest(elements):
            for elm in elements:
                start = extract_timestamp(elm)[0]
                if ('earliest' not in locals() or is_earlier(start, earliest[1])): 
                    earliest = (elm, start)
            return earliest

        def find_concurr(curr_stop, rest):
            concurr = []
            for elm in rest:
                elm_start = extract_timestamp(elm)[0]
		if is_earlier(elm_start, curr_stop):
		    concurr.append(elm)
            return concurr 

        def get_start_node(curr):
            start_node = Node(curr["info"]["name"] + ":" + curr["info"]["service"] + ":START")
            start_node.id = dot_friendlify(curr["trace_id"])
            start_node.timestamp = extract_timestamp(curr)[0] 
            start_node.corresp_end_node = get_end_node(curr)
            return start_node

        def get_end_node(curr):
            end_node = Node(curr["info"]["name"] + ":" + curr["info"]["service"] + ":END")
            end_node.id = dot_friendlify(curr["trace_id"]) + "_E"
            end_node.timestamp = extract_timestamp(curr)[1]
            corresp_start_node = None # add this outside of fxn call to avoid loop
            return end_node

        def dot_friendlify(traceid):
            return "a" + traceid.replace("-", "")
        
        # either pass this stuff or define it here but not both ***********
        def iterate(lst, check_join, branch_ends, prev_node=None, prev_end_time=None):
	    '''
	    lst = elements left to process on current level
	    check_join = False unless prev elements on this level were concurrent
	    branch_ends = [(element, end_time)] tracked in case of fan out
            prev_traceid = where to attach current node in linear case
	    '''

#            print "---------- REPORT ------------"
#            print "current list is "
#            for item in lst:
#                print item["info"]["name"]
#            print "check join is " + str(check_join)
#            print "branch ends are "
#            for end in branch_ends:
#                print end[0]["info"]["name"]
#            print "prev_node = " + str(prev_node) + " and prev_end_time = " + str(prev_end_time)
#            print "\n"

            if len(lst) == 1:
                curr = lst[0]
                rest = []
                concurrent_elms = []

            else:
                curr = find_earliest(lst)[0]
                rest = [x for x in lst if x != curr]

            # create connected start and end nodes for current span
            curr_start = get_start_node(curr)
            curr_end = curr_start.corresp_end_node
            curr_end.corresp_start_node = curr_start

            # determine if any concurrency with current element
            concurrent_elms = find_concurr(curr_end.timestamp, rest)

            # if curr has no children, track end time for later synch
            # ... because otherwise its children might be the end instead
            if len(concurrent_elms) > 0 and len(curr["children"]) == 0:
                branch_ends.append((curr, curr_end.timestamp))
                
            # add curr START to nodes whether synch or linear 
            node_list.append(curr_start)
            
            # ----------------- ATTACH CURRENT NODE ------------------------------------
            # SYNCH CASE : check for sequential relationship to add edges
            if check_join == True:
                for (b_elm, b_end) in branch_ends:
                    # add edge if branch ended before curr started
                    if is_earlier(b_end, curr_start.timestamp):
                        b_start = get_start_node(b_elm)
                        b_end = b_start.corresp_end_node
                        b_end.corresp_start_node = b_start

                        edge_latency = find_latency(b_end.timestamp, curr_start.timestamp)
                        edge_list.append((b_end.id, curr_start.id, edge_latency))

                # reset params
                check_join = False
                branch_ends = []

            # LINEAR CASE : only add edge if curr is not first / base node
            else:
                if prev_node != None and prev_end_time != None:
                    edge_latency = find_latency(prev_end_time, curr_start.timestamp)
                    edge_list.append((prev_node.id, curr_start.id, edge_latency))

            # -------------------- CHECK FOR FAN OUT  -------------------------------
            if len(concurrent_elms) > 0:
                #print "our current elm is " + str(curr_start) + " and its concurr elms are: "
                
                for elm in concurrent_elms:
 
                    # add node
                    e_start = get_start_node(elm)
                    e_end = e_start.corresp_end_node
                    e_end.corresp_start_node = e_start

                    node_list.append(e_start)

                    # add edge if not first / base node
                    if prev_node != None:
                        edge_latency = find_latency(prev_end_time, e_start.timestamp)
                        edge_list.append((prev_node.id, e_start.id, edge_latency))

                    # don't process concurrent elements twice
                    rest.remove(elm)

                    # traverse concurrent branch's children
                    if len(elm["children"]) > 0:
                        iterate(elm["children"], check_join, branch_ends, e_start, e_end.timestamp)

                    # or track end time for future synch if no children can push end time later
                    #else:
                    branch_ends.append((elm, e_end.timestamp))
 
                    ## after children: cap it no matter what! and then add to branch_ends
                    most_recent = node_list[len(node_list) - 1]

                    node_list.append(e_end)
                    edge_latency = find_latency(most_recent.timestamp, curr_end.timestamp)
                    edge_list.append((most_recent.id, e_end.id, edge_latency))
 
                # check branch end times when attaching next node on same level
                
                check_join = True

            # ---------------------------- RECURSE -----------------------------------
            # traverse any children
	    if len(curr["children"]) > 0:
		iterate(curr["children"], check_join, branch_ends, curr_start, curr_start.timestamp)
 
            if (len(concurrent_elms) > 0):
                most_recent = curr_start

            else:
                # find most recently appended node
                most_recent = node_list[len(node_list) - 1]

            # cap
            node_list.append(curr_end)
            edge_latency = find_latency(most_recent.timestamp, curr_end.timestamp)
            edge_list.append((most_recent.id, curr_end.id, edge_latency))

            # traverse rest of level
	    if len(rest) > 0:
		iterate(rest, check_join, branch_ends, curr_end, curr_end.timestamp)
            
            return

    # BEGIN CALL
    total_time = json_data["info"]["finished"]
    iterate(json_data["children"], False, [])

    # OUTPUT 
    # check to-file flag
    if len(sys.argv) > 2 and sys.argv[2] == "to-file":
        directory = sys.argv[1].rsplit('/', 1)[0]
        output_file = '%s.dot' % json_data["children"][0]["parent_id"]
        output = open(os.path.join(directory, output_file),'w')
        sys.stdout = output
 
    print " # 1 R: %d usecs \nDigraph {" % total_time
    for node in node_list:
        print '\t' + node.id + ' [label="%s"]' % node.name
    for edge in edge_list:
        print '\t' + edge[0] + ' -> ' + edge[1] + ' [label="%s"]' % str(edge[2])
    print "}"

try:
    filename = sys.argv[1]
    json_dag(filename)
except KeyError:
    print "error: could not find filename for command with argv: %s" % sys.argv
    sys.exit()
