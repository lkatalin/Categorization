#!/usr/bin/env python

import json
import re

def json_parser(file):
    """ 
    Each Json file will be parsed into one trace.
    """
    with open(file, 'r') as data_file:
        edge_list = []       
 
        # make a dict
        json_data = json.load(data_file)

        def parser(data):
            keyname = data["info"]["name"]
	    for key, value in data.iteritems():
		#print key
                print "key name: " + keyname + "key: " + key
		if key == "children" and len(value) != 0:
                    for v in value:
                        valname = v["info"]["name"]
                        print "    val name :" + valname
                        edge_list.append((keyname, valname))
                        parser(v)

    
    actual_nodes = json_data["children"]
 
    for node in actual_nodes:
        parser(node)

    print "edges: "
    print edge_list

if __name__ == '__main__':
    json_parser("traces/rightfile.json")
