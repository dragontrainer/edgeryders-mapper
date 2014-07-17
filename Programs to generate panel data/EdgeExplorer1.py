# TODO: 1. test this version. 2. figure out how to add the 'impossible edges'

# This program starts from a Tulip graph and builds a longitudinal dataset focused on edges of the graph.
# see https://docs.google.com/document/d/1y46k6Q1wrMhYDEezMwQb5EH2wwKzIN-tkJnpbOiUiAA/edit

# The final data have the form:
# source, target, timestamp, source metrics, targetmetrics, weight
# question: how do I deal with the time dimension? If nodes A and B have not been created yet at time t,
# do I consider them as "zero weight" only from the creation date of the last among them?


# UNICODE: "u'Something
from __future__ import division


import sys
sys.path.append ('/Users/albertocottica/Dropbox/PhD/MyPhDcode')

from tulip import *
import json
import csv
import datetime
import time
from tulip2networkx import *
from modularity import * 

# define the non-main function(s) needed:


def findNodeById(id, graph, idProperty):
    '''
      finds a node if it exists / return None otherwise. 
      '''
    for n in graph.getNodes():
        if idProperty[n] == id:
            return n
    return None
    


def drupal_to_unix_time(datestring):
    '''
    str => int 
    returns the Unix time corresponding to datestring of the type '14 Oct 2011 - 16:55'
    >>> drupal_to_unixtime('14 Oct 2011 - 16:55')
    requires time module
    XXXXXXXXXXXX
    >>>
    '''
    import time
    import datetime

    # convert the month, given in letter, into an int:

    # convert the month, given in letter, into an int:
    monthint = 666

    if datestring [-16:-13] == 'Jan':
        monthint = 1
    elif datestring [-16:-13] == 'Feb':
        monthint = 2
    elif datestring [-16:-13] == 'Mar':
        monthint = 3
    elif datestring [-16:-13] == 'Apr':
        monthint = 4
    elif datestring [-16:-13] == 'May':
        monthint = 5
    elif datestring [-16:-13] == 'Jun':
        monthint = 6
    elif datestring [-16:-13] == 'Jul':
        monthint = 7
    elif datestring [-16:-13] == 'Aug':
        monthint = 8
    elif datestring [-16:-13] == 'Sep':
        monthint = 9
    elif datestring [-16:-13] == 'Oct':
        monthint = 10
    elif datestring [-16:-13] == 'Nov':
        monthint = 11
    elif datestring [-16:-13] == 'Dec':
        monthint = 12
    else:
        monthint = 0

    # convert the string to a string in a time tuple: (YYYY, MM, DD, HH, MM, SS, 0, 0, 0)
    datetuple = (int(datestring[-12:-8]), monthint, int(datestring[:-17]), int(datestring[-5:-3]), int(datestring[-2:]), 0, 0, 0, 0)
    # now use time to convert the time tuple into UTC
    return (int(time.mktime(datetuple)))


def display(node, graph):
    print('node tulip id ', node.id)
    uid = graph.getIntegerProperty('user_id')
    print('user_id ',  uid[node])
    isteam = graph.getBooleanProperty('is_team')
    print('is team ',  isteam[node])
    date = graph.getIntegerProperty('timestamp')
    print ('creation date ', date[node])

def getNodeMetrics(node, graph, nodeMetricNames): 
    '''
    (node, graph, list) => dict
    Returns a dictionary in which the keys are the names of the metrics in nodeMetricsNames
    stored as node properties; the values are the metric values.
    '''
    cNode = {}
    for metricName in nodeMetricNames:
        p = graph.getProperty(metricName)
        if not p:
            continue
        
        pType = p.getTypename()
        if pType == "string":
                p = graph.getStringProperty(metricName)
        elif pType == "bool":
                p = graph.getBooleanProperty(metricName)
        elif pType == "double":
                p = graph.getDoubleProperty(metricName)
        elif pType == "int":
                p = graph.getIntegerProperty(metricName)
        cNode [metricName] = p[node]
    return cNode


# define the main method

# Powered by Python 2.7

# To cancel the modifications performed by the script
# on the current graph, click on the undo button.

# Some useful keyboards shortcuts : 
#   * Ctrl + D : comment selected lines.
#   * Ctrl + Shift + D  : uncomment selected lines.
#   * Ctrl + I : indent selected lines.
#   * Ctrl + Shift + I  : unindent selected lines.
#   * Ctrl + Return  : run script.
#   * Ctrl + F  : find selected text.
#   * Ctrl + R  : replace selected text.
#   * Ctrl + Space  : show auto-completion dialog.

# the updateVisualization(centerViews = True) function can be called
# during script execution to update the opened views

# the pauseScript() function can be called to pause the script execution.
# To resume the script execution, you will have to click on the "Run script " button.

# the runGraphScript(scriptFile, graph) function can be called to launch another edited script on a tlp.Graph object.
# The scriptFile parameter defines the script name to call (in the form [a-zA-Z0-9_]+.py)

# the main(graph) function must be defined 
# to run the script on the current graph

# GM - creating the userlis and commentlist as local variables
# GM - is not that handy (at least for debugging)
# GM - we'll turn them into global variables and pass them on to the main method

def main(graph): 
    viewBorderColor =  graph.getColorProperty("viewBorderColor")
    viewBorderWidth =  graph.getDoubleProperty("viewBorderWidth")
    viewColor =  graph.getColorProperty("viewColor")
    viewFont =  graph.getStringProperty("viewFont")
    viewFontSize =  graph.getIntegerProperty("viewFontSize")
    viewLabel =  graph.getStringProperty("viewLabel")
    viewLabelColor =  graph.getColorProperty("viewLabelColor")
    viewLabelPosition =  graph.getIntegerProperty("viewLabelPosition")
    viewLayout =  graph.getLayoutProperty("viewLayout")
    viewMetaGraph =  graph.getGraphProperty("viewMetaGraph")
    viewRotation =  graph.getDoubleProperty("viewRotation")
    viewSelection =  graph.getBooleanProperty("viewSelection")
    viewShape =  graph.getIntegerProperty("viewShape")
    viewSize =  graph.getSizeProperty("viewSize")
    viewSrcAnchorShape =  graph.getIntegerProperty("viewSrcAnchorShape")
    viewSrcAnchorSize =  graph.getSizeProperty("viewSrcAnchorSize")
    viewTexture =  graph.getStringProperty("viewTexture")
    viewTgtAnchorShape =  graph.getIntegerProperty("viewTgtAnchorShape")
    viewTgtAnchorSize =  graph.getSizeProperty("viewTgtAnchorSize")

    for n in graph.getNodes():
        print n

    # import the graph
    dataSet = tlp.getDefaultPluginParameters("TLP Import", graph)
    dataSet["file::filename"] = "/Users/albertocottica/Dropbox/PhD/MyPhDdata/Extraction 2012-12-05-1623/To_Guy/ERgraph_w_dp_subgraphs_57.tlp"
    tlp.importGraph("TLP Import", dataSet, graph)
    
    # if this does not work (it may crash Tulip), make a manual import.
    # open the Tulip GUI, import the graph file
    # /Users/albertocottica/Dropbox/PhD/MyPhDdata/Extraction 2012-12-05-1623/To_Guy/ERgraph_w_dp_subgraphs_57.tlp
    dirPanelPath = '/Users/albertocottica/edgeryders-mapper/Panel data/'
    dirGraphPath = '/Users/albertocottica/edgeryders-mapper/Network data/'
    #   graph = tlp.loadGraph(dirGraphPath+ 'ERgraph_w_subgraphs.tlp')

    # Start reading the files

    dirPath = '/Users/albertocottica/Dropbox/PhD/MyPhDdata/Extraction 2012-12-05-1623/'

    # assign the time interval step in UNIX time: 4 weeks == 2419200

    timestep = int(2419200/4) #corresponds to ONE week
    time_0 = 1321228800 # corresponds to November 14th 2011
    time_final = 1355529600
          
    # now create the subgraphs with "flickering" edges. Refer to line 196.
    # nodes are added from the deparallelized subgraphs.
    # edges are added from the main graph

    # recall properties of nodes
    my_ID_var = graph.getIntegerProperty('user_id')
    user_name = graph.getStringProperty('user_name')
    is_team = graph.getBooleanProperty('team')
    dateProperty = graph.getDoubleProperty('timestamp')

    print 'Building flickering edges subgraphs...'

    for t in range(time_0, time_final, timestep):
        # build graph with items having (t-1) <= timestamp <= t
        fesg = graph.addSubGraph()
        fesg.setName('fe_' + str(t))
        dpsgName = ('dp_' + str(t))
        dpsg = graph.getSubGraph(dpsgName)
        for n in dpsg.getNodes():
            fesg.addNode(n)
        for e in dpsg.getEdges():
            if dateProperty.getEdgeValue(e) <= t and dateProperty.getEdgeValue(e) > (t - timestep):
                fesg.addEdge(e)    
    tlp.saveGraph(graph, dirPath+"/To_Guy/ERgraph_w_fe_subgraphs_57.tlp")

    # In order to create my panel dataset, I iterate first by subgraph (period), then by source node
    # I have to use deparallelized subgraphs. This loses topic data. What the hell.
    # For each node at each point in time I have to output a list

    nodeMetricNames = ['Cluster', 'K-Cores', 'Page Rank', 'averageClusteringCoefficient','betweennessCentralityCount', 'currentCluster', 'graphDensity', 'modularityCount', 'team', 'timestamp', 'user_id']
    results = {}
    for t in range(time_0, time_final, timestep):
        fesg = graph.getSubGraph ('fe_' + str(t))
        periodDictName = str(t)
        periodDict = {}
        print ('now harvesting graph for period ' + periodDictName + ' ...')
        
        for sourceNode in fesg.getNodes():
            # grab node metrics via a function
            sourceNodeMetrics = getNodeMetrics(sourceNode, fesg, nodeMetricNames)
            sourceNodeObj = fesg.getIntegerProperty('user_id')
            sourceNodeName = str (sourceNodeObj[sourceNode])
            for targetNode in fesg.getNodes():
                edgeDict = {} # initialize a dict for this edge
                #now grab target metrics
                targetNodeMetrics = getNodeMetrics(targetNode, fesg, nodeMetricNames) 
                targetNodeObj = fesg.getIntegerProperty('user_id')
                targetNodeName = str (targetNodeObj[targetNode])
                # finds the key in results of which edgeDictName is the value
                edgeDictName = 'edge_' + sourceNodeName + '_' + targetNodeName 
                # tested so far less the function
                # populate the edge dictionary                
                # both source- and targetNodeMetrics are dicts of the form:
                # 'Page Rank' = '0.78'
                for metric in sourceNodeMetrics:
                    edgeDict ['sn_' + metric] = sourceNodeMetrics [metric]
                    edgeDict ['tn_' + metric] = targetNodeMetrics [metric]
                    nodeObj = fesg.getIntegerProperty('user_id')
                    edgeDict ['source'] = nodeObj[sourceNode]
                    edgeDict ['target'] = nodeObj[targetNode]
                # now I need to check for the existence of the edge.
                # I do it in this loop using an iteration on fesg.getInEdges(targetNode)
                # and looking if sourceNode in an in-neighbour.
                testEdge = fesg.existEdge(sourceNode, targetNode, True)
                if testEdge.isValid():
                    edgeDict ['edge'] = 1
                else:
                    edgeDict ['edge'] = 0
                periodDict [edgeDictName] = edgeDict
                # writes edgeDict as a value within periodDict. Key is the name identifying source and target nodes

        results [periodDictName] = periodDict
        # writes periodDict as a value within results
            
                    
 # so far, so good!

 # Now I need to generate the line of the CSV corresponding to each edge at each point in time.
 # For now I ignore topics, but edges carry semantic information about topics
 

    # print the csv file

##    print 'Writing the output to file...'
##    topics = ['01 - Bootcamp', '02 - Making a living', '03 - We, the people', '04 - Caring for commons', '05 - Learning',
##                  '06 - Living together', '07 -Finale', '08 - Resilience', '00 - Undefined']
##    
##    # print headers to csv file
##    csvfile = open(dirPath + 'edgeTabData1.csv', 'w')
##    activityMetricNames = []
##    for topic in topics:
##        activityMetricNames.append('NPosts in ' + topic)
##        activityMetricNames.append('EPosts in ' + topic)
##    for topic in topics:
##        activityMetricNames.append('NComms written in ' + topic)
##        activityMetricNames.append('EComms written in ' + topic)
##    for topic in topics:
##        activityMetricNames.append('NTeam comms received in ' + topic)
##        activityMetricNames.append('ETeam comms received in ' + topic)
##    for topic in topics:
##        activityMetricNames.append('NComms received in ' + topic)
##        activityMetricNames.append('EComms received in ' + topic)
##
##    neighboringMetricNames = ['Indegree','Outdegree']
##    dpGraphMetricNames = ['betweennessCentralityCount', 'betweennessCentralityEffort', 'graphDensity', 'modularityCount', 'modularityEffort', 'averageClusteringCoefficient'] 
##
##
##    fieldNames = ['node id', 'is_team', 'creation date', 'timestamp'] + activityMetricNames + nodeMetricNames + neighboringMetricNames + dpGraphMetricNames
##    csvwriter = csv.DictWriter(csvfile, fieldNames, delimiter = ',')
##    csvwriter.writerow(dict((fn,fn) for fn in fieldNames))
##
##    # node id, creation y/n, time considered, number of posts and effort of posts written per each topic, number and effort
##    # of comments received per each topic, number and effort team of comments received per each topic, 
##    for n in graph.getNodes():
##        user_i_time_t = {} # the accumulator for the row
##        user_i_time_t['node id'] = str(my_ID_var[n])
##        print 'Now processing user ', str(my_ID_var[n])
##        user_i_time_t['creation date'] = (str(dateProperty[n]))
##        user_i_time_t['is_team'] = int(is_team[n])
##
##        # iterate over time periods, grabbing the relevant subgraph for each one
##        for t in range(time_0, time_final, timestep):
##            sg = graph.getSubGraph(str(t))
##
##            user_i_time_t['timestamp'] = (str(t))
##            # print 'processing subgraph: ', str(t)
##            
##            # Initialize accumulators:
##            user_i_time_t['Indegree'] = 0
##            user_i_time_t['Outdegree'] = 0
##
##            for metric in activityMetricNames:
##                user_i_time_t[metric] = 0
##
##            for metric in nodeMetricNames:
##                user_i_time_t[metric] = 0
##
##            if not sg.isElement(n):
##                # assign default values
##                csvwriter.writerow(user_i_time_t)
##                continue
##
##            for metric in nodeMetricNames:
##                metricProperty = sg.getLocalDoubleProperty(metric)
##                user_i_time_t[metric] = metricProperty[n]
##            
##            # fill in the posts written by this user at this time.
##            for x in range (len(postslist)):
##                # 14 Oct 2011 - 16:55 %d %b %Y - %H:%M
##                if str(postslist[x]['author_id']) == str(my_ID_var[n]) and \
##                   (time.mktime(time.strptime(postslist[x]['date'], "%d %b %Y - %H:%M")) < t) and \
##                   (time.mktime(time.strptime(postslist[x]['date'], "%d %b %Y - %H:%M")) >= t - timestep):
##                    for topic in topics:
##                        if postslist[x]['topic'] == topic:
##                            user_i_time_t['NPosts in ' + topic] += 1
##                            user_i_time_t['EPosts in ' + topic] += int(postslist[x]['effort'])
##
##
##            dictInNeighbors = {}
##            for e in sg.getInEdges(n):
##                # grabbing unique in neighbors
##                neighbor = sg.source(e)
##                if neighbor not in dictInNeighbors:
##                    dictInNeighbors[neighbor] = []
##                dictInNeighbors[neighbor].append(e)
##                # counting comments and effort to our user
##
##                eTimestamp = dateProperty[e]
##                eTopic = topicProperty[e]
##                effort = int(effortProperty[e])
##                #print "timestamp: ", dateProperty[e], "/", (t - timestep), " >> ", (dateProperty[e] >= (t - timestep))
##                if dateProperty[e] >= (t - timestep):
##                    # this is to avoid multiple counting of comments left in previous periods (edges endure).
##                    if is_team[e]:
##                        user_i_time_t['NTeam comms received in ' + eTopic] += 1
##                        user_i_time_t['ETeam comms received in ' + eTopic] += effort
##                    else:
##                        user_i_time_t['NComms received in ' + eTopic] += 1
##                        user_i_time_t['EComms received in ' + eTopic] += effort
##
##
##            dictOutNeighbors = {}
##            for e in sg.getOutEdges(n):
##                # grabbing unique out neighbors
##                neighbor = sg.target(e)
##                if neighbor not in dictOutNeighbors:
##                    dictOutNeighbors[neighbor] = []
##                dictOutNeighbors[neighbor].append(e)
##
##                # counting comments and effort from our user
##                if dateProperty[e] > (int(t) - timestep) and dateProperty[e] <= int(t): # not sure about this
##                    eTopic = topicProperty[e]
##                    effort = int(effortProperty[e])
##                    user_i_time_t['NComms written in ' + eTopic] += 1
##                    user_i_time_t['EComms written in ' + eTopic] += effort
##
##
##
##            user_i_time_t['Indegree'] = len(dictInNeighbors)
##            user_i_time_t['Outdegree'] = len(dictOutNeighbors)
##
##        
##            # now metrics pertaining to the deparallelized graphs (dpGraphMetrics). First, grab the deparallelized graph.
##            dpsg = graph.getSubGraph('dp_' + str(t))
##
##            for metric in dpGraphMetricNames:
##                metricProperty = dpsg.getDoubleProperty(metric)
##                user_i_time_t[metric] = metricProperty[n]
##                
##                           
##            csvwriter.writerow(user_i_time_t)
##
##
##
##    csvfile.close()
##    print ("The end")
    


