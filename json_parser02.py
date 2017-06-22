#!/usr/bin/env python

import json
import re

def json_parser(file):
    """ 
    Each Json file will be parsed into one trace.
    """
    with open(file, 'r') as data_file:
        
        # make a dict
        json_data = json.load(data_file)

#        def trace_parser(data):
#            for key, value in data.iteritems():
#                if key == "children" and len(value) != 0:
#                    node_parser(value)
#
        def parser(data):
	    for key, value in data.iteritems():
		print key
		if key == "children" and len(value) != 0:
                    for v in value:
                        parser(v)

    
    actual_nodes = json_data["children"]
 
    for node in actual_nodes:
        parser(node)

if __name__ == '__main__':
    json_parser("traces/rightfile.json")
