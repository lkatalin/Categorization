import json
import sys
from datetime import datetime

def json_dag(file):
    with open(file, 'r') as data_file:
        json_data = json.load(data_file)

        # edge list as [traceid -> traceid]
        edge_list = []

        # node list as [(traceid, name, service)]
        node_list = []

        # for testing
        join_ctr = 0
 
        def extract_timestamp(element):
            for key in element["info"].keys():
                if 'meta.raw_payload' in key:
                    if 'start' in key:
                        start = element["info"][key]["timestamp"]
                    elif 'stop' in key:
                        stop = element["info"][key]["timestamp"]
            return(start, stop) # optimize to return immediately if it has both of these ******

        def extract_traceid(element):
            for key in element["info"].keys():
                if 'meta.raw_payload' in key:
                    traceid = element["info"][key]["trace_id"]
                    return traceid
            return None

        def is_earlier(fst, snd):
            t1 = datetime.strptime(fst, "%Y-%m-%dT%H:%M:%S.%f")
            t2 = datetime.strptime(snd, "%Y-%m-%dT%H:%M:%S.%f")
            return(t1 < t2)
        
        def find_earliest(elements):
            # earliest = (element, its start time)
            earliest = (None, None)
            for elm in elements:
                start = extract_timestamp(elm)[0]
                if (earliest == (None, None)) or is_earlier(start, earliest[1]): 
                    earliest = (elm, start)
            return earliest

        def find_concurr(curr, rest):
            concurr = []
            #to do: don't do this twice **************
            if curr is None:
                print "curr is none"
            curr_end = extract_timestamp(curr)[1]
            if rest is not None: # take this out bc now there's a check
		for elm in rest:
		    elm_start = extract_timestamp(elm)[0]
		    if is_earlier(elm_start, curr_end):
			concurr.append(elm)
            return concurr
            
        def collect_data(data):
            #import pdb; pdb.set_trace()
            name = data["info"]["name"]
            service = data["info"]["service"]
            start = data["info"]["started"]
            stop = data["info"]["finished"]
            time = extract_timestamp(data)
            start_stamp = time[0]
            stop_stamp = time[1]
            return (name, service, start, stop, start_stamp, stop_stamp)

        # default for whether to check branch end times; 
        # set to true when coming out of concurrent branches;
        # use when last elements on same level were concurrent batch

        # tracker for branch end times in concurrent cases;
        
        def iterate(lst, check_join, branch_end_times):
	    '''
	    lst = elements left to process on current level (where a level is a group
		  of spans that share a parent in the span model)
	    check_join = True or False indicating whether to check which branches
			 to append current item to; default is False unless previous 
			 elements on the level were concurrent
	    branch_end_times = keeps track of end timestamps of all end nodes in case
			 of concurrency, to be used when checking join relationships
	    '''
            if len(lst) == 1:
                curr = lst[0]
                rest = []
                concurrent_elms = []

            else:
                curr = find_earliest(lst)[0]
                rest = [x for x in lst if x != curr]
                concurrent_elms = find_concurr(curr, rest)

            if check_join == True:
                for (elm, time) in branch_end_times:
                    # if this branch ended earlier than current elm started
                    # then add an edge
                    if is_earlier(time, extract_timestamp(curr)[0]):
                        (vname, vservice, vstart, vstop, vstart_stamp, 
                                           vstop_stamp) = collect_data(elm)
                        edge_latency = 1.0 #float(vstart) - float(kstop)
                        edge_list.append((kstart_stamp, vstart_stamp, 
                                                            edge_latency))

                # then reset check_join and branch_end_times
                check_join = False
                branch_end_times = []

            # node data 
            (kname, kservice, kstart, kstop, kstart_stamp, 
                                       kstop_stamp) = collect_data(curr)
            node_list.append((kstart_stamp, kname, kservice))

            # add curr into edges
            (vname, vservice, vstart, vstop, vstart_stamp, 
                                           vstop_stamp) = collect_data(curr)

            edge_latency = 1.0 #float(vstart) - float(kstop) ********************
            edge_list.append((kstart_stamp, vstart_stamp, edge_latency))

            print "appended %s" % str(curr["info"]["name"])

            # add branches of concurrent elements
            if len(concurrent_elms) > 0:
                print "concur elm found"
 

                for elm in concurrent_elms:
                    dag.append(elm["info"]["name"])
                    rest.remove(elm)
                    if len(elm["children"]) > 0:
                        iterate(elm["children"], check_join)

                # important: concurrent elms have been removed from "rest" at this point
                #
                # check_join is true if next "earliest" item on this level
                # potentially needs to be joined to several branches
                # depending on happens-before relationship (determined by timestamp)

                check_join = True
                #join_ctr += 1

            # check if end of branch
	    if len(curr["children"]) == 0 and len(rest) == 0:
                # keep track of ending times and elements for potential joins

                # this should be local to a level and needs to get reset **************
                branch_end_times.append((extract_traceid(curr), extract_timestamp(curr)[1]))

                print "returning from end of branch"
		return

            # traverse children
	    if len(curr["children"]) > 0:
		print "iterating over children"
		iterate(curr["children"], check_join, branch_end_times)

            # traverse rest of level
	    if len(rest) > 0:
		print "iterating over rest of this level"
		iterate(rest, check_join, branch_end_times)

    iterate(json_data["children"], False, [])

    # print DOT format to file
    if len(sys.argv) > 2 and sys.argv[2] == "to-file":
        sys.stdout = open('%s.dot' % trace_id, 'w')
 
    print "' # RT: 0.000000 usecs Digraph X {"
    for node in node_list:
        print '\t' + str(node[0]) + ' [label="%s - %s"]' % (str(node[1]), str(node[2]))
    for edge in edge_list:
        print '\t' + edge[0] + ' -> ' + edge[1] + ' [label="%s"]' % str(edge[2])
    print "}'"

filename = sys.argv[1]
json_dag(filename)
