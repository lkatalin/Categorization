import re
from objectify import *

def extract_traces(infile):
    # collects text until complete trace is read in
    buff = []
    # list of all traces read in from file - why is this a list??
    tracelist = []
   
    for line in infile:
        #parse line to see if end of trace
        completeTrace = re.search(r'(.*?})(.*)', line)

        #if end, add last part to buffer and create trace object
        if completeTrace:
            print completeTrace.group(1)
            buff.append(completeTrace.group(1))
            traceObj = make_trace("".join(buff))
            tracelist.append(traceObj)

            #start a new list
            print completeTrace.group(2)
            buff = [completeTrace.group(2)]

        else:
            buff.append(line)

    return tracelist
