# This program starts from a Tulip graph and builds a longitudinal dataset focused on edges of the graph.
# see https://docs.google.com/document/d/1y46k6Q1wrMhYDEezMwQb5EH2wwKzIN-tkJnpbOiUiAA/edit

# The final data have the form:
# source, target, timestamp, source metrics, targetmetrics, weight
# question: how do I deal with the time dimension? If nodes A and B have not been created yet at time t,
# do I consider them as "zero weight" only from the creation date of the last among them?


# UNICODE: "u'Something"
from __future__ import division


from tulip import *
import json
import csv
import datetime
import time



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


    # Due to a Tulip bug I have to make a manual import.
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

    print 'Building flickering edges subgraphs...'
    dateProperty = graph.getDoubleProperty('timestamp')
	
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
    tlp.saveGraph(graph, dirPath+"/To_Guy/ERgraph_w_fe_subgraphs_57.tlp")
