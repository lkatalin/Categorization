import sys
from make_dag import *
from extract_traces import *
from print_stuff import *
from group_traces import *
import fileinput

# open file from arg or use piped input from stdin
try:
    filename = sys.argv[1]
    with open(filename) as infile:
        tracelist = extract_traces(infile)
except IndexError:
    tracelist = extract_traces(sys.stdin.readlines())

# group traces based on hashvalue (structure)
for trace in tracelist:
    group_traces(trace)

# analyze groups for avg latency and variance
info = process_groups(categories, tracelist)

for key in categories.keys():
    latencies = edge_latencies(key, tracelist)

info2 = group_cov(categories, tracelist)

# print human-meaningful info
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
