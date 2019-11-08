'''
Created on 2017/04/10
Modified on 2019/10/11
This program generates a customized topology for given number of nodes and network degree.
@author: smallcat
'''

import algorithm                        # algorithms including modified dijkstra algo.
import trafficPattern as tp            # generator of traffic pattern
import datetime                         # output
import networkx as nx   
import sys, getopt
import pandas as pd

def main(argv):
    # self-defined traffic pattern
    try:
        opts, args = getopt.getopt(argv, "hf:n:d:")
    except getopt.GetoptError:
        print 'Usage: python nwGen.py -f <inputfile> -n <nodes> -d <degree>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'Usage: python nwGen.py -f <inputfile> -n <nodes> -d <degree>'
            sys.exit()
        elif opt == "-f":
            tp.archive = arg
        elif opt == "-n":
            tp.nodes = int(arg)   
        elif opt == "-d":
            tp.degree = int(arg)
        else:
            print 'Usage: python nwGen.py -f <inputfile> -n <nodes> -d <degree>'
            sys.exit(2)

    # traffic_pattern = tp.traffic_pattern
    archive = tp.archive    # inputfile
    degree = tp.degree      # network degree
    nodes = tp.nodes        # number of nodes

    # print "=============================================== simulation begins ==============================================="
    # print "sw_node: " + str(sw_node)
    # print "sw_sw: " + str(sw_sw)
    print "Number of nodes: ", nodes, ", Network degree: ", degree, ", Input file: ", archive
    # print "=============================================== switch partition starts ==============================================="

    sw = 1                  # total number of switches
    sw_bp = 1               # number of switches before each partition
    sw_node = {}            # nodes connected to a switch
    sw_sw = {}              # switches connected to a switch

    # Initialize a giant switch connecting all nodes
    sw_node[0] = []
    for i in range(nodes):
        sw_node[0].append(i)
    sw_sw[0] = []

    partition = True    # switch partition
    while partition:
        for i in range(sw_bp):
            if len(sw_node[i]) > 1: # one node per sw
    #             print "   " + str(i)
    #             print len(sw_node[i])
    #             print len(sw_sw[i])
                sw_sw[sw] = []
                sw_sw[i].append(sw)     # append switch connection 
                sw_sw[sw].append(i)     # append switch connection            
                for c_sw in sw_sw[i]:   # append connected switches
                    if c_sw != sw and len(sw_sw[c_sw]) + len(sw_node[c_sw]) < degree:
                        sw_sw[c_sw].append(sw)  
                        sw_sw[sw].append(c_sw)
                sw_node[sw] = []  
                if len(sw_sw[i]) >= degree-1:  # avoid len(sw_sw[i]) >= degree
                    for x in range(len(sw_node[i])-1):
                        sw_node[sw].append(sw_node[i].pop())
                else:
                    for x in range(len(sw_node[i])/2):
                        sw_node[sw].append(sw_node[i].pop())
                sw = sw + 1
            if i == sw_bp - 1 and sw_bp == sw:
                partition = False
        sw_bp = sw
        #print sw_bp

    # switch id = node id (one node per switch)
    for i in range(len(sw_node)):
        sw_node[i] = []
        sw_node[i].append(i)
        
    # print "=============================================== after switch partition ==============================================="                
    # print "sw_node: " + str(sw_node)
    # print "sw_sw: " + str(sw_sw)
    # print "number of switches: " + str(len(sw_sw))

    # topo = 0-1 matrix, edges = (src, dst, dis)
    topo = algorithm.get_topo(sw_sw)
    # print "topo: " + str(topo)
    edges = algorithm.get_edges(topo)    

    # optimize topology according to traffic pattern
    # data = tp.data  # read data flows
    data = pd.read_csv(archive, comment=";", sep="\s+", names=["src", "dst"])
    num_dataflow = len(data)
    src_dst = {}    # num: (src, dst)
    for i in range(num_dataflow):
        src_dst[i] = (data["src"][i], data["dst"][i])  
    src_dst_sw = algorithm.get_src_dst_sw(src_dst, sw_node) # node pair --> switch pair
    # print "src_dst: ", str(src_dst)
    # print "src_dst_sw: ", str(src_dst_sw)

    # slot_num = number of slots, total = total hops, max_hops = max. hops
    # routes = num: (src_node, src_sw, ..., dst_sw, dst_node), src_node, dst_node > 10000
    slot_num, total, max_hops, routes = algorithm.get_slot_num(edges, src_dst, src_dst_sw)    
    slots, congestion, avg = algorithm.print_result(routes, total, src_dst_sw, slot_num)

    # print "=============================================== link add starts ==============================================="        
    sw_sw, added_links = algorithm.get_update_sw_sw(sw_sw, sw_node, degree, edges)
    # print "added_links: ", str(added_links)
    # print "sw_sw: ", str(sw_sw)      
    topo = algorithm.get_topo(sw_sw)
    edges = algorithm.get_edges(topo)   
    slot_num, total, max_hops, routes = algorithm.get_slot_num(edges, src_dst, src_dst_sw)    
    slots, congestion, avg = algorithm.print_result(routes, total, src_dst_sw, slot_num)     

    # print "=============================================== node swap starts ==============================================="         
    # node_switch = (src_node, dst_node), dataflow = congested flow
    node_switch, dataflow = algorithm.get_node_switch(routes, congestion)   
    # print "node_switch: ", str(node_switch)
    import copy
    current_slots = slots
    node_switch_improve = []
    sw_node_before = sw_node
    node_switch_improve.append(sw_node_before)         
    for ns in node_switch:
        sw_node_switch = copy.deepcopy(sw_node_before) 
        for i in range(len(sw_node_switch)):
            if ns[0] in sw_node_switch[i] and ns[1] not in sw_node_switch[i]:
                sw_node_switch[i].remove(ns[0])
                sw_node_switch[i].append(ns[1])
            elif ns[1] in sw_node_switch[i] and ns[0] not in sw_node_switch[i]:
                sw_node_switch[i].remove(ns[1])
                sw_node_switch[i].append(ns[0])   
    #     print "sw_node after node switch: ", str(sw_node_switch)           
        src_dst_sw_switch = algorithm.get_src_dst_sw(src_dst, sw_node_switch)
    #     print "src_dst_sw after node switch: ", str(src_dst_sw_switch)    
        slot_num_switch, total_switch, max_hops_switch, routes_switch = algorithm.get_slot_num(edges, src_dst, src_dst_sw_switch)    
        slots_switch, congestion_switch, avg_switch = algorithm.print_result(routes_switch, total_switch, src_dst_sw_switch, slot_num_switch)

        if slots_switch <= current_slots:
            node_switch_improve.append(sw_node_switch)
            
            # print "=============================================== indirect_parallel start after node_switch ", str(ns), "===============================================" 
            node_switch, dataflow_switch = algorithm.get_node_switch(routes_switch, congestion_switch)
            slot_num_switch, total_switch, routes_switch = algorithm.replace_indirect_parallel_path(added_links, slots_switch, dataflow_switch, sw_sw, slot_num_switch, total_switch, routes_switch)                    
            slots_switch, congestion_switch, avg_switch = algorithm.print_result(routes_switch, total_switch, src_dst_sw_switch, slot_num_switch)
            if slots_switch < slots:
                slots = slots_switch
                avg = avg_switch
                slot_num = slot_num_switch
                total = total_switch
                max_hops = max_hops_switch
                routes = routes_switch
                congestion = congestion_switch
                sw_node = sw_node_switch
    # print "=============================================== indirect_parallel end ==============================================="  

    # print "=============================================== results ==============================================="
    # print "routes: ", str(routes)
    # print "slot_num:", slot_num
    # print "sw_node: ", sw_node
    # print "sw_sw: ", sw_sw
    # print "max number of slots: ", str(slots)
    num_max = 0
    for i in slot_num.values():
        if i == slots:
            num_max = num_max + 1 
    # print "num_max: ", str(num_max), " / ", str(len(slot_num))
    print "average switch hops: ", str(avg)
    print "max hops: ", str(max_hops)
    print "number of switches: ", str(len(sw_sw))

    links = 0
    for item in sw_sw.values():
        links = links + len(item)
    links = links/2
    print "number of links: ", str(links)

    print "=============================================== topology information is stored in output/ ==============================================="
    # switch connection file
    fn = "output/node_" + str(nodes) + "_degree_" + str(degree) + "_time_" + str(datetime.datetime.now()).replace(" ", "-").replace(".", "-").replace(":", "-") + str(".txt")
    f = open(fn, "w")
    for i in range(len(sw_sw)):                             # i --> src_sw
        for j in range(len(sw_sw[i])):                      # j+1 --> src_port, 0 is retained for localhost
            if sw_sw[i][j] > i:                             # sw_sw[i][j] --> dst_sw
                f.write(str(i) + " " + str(j+1) + " ")
                for k in range(len(sw_sw[sw_sw[i][j]])):
                    if sw_sw[sw_sw[i][j]][k] == i:
                        f.write(str(sw_sw[i][j]) + " " + str(k+1) + "\n")   # k+1 --> dst_port, 0 is retained for localhost
    f.close()   

if __name__ == "__main__":
   main(sys.argv[1:])      