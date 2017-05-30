# ------------------------------------------------
#             TRACE CATEGORIZATION
#
# this creates a dictionary of trace objects using
# a hash of each trace's list of edges as the key.
# a "category" is a specific set of directed edges.
# data stored for each key includes labels for nodes
# and edges and response times for edges.
# -------------------------------------------------

import os
import re

# read from DOT file (placeholder)
homeDir = os.environ['HOME']
f = open( homeDir + '/Documents/MoC/Monitoring/Categorization/dotfile.txt', 'r')
wholeText=file.read(f)

# create class of trace objects to store trace data
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
    def __init__(self, traceId, traceName, mainText, response, 
    responseTime, labels, edgeLabels, nodeLabels, edges, hashval):
        self.traceId = traceId
        self.traceName = traceName
        self.mainText = mainText
        self.response = response
        self.responseTime = responseTime
        self.labels = labels
        self.edgeLabels = edgeLabels
        self.nodeLabels = nodeLabels
        self.edges = edges
        self.hashval = hashval

# function to create new trace object
def make_trace(traceId, traceName, mainText, response, 
    responseTime, labels, edgeLabels, nodeLabels, edges, hashval):
        trace = Trace(traceId, traceName, mainText, response, 
        responseTime, labels, edgeLabels, nodeLabels, edges, hashval)
        return trace

# break DOT into list of traces
tracesFull = re.findall(r"(?<=')[^']+(?=')", wholeText)
for trace in tracesFull:
    if trace == ' ':
        tracesFull.remove(trace)

# for each trace in list, create trace object holding trace metadata
traceid = 0
tracelist = []

for trace in tracesFull:
    labels = re.findall(r'\"(.*?)\"', trace) 
    traceObj = make_trace( 
    traceid, #traceid
    re.search(r'Digraph \w', trace).group(0), #trace name
    re.search(r'{(.*?)}', trace).group(1), #main text of trace
    re.search(r'R: (.*?) usecs', trace).group(1), #response 
    re.search(r'RT: (.*?) usecs', trace).group(1), #response time
    labels, #labels
    [ label for label in labels if label[0] == 'R' ], #edge labels 
    [ label for label in labels if label[0] != 'R' ], #node labels 
    re.findall(r'\d+\.\d+ -> \d+\.\d+', trace), #edges
    "" #hashvalue TBD
    )
    tracelist.append(traceObj)
    traceid += 1

# MAP edges of each trace to hashval and store in trace object
for trace in tracelist:
    hashval = ""
    for edge in trace.edges:
        n1 = re.search(r'(\d{5}) ->', edge).group(1)
        n2 = re.search(r'.*?(\d{5})$', edge).group(1)
        partial = '-'.join([re.search(r'(\d{5}) ->', 
            edge).group(1), re.search(r'.*?(\d{5})$', edge).group(1)])
        hashval += (partial + '|')
    trace.hashval = hashval

# REDUCE traces into dict with hashval (edges) as keys
# same hashval = same structure = same key = same cateogry
catDict = {}

for trace in tracelist:
    if trace.hashval in catDict:
        catDict[trace.hashval].append(trace)
    else:
        catDict[trace.hashval] = [trace]

# testing
for keys,values in catDict.items():
    print(keys)
    print(values)
    for value in values:
        print value.traceId
