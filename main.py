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

# PROCESS TRACE INFO
info = process_groups(categories, tracelist)

# OUTPUT INFO FOR HUMAN
print "\nInfo dump about current traces: \n"

key_counter = 0
for key in categories.keys():
    key_counter += 1

print "Number of traces: %d" % len(tracelist)
print "Number of categories: %d \n" % key_counter

print "Categories: \n"
for key, values in categories.items():
    print "Category hashval: " + str(key)
    print "Number of traces: " + str(len(values))
    for val in info[key]:
        print (val + ': ' + str(info[key][val]))
    print "\n"

#print "\n|| Relevant trace info: ||\n"
#for trace in tracelist:
#    print "TraceId: %d" % trace.traceId
#    print "Trace name: %s" % trace.traceName
#    print "Hashval: %s\n" % trace.hashval
