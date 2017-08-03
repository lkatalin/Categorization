import json
import sys
from datetime import datetime

# TO DO:
# - control for two sequential concurrent batches
# - handle two starting elements (fan out at beginning)
# - only toggle or only pass check_join?

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
            
        def collect_data(curr):
            name = curr["info"]["name"]
            service = curr["info"]["service"]
            traceid = curr["trace_id"]
            (start, stop) = extract_timestamp(curr)
            return (name, service, start, stop, traceid)

        def dot_friendlify(traceid):
            return "a" + traceid.replace("-", "")
        
        # either pass this stuff or define it here but not both ***********
        def iterate(lst, check_join, branch_ends, prev_traceid=None, prev_stop=None):
	    '''
	    lst = elements left to process on current level
	    check_join = False unless prev elements on this level were concurrent
	    branch_ends = [(element, end_time)] tracked in case of fan out
            prev_traceid = where to attach current node in linear case
	    '''
            if len(lst) == 1:
                curr = lst[0]
                rest = []
                concurrent_elms = []

            else:
                curr = find_earliest(lst)[0]
                rest = [x for x in lst if x != curr]

            # current node data
            (curr_name, curr_service, curr_start, curr_stop, curr_traceid) = collect_data(curr)

            # because apparently DOT can't handle alphanumeric traceids
            dcurr_traceid = dot_friendlify(curr_traceid)

            # determine if any concurrency with current element
            concurrent_elms = find_concurr(curr_stop, rest)

            # if curr has no children, track end time for later synch
            if len(concurrent_elms) > 0 and len(curr["children"]) == 0:
                branch_ends.append((curr, extract_timestamp(curr)[1]))

            # add curr to nodes whether synch or linear
            node_list.append((dcurr_traceid, curr_name, curr_service))
            
            # ----------------- ATTACH CURRENT NODE ------------------------------------
            # SYNCH CASE : check for sequential relationship to add edges
            if check_join == True:
                for (b_elm, b_end) in branch_ends:
                    # add edge if branch ended before curr started
                    if is_earlier(b_end, extract_timestamp(curr)[0]):
                        (b_name, b_service, b_start, b_stop, b_traceid) = collect_data(b_elm)
                        edge_latency = find_latency(b_end, curr_start)
                        edge_list.append((dot_friendlify(b_traceid), dcurr_traceid, edge_latency))

                # reset params
                check_join = False
                branch_ends = []

            # LINEAR CASE : only add edge if curr is not first / base node
            else:
                if prev_traceid != None and prev_stop != None:
                    edge_latency = find_latency(prev_stop, curr_start)
                    edge_list.append((prev_traceid, dcurr_traceid, edge_latency))

            # -------------------- CHECK FOR FAN OUT  -------------------------------
            if len(concurrent_elms) > 0:
                for elm in concurrent_elms:

                    # add node
                    (e_name, e_service, e_start, e_stop, e_traceid) = collect_data(elm)
                    node_list.append((dot_friendlify(e_traceid), e_name, e_service))

                    # add edge if not first / base node
                    if prev_traceid != None:
                        edge_latency = find_latency(prev_stop, e_start)
                        edge_list.append((prev_traceid, dot_friendlify(e_traceid), edge_latency))

                    # don't process concurrent elements twice
                    rest.remove(elm)

                    # traverse concurrent branch's children
                    if len(elm["children"]) > 0:
                        iterate(elm["children"], check_join, branch_ends, dot_friendlify(e_traceid), e_stop)

                    # or track end time for future synch
                    else:
                        branch_ends.append((elm, extract_timestamp(elm)[1]))
                
                # check branch end times when attaching next node on same level
                check_join = True

            # ---------------------------- RECURSE -----------------------------------
            # check if end of branch
	    if len(curr["children"]) == 0 and len(rest) == 0:
                branch_ends.append((curr, extract_timestamp(curr)[1]))
		return

            # traverse any children
	    if len(curr["children"]) > 0:
		iterate(curr["children"], check_join, branch_ends, dcurr_traceid, curr_stop)

            # traverse rest of level
	    if len(rest) > 0:
		iterate(rest, check_join, branch_ends, dcurr_traceid, curr_stop)


    # BEGIN CALL
    iterate(json_data["children"], False, [])

    # OUTPUT 
    # check to-file flag
    if len(sys.argv) > 2 and sys.argv[2] == "to-file":
        sys.stdout = open('%s.dot' % json_data["children"][0]["parent_id"], 'w')
 
    print " # 1 R: 0.000000 usecs \nDigraph X {"
    for node in node_list:
        print '\t' + str(node[0]) + ' [label="%s - %s"]' % (str(node[1]), str(node[2]))
    for edge in edge_list:
        print '\t' + edge[0] + ' -> ' + edge[1] + ' [label="%s"]' % str(edge[2])
    print "}"


filename = sys.argv[1]
json_dag(filename)
