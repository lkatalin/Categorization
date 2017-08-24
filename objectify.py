import re
from group_traces import *

ids_used = []
ctr = 1

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

class Trace(object):
    '''
    stores the data extracted from one trace.
    '''
    traceName = ""
    mainText = ""
    response = 0
    fullEdges = []
    fullNodes = []
    dag = {}
    hashval = ""
    traceId = 0

    def __init__(self, trace):
        self.traceName = re.search(r'[D|d]igraph \w*', trace)#.group(0)
        self.mainText = trace
        if re.search(r'R: (.*?) usecs', trace) is not None:
            self.response = re.search(r'R: (.*?) usecs', trace).group(1)
        self.fullNodes = re.findall(r'^\s*((?!.* -> .*).*\[.*\])$', trace, re.MULTILINE)
        self.fullEdges = re.findall(r'\S+ -> .+', trace)
        self.dag = dag(self)
        self.hashval = hashval(self)
        self.traceId = gen_traceid(self.dag.id)

def make_trace(trace):
    t = Trace(trace)
    return t
