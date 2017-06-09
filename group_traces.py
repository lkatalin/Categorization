categories = {}

def group_traces(trace):
    #has this trace's structure been seen before?
    maybe_key = categories.get(trace.hashval)
    if maybe_key:
        categories[trace.hashval].append(trace.traceId)
    else:
        categories[trace.hashval] = [trace.traceId]


