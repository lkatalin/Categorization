from sys import argv
from simple_dag import *
from extract_traces import *
from print_stuff import *

filename = argv[1]

# EXTRACT TRACES
with open(filename) as infile:
        tracelist = extract_traces(infile)


# GROUP TRACES
# to do


# TESTING
print_trace(tracelist)

for trace in tracelist:
     dirgraph = dag(trace)
     print dirgraph
     for key in dirgraph:
          for item in dirgraph[key]:
              print item.ppath

#first node label is call and end is reply
# make sure each has a reply
