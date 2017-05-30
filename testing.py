def test(tracelist):
    for trace in tracelist:
        print trace.traceId
        print "trace: "
        print trace.mainText
        print "\ntracename: " + trace.traceName
        print "response: " + trace.response
        print "response time: " + trace.responseTime
        print "\nlabels: "
        for label in trace.labels:
            print label
        print "\nedge labels: " 
        for label in trace.edgeLabels:
            print label
        print "\nnode labels: "
        for label in trace.nodeLabels:
            print label
        print "\nedges:"
        for edge in trace.edges:
            print edge
        print "hashval: " + trace.hashval
