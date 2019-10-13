'''
Created on 2017/04/13
Modified on 2019/10/11
This program provides various algorithms including dijkstra algo.
@author: smallcat
'''

from collections import defaultdict  
from heapq import *  
  
# raw dijkstra algo
def dijkstra_raw(edges, from_node, to_node):  
    g = defaultdict(list)  
    for l,r,c in edges:  
        g[l].append((c,r))  
    q, seen = [(0,from_node,())], set()  
    while q:  
        (cost,v1,path) = heappop(q)  
        if v1 not in seen:  
            seen.add(v1)  
            path = (v1, path)  
            if v1 == to_node:  
                return cost,path  
            for c, v2 in g.get(v1, ()):  
                if v2 not in seen:  
                    heappush(q, (cost+c, v2, path))  
    return float("inf"),[]  
  
# modified dijkstra algo
def dijkstra(edges, from_node, to_node):  
    len_shortest_path = -1  
    ret_path=[]  
    length,path_queue = dijkstra_raw(edges, from_node, to_node)  
    if len(path_queue)>0:  
        len_shortest_path = length      ## 1. Get the length firstly;  
        ## 2. Decompose the path_queue, to get the passing nodes in the shortest path.  
        left = path_queue[0]  
        ret_path.append(left)       ## 2.1 Record the destination node firstly;  
        right = path_queue[1]  
        while len(right)>0:  
            left = right[0]  
            ret_path.append(left)   ## 2.2 Record other nodes, till the source-node.  
            right = right[1]  
        ret_path.reverse()  ## 3. Reverse the list finally, to make it be normal sequence.  
    return len_shortest_path,ret_path  

# ### ==================== Given a list of nodes in the topology  
# list_nodes_id = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20];  
# ### ==================== Given constants matrix of topology.  
# M=99999 # This represents a large distance. It means that there is no link.  
# ### M_topo is the 2-dimensional adjacent matrix used to represent a topology.  
# M_topo = [  
# [M, 1,1,M,1,M, 1,1,1,M,M, M,M,M,M,M, M,M,M,M,M],  
# [1, M,1,M,M,1, M,M,M,M,M, M,M,M,M,M, M,M,M,M,M],  
# [1, 1,M,1,M,M, M,M,M,M,M, M,M,M,M,M, M,M,M,M,M],  
# [M, M,1,M,1,M, M,M,M,M,M, M,M,M,M,M, M,M,M,M,M],  
# [1, M,M,1,M,M, M,M,M,1,1, 1,M,M,M,M, M,M,M,M,M],  
# [M, 1,M,M,M,M, 1,M,M,M,M, M,M,M,M,M, M,M,M,M,M],  
# [1, M,M,M,M,1, M,1,M,M,M, M,M,M,M,M, M,M,M,M,M],  
# [1, M,M,M,M,M, 1,M,1,M,M, M,M,M,M,M, M,M,M,M,M],  
# [1, M,M,M,M,M, M,1,M,1,M, M,1,M,M,M, M,M,M,M,M],  
# [M, M,M,M,1,M, M,M,1,M,M, 1,M,M,M,M, M,M,M,M,M],  
# [M, M,M,M,1,M, M,M,M,M,M, 1,M,1,M,M, M,M,M,M,M],  
# [M, M,M,M,1,M, M,M,M,1,1, M,M,1,1,M, M,M,M,M,M],  
# [M, M,M,M,M,M, M,M,1,M,M, M,M,M,1,M, M,M,M,M,M],  
# [M, M,M,M,M,M, M,M,M,M,1, 1,M,M,1,M, M,1,1,M,M],  
# [M, M,M,M,M,M, M,M,M,M,M, 1,1,1,M,1, 1,M,M,M,M],  
# [M, M,M,M,M,M, M,M,M,M,M, M,M,M,1,M, 1,M,1,1,M],  
# [M, M,M,M,M,M, M,M,M,M,M, M,M,M,1,1, M,M,M,M,1],  
# [M, M,M,M,M,M, M,M,M,M,M, M,M,1,M,M, M,M,1,M,M],  
# [M, M,M,M,M,M, M,M,M,M,M, M,M,1,M,1, M,1,M,1,M],  
# [M, M,M,M,M,M, M,M,M,M,M, M,M,M,M,1, M,M,1,M,1],  
# [M, M,M,M,M,M, M,M,M,M,M, M,M,M,M,M, 1,M,M,1,M]  
# ]     
#   
# ### --- Read the topology, and generate all edges in the given topology.  
# edges = []    
# for i in range(len(M_topo)):  
#     for j in range(len(M_topo[0])):  
#         if i!=j and M_topo[i][j]!=M:  
#             edges.append((i,j,M_topo[i][j]))### (i,j) is a link; M_topo[i][j] here is 1, the length of link (i,j). 
#             
# print "=== Dijkstra ==="  
# print "Let's find the shortest-path from 0 to 9:"  
# length,Shortest_path = dijkstra(edges, 0, 9)  
# print 'length = ',length  
# print 'The shortest path is ',Shortest_path  

## 0-1 matrix
def get_topo(sw_sw):
    topo = []
    for i in range(len(sw_sw)):
        dis = []
        for j in range(len(sw_sw)):
            if j in sw_sw[i]:
                dis.append(1)
            else:
                dis.append(0)
        topo.append(dis)
    return topo

## --- Read the topology, and generate all edges in the given topology.  
def get_edges(topo):
    edges = []    
    for i in range(len(topo)):  
        for j in range(len(topo[0])):  
            if i!=j and topo[i][j]!=0:  
                edges.append((i,j,topo[i][j]))### (i,j) is a link; topo[i][j] here is 1, the length of link (i,j). 
    return edges

## node pair --> switch pair
def get_src_dst_sw(src_dst, sw_node):
    src_dst_sw = {}
    for i in range(len(src_dst)):
        src = src_dst[i][0]
        dst = src_dst[i][1]
        src_sw = -1
        dst_sw = -1
        for j in range(len(sw_node)):
            if src in sw_node[j]:
                src_sw = j
            if dst in sw_node[j]:
                dst_sw = j
            if src_sw != -1 and dst_sw != -1:
                src_dst_sw[i] = (src_sw, dst_sw)
                break    
    return src_dst_sw

## 
def get_slot_num(edges, src_dst, src_dst_sw):
    slot_num = {}   # (pre, next): slot
    total = 0       # total hops
    max_hops = 0    # max. hops
    routes = {}     # num: (src_node, src_sw, ..., dst_sw, dst_node)
    for i in range(len(src_dst_sw)):   
        if src_dst_sw[i][0] != src_dst_sw[i][1]:    # different attached sw
            length, Shortest_path = dijkstra(edges, src_dst_sw[i][0], src_dst_sw[i][1])
            total += length
            if length > max_hops:
                max_hops = length
            routes[i] = []
            routes[i].append(10000+src_dst[i][0])
            for s in range(len(Shortest_path)):
                routes[i].append(Shortest_path[s])
            routes[i].append(10000+src_dst[i][1])
            # src_node --> src_sw
            if (10000+src_dst[i][0], src_dst_sw[i][0]) not in slot_num:
                slot_num[(10000+src_dst[i][0], src_dst_sw[i][0])] = 1
            else:
                slot_num[(10000+src_dst[i][0], src_dst_sw[i][0])] = slot_num[(10000+src_dst[i][0], src_dst_sw[i][0])] + 1
            # src_sw --> dst_sw
            for j in range(len(Shortest_path)-1):
                if (Shortest_path[j], Shortest_path[j+1]) not in slot_num:
                    slot_num[(Shortest_path[j], Shortest_path[j+1])] = 1
                else:
                    slot_num[(Shortest_path[j], Shortest_path[j+1])] = slot_num[(Shortest_path[j], Shortest_path[j+1])] + 1
            # dst_sw --> dst_node
            if (src_dst_sw[i][1], 10000+src_dst[i][1]) not in slot_num:
                slot_num[(src_dst_sw[i][1], 10000+src_dst[i][1])] = 1
            else:
                slot_num[(src_dst_sw[i][1], 10000+src_dst[i][1])] = slot_num[(src_dst_sw[i][1], 10000+src_dst[i][1])] + 1 
        else:   # the same attached sw
            routes[i] = []
            routes[i].append(10000+src_dst[i][0])
            routes[i].append(src_dst_sw[i][0])
            routes[i].append(10000+src_dst[i][1])
            # src_node --> sw
            if (10000+src_dst[i][0], src_dst_sw[i][0]) not in slot_num:
                slot_num[(10000+src_dst[i][0], src_dst_sw[i][0])] = 1
            else:
                slot_num[(10000+src_dst[i][0], src_dst_sw[i][0])] = slot_num[(10000+src_dst[i][0], src_dst_sw[i][0])] + 1  
            # sw --> dst_node
            if (src_dst_sw[i][1], 10000+src_dst[i][1]) not in slot_num:
                slot_num[(src_dst_sw[i][1], 10000+src_dst[i][1])] = 1
            else:
                slot_num[(src_dst_sw[i][1], 10000+src_dst[i][1])] = slot_num[(src_dst_sw[i][1], 10000+src_dst[i][1])] + 1 
    return slot_num, total, max_hops, routes

## get the node pairs which cause the most congested link
def get_node_switch(routes, congestion):
    node_switch = []    # (node pair)
    dataflow = []       # num
    for route in routes.items():
        links = []
        contain = True
        for i in range(len(route[1])-1):
            links.append((route[1][i], route[1][i+1]))
        for link in congestion:
            if link not in links:
                contain = False
                break
        if contain == True:
            node_switch.append((route[1][0]-10000, route[1][-1]-10000))  
            dataflow.append(route[0]) 
    return node_switch, dataflow

## get updated sw_sw after links added
def get_update_sw_sw(sw_sw, sw_node, degree, edges):
    add_link = {}   # sw: dis (degree)
    for i in range(len(sw_sw)):
        dis = degree - (len(sw_node[i]) + len(sw_sw[i]))
        if dis > 0:
            add_link[i] = dis
    pair_dis = {}   # sw pair: dis (hops)
    k = add_link.keys() 
    added_links = []    # sw pair
    if len(k) > 1:
        for i in range(len(k)-1):
            for j in range(i+1, len(k)):
                if k[j] not in sw_sw[k[i]] and k[i] not in sw_sw[k[j]]:
                    len_shortest_path, ret_path = dijkstra(edges, k[i], k[j])
                    pair_dis[(k[i], k[j])] = len_shortest_path
        pair_dis = sorted(pair_dis.items(), lambda x, y: cmp(x[1], y[1]), reverse=True) 
        while len(pair_dis) > 0:
            pair_a = pair_dis[0][0][0]
            pair_b = pair_dis[0][0][1]
            sw_sw[pair_a].append(pair_b) 
            sw_sw[pair_b].append(pair_a) 
            pair_dis.pop(0)
            add_link[pair_a] = add_link[pair_a] - 1
            if add_link[pair_a] == 0:
                #add_link.pop(pair_a)
                for i in pair_dis:
                    if pair_a in i[0]:
                        pair_dis.remove(i)
            add_link[pair_b] = add_link[pair_b] - 1
            if add_link[pair_b] == 0:
                #add_link.pop(pair_b)          
                for i in pair_dis:
                    if pair_b in i[0]:
                        pair_dis.remove(i) 
            added_links.append((pair_a, pair_b))
    return sw_sw, added_links

## replace the most congested path by indirect or parallel paths
def replace_indirect_parallel_path(added_links, slots, dataflow, sw_sw, slot_num, total, routes):
    for pair in added_links: 
        if (pair[0], pair[1]) not in slot_num.keys() or slot_num[(pair[0], pair[1])] < slots - 1:
            for df in dataflow:
                for i in range(len(routes[df])-2):
                    if routes[df][i] == pair[0]: 
                        # indirect path  pair[0]->routes[df][i+1] to pair[0]->pair[1]->routes[df][i+1]
                        if routes[df][i+1] in sw_sw[pair[1]] and ((pair[1], routes[df][i+1]) not in slot_num.keys() or slot_num[(pair[1], routes[df][i+1])] < slots - 1):
                            if (pair[0], pair[1]) not in slot_num:
                                slot_num[(pair[0], pair[1])] = 1
                            else:
                                slot_num[(pair[0], pair[1])] = slot_num[(pair[0], pair[1])] + 1  
                            if (pair[1], routes[df][i+1]) not in slot_num:
                                slot_num[(pair[1], routes[df][i+1])] = 1
                            else:
                                slot_num[(pair[1], routes[df][i+1])] = slot_num[(pair[1], routes[df][i+1])] + 1   
                            slot_num[(pair[0], routes[df][i+1])] = slot_num[(pair[0], routes[df][i+1])] - 1
                            if slot_num[(pair[0], routes[df][i+1])] == 0:
                                slot_num.pop((pair[0], routes[df][i+1]))
                            total = total + 1
                            routes[df].insert(i+1, pair[1])        
                        # parallel path  pair[0]->routes[df][i+1]->routes[df][i+2] to pair[0]->pair[1]->routes[df][i+2]                                 
                        elif routes[df][i+2] in sw_sw[pair[1]] and routes[df][i+1] != pair[1] and ((pair[1], routes[df][i+2]) not in slot_num.keys() or slot_num[(pair[1], routes[df][i+2])] < slots - 1): 
                            if (pair[0], pair[1]) not in slot_num:
                                slot_num[(pair[0], pair[1])] = 1
                            else:
                                slot_num[(pair[0], pair[1])] = slot_num[(pair[0], pair[1])] + 1  
                            if (pair[1], routes[df][i+2]) not in slot_num:
                                slot_num[(pair[1], routes[df][i+2])] = 1
                            else:
                                slot_num[(pair[1], routes[df][i+2])] = slot_num[(pair[1], routes[df][i+2])] + 1   
                            slot_num[(pair[0], routes[df][i+1])] = slot_num[(pair[0], routes[df][i+1])] - 1
                            if slot_num[(pair[0], routes[df][i+1])] == 0:
                                slot_num.pop((pair[0], routes[df][i+1]))
                            slot_num[(routes[df][i+1], routes[df][i+2])] = slot_num[(routes[df][i+1], routes[df][i+2])] - 1
                            if slot_num[(routes[df][i+1], routes[df][i+2])] == 0:
                                slot_num.pop((routes[df][i+1], routes[df][i+2]))                        
                            routes[df].pop(i+1)
                            routes[df].insert(i+1, pair[1])                          
                    elif routes[df][i+2] == pair[1]: 
                        # indirect path  routes[df][i+1]->pair[1] to routes[df][i+1]->pair[0]->pair[1]
                        if routes[df][i+1] in sw_sw[pair[0]] and ((routes[df][i+1], pair[0]) not in slot_num.keys() or slot_num[(routes[df][i+1], pair[0])] < slots - 1):
                            if (pair[0], pair[1]) not in slot_num:
                                slot_num[(pair[0], pair[1])] = 1
                            else:
                                slot_num[(pair[0], pair[1])] = slot_num[(pair[0], pair[1])] + 1  
                            if (routes[df][i+1], pair[0]) not in slot_num:
                                slot_num[(routes[df][i+1], pair[0])] = 1
                            else:
                                slot_num[(routes[df][i+1], pair[0])] = slot_num[(routes[df][i+1], pair[0])] + 1   
                            slot_num[(routes[df][i+1], pair[1])] = slot_num[(routes[df][i+1], pair[1])] - 1
                            if slot_num[(routes[df][i+1], pair[1])] == 0:
                                slot_num.pop((routes[df][i+1], pair[1]))
                            total = total + 1
                            routes[df].insert(i+2, pair[0])     
                        # parallel path  routes[df][i]->routes[df][i+1]->pair[1] to routes[df][i]->pair[0]->pair[1]                                    
                        elif routes[df][i] in sw_sw[pair[0]] and routes[df][i+1] != pair[0] and ((routes[df][i], pair[0]) not in slot_num.keys() or slot_num[(routes[df][i], pair[0])] < slots - 1): 
                            if (pair[0], pair[1]) not in slot_num:
                                slot_num[(pair[0], pair[1])] = 1
                            else:
                                slot_num[(pair[0], pair[1])] = slot_num[(pair[0], pair[1])] + 1  
                            if (routes[df][i], pair[0]) not in slot_num:
                                slot_num[(routes[df][i], pair[0])] = 1
                            else:
                                slot_num[(routes[df][i], pair[0])] = slot_num[(routes[df][i], pair[0])] + 1   
                            slot_num[(routes[df][i+1], pair[1])] = slot_num[(routes[df][i+1], pair[1])] - 1
                            if slot_num[(routes[df][i+1], pair[1])] == 0:
                                slot_num.pop((routes[df][i+1], pair[1]))
                            slot_num[(routes[df][i], routes[df][i+1])] = slot_num[(routes[df][i], routes[df][i+1])] - 1
                            if slot_num[(routes[df][i], routes[df][i+1])] == 0:
                                slot_num.pop((routes[df][i], routes[df][i+1]))                        
                            routes[df].pop(i+1)
                            routes[df].insert(i+1, pair[0])  
                    # indirect path  routes[df][i]->routes[df][i+1] to routes[df][i]->pair[0]->pair[1]->routes[df][i+1]                     
                    elif routes[df][i] in sw_sw[pair[0]] and routes[df][i] != pair[1] and routes[df][i+1] in sw_sw[pair[1]] and routes[df][i+1] != pair[0] and ((routes[df][i], pair[0]) not in slot_num.keys() or slot_num[(routes[df][i], pair[0])] < slots - 1) and ((pair[1], routes[df][i+1]) not in slot_num.keys() or slot_num[(pair[1], routes[df][i+1])] < slots - 1): 
                        if (pair[0], pair[1]) not in slot_num:
                            slot_num[(pair[0], pair[1])] = 1
                        else:
                            slot_num[(pair[0], pair[1])] = slot_num[(pair[0], pair[1])] + 1  
                        if (routes[df][i], pair[0]) not in slot_num:
                            slot_num[(routes[df][i], pair[0])] = 1
                        else:
                            slot_num[(routes[df][i], pair[0])] = slot_num[(routes[df][i], pair[0])] + 1   
                        if (pair[1], routes[df][i+1]) not in slot_num:
                            slot_num[(pair[1], routes[df][i+1])] = 1
                        else:
                            slot_num[(pair[1], routes[df][i+1])] = slot_num[(pair[1], routes[df][i+1])] + 1                      
                        slot_num[(routes[df][i], routes[df][i+1])] = slot_num[(routes[df][i], routes[df][i+1])] - 1
                        if slot_num[(routes[df][i], routes[df][i+1])] == 0:
                            slot_num.pop((routes[df][i], routes[df][i+1]))
                        total = total + 2
                        routes[df].insert(i+1, pair[0])      
                        routes[df].insert(i+2, pair[1])  
                    # indirect path  routes[df][i]->routes[df][i+1]->routes[df][i+2] to routes[df][i]->pair[0]->pair[1]->routes[df][i+2]    
                    elif routes[df][i] in sw_sw[pair[0]] and routes[df][i] != pair[1] and routes[df][i+2] in sw_sw[pair[1]] and routes[df][i+2] != pair[0] and routes[df][i+1] != pair[0] and routes[df][i+1] != pair[1] and ((routes[df][i], pair[0]) not in slot_num.keys() or slot_num[(routes[df][i], pair[0])] < slots - 1) and ((pair[1], routes[df][i+1]) not in slot_num.keys() or slot_num[(pair[1], routes[df][i+1])] < slots - 1): 
                        if (pair[0], pair[1]) not in slot_num:
                            slot_num[(pair[0], pair[1])] = 1
                        else:
                            slot_num[(pair[0], pair[1])] = slot_num[(pair[0], pair[1])] + 1  
                        if (routes[df][i], pair[0]) not in slot_num:
                            slot_num[(routes[df][i], pair[0])] = 1
                        else:
                            slot_num[(routes[df][i], pair[0])] = slot_num[(routes[df][i], pair[0])] + 1   
                        if (pair[1], routes[df][i+2]) not in slot_num:
                            slot_num[(pair[1], routes[df][i+2])] = 1
                        else:
                            slot_num[(pair[1], routes[df][i+2])] = slot_num[(pair[1], routes[df][i+2])] + 1                      
                        slot_num[(routes[df][i], routes[df][i+1])] = slot_num[(routes[df][i], routes[df][i+1])] - 1
                        if slot_num[(routes[df][i], routes[df][i+1])] == 0:
                            slot_num.pop((routes[df][i], routes[df][i+1]))
                        slot_num[(routes[df][i+1], routes[df][i+2])] = slot_num[(routes[df][i+1], routes[df][i+2])] - 1
                        if slot_num[(routes[df][i+1], routes[df][i+2])] == 0:
                            slot_num.pop((routes[df][i+1], routes[df][i+2]))                        
                        total = total + 1
                        routes[df].pop(i+1)
                        routes[df].insert(i+1, pair[0])      
                        routes[df].insert(i+2, pair[1])          
                    # parallel path  routes[df][i]->routes[df][i+1]->routes[df][i+2]->routes[df][i+3] to routes[df][i]->pair[0]->pair[1]->routes[df][i+3]                                            
                    elif i+3<len(routes[df]) and routes[df][i] in sw_sw[pair[0]] and routes[df][i] != pair[1] and routes[df][i+3] in sw_sw[pair[1]] and routes[df][i+3] != pair[0] and routes[df][i+1] != pair[0] and routes[df][i+1] != pair[1] and routes[df][i+2] != pair[0] and routes[df][i+2] != pair[1] and ((routes[df][i], pair[0]) not in slot_num.keys() or slot_num[(routes[df][i], pair[0])] < slots - 1) and ((pair[1], routes[df][i+1]) not in slot_num.keys() or slot_num[(pair[1], routes[df][i+1])] < slots - 1): 
                        if (pair[0], pair[1]) not in slot_num:
                            slot_num[(pair[0], pair[1])] = 1
                        else:
                            slot_num[(pair[0], pair[1])] = slot_num[(pair[0], pair[1])] + 1  
                        if (routes[df][i], pair[0]) not in slot_num:
                            slot_num[(routes[df][i], pair[0])] = 1
                        else:
                            slot_num[(routes[df][i], pair[0])] = slot_num[(routes[df][i], pair[0])] + 1   
                        if (pair[1], routes[df][i+3]) not in slot_num:
                            slot_num[(pair[1], routes[df][i+3])] = 1
                        else:
                            slot_num[(pair[1], routes[df][i+3])] = slot_num[(pair[1], routes[df][i+3])] + 1                      
                        slot_num[(routes[df][i], routes[df][i+1])] = slot_num[(routes[df][i], routes[df][i+1])] - 1
                        if slot_num[(routes[df][i], routes[df][i+1])] == 0:
                            slot_num.pop((routes[df][i], routes[df][i+1]))
                        slot_num[(routes[df][i+1], routes[df][i+2])] = slot_num[(routes[df][i+1], routes[df][i+2])] - 1
                        if slot_num[(routes[df][i+1], routes[df][i+2])] == 0:
                            slot_num.pop((routes[df][i+1], routes[df][i+2]))    
                        slot_num[(routes[df][i+2], routes[df][i+3])] = slot_num[(routes[df][i+2], routes[df][i+3])] - 1
                        if slot_num[(routes[df][i+2], routes[df][i+3])] == 0:
                            slot_num.pop((routes[df][i+2], routes[df][i+3]))                     
                        routes[df].pop(i+1)
                        routes[df].pop(i+1)
                        routes[df].insert(i+1, pair[0])      
                        routes[df].insert(i+2, pair[1])                                      
        if (pair[1], pair[0]) not in slot_num.keys() or slot_num[(pair[1], pair[0])] < slots - 1:
            for df in dataflow:
                for i in range(len(routes[df])-2):
                    if routes[df][i] == pair[1]: 
                        # indirect path  pair[1]->routes[df][i+1] to pair[1]->pair[0]->routes[df][i+1]
                        if routes[df][i+1] in sw_sw[pair[0]] and ((pair[0], routes[df][i+1]) not in slot_num.keys() or slot_num[(pair[0], routes[df][i+1])] < slots - 1): 
                            if (pair[1], pair[0]) not in slot_num:
                                slot_num[(pair[1], pair[0])] = 1
                            else:
                                slot_num[(pair[1], pair[0])] = slot_num[(pair[1], pair[0])] + 1  
                            if (pair[0], routes[df][i+1]) not in slot_num:
                                slot_num[(pair[0], routes[df][i+1])] = 1
                            else:
                                slot_num[(pair[0], routes[df][i+1])] = slot_num[(pair[0], routes[df][i+1])] + 1   
                            slot_num[(pair[1], routes[df][i+1])] = slot_num[(pair[1], routes[df][i+1])] - 1
                            if slot_num[(pair[1], routes[df][i+1])] == 0:
                                slot_num.pop((pair[1], routes[df][i+1]))
                            total = total + 1
                            routes[df].insert(i+1, pair[0])    
                        # parallel path  pair[1]->routes[df][i+1]->routes[df][i+2] to pair[1]->pair[0]->routes[df][i+2]                                     
                        elif routes[df][i+2] in sw_sw[pair[0]] and routes[df][i+1] != pair[0] and ((pair[0], routes[df][i+2]) not in slot_num.keys() or slot_num[(pair[0], routes[df][i+2])] < slots - 1): 
                            if (pair[1], pair[0]) not in slot_num:
                                slot_num[(pair[1], pair[0])] = 1
                            else:
                                slot_num[(pair[1], pair[0])] = slot_num[(pair[1], pair[0])] + 1  
                            if (pair[0], routes[df][i+2]) not in slot_num:
                                slot_num[(pair[0], routes[df][i+2])] = 1
                            else:
                                slot_num[(pair[0], routes[df][i+2])] = slot_num[(pair[0], routes[df][i+2])] + 1   
                            slot_num[(pair[1], routes[df][i+1])] = slot_num[(pair[1], routes[df][i+1])] - 1
                            if slot_num[(pair[1], routes[df][i+1])] == 0:
                                slot_num.pop((pair[1], routes[df][i+1]))
                            slot_num[(routes[df][i+1], routes[df][i+2])] = slot_num[(routes[df][i+1], routes[df][i+2])] - 1
                            if slot_num[(routes[df][i+1], routes[df][i+2])] == 0:
                                slot_num.pop((routes[df][i+1], routes[df][i+2]))                        
                            routes[df].pop(i+1)
                            routes[df].insert(i+1, pair[0])                          
                    elif routes[df][i+2] == pair[0]: 
                        # indirect path  routes[df][i+1]->pair[0] to routes[df][i+1]->pair[1]->pair[0]
                        if routes[df][i+1] in sw_sw[pair[1]] and ((routes[df][i+1], pair[1]) not in slot_num.keys() or slot_num[(routes[df][i+1], pair[1])] < slots - 1): 
                            if (pair[1], pair[0]) not in slot_num:
                                slot_num[(pair[1], pair[0])] = 1
                            else:
                                slot_num[(pair[1], pair[0])] = slot_num[(pair[1], pair[0])] + 1  
                            if (routes[df][i+1], pair[1]) not in slot_num:
                                slot_num[(routes[df][i+1], pair[1])] = 1
                            else:
                                slot_num[(routes[df][i+1], pair[1])] = slot_num[(routes[df][i+1], pair[1])] + 1   
                            slot_num[(routes[df][i+1], pair[0])] = slot_num[(routes[df][i+1], pair[0])] - 1
                            if slot_num[(routes[df][i+1], pair[0])] == 0:
                                slot_num.pop((routes[df][i+1], pair[0]))
                            total = total + 1
                            routes[df].insert(i+2, pair[1])    
                        # parallel path  routes[df][i]->routes[df][i+1]->pair[0] to routes[df][i]->pair[1]->pair[0]                                     
                        elif routes[df][i] in sw_sw[pair[1]] and routes[df][i+1] != pair[1] and ((routes[df][i], pair[1]) not in slot_num.keys() or slot_num[(routes[df][i], pair[1])] < slots - 1): 
                            if (pair[1], pair[0]) not in slot_num:
                                slot_num[(pair[1], pair[0])] = 1
                            else:
                                slot_num[(pair[1], pair[0])] = slot_num[(pair[1], pair[0])] + 1  
                            if (routes[df][i], pair[1]) not in slot_num:
                                slot_num[(routes[df][i], pair[1])] = 1
                            else:
                                slot_num[(routes[df][i], pair[1])] = slot_num[(routes[df][i], pair[1])] + 1   
                            slot_num[(routes[df][i+1], pair[0])] = slot_num[(routes[df][i+1], pair[0])] - 1
                            if slot_num[(routes[df][i+1], pair[0])] == 0:
                                slot_num.pop((routes[df][i+1], pair[0]))
                            slot_num[(routes[df][i], routes[df][i+1])] = slot_num[(routes[df][i], routes[df][i+1])] - 1
                            if slot_num[(routes[df][i], routes[df][i+1])] == 0:
                                slot_num.pop((routes[df][i], routes[df][i+1]))                        
                            routes[df].pop(i+1)
                            routes[df].insert(i+1, pair[1])  
                    # indirect path  routes[df][i]->routes[df][i+1] to routes[df][i]->pair[1]->pair[0]->routes[df][i+1]                     
                    elif routes[df][i] in sw_sw[pair[1]] and routes[df][i] != pair[0] and routes[df][i+1] in sw_sw[pair[0]] and routes[df][i+1] != pair[1] and ((routes[df][i], pair[1]) not in slot_num.keys() or slot_num[(routes[df][i], pair[1])] < slots - 1) and ((pair[0], routes[df][i+1]) not in slot_num.keys() or slot_num[(pair[0], routes[df][i+1])] < slots - 1): 
                        if (pair[1], pair[0]) not in slot_num:
                            slot_num[(pair[1], pair[0])] = 1
                        else:
                            slot_num[(pair[1], pair[0])] = slot_num[(pair[1], pair[0])] + 1  
                        if (routes[df][i], pair[1]) not in slot_num:
                            slot_num[(routes[df][i], pair[1])] = 1
                        else:
                            slot_num[(routes[df][i], pair[1])] = slot_num[(routes[df][i], pair[1])] + 1   
                        if (pair[0], routes[df][i+1]) not in slot_num:
                            slot_num[(pair[0], routes[df][i+1])] = 1
                        else:
                            slot_num[(pair[0], routes[df][i+1])] = slot_num[(pair[0], routes[df][i+1])] + 1                      
                        slot_num[(routes[df][i], routes[df][i+1])] = slot_num[(routes[df][i], routes[df][i+1])] - 1
                        if slot_num[(routes[df][i], routes[df][i+1])] == 0:
                            slot_num.pop((routes[df][i], routes[df][i+1]))
                        total = total + 2
                        routes[df].insert(i+1, pair[1])      
                        routes[df].insert(i+2, pair[0])  
                    # indirect path  routes[df][i]->routes[df][i+1]->routes[df][i+2] to routes[df][i]->pair[1]->pair[0]->routes[df][i+2]    
                    elif routes[df][i] in sw_sw[pair[1]] and routes[df][i] != pair[0] and routes[df][i+2] in sw_sw[pair[0]] and routes[df][i+2] != pair[1] and routes[df][i+1] != pair[1] and routes[df][i+1] != pair[0] and ((routes[df][i], pair[1]) not in slot_num.keys() or slot_num[(routes[df][i], pair[1])] < slots - 1) and ((pair[0], routes[df][i+1]) not in slot_num.keys() or slot_num[(pair[0], routes[df][i+1])] < slots - 1): 
                        if (pair[1], pair[0]) not in slot_num:
                            slot_num[(pair[1], pair[0])] = 1
                        else:
                            slot_num[(pair[1], pair[0])] = slot_num[(pair[1], pair[0])] + 1  
                        if (routes[df][i], pair[1]) not in slot_num:
                            slot_num[(routes[df][i], pair[1])] = 1
                        else:
                            slot_num[(routes[df][i], pair[1])] = slot_num[(routes[df][i], pair[1])] + 1   
                        if (pair[0], routes[df][i+2]) not in slot_num:
                            slot_num[(pair[0], routes[df][i+2])] = 1
                        else:
                            slot_num[(pair[0], routes[df][i+2])] = slot_num[(pair[0], routes[df][i+2])] + 1                      
                        slot_num[(routes[df][i], routes[df][i+1])] = slot_num[(routes[df][i], routes[df][i+1])] - 1
                        if slot_num[(routes[df][i], routes[df][i+1])] == 0:
                            slot_num.pop((routes[df][i], routes[df][i+1]))
                        slot_num[(routes[df][i+1], routes[df][i+2])] = slot_num[(routes[df][i+1], routes[df][i+2])] - 1
                        if slot_num[(routes[df][i+1], routes[df][i+2])] == 0:
                            slot_num.pop((routes[df][i+1], routes[df][i+2]))                        
                        total = total + 1
                        routes[df].pop(i+1)
                        routes[df].insert(i+1, pair[1])      
                        routes[df].insert(i+2, pair[0])    
                    # parallel path  routes[df][i]->routes[df][i+1]->routes[df][i+2]->routes[df][i+3] to routes[df][i]->pair[1]->pair[0]->routes[df][i+3]                                                  
                    elif i+3<len(routes[df]) and routes[df][i] in sw_sw[pair[1]] and routes[df][i] != pair[0] and routes[df][i+3] in sw_sw[pair[0]] and routes[df][i+3] != pair[1] and routes[df][i+1] != pair[1] and routes[df][i+1] != pair[0] and routes[df][i+2] != pair[1] and routes[df][i+2] != pair[0] and ((routes[df][i], pair[1]) not in slot_num.keys() or slot_num[(routes[df][i], pair[1])] < slots - 1) and ((pair[0], routes[df][i+1]) not in slot_num.keys() or slot_num[(pair[0], routes[df][i+1])] < slots - 1): 
                        if (pair[1], pair[0]) not in slot_num:
                            slot_num[(pair[1], pair[0])] = 1
                        else:
                            slot_num[(pair[1], pair[0])] = slot_num[(pair[1], pair[0])] + 1  
                        if (routes[df][i], pair[1]) not in slot_num:
                            slot_num[(routes[df][i], pair[1])] = 1
                        else:
                            slot_num[(routes[df][i], pair[1])] = slot_num[(routes[df][i], pair[1])] + 1   
                        if (pair[0], routes[df][i+3]) not in slot_num:
                            slot_num[(pair[0], routes[df][i+3])] = 1
                        else:
                            slot_num[(pair[0], routes[df][i+3])] = slot_num[(pair[0], routes[df][i+3])] + 1                      
                        slot_num[(routes[df][i], routes[df][i+1])] = slot_num[(routes[df][i], routes[df][i+1])] - 1
                        if slot_num[(routes[df][i], routes[df][i+1])] == 0:
                            slot_num.pop((routes[df][i], routes[df][i+1]))
                        slot_num[(routes[df][i+1], routes[df][i+2])] = slot_num[(routes[df][i+1], routes[df][i+2])] - 1
                        if slot_num[(routes[df][i+1], routes[df][i+2])] == 0:
                            slot_num.pop((routes[df][i+1], routes[df][i+2]))    
                        slot_num[(routes[df][i+2], routes[df][i+3])] = slot_num[(routes[df][i+2], routes[df][i+3])] - 1
                        if slot_num[(routes[df][i+2], routes[df][i+3])] == 0:
                            slot_num.pop((routes[df][i+2], routes[df][i+3]))                     
                        routes[df].pop(i+1)
                        routes[df].pop(i+1)
                        routes[df].insert(i+1, pair[1])      
                        routes[df].insert(i+2, pair[0])  
    return slot_num, total, routes

## not used
def optimize_links(sw_sw, sw_node, degree, edges, src_dst):
    sw_sw, added_links = get_update_sw_sw(sw_sw, sw_node, degree, edges)
#     print "added_links: ", str(added_links)
#     print "sw_sw (renewed): ", str(sw_sw)                  
    topo = get_topo(sw_sw)
    edges = get_edges(topo) 
    src_dst_sw = get_src_dst_sw(src_dst, sw_node)
#     print "src_dst: ", str(src_dst)
#     print "src_dst_sw: ", str(src_dst_sw)   
    slot_num, total, routes = get_slot_num(edges, src_dst, src_dst_sw)    
#     print "routes: ", routes
    avg = (float)(total)/len(src_dst_sw)
#     print "average hops: ", str(avg)
    slots = max(slot_num.values())
#     print "max number of slots: ", str(slots)
#     print "links with max number of slots:",
    congestion = []
    for i in slot_num.keys():
        if slot_num[i] == slots:
            congestion.append(i)   
#     print congestion    
    node_switch, dataflow = get_node_switch(routes, congestion)
    slot_num, total, routes = replace_indirect_parallel_path(added_links, slots, dataflow, sw_sw, slot_num, total, routes)                        
#     print "routes updated: ", routes
    avg = (float)(total)/len(src_dst_sw)
#     print "average hops: ", str(avg)
    slots = max(slot_num.values())
#     print "max number of slots: ", str(slots)
#     print "links with max number of slots:",
    congestion = []
    for i in slot_num.keys():
        if slot_num[i] == slots:
            congestion.append(i)   
#     print congestion
    links = 0
    for item in sw_sw.values():
        links = links + len(item)
    links = links/2
    return slots, avg, len(sw_sw), links

## print result
def print_result(routes, total, src_dst_sw, slot_num):
#     print "routes: ", routes
    avg = (float)(total)/len(src_dst_sw)
    # print "average switch hops: ", str(avg)
    slots = max(slot_num.values())
    # print "max number of slots: ", str(slots)
#     print "links with max number of slots:",
    congestion = []
    for i in slot_num.keys():
        if slot_num[i] == slots:
            congestion.append(i)   
#     print congestion    
    return slots, congestion, avg
