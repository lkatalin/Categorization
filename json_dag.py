import json
import sys
from datetime import datetime

def json_dag(file):
    with open(file, 'r') as data_file:
        #import pdb; pdb.set_trace()
        json_data = json.load(data_file)
        dag = []

        def extract_timestamp(element):
            for key in element["info"].keys():
                if 'meta.raw_payload' in key:
                    if 'start' in key:
                        start = element["info"][key]["timestamp"]
                    elif 'stop' in key:
                        stop = element["info"][key]["timestamp"]
            return(start, stop)

        def is_earlier(fst, snd):
            t1 = datetime.strptime(fst, "%Y-%m-%dT%H:%M:%S.%f")
            t2 = datetime.strptime(snd, "%Y-%m-%dT%H:%M:%S.%f")
            return(min((t1, t2)) == t1)
        
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
            curr_end = extract_timestamp(curr)[1]
            if rest is not None:
		for elm in rest:
		    elm_start = extract_timestamp(elm)[0]
		    if is_earlier(elm_start, curr_end):
			concurr.append(elm)
            return concurr
            
        def iterate(lst):
            curr = find_earliest(lst)[0]
            #import pdb; pdb.set_trace()
            rest = lst.remove(curr)

            concurrent_elms = find_concurr(curr, rest)
            # if we have concurrenct elements
            if len(concurrent_elms) > 0:
                # deal with it
                pass

            # no concurrency, everything normal
            else:
                dag.append(curr)

                # if it has children, add those next ** DFT **
                if len(curr["children"]) > 0:
                    iterate(curr["children"]) 
                # else process rest of current level
                elif rest is not None:
                    iterate(rest)
                # or come back up
                else:
                    return

    iterate(json_data["children"])
    return dag

filename = sys.argv[1]
print json_dag(filename)
