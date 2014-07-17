# TODO: 1. test this version. 2. figure out how to add the 'impossible edges'

# This program starts from a Tulip graph and builds "flickering edges" subgraphs
# Each subgraph correspond to a time period.
# the dpsg_ subgraphs nodes store the node properties
# the fesg_ subgraph store the connectivity,
# to become boolean variables with  value 1 is an edge is present IN THAT PERIOD and 0 otherwise-

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
    #print node, graph, nodeMetricNames
    cNode = {}
    for metricName in nodeMetricNames:
        p = graph.getProperty(metricName)
        #print metricName,': ', graph.existProperty(metricName)        
        #print metricName,': ', graph.existLocalProperty(metricName)        
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
    #graph.clear()
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

    #for n in graph.getNodes():
    #    print n

    # import the graph
    #dataSet = tlp.getDefaultPluginParameters("TLP Import", graph)
    #dataSet["file::filename"] = "/Users/albertocottica/Dropbox/PhD/MyPhDdata/Extraction 2012-12-05-1623/To_Guy/ERgraph_w_dp_subgraphs_57.tlp"
    #dataSet["file::filename"] = "/work/AlbertoThesis/ERgraph_w_dp_subgraphs.tlp"
    #tlp.importGraph("TLP Import", dataSet, graph)
    
    # if this does not work (it may crash Tulip), make a manual import.
    # open the Tulip GUI, import the graph file
    # /Users/albertocottica/Dropbox/PhD/MyPhDdata/Extraction 2012-12-05-1623/To_Guy/ERgraph_w_dp_subgraphs_57.tlp
   
    ##dirPanelPath = '/Users/albertocottica/edgeryders-mapper/Panel data/'
    ##dirGraphPath = '/Users/albertocottica/edgeryders-mapper/Network data/'
    
    #   graph = tlp.loadGraph(dirGraphPath+ 'ERgraph_w_subgraphs.tlp')

    # Start reading the files

    dirPath = '/Users/albertocottica/Dropbox/PhD/MyPhDdata/Extraction 2012-12-05-1623/'
    # dirPath = '/work/AlbertoThesis//'

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
        for n in graph.getNodes():
            if dateProperty.getNodeValue(n) <= t:
                fesg.addNode(n)
        for e in graph.getEdges():
            if dateProperty.getEdgeValue(e) <= t and dateProperty.getEdgeValue(e) > (t - timestep):
                fesg.addEdge(e)    
    tlp.saveGraph(graph, dirPath+"/ERgraph_w_fe_subgraphs_10.tlp")

