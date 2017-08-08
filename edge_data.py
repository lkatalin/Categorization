import re
import numpy as np
from make_dag import *
from decimal import *
from datetime import datetime
from datetime import timedelta
from group_traces import *

# ----------- time conversion helpers --------------------------------------------

def str_to_time(string):
    '''
    casts formatted string into datetime's time type
    '''
    return datetime.strptime(string, "%H:%M:%S.%f").time()

def time_to_float(time):
    '''
    casts datetime type into float in microseconds
    '''
    return float((time.hour * 3600000000) + (time.minute * 60000000) + 
		 (time.second * 1000000) + time.microsecond)

def timedelta_to_float(td):
    '''
    casts timedelta to float in microseconds. timedelta does not have
    hour or minute methods like time does
    '''
    return float((td.seconds * 1000000) + td.microseconds)

def time_to_timedelta(time):
    '''
    casts time to timedelta
    '''
    return timedelta(hours=time.hour, minutes=time.minute, seconds=time.second, 
		     microseconds=time.microsecond)
        
# --------------------------------------------------------------------------

def edge_latencies(group, tlist):
    """
    creates key-value pairs of edge : [list of latencies found for edge]
    in one group;
    returns this list, a list of average latencies per edge, and a list 
    of variance per edge;
    variance calculated in microseconds
    ...
    ** assumes all traces in group have exact same structure **
    ...
    possibly, we could group the edges by label instead of tid -> tid,
    which would give us more data per edge
    """
    traces = categories[group]
    edge_latencies = {}
    edge_averages = {}
    edge_variance = {}
    for traceid in traces:
        t = trace_lookup(traceid, tlist)
        for full_edge in t.fullEdges:
            #edge = re.search(r'(\d+.* -> \d+.*) \[', full_edge).group(1)
            #time = re.search(r'label="(.*)"', full_edge).group(1)
            edge = re.search(r'(.* -> .*) \[', full_edge).group(1)
            time = re.search(r'label=\"(.+)\"', full_edge).group(1)
            if edge in edge_latencies:
                edge_latencies[edge].append(time)
            else: 
                edge_latencies[edge] = [time]

    # calculate averages
    for key, values in edge_latencies.items():

        # baseline
        psum = timedelta(hours=0, minutes=0, seconds=0, microseconds=0)
        numvals = len(values)

        for value in values:
            # sum up all latencies in this group as timedelta values
            dateval = str_to_time(value)
            deltaval = time_to_timedelta(dateval)
            psum += deltaval

        avg = psum / numvals
        edge_averages[key] = avg
        #print "edge average is: " + str(edge_averages[key])

    # calculate variance
    '''
    in microseconds
    '''
    print "\n--------------------------- EDGE VARIANCE DATA -------------------------------\n"
    for key, values in edge_latencies.items():
	if numvals < 2:
	    edge_variance[key] = 0
	else:
	    psum = 0
            print "Calculating variance for edge: " + str(key)
	    for value in values:
                dateval = str_to_time(value)
		avg = edge_averages[key]
                print "current value: %s, avg: %s" % (str(value), str(avg))
                float_val = time_to_float(dateval) 
                float_avg = timedelta_to_float(avg)
		psum += ((float_val - float_avg) ** 2)
            edge_variance[key] = (1 / float(numvals)) * psum
        print "edge variance is: " + str(edge_variance[key]) + " microseconds\n"

    #print "edges in group: "
    #print edge_latencies

    return (edge_latencies, edge_averages, edge_variance)


def cov_matrix(e_lat_dict, tlist, ctr):
    """
    takes an edge latency dict (such as from above) and a tracelist as args;
    returns covariance matrix for each pair of edges within a group.
    """
    def to_float(time_list):
	ftime_list = []
	for time in time_list:
	    t = str_to_time(time)
	    ftime = time_to_float(t)
	    ftime_list.append(ftime)
	return ftime_list

    print "--------------------------- COVARIANCE DATA -----------------------------------"
    if len(tlist) == 1:
        print "\ncannot create covariance matrix from one trace... skipping \n"
    else:
        float_list = [to_float(e_lat_dict[k]) for k in e_lat_dict]
        lat_array = np.array([f for f in float_list]).astype(np.float)
        print "\narray of latencies in group %d per edge (one edge per row): \n" % ctr
        print  lat_array
	matrix = np.cov(lat_array)
        print "\ncovariance matrix for edges of group %d: \n" % ctr
	print matrix
	print "\n"
        return matrix
