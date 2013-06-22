# This code needs to be inserted after subgraphs are created.
# It creates t subgraphs with no parallel edges.
# If a source-target pair is connected by at least one edge in the "normal" subgraph
# it is connected by one single edge in the dp (de-parallized) subgraph.
# Such edge has weight = number of parallel edges for same source-target pair
# and effort = sum of efforts of said parallel edges.


    # much earlier, when creating properties:
    
    weightProperty = graph.getIntegerProperty('weight')
    # weightProperty is for deparallelized, weighted subgraphs.
    # weightProperty is then initialized to 1 for all edges.

    

    # create deparallelized subgraphs

    print 'Creating deparallelized subgraphs...'

    for time in range(time_0, time_final, timestep):
        # add nodes. This can be done in one pass.
        dpsg = graph.addSubGraph()
        dpsg.setName('dp_' + str(time))
        print 'Now building subgraph ' + str (dpsg.getName()
        for n in graph.getNodes():
            if dateProperty.getNodeValue(n) <= time:
                dpsg.addNode(n)

        # to add edges, iterate over nodes in the newly built subgraph and look for unique neighbors.

        for n in dpsg.getNodes():
            dictOutNeighbors = {}
            for e in graph.getOutEdges(n): # this iteration happens over the MAIN graph.

                if dateProperty.getEdgeValue(e) <= int(time):

                    neighbor = graph.target(e)
                    if neighbor not in dictOutNeighbors:
                        dictOutNeighbors[neighbor] = []
                        sc = graph.source(e)
                        tg = graph.target(e)
                        newEdge = dpsg.addEdge(sc,tg) # notice: add new edge, not reuse e.
                        # now populate the properties of this edge.
                        weightProperty[newEdge] = 1
                        effortProperty[newEdge] = effortProperty[e] 
                        
                    else:
                        # iterate over OutEdges already added to the new subgraph and look for the one
                        # with the same target as e.
                        for e2 in dpsg.getOutEdges(n):
                            if neighbor == dpsg.target(e2):
                                weightProperty[e2] += 1
                                effortProperty[e2] = effortProperty[e2] + effortProperty[e]
                    

    tlp.saveGraph(graph, dirPath+"/ERgraph_w_dp_subgraphs_ben.tlp")
