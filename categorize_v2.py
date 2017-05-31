from sys import argv
from dag import *
from testing import *
from extract_trace import *

filename = argv[1]

# EXTRACT TRACES
with open(filename) as infile:
        tracelist = extract_traces(infile)


# GROUP TRACES
# to do


# TESTING
trace_test(tracelist)

# create dag for each trace
daglist = []
print "dags: "
for trace in tracelist:
    graph = dag(trace)
    daglist.append(graph)

for dag in daglist:
    print_tree(dag)

#first node label is call and end is reply
# make sure each has a reply
