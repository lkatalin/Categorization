import json
import sys
from datetime import datetime

def json_dag(file):
    with open(file, 'r') as data_file:
        json_data = json.load(data_file)

        # the graph we are making
        dag = []

        # default for whether to check branch end times; 
        # set to true when coming out of concurrent branches;
        # determines the existence / properties of a join
        check_join = False

        # tracker for branch end times in concurrent cases;
        # this info necessary for joins
        branch_end_times = []

        # for testing
        join_ctr = 0
 
        def extract_timestamp(element):
            for key in element["info"].keys():
                if 'meta.raw_payload' in key:
                    if 'start' in key:
                        start = element["info"][key]["timestamp"]
                    elif 'stop' in key:
                        stop = element["info"][key]["timestamp"]
            return(start, stop)

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
            
        def iterate(lst, check_join):
            if len(lst) == 1:
                curr = lst[0]
            else:
                curr = find_earliest(lst)[0]
            #import pdb; pdb.set_trace()
            rest = [x for x in lst if x != curr]

            if len(rest) == 0:
                concurrent_elms = []
            else:
                concurrent_elms = find_concurr(curr, rest)

            # check if this may be a join
            if check_join == True:
                # check where to append the thing
                edges = []
                for (elm, time) in branch_end_times:
                    if is_earlier(time, extract_timestamp(curr)[0]):
                        edges.append(elm)
                        #add edge to DAG from elm to curr ************
                        pass
                if len(edges) < 1:
                    print "ERROR: join cannot be created for %s" % str(curr["info"]["name"])

                # then reset check_join
                check_join = False

            dag.append(curr["info"]["name"])
            print "appended %s" % str(curr["info"]["name"])

            # add branches of concurrent elements
            if len(concurrent_elms) > 0:
                print "concur elm found"
 

                for elm in concurrent_elms:
                    dag.append(elm["info"]["name"])
                    rest.remove(elm)
                    if len(elm["children"]) > 0:
                        iterate(elm["children"], check_join)

                # create a marker that first elm of "rest" is potential join
                # concurrent elms have been removed from "rest" at this point
                #
                # if on this level, we have concurrent elements, then when we
                # get through the concurrent elements, we should check if the next
                # item on this level is a join
                check_join = True
                #join_ctr += 1

            # check if end of branch
	    if len(curr["children"]) == 0 and len(rest) == 0:
                # keep track of ending times and elements for potential joins
                branch_end_times.append((extract_traceid(curr), extract_timestamp(curr)[1]))

                print "returning from end of branch"
		return

            # traverse children
	    if len(curr["children"]) > 0:
		print "iterating over children"
		iterate(curr["children"], check_join)

            # traverse rest of level
	    if len(rest) > 0:
		print "iterating over rest of this level"
		iterate(rest, check_join)

    iterate(json_data["children"], check_join)
    return dag

filename = sys.argv[1]
print json_dag(filename)
