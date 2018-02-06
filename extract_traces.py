import re
import sys
from objectify import *
from group_traces import *

def gen_traceid(base):
    ''' 
    generates traceId for a trace object. traceId is
    either the base_id of the trace, based on the root
    node of DAG (created in make_dag.py), or it is the
    base_id plus a numerical suffix if that base_id
    has already been used by another trace.
    '''
    global ctr 
    if base in ids_used:
        new_base = base + "_%03d" % ctr 
        ids_used.append(new_base)
        ctr += 1
        return new_base
    else:
        ids_used.append(base)
        return base


def extract_traces(infile):
    # count traces as they come through
    numtraces = 0

    # collects text until complete trace is read in
    buff = []
   
    for line in infile:

        #parse line to see if end of trace
        completeTrace = re.search(r'(.*?})(.*?)$', line)

        #if end, add last part to buffer and create trace object
        if completeTrace:

            buff.append(completeTrace.group(1))
            traceObj = make_trace("".join(buff))
            traceObj.dag = dag(traceObj)
               
            # only traverse dag once in DFT to get both hashval and edge list
	    #(hashv, edges) = hashval(traceObj)
            #traceObj.hashval = hashv
            #traceObj.edgelst = edges

            # create unique ID based on id of root node
            traceObj.traceId =  gen_traceid(traceObj.dag.id)


	    #place the trace in a group
            add_to_categories(traceObj.hashval, traceObj.response, traceObj.dag, traceObj.traceId, traceObj.edgelst)	    

            #start a new list
            buff = [completeTrace.group(2)]

            numtraces += 1

        else:
            buff.append(line)

    return numtraces
