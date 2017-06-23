#!/usr/bin/env python
import json

def json_parser(file):
    """ 
    each json file is parsed into one trace
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
            time = extract_timestamp(data["info"])
            start = time[0]
            stop = time[1]
            return (name, service, start, stop)

        def parser(data):
            # node data 
            (kname, kservice, kstart, kstop) = collect_data(data)
            node_list.append((kstart, kname, kservice))

	    for key, value in data.iteritems():
		if key == "children" and len(value) != 0:
                    for v in value:
                        # edge data
                        (vname, vservice, vstart, vstop) = collect_data(v)
                        edge_latency = 0
                        edge_list.append((kstart, vstart, edge_latency))

                        # find nested nodes
                        parser(v)
 
    # extract full-trace metadata
    total_time = json_data["info"]["finished"]
 
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


    # print DOT format
    print "' # 1 R: %d usecs RT: 0.000000 usecs Digraph X {" % total_time
    for node in node_list:
        print '\t' + str(node[0]) + ' [label="%s - %s"]' % (str(node[1]), str(node[2]))
    for edge in edge_list:
        print '\t' + edge[0] + ' -> ' + edge[1] + ' [label="%s"]' % str(edge[2])
    print "}'"

if __name__ == '__main__':
    json_parser("traces/rightfile.json")
