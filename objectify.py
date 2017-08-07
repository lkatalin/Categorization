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

    def __init__(self, trace):
        self.traceId = re.search(r'# (.*) R:', trace).group(1)
        self.traceName = re.search(r'Digraph \w', trace).group(0)
        self.mainText = trace
        self.response = re.search(r'R: (.*?) usecs', trace).group(1)
        #self.responseTime = re.search(r'RT: (.*?) usecs', trace).group(1)
        self.labels = re.findall(r'\"(.*?)\"', trace)
        self.edgeLabels = [ label for label in self.labels if (label[0].isdigit() or label[0] == '-')]
        self.nodeLabels = [ label for label in self.labels if not (label[0].isdigit() or label[0] == '-')]
        #self.fullNodes = re.findall(r'[^(\d+ -> \w*)](\d+[-*:*\w*\.*]*\s\[.+\])', trace)
        self.fullEdges = re.findall(r'\d+.* -> .+', trace)
        self.edges = re.findall(r'.+ -> .+ ([^\s]*).*', trace)
        #self.dag = dag(self)
        #self.hashval = hashval(self)

        # for DOTs that came out of OSP span JSONs
        self.fullNodes = re.findall(r'^\s*((?!.* -> .*).*\[.*\])$', trace, re.MULTILINE)

        # FOR SPECTROSCOPE VERSION
        #self.edges = re.findall(r'\d+\.\d+ -> \d+\.\d+', trace)
        #self.edgeLabels = [ label for label in self.labels if label[0] == 'R' ]
        #self.nodeLabels = [ label for label in self.labels if label[0] != 'R' ]
        #self.fullNodes = re.findall(r'\d+.\d+ \[label="(?!R\:).*"\]', trace)
        #self.fullEdges = re.findall(r'\d+.\d+ -> .*]', trace)

def make_trace(trace):
    t = Trace(trace)
    return t
