from simple_dag import *

#path = []
#path_list = []

#traversal - this is passed a list of nodes
def depth_first_traversal(start_nodes):
    start_node = start_nodes.pop()
    jxn_stack = []
    allpaths = []

        print "node %s's ppath is: " % node.name
        print node.ppath

    #print "start node is: "
    #print start_node
    #print "start node has children: "
    #print start_node.children
    #path = []
    #def dft_helper(start):
    #    path.append(start)
    #    stack = [start]
    #    jnct_pts_stack = [(start, 0, len(start.children))]
    #    print "start helper. "
    #    #print stack
    #    while jnct_pts_stack:
    #        next_visit = 1
    #        total = 1
    #        while next_visit/total == 1:
    #            (curr_jnct, next_visit, total) = jnct_pts_stack.pop()
    #        if curr_jnct.children:
    #            next_visit += 1
    #            jnct_pts_stack.append((curr_jnct, next_visit, total))
    #            
    #            #traverse from first unexplored child
    #            curr_node = curr_jnct.children[next_visit - 1]
    #            while curr_node.children:
    #                path.append("->" + curr_node)
    #                jnct_pts_stack.append(curr_node, 0, len(curr_node.children))
    #                curr_node = curr_node.children[0]
    #            path.append(curr_node.name + "|")
    #
    #    return path

        #while stack:
        #    curr = stack.pop()
        #    print "current is " + curr.name
        #    if not curr.children:
        #        print "curr has no children"
        #        path.append(curr.name + "|")
        #        #print "updated path is: "
        #        #print path
                
        #        #to find most recent jnct, pop it off the stack
        #        (point, nextchild) = junct_pots_stack.pop()
        #        #check if we've exhausted children?
        #        if point.children == nextchild:
                
        #    else: 
        #        print "curr has children: "
        #        print curr.children
        #        #add to junctpoint stack if 
        #        junct_pts_stack.append((curr, 1))
        #        for child in curr.children:
        #            stack.append(child)
        #            print "appended stack is: "
        #            print stack
        #        path.append(curr.name + "->")
        #return path
        
    answer = "".join(dft_helper(start_node))
    print "answer: "
    print answer
    return answer
        
def dft(root):
    nodes = []
    stack = root
    while stack:
        cur_node = stack[0]
        stack = stack[1:]
        nodes.append(cur_node)        
        for child in cur_node.get_rev_children():
            stack.insert(0, child)
    return nodes

# HASHVAL: uses depth-first traversal of dag to form
# value to be used with grouping
#
def hashval(trace):
    #the dag is a dict of (parent, [children]) "pairs"
    hashval = ""
    node_dict = dag(trace)
    print "now in hashval. node dict is: "
    print node_dict
    for key in node_dict.items():
        print "first key: "
        print key
        print "key object: "
        print key[0]
        print "key object's children: "
        print key[0].children

    #find starting nodes
    start_nodes = []
    for key in node_dict.keys():
        #print start_nodes
        if key.parents == []: #and key not in start_nodes:
            start_nodes.append(key)

    print "about to do dft on this node:"
    print start_nodes[0]
    print "which has these children: "
    print start_nodes[0].children

    all_paths = depth_first_traversal(start_nodes)
    #all_paths = dft(start_nodes)
    print "all paths: "
    print all_paths
    return all_paths
                            
#for trace in tracelist:
#    hashval = ""
#    for edge in trace.edges:
#        n1 = re.search(r'(\d{5}) ->', edge).group(1)
#        n2 = re.search(r'.*?(\d{5})$', edge).group(1)
#        partial = '-'.join([re.search(r'(\d{5}) ->',
#            edge).group(1), re.search(r'.*?(\d{5})$', edge).group(1)])
#        hashval += (partial + '|')
#    trace.hashval = hashval
