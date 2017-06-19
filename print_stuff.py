# coding: utf-8
# credit for print tree: https://stackoverflow.com/questions/30893895/how-to-print-a-tree-in-python

def print_trace(tracelist):
    for trace in tracelist:
        print trace.traceId
        print "trace: "
        print trace.mainText
        print "\ntracename: " + trace.traceName
        print "response: " + trace.response
        print "response time: " + trace.responseTime
        #print "\nlabels: "
        #for label in trace.labels:
        #    print label
        print "\nedge labels: "
        for label in trace.edgeLabels:
            print label
        print "\nnode labels: "
        for label in trace.nodeLabels:
            print label
        print "\nfull nodes: "
        for node in trace.fullNodes:
            print node
        print "\nedges:"
        for edge in trace.edges:
            print edge
        print "\nhashval: ~~~~"
        print trace.hashval 
        print "~~~~"

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

