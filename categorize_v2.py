import re
import os
from sys import argv
import hashval
from objectify import *
from testing import test

scriptname, filename = argv

buff = []
tracelist = []
traceid = 1

# READ FILE INTO LIST OF TRACE OBJECTS
with open(filename) as infile:
    for line in infile:
        #parse line to see if end of trace
        completeTrace = re.search(r'(.*?}.)(.*?)$', line)

        #if end, add last part to buffer and create metadata object
        if completeTrace:
            buff.append(completeTrace.group(1))
            traceObj = make_trace("".join(buff), traceid)
            tracelist.append(traceObj)
            traceid += 1

            #start a new list
            buff = [completeTrace.group(2)]

        else:
            buff.append(line)


# testing
hashval.dag(tracelist[0])

#for trace in tracelist:
#    hashval.dag(trace)

#test(tracelist)
