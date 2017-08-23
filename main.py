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
#print_trace(tracelist)

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
    print "The traces are: " + str (values) 
    for val in group_data[key]:
        print (val + ': ' + str(group_data[key][val]))
    print "\n"

for key in categories.keys():
    latencies = edge_latencies(key, tracelist)
    if len(categories[key]) > 1:
        cov_matrix(key, latencies[0], tracelist)

def report_anomaly(anomaly, threshold):
    def ret_string(nonstring):
        return {
            "anomalous_groups": "anomalous groups",
            "anomalous_edges": "anomalous edges",
            "high_covar_edges": "high covariance edges"
        }[nonstring[0]]

    def print_report(rep_type):
        if rep_type[0] == 'anomalous_groups':
            print "{}---> Anomalous groups found (var > %d):{} ".format(R, W) % threshold + str(rep_type[1]) + "\n"
        elif rep_type[0] == 'anomalous_edges':
            print "\n{}---> Anomalous edges found (var > %d):{}\n".format(R, W) % threshold
            for group, edges in rep_type[1].iteritems():
                print "    Group: " + str(group)
                print "    Edges: " 
                for edge in edges:
                    print "           " + str(edge)    
        else:
            assert(rep_type[0] == 'high_covar_edges')
            print "\n{}---> High covariance edges found (var > %d):{}\n".format(R, W) % threshold
            for group, var in rep_type[1].iteritems():
                print "     Group: " + str(group)
                print "     Edges: "
                for v in var:
                    print "            " + str(v[0])
                    print "            " + "with"
                    print "            " + str(v[1])
                    print "            " + "Observation values: " + str(v[2]) + " " + str(v[3])
                    print "            " + "Covar: " + str(v[4]) + "\n\n"

    if len(anomaly[1].keys()) == 0:
        print "{}---> No %s found (var > %d).{}\n".format(G, W) % (ret_string(anomaly), threshold)
    else:
        print_report(anomaly)
    
print "------------------------------- VARIANCE RESULTS --------------------------------"
#report_anomaly(anomalous_groups, 5)
for anomaly, data in anomaly_types.iteritems():
    report_anomaly((anomaly, data), 5)

#report_anomaly(anomalous_edges, 5)
#report_anomaly(high_covar_edges, 5)

#print "VARIANCE RESULTS:\n"
#if len(anomalous_groups) == 0:
#    print "{}---> No anomalous groups found (var > 20).{}\n".format(G, W)
#else:
#    print "{}---> Anomalous groups found (var > 20):{} ".format(R, W) + str(anomalous_groups) + "\n"
#if len(anomalous_edges) == 0:
#    print "\n{}---> No anomalous edges found (var > 5).{}\n".format(G, W)
#else:
#    print "\n{}---> Anomalous edges found (var > 5):{}\n".format(R, W)
#    for group, edges in anomalous_edges.iteritems():
#        print "     Group: " + str(group)
#        print "     Edges: "
#        for edge in edges:
#            print "            " + str(edge)
#if len(high_covar_edges) == 0:
#    print "\n{}---> No high covariance edges found (var > 3000000000).{}\n".format(G, W)
#else:
#    print "\n{}---> High covariance edges found (var > 3000000000):{}\n".format(R, W)
#    for group, var in high_covar_edges.iteritems():
#        print "     Group: " + str(group)
#        print "     Edges: "
#        for v in var:
#            print "            " + str(v[0])
#            print "            " + "with"
#            print "            " + str(v[1])
#            print "            " + "Observation values: " + str(v[2]) + " " + str(v[3])
#            print "            " + "Covar: " + str(v[4]) + "\n\n"
