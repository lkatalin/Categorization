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


# from here: https://github.com/the-gigi/deep/blob/master/deeper.py#L80
def deep_getsizeof(o, ids):
    """Find the memory footprint of a Python object
    This is a recursive function that rills down a Python object graph
    like a dictionary holding nested ditionaries with lists of lists
    and tuples and sets.
    The sys.getsizeof function does a shallow size of only. It counts each
    object inside a container as pointer only regardless of how big it
    really is.
    :param o: the object
    :param ids:
    :return:
    """
    d = deep_getsizeof
    if id(o) in ids:
        return 0

    r = getsizeof(o)
    ids.add(id(o))

    if isinstance(o, str) or isinstance(0, unicode):
        return r

    if isinstance(o, Mapping):
        return r + sum(d(k, ids) + d(v, ids) for k, v in o.iteritems())

    if isinstance(o, Container):
        return r + sum(d(x, ids) for x in o)

    return r


def extract_traces(infile):
    # count traces as they come through
    numtraces = 0
    printtrace = 10
    orig = 10

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
	    (hashv, edges) = hashval(traceObj)
            traceObj.hashval = hashv
            traceObj.edgelst = edges

            # create unique ID based on id of root node
            traceObj.traceId =  gen_traceid(traceObj.dag.id)

	    #place the trace in a group
            add_to_categories(traceObj.hashval, traceObj.response, traceObj.dag, traceObj.traceId, traceObj.edgelst)	    


            #start a new list
            buff = [completeTrace.group(2)]

#            if numtraces == printtrace:
#                size_tobj = sys.getsizeof(traceObj)
#                size_categories = sys.getsizeof(categories)
#
#                deepsize_tobj = deep_getsizeof(traceObj, [id(traceObj)])
#                deepsize_categories = deep_getsizeof(categories, [id(categories)])
#
#                print str(numtraces) + ": size of new object is " + str(size_tobj)
#                print str(numtraces) + ": size of category dict is " + str(size_categories)
#
#                print str(numtraces) + ": deepsize of new object is " + str(deepsize_tobj)
#                print str(numtraces) + ": deepsize of category dict is " + str(size_categories)
#
#                printtrace = printtrace + orig

            numtraces += 1

        else:
            buff.append(line)

    return numtraces
