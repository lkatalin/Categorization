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

# TESTING
print categories
