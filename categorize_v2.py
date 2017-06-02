from sys import argv
from simple_dag import *
from testing import *
from extract_traces import *
from print_stuff import *

filename = argv[1]

# EXTRACT TRACES
with open(filename) as infile:
        tracelist = extract_traces(infile)


# GROUP TRACES
# to do


# TESTING
trace_test(tracelist)

for trace in tracelist:
    nodes = dag(trace)

print_dag(nodes)

#first node label is call and end is reply
# make sure each has a reply
