# coding: utf-8
# credit for print tree: https://stackoverflow.com/questions/30893895/how-to-print-a-tree-in-python

import sys
from def_color import *

def print_trace(tracelist):
    for trace in tracelist:
	print "\n\ntrace id: " + trace.traceId
	print "\ntrace raw text: \n"
	print trace.mainText
	print "\ntracename: " + str(trace.traceName)
	print "\ntotal response time: " + trace.response
	print "\nfull nodes: "
	for node in trace.fullNodes:
	    print node
	print "\nfull edges: "
	for edge in trace.fullEdges:
	    print edge
	print "\nhashval: " + trace.hashval

def report_anomaly(anomaly, threshold):
    def ret_string(nonstring):
        return {
            "anomalous_groups": "anomalous groups",
            "anomalous_edges": "anomalous edges",
            "high_covar_edges": "high covariance edges"
        }[nonstring[0]]

    def print_report(rep_type):
        if rep_type[0] == 'anomalous_groups':
            print "{}---> Anomalous groups found (var > %d):{}\n".format(R, W) % threshold 
            for group in rep_type[1]["Groups:"]:
                print group + "\n"
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


def print_tree(current_node, indent="", last='updown'):
    nb_children = lambda node: sum(nb_children(child) for child in node.children) + 1
    size_branch = {child: nb_children(child) for child in current_node.children}

    """ Creation of balanced lists for "up" branch and "down" branch. """
    up = sorted(current_node.children, key=lambda node: nb_children(node))
    down = []
    while up and sum(size_branch[node] for node in down) < sum(size_branch[node] for node in up):
        down.append(up.pop())

    """ Printing of "up" branch. """
    for child in up:
        next_last = 'up' if up.index(child) is 0 else ''
        next_indent = '{0}{1}{2}'.format(indent, ' ' if 'up' in last else '│', " " * len(current_node.name))
        print_tree(child, indent=next_indent, last=next_last)

    """ Printing of current node. """
    if last == 'up': start_shape = '┌'
    elif last == 'down': start_shape = '└'
    elif last == 'updown': start_shape = ' '
    else: start_shape = '├'

    if up: end_shape = '┤'
    elif down: end_shape = '┐'
    else: end_shape = ''

    print '{0}{1}{2}{3}'.format(indent, start_shape, current_node.name, end_shape)

    """ Printing of "down" branch. """
    for child in down:
        next_last = 'down' if down.index(child) is len(down) - 1 else ''
        next_indent = '{0}{1}{2}'.format(indent, ' ' if 'down' in last else '│', " " * len(current_node.name))
        print_tree(child, indent=next_indent, last=next_last)


def print_dag(nodes_seen):
    print "dag : \n"
    for key in nodes_seen.keys():
        for value in nodes_seen[key]:
            print "the key name is" + key.name + "and one of its values is " + value.name

