import re
from group_traces import *

ids_used = []
ctr = 1

def gen_traceid(base):
    global ctr
    if base in ids_used:
        new_base = base + "_%03d" % ctr
        ids_used.append(new_base)
        ctr += 1
        return new_base
    else:
        ids_used.append(base)
        return base

# each trace object will store data for one trace
class Trace(object):
    traceId = 0
    traceName = ""
    mainText = ""
    response = 0
    responseTime = 0
    labels = []
    edgeLabels = []
    nodeLabels = []
    edges = []
    fullEdges = []
    dag = {}
    hashval = ""

    def __init__(self, trace):
        #self.traceId = gen_traceid(re.search(r'# (.*) R:', trace).group(1))
        self.traceName = re.search(r'Digraph \w*', trace).group(0)
        self.mainText = trace
        self.response = re.search(r'R: (.*?) usecs', trace).group(1)
        #self.responseTime = re.search(r'RT: (.*?) usecs', trace).group(1)
        self.labels = re.findall(r'\"(.*?)\"', trace)
        self.edgeLabels = [ label for label in self.labels if (label[0].isdigit() or label[0] == '-')]
        self.nodeLabels = [ label for label in self.labels if not (label[0].isdigit() or label[0] == '-')]
        #self.fullNodes = re.findall(r'[^(\d+ -> \w*)](\d+[-*:*\w*\.*]*\s\[.+\])', trace)
        # below is for DOTs that came out of OSP span JSONs
        self.fullNodes = re.findall(r'^\s*((?!.* -> .*).*\[.*\])$', trace, re.MULTILINE)
        self.fullEdges = re.findall(r'\S+ -> .+', trace)
        self.edges = re.findall(r'.+ -> .+ ([^\s]*).*', trace)
        self.dag = dag(self)
        self.traceId = gen_traceid(self.dag.id)
        self.hashval = hashval(self)


        # FOR SPECTROSCOPE VERSION
        #self.edges = re.findall(r'\d+\.\d+ -> \d+\.\d+', trace)
        #self.edgeLabels = [ label for label in self.labels if label[0] == 'R' ]
        #self.nodeLabels = [ label for label in self.labels if label[0] != 'R' ]
        #self.fullNodes = re.findall(r'\d+.\d+ \[label="(?!R\:).*"\]', trace)
        #self.fullEdges = re.findall(r'\d+.\d+ -> .*]', trace)

def make_trace(trace):
    t = Trace(trace)
    return t
