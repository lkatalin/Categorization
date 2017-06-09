import re
from hashval import *

#create the class of trace objects to store trace data
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
    hashval = ""

    # construct trace class
    def __init__(self, trace, traceId):
        self.traceId = traceId
        self.traceName = re.search(r'Digraph \w', trace).group(0)
        self.mainText = trace
        self.response = re.search(r'R: (.*?) usecs', trace).group(1)
        self.responseTime = re.search(r'RT: (.*?) usecs', trace).group(1)
        self.labels = re.findall(r'\"(.*?)\"', trace)
        self.edgeLabels = [ label for label in self.labels if label[0] == 'R' ]
        self.nodeLabels = [ label for label in self.labels if label[0] != 'R' ]
        self.edges = re.findall(r'\d+\.\d+ -> \d+\.\d+', trace)
        self.fullEdges = re.findall(r'\d+.\d+ -> .*]', trace)
        self.dag = dag(self)
        self.allpaths = all_paths(self)
        self.hashval =  hashval(self)

def make_trace(trace, traceId):
    trace = Trace(trace, traceId)
    return trace
