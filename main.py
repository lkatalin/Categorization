import sys
from def_color import *
from make_dag import *
from extract_traces import *
from print_stuff import *
from group_traces import *
from edge_data import *

# open file from arg or use piped input from stdin
# to be used if piping from json_parser
try:
    filename = sys.argv[1]
    with open(filename) as infile:
        tracelist = extract_traces(infile)
except IndexError:
    tracelist = extract_traces(sys.stdin.readlines())

# uncomment below to get verbose dump of all trace-object data per trace
#print_trace(tracelist, str(7951795279537954795579567957795879599510951195129513951495159516951795189519952095219522952395249525952695279528952995309531953295339534))

# group traces based on hashvalue (structure)
for trace in tracelist:
    group_traces(trace)

#analyze groups for avg latency and variance
group_data = process_groups(categories, tracelist)

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
    print "The traces are..." 
    print values
    for val in group_data[key]:
        print (val + ': ' + str(group_data[key][val]))
    print "\n"

for key in categories.keys():
    # to do: fix this because latencies will keep getting updated
    latencies = edge_latencies(key, tracelist)
    if len(categories[key]) > 1:
        cov_matrix(key, latencies[0], tracelist)
