# This program accepts a list of users and a list of comments as CSV files and builds the associated graph.
# In this version I am not loading nodes. Not sure yet whether I need them.

# UNICODE: "u'Something"



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


    # Start reading the files
    dirPath = '/Users/albertocottica/Dropbox/PhD/MyPhDdata/Extraction 2012-12-05-1623/'

    # Here's the output file: REMEMBER TO CHANGE THIS
    # to_filename = dirPath + 'output.csv'
    # to_file = open(to_filename, 'w')

    # load comments
    comments_filename = dirPath + 'commentslist.csv'
    comments_reader = csv.DictReader(open(comments_filename, 'rb'), delimiter=',')
    commentslist = []
    for line in comments_reader:
        commentslist.append(line)

    # load posts
    posts_filename = dirPath + 'postslist.csv' 
    posts_reader = csv.DictReader(open(posts_filename, 'rb'), delimiter=',')
    postslist = []
    for line in posts_reader:
          postslist.append(line)
    

    # load users
    users_filename = dirPath + 'userlist_w_xusers.csv' 
    users_reader = csv.DictReader(open(users_filename, 'rb'), delimiter=',')
    userlist = []
    for line in users_reader:
        userlist.append(line)

    # assign the time interval step in UNIX time: 4 weeks == 2419200

    timestep = 2419200 #corresponds to four weeks
    time_0 = 1321228800 # corresponds to November 14th 2011
    time_final = 1355529600
    

    # We build the graph


    # graph = tlp.newgraph() # when executing from within Tulip GUI, you omit this. The empty graph is loaded by default.

    # GM - I am unsure what this instruction does
    # GM - I'll assume we are working with a brand new, empty,
    # GM - graph so we don't need to invoke this method
    # graph = graph.clear()

    print 'Building graph...'

    # create the properties of nodes 
    my_ID_var = graph.getIntegerProperty('user_id')
    user_name = graph.getStringProperty('user_name')
    is_team = graph.getBooleanProperty('team')
    dateProperty = graph.getIntegerProperty('timestamp')
    # dateProperty stores the account creation date of node (user)
    # dateProperty stores the publication date of a comment (edge)
    effortProperty = graph.getIntegerProperty('effort')
    # effortProperty stores the length of the comment.
    topicProperty = graph.getStringProperty('topic')
    briefIDProperty = graph.getStringProperty('brief_id')
    #topicProperty stores the Edgeryders campaign under which the comment is nested.
    #briefIDProperty stores the Edgeryders mission brief under which the comment is nested.

    # create nodes and populate their properties.
    for u in range (len (userlist)):
        n = graph.addNode()
        my_ID_var[n] = int (userlist[u]['user_id']) # the name my_ID_var is to distinguish it from Tulip's internally assigned node ID.
        # user_name[n] = userlist[u]['user_id'] # this property runs into unicode errors
        is_team[n] = bool (int(userlist[u]['team'])) #this property loads as always true! 
        dateProperty[n] = time.mktime(time.strptime(userlist[u]['joindate'], '%Y-%m-%d'))
        #print ('Node ' + str(n) + ' created, with id ', my_ID_var[n])
        #print (str(u) + ' nodes created.')

    # now create edges. Loop over comments:
    
    for comment in commentslist:
        # comment

        # GM - the following line throws an exception 'KeyError'
        # GM - and says the 'nid' key does not exist
        #print comment

        if not comment['author_id'] == '0':
            if not comment['target_id'] == '0': # we weed out comments that don't refer to valid users
    
                sid = int(comment['author_id'])
                tid = int(comment['target_id'])
                sNode = findNodeById(sid, graph, my_ID_var) 
                tNode = findNodeById(tid, graph, my_ID_var)

                try:
                    edge = graph.addEdge(sNode, tNode)
                except TypeError:
                    print(sid, sNode)
                    print(tid, tNode)
                    print '***'
                    pass

            # add property values to this edge
            # ...
                dateProperty[edge] = int(comment['timestamp'])
                effortProperty[edge] = int(comment['effort'])
                is_team[edge] = int(comment['author_team'])
                topicProperty[edge] = comment['topic']
                briefIDProperty[edge] = comment['brief_id']

    tlp.saveGraph(graph, (dirPath + 'To Guy/ERgraph_no_subgraphs.tlp'))

    # create subgraphs

    print 'Building subgraphs...'

    for t in range(time_0, time_final, timestep):
        # build graph with items having timestamp <= t
        sg = graph.addSubGraph()
        sg.setName(str(t))
        for n in graph.getNodes():
            if dateProperty.getNodeValue(n) <= t:
                sg.addNode(n)
        for e in graph.getEdges():
            if dateProperty.getEdgeValue(e) <= t:
                sg.addEdge(e)

    # compute node-specific network properties

    nodeMetricNames = ['Betweenness Centrality', 'Cluster', 'K-Cores', 'PageRank']#, 'Eccentricity'] # add more ...
    #nodeMetricProperties = {}
    for sg in graph.getSubGraphs():

        # compute subgraph metrics and store as local properties
        for metricName in nodeMetricNames:
            resultProperty = sg.getLocalDoubleProperty(metricName)
            dataSet = tlp.getDefaultPluginParameters(metricName, sg)
            # WARNING THE PROPERTY IS OVERWRITTEN HERE THROUGH DIFFERENT SUBGRAPH
            #nodeMetricProperties[metricName] = resultProperty
            sg.applyDoubleAlgorithm(metricName, resultProperty, dataSet)
            
    tlp.saveGraph(graph, (dirPath + "/To Guy/ERgraph_w_subgraphs.tlp"))


    
##       here starts the dynamic (bigtable) part. 

    print 'Writing the output to file...'
    topics = ['01 - Bootcamp', '02 - Making a living', '03 - We, the people', '04 - Caring for commons', '05 - Learning',
                  '06 - Living together', '07 -Finale', '08 - Resilience', '00 - Undefined']
    
    # print headers to csv file
    csvfile = open(dirPath + 'subGraphsTabData4.csv', 'w')
    activityMetricNames = []
    for topic in topics:
        activityMetricNames.append('NPosts in ' + topic)
        activityMetricNames.append('EPosts in ' + topic)
    for topic in topics:
        activityMetricNames.append('NComms written in ' + topic)
        activityMetricNames.append('EComms written in ' + topic)
    for topic in topics:
        activityMetricNames.append('NTeam comms received in ' + topic)
        activityMetricNames.append('ETeam comms received in ' + topic)
    for topic in topics:
        activityMetricNames.append('NComms received in ' + topic)
        activityMetricNames.append('EComms received in ' + topic)

    neighboringMetricNames = ['Indegree','Outdegree']
    fieldNames = ['node id', 'is_team', 'creation date', 'timestamp'] + activityMetricNames + nodeMetricNames + neighboringMetricNames
    csvwriter = csv.DictWriter(csvfile, fieldNames, delimiter = ',')
    csvwriter.writerow(dict((fn,fn) for fn in fieldNames))

    # node id, creation y/n, time considered, number of posts and effort of posts written per each topic, number and effort
    # of comments received per each topic, number and effort team of comments received per each topic, 
    for n in graph.getNodes():
        user_i_time_t = {} # the accumulator for the row
        user_i_time_t['node id'] = str(my_ID_var[n])
        # print 'Now processing user ', str(my_ID_var[n])
        user_i_time_t['creation date'] = (str(dateProperty[n]))
        user_i_time_t['is_team'] = int(is_team[n])
        
        for sg in graph.getSubGraphs():
            # for t in range(time_0, time_final, timestep):
            t = int(sg.getName())
            user_i_time_t['timestamp'] = (str(t))
            # print 'processing subgraph: ', str(t)
            
            # I am using dicts as accumulators of comments written and received. Reason: so I don't get lost in indices while programming.
            # each accumulator dict's elements are lists of 2 elements. The first is the number of comments/posts; the second is 
            # the sum of their lengths, and can be thought of as effort level.

            # Initialize accumulators:
            user_i_time_t['Indegree'] = 0
            user_i_time_t['Outdegree'] = 0

            for metric in activityMetricNames:
                user_i_time_t[metric] = 0

            for metric in nodeMetricNames:
                user_i_time_t[metric] = 0

            if not sg.isElement(n):
                # assign default values
                csvwriter.writerow(user_i_time_t)
                continue

            for metric in nodeMetricNames:
                metricProperty = sg.getLocalDoubleProperty(metric)
                user_i_time_t[metric] = metricProperty[n]
            
            # fill in the posts written by this user at this time.
            for x in range (len(postslist)):
                # 14 Oct 2011 - 16:55 %d %b %Y - %H:%M
                if str(postslist[x]['author_id']) == str(my_ID_var[n]) and \
                   (time.mktime(time.strptime(postslist[x]['date'], "%d %b %Y - %H:%M")) < t) and \
                   (time.mktime(time.strptime(postslist[x]['date'], "%d %b %Y - %H:%M")) >= t - timestep):
                    for topic in topics:
                        if postslist[x]['topic'] == topic:
                            user_i_time_t['NPosts in ' + topic] += 1
                            user_i_time_t['EPosts in ' + topic] += int(postslist[x]['effort'])


            dictInNeighbors = {}
            for e in sg.getInEdges(n):
                # grabbing unique in neighbors
                neighbor = sg.source(e)
                if neighbor not in dictInNeighbors:
                    dictInNeighbors[neighbor] = []
                dictInNeighbors[neighbor].append(e)
                # counting comments and effort to our user
                # TODO: filter here for the timestamp property of the edge. It must not count edges created in earlier periods!

                eTimestamp = dateProperty[e]
                eTopic = topicProperty[e]
                effort = int(effortProperty[e])
                #print "timestamp: ", dateProperty[e], "/", (t - timestep), " >> ", (dateProperty[e] >= (t - timestep))
                if dateProperty[e] >= (t - timestep):
                    # this is to avoid multiple counting of comments left in previous periods (edges endure).
                    if is_team[e]:
                        user_i_time_t['NTeam comms received in ' + eTopic] += 1
                        user_i_time_t['ETeam comms received in ' + eTopic] += effort
                    else:
                        user_i_time_t['NComms received in ' + eTopic] += 1
                        user_i_time_t['EComms received in ' + eTopic] += effort


            dictOutNeighbors = {}
            for e in sg.getOutEdges(n):
                # grabbing unique out neighbors
                neighbor = sg.target(e)
                if neighbor not in dictOutNeighbors:
                    dictOutNeighbors[neighbor] = []
                dictOutNeighbors[neighbor].append(e)

                # counting comments and effort from our user
                if dateProperty[e] >= (t - timestep):
                    eTopic = topicProperty[e]
                    effort = int(effortProperty[e])
                    user_i_time_t['NComms written in ' + eTopic] += 1
                    user_i_time_t['EComms written in ' + eTopic] += effort



            user_i_time_t['Indegree'] = len(dictInNeighbors)
            user_i_time_t['Outdegree'] = len(dictOutNeighbors)



                
                # this lists the edges for which my node is a target
                

            # user_i_time_t = 
            # now comments, all three categories:

            
            '''
            for j in range (len (commentslist)):
                if (commentslist[j]['author_id'] == userlist[i]['user_id']) and (commentslist[j]['timestamp'] > t) and (commentslist[j]['timestamp'] <= t + timestep):
                    for topic in topics:
                        if commentslist[j]['topic'] == topic:
                            commentswritten[topic][0] = commentswritten[topic][0] + 1
                            commentswritten[topic][1] = commentswritten[topic][1] + int (commentslist[j]['effort'])
                elif (commentslist[j]['target_id'] == userlist[i]['user_id']) and (commentslist[j]['timestamp'] > t) and (commentslist[j]['timestamp'] <= t + timestep):
                    if commentslist[j]['team'] == '0': 
                        for topic in topics:
                            if commentslist[j]['topic'] == topic:
                                commentsreceived[topic][0] = commentsreceived[topic][0] + 1
                                commentsreceived[topic][1] = commentsreceived[topic][1] + int( commentslist[j]['effort'])
                    else:
                        for topic in topics:
                            if commentslist[j]['topic'] == topic:
                                commentsreceived_team[topic][0] = commentsreceived_team[topic][0] + 1
                                commentsreceived_team[topic][1] = commentsreceived_team[topic][1] + commentslist[j]['effort']
            '''
            #now subgraph properties
            # node metrics first    
            #nodeMetricValues = {}
            #for metricName in nodeMetricNames:
            #    user_i_time_t[metricName] = nodeMetrics[metricName][n]
            
            # now global metrics
            csvwriter.writerow(user_i_time_t)



    csvfile.close()
    print ("The end")
    


# define the non-main function(s) needed:


def findNodeById(id, graph, idProperty):
    '''
      finds a node if it exists / return None otherwise. This function has a bug I was not able to fix, and always returns None. However, idProperty seems to be stored correctly!
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


graph = tlp.newGraph()
main(graph)

def display(node, graph):
    print('node tulip id ', node.id)
    uid = graph.getIntegerProperty('user_id')
    print('user_id ',  uid[node])
    isteam = graph.getBooleanProperty('is_team')
    print('is team ',  isteam[node])
    date = graph.getIntegerProperty('timestamp')
    print ('creation date ', date[node])
    
