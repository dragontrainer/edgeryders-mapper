# This program accepts a list of users and a list of comments as CSV files and builds the associated graph.
# Italso needs a JSON file containing nodes


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
	to_filename = dirPath + 'output.csv'
	to_file = open(to_filename, 'w')

	# load comments
	comments_filename = dirPath + 'commentslist.csv'
	comments_reader = csv.DictReader(open(comments_filename, 'rb'), delimiter=',')
	commentslist = []
	for line in comments_reader:
		commentslist.append(line)

	# load posts? Maybe I don't need them here
	# nodes_filename = dirPath + 'postslist.csv' 
	# nodes_reader = csv.DictReader(open(nodes_filename, 'rb'), delimiter=',')
	# nodeslist = []
	# for line in nodes_reader:
	#	nodeslist.append(line)
	

	# load users
	users_filename = dirPath + 'userlist.csv' 
	users_reader = csv.DictReader(open(users_filename, 'rb'), delimiter=',')
	userlist = []
	for line in users_reader:
		userlist.append(line)

	# assign the time interval step in UNIX time: 4 weeks == 2419200

	timestep = 2419200
	time_0 = 1321228800  
	

	# We build the graph


	# graph = tlp.newgraph() # when executing from within Tulip GUI, you omit this. The empty graph is loaded by default.

        # GM - I am unsure what this instruction does
        # GM - I'll assume we are working with a brand new, empty,
        # GM - graph so we don't need to invoke this method
	# graph = graph.clear()

	# create the properties of nodes 
	my_ID_var = graph.getIntegerProperty('user_id')
	user_name = graph.getStringProperty('user_name')
	team = graph.getBooleanProperty('team')
	dateProperty = graph.getIntegerProperty('timestamp')
	# dateProperty stores the account creation date of node (user)
	# dateProperty stores the publication date of a comment (edge)

	# create nodes and populate their properties.
	for u in range (len (userlist)):
		n = graph.addNode()
		my_ID_var[n] = int (userlist[u]['user_id']) # the name my_ID_var is to distinguish it from Tulip's internally assigned node ID.
		# user_name[n] = userlist[u]['user_id']
		team[n] = bool (userlist[u]['team'])
		dateProperty[n] = time.mktime(time.strptime(userlist[u]['joindate'], '%Y-%m-%d'))
		print ('Node ' + str(my_ID_var(n)) + ' created.')
		
##	# now create edges. Loop over comments:
##	
##	for comment in commentslist:
##		# comment
##
##                # GM - the following line throws an exception 'KeyError'
##                # GM - and says the 'nid' key does not exist
##		print comment
##
##		if not comment['author_id'] == '0' and not comment['target_id'] == 0: # we weed out comments that don't refer to valid users
##		
##			sid = int(comment['author_id'])
##			tid = int(comment['target_id'])
##			sNode = findNodeById(sid, graph, my_ID_var)
##			tNode = findNodeById(tid, graph, my_ID_var)
##
##			edge = graph.addEdge(sNode, tNode)
##
##		# add property values to this edge
##		# ...
##			timeStamp = comment['timestamp']
##
##			dateProperty[edge] = timeStamp
##			
##	
##	# here starts the dynamic part. For the moment I am not including it, so I speed up the program. It is in the file comment_posts_counter.py.


	print ("end")
	


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


graph = tlp.newGraph()
main(graph)
