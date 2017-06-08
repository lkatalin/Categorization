from sys import argv
from simple_dag import *
from extract_traces import *
from print_stuff import *
from group_traces import *

filename = argv[1]

# EXTRACT TRACES
with open(filename) as infile:
        tracelist = extract_traces(infile)

# GROUP TRACES
for trace in tracelist:
    group_traces(trace)

# OUTPUT INFO FOR HUMAN
print "\nInfo dump about current traces: \n"

key_counter = 0
for key in categories.keys():
    key_counter += 1

print "Number of traces: %d" % len(tracelist)
print "Number of categories: %d" % key_counter
print "Category names: "

for key in categories.keys():
    print key

print "\nRelevant trace info: \n"
for trace in tracelist:
    print "TraceId: %d" % trace.traceId
    print "Hashval: %s" % trace.hashval
    print "\nAll paths: " 
    print trace.allpaths

print "\nEdge latency info: \n"
for trace in tracelist:
    ctr = 0
    for edge in trace.edges:
        print "Edge %d: " % ctr
        print edge
        print "Latency: %s" % trace.edgeLabels[ctr]
        ctr += 1
