import re
from group_traces import *

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
        self.fullNodes = re.findall(r'\d+.\d+ \[label="(?!R\:).*"\]', trace)
        self.fullEdges = re.findall(r'\d+.\d+ -> .*]', trace)
        self.dag = dag(self)
        self.hashval = hashval(self)

def make_trace(trace, traceId):
    trace = Trace(trace, traceId)
    return trace
