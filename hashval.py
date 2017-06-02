from simple_dag import *

# HASHVAL: uses depth-first traversal of dag to form
# value to be used with grouping
#
def hashval(trace):
    #the dag is a tree
    hashval = ""
    curr_node = dag(trace)
 
    def add_info(curr_node):
        if curr_node:
            hashval.append(curr_node.name + '| ')
            for child in curr_node.children:
                add_info(child)

    return hashval
    

#for trace in tracelist:
#    hashval = ""
#    for edge in trace.edges:
#        n1 = re.search(r'(\d{5}) ->', edge).group(1)
#        n2 = re.search(r'.*?(\d{5})$', edge).group(1)
#        partial = '-'.join([re.search(r'(\d{5}) ->',
#            edge).group(1), re.search(r'.*?(\d{5})$', edge).group(1)])
#        hashval += (partial + '|')
#    trace.hashval = hashval


