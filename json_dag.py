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
 
        def extract_timestamp(element):
            for key in element["info"].keys():
                if 'meta.raw_payload' in key:
                    if 'start' in key:
                        start = element["info"][key]["timestamp"]
                    elif 'stop' in key:
                        stop = element["info"][key]["timestamp"]
            return(start, stop) # optimize to return immediately if it has both of these ******

        def extract_traceid(element):
            traceid = element["trace_id"]
            return traceid

        def is_earlier(fst, snd):
            t1 = datetime.strptime(fst, "%Y-%m-%dT%H:%M:%S.%f")
            t2 = datetime.strptime(snd, "%Y-%m-%dT%H:%M:%S.%f")
            return(t1 < t2)
        
        def find_earliest(elements):
            earliest = None
            for elm in elements:
                start = extract_timestamp(elm)[0]
                if (earliest == None or is_earlier(start, earliest[1])): 
                    earliest = (elm, start)
            return earliest

        def find_concurr(curr, rest): # move this into collect data?? ****
            if rest is None or curr is None:  # handle this error better ****
                return None
            concurr = []
            #to do: don't do this twice **************
            curr_end = extract_timestamp(curr)[1]
            for elm in rest:
                elm_start = extract_timestamp(elm)[0]
		if is_earlier(elm_start, curr_end):
		    concurr.append(elm)
            return concurr
            
        def collect_data(curr):
            name = curr["info"]["name"]
            service = curr["info"]["service"]
            traceid = extract_traceid(curr)
            (start, stop) = extract_timestamp(curr)
            return (name, service, start, stop, traceid)

        def dot_friendlify(traceid):
            return "a" + traceid.replace("-", "")
        
        # either pass this stuff or define it here but not both ***********
        def iterate(lst, check_join, branch_end_times, prev_traceid=None):
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
                print "just one elm on this level: %s" % lst[0]["info"]["name"] 
                curr = lst[0]
                rest = []
                concurrent_elms = []

            else:
                curr = find_earliest(lst)[0]
                rest = [x for x in lst if x != curr]
                concurrent_elms = find_concurr(curr, rest)

                print "earliest is %s" % curr["info"]["name"]

            if len(concurrent_elms) > 0:
                print "concur elms:"
                for e in concurrent_elms:
                    print e["info"]["name"]

            # track curren branch end time for later synch
            if len(concurrent_elms) > 0 and len(curr["children"]) == 0:
                branch_end_times.append((curr, extract_timestamp(curr)[1]))

            # current node data
            (curr_name, curr_service, curr_start, curr_stop, curr_traceid) = collect_data(curr)

            dcurr_traceid = dot_friendlify(curr_traceid)
            node_list.append((dcurr_traceid, curr_name, curr_service))
            
            # ------------------ CURRENT NODE ------------------------------------
            # SYNCH CASE
            # if previous is concurrent, check where to add edges
            # maybe pass this as prev_traceid?? *********************************
            if check_join == True:
                print "check join is True for %s" % curr_name
                print "len bet is: %d" % len(branch_end_times)
                for (b_elm, b_time) in branch_end_times:
                    # if this branch ended earlier than current elm started
                    # then add an edge
                    if is_earlier(b_time, extract_timestamp(curr)[0]):
                        (b_name, b_service, b_start, b_stop, b_traceid) = collect_data(b_elm)
                        edge_latency = 1.0 #float(vstart) - float(kstop)
                        edge_list.append((dot_friendlify(b_traceid), dcurr_traceid, edge_latency))
                        print "appended node to a multi-branch: %s -> %s" % (b_name, curr_name)

                # then reset check_join and branch_end_times
                # control for two sequential concurrent batches? ****************
                check_join = False
                branch_end_times = []

            # LINEAR CASE
            # only add an edge if it's not the first node
            else:
                if prev_traceid != None:
                    edge_latency = 3.0 #float(vstart) - float(kstop) ********************
                    edge_list.append((prev_traceid, dcurr_traceid, edge_latency))
                    print "appended node to linear branch: %s -> %s" % (str(prev_traceid), curr_name)

            # -------------------- OTHER SAME-LEVEL NODES -------------------------------
            # FAN OUT CASE
            if len(concurrent_elms) > 0:
                for elm in concurrent_elms:
                    # add edges of concurrent elements
                    (e_name, e_service, e_start, e_stop, e_traceid) = collect_data(elm)
                    node_list.append((dot_friendlify(e_traceid), e_name, e_service))

                    print "fan out info for element is:"
                    print e_name + e_service + e_start + e_stop + e_traceid
                    
                    print "adding concurrent elm: %s-%s" % (e_name, e_service)

                    if prev_traceid != None:
                        edge_list.append((prev_traceid, dot_friendlify(e_traceid), 2.0))
                        print "appended node in fan out: %s -> %s" % (prev_traceid, e_name)

                    # don't include these on the level anymore
                    rest.remove(elm)

                    # take care of concurrent branch's children
                    if len(elm["children"]) > 0:
                        print "going down concur branch children for %s-%s" % (e_name, e_service)
                        print "the traceid passed down is!: %s" % e_traceid
                        iterate(elm["children"], check_join, branch_end_times, dot_friendlify(e_traceid))

                    else:
                        branch_end_times.append((elm, extract_timestamp(elm)[1]))
                
                # when processing next nodes on this level, check the join relationship
                # maybe don't toggle this & just pass it? ***************************
                check_join = True

            # ------------------- NEXT RECURSIVE ITERATION --------------------------------
            # check if end of branch
	    if len(curr["children"]) == 0 and len(rest) == 0:
                # keep track of ending times and elements for potential joins
                # make sure this is local to a level and gets reset **************
                branch_end_times.append((curr, extract_timestamp(curr)[1]))
                print "returning from end of branch"
		return

            # traverse children
	    if len(curr["children"]) > 0:
                print "traversing children of current element"
		iterate(curr["children"], check_join, branch_end_times, dcurr_traceid)

            # traverse rest of level
	    if len(rest) > 0:
                print "now traversing rest of level"
		iterate(rest, check_join, branch_end_times, dcurr_traceid)


    # ------------  OVERALL STRUCTURE BEGINS HERE -------------------------------------------
    iterate(json_data["children"], False, [])

    # print DOT format to file
    if len(sys.argv) > 2 and sys.argv[2] == "to-file":
        sys.stdout = open('%s.dot' % json_data["children"][0]["parent_id"], 'w')
 
    print " # 1 R: 0.000000 usecs \nDigraph X {"
    for node in node_list:
        print '\t' + str(node[0]) + ' [label="%s - %s"]' % (str(node[1]), str(node[2]))
    for edge in edge_list:
        print '\t' + edge[0] + ' -> ' + edge[1] + ' [label="%s"]' % str(edge[2])
    print "}"

# ----- CALL FUNCTION -------------------
filename = sys.argv[1]
json_dag(filename)
