import sys
from make_dag import *
from extract_traces import *
from print_stuff import *
from group_traces import *
from edge_data import *
from json_dag_multi import json_dag

# open file from arg or use piped input from stdin
# to be used if piping from json_parser

try:
    filename = sys.argv[1]
    if filename.endswith(".json"):
        dot_format = iter((json_dag(filename, True)).splitlines())
        numtraces = extract_traces(dot_format)
                
    else:
	with open(filename) as infile:
	    numtraces = extract_traces(infile)

except IndexError:
    numtraces = extract_traces(sys.stdin.readlines())

# uncomment below to get verbose dump of all trace-object data per trace
#print_trace(tracelist)

#analyze groups for avg latency and variance
#group_data = process_groups(categories, tracelist)

# print human-meaningful info
print "\n----------------------------SUMMARY OF TRACE DATA------------------------------ \n"

key_counter = 0
for key in categories.keys():
    key_counter += 1

print "Number of traces: %d" % numtraces
print "Number of categories: %d \n" % key_counter

print "INFO BY CATEGORY: \n"
for key, values in categories.items():
    print "Category hashval: " + str(key)

    # count traces in category
    numincategory = 0
    for trace in categories[key][2]:
        numincategory += 1

    print "Number of traces: %d" % numincategory
    print "Example trace: %s" % values[0]

    print "Total overall response times listed in category: " + str(values[1])
    print "Average overall response time: "
    
    print "Traces included:\n"

    for trace in categories[key][2]:
        print "\tTrace ID: " + trace
        print "\tEdge latencies: " + str(categories[key][2][trace])

#    for val in group_data[key]:
#        print (val + ': ' + str(group_data[key][val]))
    print "\n"

#for key in categories.keys():
#    latencies = edge_latencies(key, tracelist)
#    # only calculate covariance if > 1 observation (> 1 trace in group)
#    if len(categories[key]) > 1:
#        cov_matrix(key, latencies[0], tracelist)
    
#print "------------------------------- VARIANCE RESULTS --------------------------------\n"
#for anomaly, data in anomaly_types.iteritems():
#    report_anomaly((anomaly, data), 5)
