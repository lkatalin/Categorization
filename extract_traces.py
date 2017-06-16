import re
from objectify import *

def extract_traces(infile):
    # collects text until complete trace is read in
    buff = []
    # list of all traces read in from file
    tracelist = []
    # first trace has traceid 1
    traceid = 1
   
    for line in infile:
        #parse line to see if end of trace
        completeTrace = re.search(r'(.*?}.)(.*?)$', line)

        #if end, add last part to buffer and create trace object
        if completeTrace:
            buff.append(completeTrace.group(1))
            traceObj = make_trace("".join(buff), traceid)
            tracelist.append(traceObj)
            traceid += 1

            #start a new list
            buff = [completeTrace.group(2)]

        else:
            buff.append(line)

    return tracelist
