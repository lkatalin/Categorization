import numpy as np
import re
from datetime import time, datetime, timedelta
from def_color import *
from make_dag import *
from decimal import *
from group_traces import *

# ----------- time conversion helpers --------------------------------------------

def convert_microsec(string):
    '''
    converts strings incompatible with datetime format
    ex. 'R: 47.363121 us' to datetime
    '''
    raw_time = re.search(r'\d+(.\d+)*', string).group(0)
    if raw_time > 1000000:
        secs = int(float(raw_time) / 1000000)
        msecs = int(float(raw_time) % 1000000)
    else:
        msecs = float(raw_time.split("."))
    return time(0, 0, secs, msecs)
    

def str_to_time(string):
    '''
    casts formatted string into datetime's time type
    '''
    try:
        return datetime.strptime(string, "%H:%M:%S.%f").time()
    except ValueError:
        return convert_microsec(string)

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
    casts time to timedelta for adding / accumulating time
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
    global anomaly_types

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
    #print "\n--------------------------- EDGE VARIANCE DATA -------------------------------\n"
    for key, values in edge_latencies.items():
	if numvals < 2:
	    edge_variance[key] = 0
	else:
	    psum = 0
	    for value in values:
                dateval = str_to_time(value)
       	        avg = edge_averages[key]
                float_val = time_to_float(dateval) 
                float_avg = timedelta_to_float(avg)
                psum += ((float_val - float_avg) ** 2)
            edge_variance[key] = (1 / float(numvals)) * psum
        #arbitrary threshold
        if edge_variance[key] > 5:
            add_to_dict(anomaly_types['anomalous_edges'], group, key)
    return (edge_latencies, edge_averages, edge_variance)


def cov_matrix(group, e_lat_dict, tlist):
    """
    takes an edge latency dict (such as from above) and a tracelist as args;
    returns covariance matrix for each pair of edges within a group.
    """
    global anomaly_types

    def to_float(time_list):
	ftime_list = []
	for time in time_list:
	    t = str_to_time(time)
	    ftime = time_to_float(t)
	    ftime_list.append(ftime)
	return ftime_list

    #print "------------------------------- COVARIANCE DATA --------------------------------"
    if len(tlist) == 1:
        pass
        #print "\ncannot create covariance matrix from one trace... skipping \n"
    else:
        float_list = [to_float(e_lat_dict[k]) for k in e_lat_dict]
        lat_array = np.array([f for f in float_list]).astype(np.float)
        #print "\narray of latencies for group {}%s{} per edge (one edge per row): \n".format(G, W) % group
        #print  lat_array
	matrix = np.cov(lat_array)
        #print "\ncovariance matrix for edges of group {}%s{}: \n".format(G, W) % group
	#print matrix
	#print "\n"
        row_ctr = 1
        for i, j in enumerate(matrix):
            col_ctr = 1
            for covar in j:
                # arbitrary threshold
                if covar > 3000000000:
                    # find which edges produced the anomaly
                    cell_no = (row_ctr, col_ctr)
                    edge_val1 = lat_array[row_ctr - 1]
                    edge_val2 = lat_array[col_ctr - 1]

                    edge1 = e_lat_dict.keys()[row_ctr - 1]
                    edge2 = e_lat_dict.keys()[col_ctr - 1]
                   
                    add_to_dict(anomaly_types['high_covar_edges'], group, (edge1, edge2, edge_val1, edge_val2, covar))

                col_ctr += 1
            row_ctr += 1
        return matrix
