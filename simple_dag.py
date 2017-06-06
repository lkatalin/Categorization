import re
from make_tree import *
from print_tree import *

#parent nodes are keys, children are values (as list)
nodes_seen = {}

#this is given a trace object
#and returns a dict of parent/children pairs
def dag(trace):
    #print "dag has been called from hashval" 
    def lookup(dictionary, name):
        for key, value in dictionary.items():
            #print "an example key is : "
            #print key
            #print "the key, value pair is: "
            #print (key, value)
            #print "key name is: " + key.name
            if key.name == name:
                #print "found key"
                return key
        #for key in dictionary.keys():
            #print "the key name is" + key.name + "and its value is: " 
            #print dictionary[key]
        return False

    for edge in trace.edges:
        #extract source and dest nodes as strings
        src = re.search(r'(\d+.\d+) ->', edge).group(1)
        dst = re.search(r'-> (\d+.\d+)', edge).group(1)

        #create new dst_tree
        dst_tree = Tree(dst)
        #print "new dst tree created: "
        #print dst_tree
        #print "dst tree's children: "
        #print dst_tree.children

        #check whether src in dict already
        src_present = lookup(nodes_seen, src)
        if src_present:
            #create obj attachments to dst tree
            src_present.add_child(dst_tree)
            dst_tree.add_parent(src_present)
            #add dst as value to src key
            nodes_seen[src_present].append(dst_tree)
   
        else: 
            #create src obj and update attachments
            #print "src not yet present. creating src tree"
            src_tree = Tree(src) 
            #print src_tree
            src_tree.add_child(dst_tree)
            dst_tree.add_parent(src_tree)
            #add to dict
            #print "adding src tree to dict"
            nodes_seen[src_tree] = [dst_tree]
            #print nodes_seen[src_tree]
    
    #print "nodes seen in dag:" 
    #print nodes_seen
    #for key, value in nodes_seen.items():
    #    print (key, value)
    #    for vals in value:
    #        print "value: "
    #        print vals
    #        print "value's children: "
    #        print vals.children
    return nodes_seen
