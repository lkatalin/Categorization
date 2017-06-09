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

print "\n........................"
print "\n| Relevant trace info: |"
print "........................\n"
for trace in tracelist:
    print "TraceId: %d" % trace.traceId
    print "Trace name: %s" % trace.traceName
    print "Hashval: %s" % trace.hashval
    print "\nAll paths for %s: " % trace.traceName 
    print trace.allpaths
    print "\n"

print "\nEdge latency info: \n"
for trace in tracelist:
    print "\nTrace %d:" % trace.traceId
    ctr = 0
    for edge in trace.edges:
        print "Edge %d: " % ctr
        print edge
        print "Latency: %s" % trace.edgeLabels[ctr]
        ctr += 1
