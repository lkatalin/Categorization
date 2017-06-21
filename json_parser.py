#!/usr/bin/env python

# This code is written in the middle of the night, so it definately need some
# refactoring to make it pythonic.
#                                   -- Jethro

import json


def json_parser(file):
    """
    Each Json file will be parsed into one trace.
    """
    with open(file) as data_file:
        json_data = json.load(data_file)
    for k, v in json_data.iteritems():
        if k == "info":
            info_parser(v)
        if k == "stats":
            stats_parser(v)
        if k == "children":
            for i in range(len(v)):
                span_parser(v[i])


#def info_parser(info):
#    print "::INFO::"
#
#    for k, v in info.iteritems():
#        if k == "name":
#            print "name:  " + v
#        if k == "started":
#            print  v
#        if k == "finished":
#            print v
#        if k == "meta.raw_payload.wsgi-start":
#            print "wsgi-start: "
#            wsgi_parser(v)
#        if k == "meta.raw_payload.wsgi-stop":
#            print "wsgi-stop: "
#            wsgi_parser(v)
#        if k == "host":
#            print "host" + v
#        if k == "project":
#            print v
#


def info_parser(info):
    print "::INFO::"

    for k, v in info.iteritems():
        print str(k) + " : " + str(v)


def stats_parser(stats):
    print "\n::STATS::"
    
    for k, v in stats.iteritems():
        print k + ": "
        for k2, v2 in v.iteritems():
            print k2 + " : " + str(v2) + "\n"


def wsgi_parser(wsgi):
    print "wsgi"
    for k, v in wsgi.iteritems():
        if k == "wsgi":
            print v
        if k == "info":
            info_parser(v)
        if k == "name":
            print v
        if k == "service":
            print v
        if k == "timestamp":
            print v
        if k == "trace_id":
            print v
        if k == "project:":
            print v
        if k == "parent_id":
            print v
        if k == "base_id":
            print v


def span_parser(span):
    """
    Raja is not gonna be happy about the name, but I assume he won't check out
    this file.
    """
    #print span
    for k, v in span.iteritems():
        #print k
        if k == "info":
            info = info_parser(v)
        if k == "parent_id":
            print "parent_id is: " + v
        if k == "trace_id":
            print "trace_id is: " + v
        if k == "children":
            if len(v) == 0:
                return
            else:
                print "parse children"
    #print span['info']



if __name__ == '__main__':
    json_parser("dataset/test.json")


