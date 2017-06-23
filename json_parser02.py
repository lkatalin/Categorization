#!/usr/bin/env python
import json

def json_parser(file):
    """ 
    Each Json file will be parsed into one trace.
    """
    with open(file, 'r') as data_file:
        json_data = json.load(data_file)
       
        # edge list as [(start time -> start time)]
        edge_list = []
 
        # node list as [(start time, name service)]
        node_list = [(0, 'root', 'caller')]
 
        def extract_timestamp(data):
            for key in data.keys():
                if 'meta.raw_payload' in key:
                    if 'start' in key:
                        start = data[key]["timestamp"]
                    elif 'stop' in key:
                        stop = data[key]["timestamp"]
            return (start, stop)

        def parser(data):
            # collect key data
            k_info = data["info"]
            keyname = k_info["name"]
            keyservice = k_info["service"]
            k_time = extract_timestamp(k_info)
            keystart = k_time[0]
            keystop = k_time[1]
            
            print "key values:" 
            print keyname 
            print keyservice
            print keystart
            node_list.append((keystart, keyname, keyservice))

	    for key, value in data.iteritems():
                print "key name: " + keyname + "key: " + key
		if key == "children" and len(value) != 0:
                    for v in value:
                        # collect value data
                        v_info = v["info"]
                        valname = v_info["name"]
                        v_time = extract_timestamp(v_info)    
                        valstart = v_time[0]
                        valstop = v_time[1]                    

                        edge_latency = 0
                        print "    val name :" + valname
                        edge_list.append((keystart, valstart, edge_latency))
                        parser(v)
    
    actual_nodes = json_data["children"]
 
    for node in actual_nodes:
        n_info = node["info"]
        n_time = extract_timestamp(n_info)
        nodestart = n_time[0]
        nodestop = n_time[1]

        edge_list.append(('0', nodestart, '0'))
        parser(node)

#    print "edges: "
#    print edge_list
#    print "nodes: "
#    print node_list

if __name__ == '__main__':
    json_parser("traces/rightfile.json")
