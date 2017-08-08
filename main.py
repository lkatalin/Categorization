import sys
from make_dag import *
from extract_traces import *
from print_stuff import *
from group_traces import *
import fileinput
from edge_data import *

# open file from arg or use piped input from stdin
# to be used if piping from json_parser
try:
    #import pdb; pdb.set_trace()
    filename = sys.argv[1]
    with open(filename) as infile:
        tracelist = extract_traces(infile)
except IndexError:
    print "index error"
    tracelist = extract_traces(sys.stdin.readlines())

#print_trace(tracelist)

# group traces based on hashvalue (structure)
for trace in tracelist:
    group_traces(trace)

#analyze groups for avg latency and variance
info = process_groups(categories, tracelist)

# print human-meaningful info
print "\n----------------------------SUMMARY OF TRACE DATA------------------------------ \n"

key_counter = 0
for key in categories.keys():
    key_counter += 1

print "Number of traces: %d" % len(tracelist)
print "Number of categories: %d \n" % key_counter

print "INFO BY CATEGORY: \n"
for key, values in categories.items():
    print "Category hashval: " + str(key)
    print "Number of traces: " + str(len(values))
    for val in info[key]:
        print (val + ': ' + str(info[key][val]))
    print "\n"

group_ctr = 1
for key in categories.keys():
    # fix this because latencies will keep getting updated
    latencies = edge_latencies(key, tracelist)
    cov_matrix(latencies[0], tracelist, group_ctr)
    group_ctr += 1
