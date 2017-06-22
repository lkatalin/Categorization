#!/usr/bin/env python

import json
import re

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

def request_parser(request):
    print "::REQUEST::"
    for k, v in request.iteritems():
        print str(k) + " : " + str(v)

def info_parser(info):
    print "::INFO::"
    for k, v in info.iteritems():
        if re.search(r'wsgi', k) is not None:
            wsgi_parser(v)
        if k == "request":
            request_parser(v)
        else:
            print str(k) + " : " + str(v)

def stats_parser(stats):
    print "\n::STATS::"
    for k, v in stats.iteritems():
        print k + ": "
        for k2, v2 in v.iteritems():
            print k2 + " : " + str(v2)

def wsgi_parser(wsgi):
    print "::WSGI::"
    for k, v in wsgi.iteritems():
        if k == "info":
            info_parser(v)
        elif re.search(r'wsgi', k) is not None:
            wsgi_parser(v)
        else:
            print k + ": " + v

def span_parser(span):
    """
    Raja is not gonna be happy about the name, but I assume he won't check out
    this file.
    """
    #print span
    for k, v in span.iteritems():
        #print k
        if k == "info":
            info_parser(v)
        elif re.search(r'wsgi', k) is not None:
            wsgi_parser(v)
        elif k == "children":
            if len(v) == 0:
                return
            else:
                print "\n::BEGINNING CHILDREN::"
        else:
            print k + " is: " + v

if __name__ == '__main__':
    json_parser("dataset/test.json")
