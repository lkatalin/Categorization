from make_tree import *
from print_stuff import *
from hashval import *

def trace_test(tracelist):
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
        print "\nedges:"
        for edge in trace.edges:
            print edge
        print "\nhashval: TBD\n"

def tree_test():
    t = Tree('*', [Tree('1'), Tree('2'), Tree('+', [Tree('3'), Tree('4')])])

    t1 = Tree('a', [Tree('b'), Tree('c')])

    t2 = Tree('c', [Tree('d')])

    t3 = Tree('e', [Tree('f')])

    lst = [t1, t2, t3]

    #result = combine_trees(lst)

    #print "our resulting tree list is "
    #print result

    print "\n and our trees are "
    for tree in lst:
        print_tree(tree)

tree_test()
