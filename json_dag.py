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
            print "we are on level %d" % ctr
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
            # if we have concurrenct elements
            if len(concurrent_elms) > 0:
                # deal with it ***********************
                for elm in concurrent_elms:
                    dag.append(elm["info"]["name"])

            # no concurrency, everything normal
            else:
                dag.append(curr["info"]["name"])

                if len(curr["children"]) == 0 and len(rest) == 0:
                    return

                elif len(curr["children"]) > 0:
                    print "iterating over children"
                    iterate(curr["children"])

                if len(rest) > 0:
                    print "iterating over rest of this level"
                    iterate(rest)


    iterate(json_data["children"])
    return dag

filename = sys.argv[1]
print json_dag(filename)
