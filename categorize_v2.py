from sys import argv
from dag import *
from testing import *
from extract_trace import *

filename = argv[1]

# read file into list of trace objects
# with "extract_traces" module as pluggable 
# interface

with open(filename) as infile:
        tracelist = extract_traces(infile)

trace_test(tracelist)

# create dag for each trace
for trace in tracelist:
    dag = dag(trace)
    print dag
