import json
import sys
from datetime import datetime

ctr = 1

def json_dag(file):
    with open(file, 'r') as data_file:
        #import pdb; pdb.set_trace()
        json_data = json.load(data_file)
        dag = []
 
        def extract_timestamp(element):
            #print "element name is " + element["info"]["name"]
            for key in element["info"].keys():
                if 'meta.raw_payload' in key:
                    if 'start' in key:
                        start = element["info"][key]["timestamp"]
                    elif 'stop' in key:
                        stop = element["info"][key]["timestamp"]
            #import pdb; pdb.set_trace()
            #print "start stop is " + start + stop
            return(start, stop)

        def is_earlier(fst, snd):
            #import pdb; pdb.set_trace()
            t1 = datetime.strptime(fst, "%Y-%m-%dT%H:%M:%S.%f")
            t2 = datetime.strptime(snd, "%Y-%m-%dT%H:%M:%S.%f")

            #print "t1 is %s and t2 is %s." % (str(t1), str(t2))
            #print "it is %s that t1 is earlier than t2" % (str(t1 < t2))
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
            #import pdb; pdb.set_trace()
            concurr = []
            #to do: don't do this twice **************
            if curr is None:
                print "curr is none"
            curr_end = extract_timestamp(curr)[1]
            if rest is not None: # also fix this *******
		for elm in rest:
		    elm_start = extract_timestamp(elm)[0]
		    if is_earlier(elm_start, curr_end):
			concurr.append(elm)
            return concurr
            
        def iterate(lst):
            global ctr
            if len(lst) == 0:
                return
            if len(lst) == 1:
                curr = lst[0]
            else:
                curr = find_earliest(lst)[0]
            #import pdb; pdb.set_trace()
            rest = [x for x in lst if x != curr]

            # maybe don't do this check for a one-item list... ***
            concurrent_elms = find_concurr(curr, rest)

            dag.append(curr["info"]["name"])
            print "appended %s" % str(curr["info"]["name"])

            # add branches of concurrent elements
            if len(concurrent_elms) > 0:
                print "concur elm found"
                for elm in concurrent_elms:
                    dag.append(elm["info"]["name"])
                    rest.remove(elm)
                    if len(elm["children"]) > 0:
                        iterate(elm["children"])

            # check if end of branch
	    if len(curr["children"]) == 0 and len(rest) == 0:
                print "returning from end of branch"
		return

            # traverse children
	    if len(curr["children"]) > 0:
		print "iterating over children"
		iterate(curr["children"])

            # traverse rest of level
	    if len(rest) > 0:
		print "iterating over rest of this level"
		iterate(rest)

    iterate(json_data["children"])
    return dag

filename = sys.argv[1]
print json_dag(filename)
