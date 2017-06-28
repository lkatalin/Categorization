#!/usr/bin/env python
import json
import sys

"""
NOTE: this creates a DOT file in the correct format of the 
spectroscope DOTs from OSprofiler's JSON format. however,
some of the formatting is not meaningful. ex:

- traces do not have names in OSprofiler, so 
  they are all hard-coded to be called 'Digraph X'
- 'RT' field is preserved even though we do not know what
  it means and it is always 0.000000
- a fake "root" is kept with data for the entire trace, 
  instead of being a real service or process
- etc.

broader questions: 
1. how to uniquely identify nodes from the OSP JSON output?
2. what data should be kept? aside from: name, service, 
   start/stop times
"""

def json_parser(file):
    """ 
    usage: 
    python json_parser.py file.json -> prints to stdout
    python json_parser.py file.json to-file -> prints to file [trace_id].dot
    """
    with open(file, 'r') as data_file:
        json_data = json.load(data_file)
       
        # edge list as [(start time -> start time)]
        edge_list = []
 
        # node list as [(start time, name, service)]
        node_list = [(0, 'root', 'caller')]
 
        def extract_timestamp(data):
            for key in data.keys():
                if 'meta.raw_payload' in key:
                    if 'start' in key:
                        start = data[key]["timestamp"]
                    elif 'stop' in key:
                        stop = data[key]["timestamp"]
            return (start, stop)

        def collect_data(data):
            name = data["info"]["name"]
            service = data["info"]["service"]
            start = data["info"]["started"]
            stop = data["info"]["finished"]
            time = extract_timestamp(data["info"])
            start_stamp = time[0]
            stop_stamp = time[1]
            return (name, service, start, stop, start_stamp, stop_stamp)

        def parser(data):
            # node data 
            (kname, kservice, kstart, kstop, kstart_stamp, 
                                       kstop_stamp) = collect_data(data)
            node_list.append((kstart_stamp, kname, kservice))

	    for key, value in data.iteritems():
		if key == "children" and len(value) != 0:
                    for v in value:
                        # edge data
                        (vname, vservice, vstart, vstop, vstart_stamp, 
                                           vstop_stamp) = collect_data(v)

                        edge_latency = float(vstart) - float(kstop)
                        edge_list.append((kstart_stamp, vstart_stamp, 
                                                            edge_latency))

                        # find nested nodes
                        parser(v)
 
    # extract full-trace metadata
    total_time = json_data["info"]["finished"]
    trace_id = json_data["children"][0]["parent_id"]
 
    # begins data only for nodes/edges
    actual_nodes = json_data["children"]
    
    # add edges from the fake 'root' to beginning nodes
    for node in actual_nodes:
        n_info = node["info"]
        n_time = extract_timestamp(n_info)
        nodestart = n_time[0]
        nodestop = n_time[1]

        edge_list.append(('0', nodestart, '0'))
        parser(node)


    # print DOT format to file
    if len(sys.argv) > 2 and sys.argv[2] == "to-file":
        sys.stdout = open('%s.dot' % trace_id, 'w')
 
    print "' # %s R: %d usecs RT: 0.000000 usecs Digraph X {" % (trace_id, total_time)
    for node in node_list:
        print '\t' + str(node[0]) + ' [label="%s - %s"]' % (str(node[1]), str(node[2]))
    for edge in edge_list:
        print '\t' + edge[0] + ' -> ' + edge[1] + ' [label="%s"]' % str(edge[2])
    print "}'"

filename = sys.argv[1]
json_parser(filename)
