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

def main(graph, userlist, commentslist): 
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

	# load nodes
	nodes_filename = dirPath + 'nodeslist.csv' 
	nodes_reader = csv.DictReader(open(nodes_filename, 'rb'), delimiter=',')
	nodeslist = []
	for line in nodes_reader:
		nodeslist.append(line)
	

	# load users
	users_filename = dirPath + 'userlist.csv' 
	users_reader = csv.DictReader(open(users_filename, 'rb'), delimiter=',')
	userlist = []
	for line in users_reader:
		userlist.append(line)

	# assign the time interval step in UNIX time: 4 weeks == 2419200

	timestep = 2419200
	time_0 = 1321228800  
	
	len_allcomments = len(allcomments)
	len_allnodes = len(allnodes)
	len_allusers = len(allusers)

	# build a list of user ids and their (time-invariant) attributes

	userlist = [] # this accumulator contains anagraphic information about active users

	for i in range (len(allusers)):
	
		active = False

		for w in range (len_allnodes):
			if 'uid' in allnodes[w]['node']: # takes care of some incomplete records
				if allnodes[w]['node']['uid'] != allusers[i]['user']['uid'] and w < len_allnodes - 1:
					w = w + 1
				elif allnodes[w]['node']['uid'] == allusers[i]['user']['uid']:
					active = True

				if active == False:

					for j in range (len(allcomments)): 
						if allcomments[j]['comment']['uid'] == allusers[i]['user']['uid']:
							active = True
		# write the corresponding item in userlist
		if active == True:
			user = {}
			user['user_id']= allusers[i]['user']['uid']
			user['user_name'] = allusers[i]['user']['name']
			user['joindate'] = datetime.datetime.fromtimestamp(int(allusers[i]['user']['created'])).strftime('%Y-%m-%d')

			if 'roles' in allusers[i]['user']:
				user['team'] = 1
			else:
				user['team'] = 0

			userlist.append(user)
			print ('User ' + repr (allusers[i]['user']['name']) + ' added to active list')
	print ('Userlist complete. ' + str(len(userlist)) + ' active users found.')

		
	# build a list of comments and store it to get rid of allcomments and speed up the program

	commentslist = []

	for j in range (len(allcomments)):
                # GM - added these printouts to see what there really were inside comments
		# print allcomments[j]
		# break
		comment = {}
		# get the comment id
		comment['comment_id'] = allcomments[j]['comment']['cid']
	
		#get the topic. Begin by getting the node that the comment is a comment to and store it in a variable
		node_id = allcomments[j]['comment']['nid']
		# GM - found it
		# GM - you simply forgot to create a 'nid' field for comment. fixed.
		comment['nid'] = node_id

		# find the node id that corresponds to the jth comment, and read its mission brief (gid)
		# read also the author's id (uid)
		k = 0
		while k < len(allnodes) and  allnodes[k]['node']['nid'] != node_id:
			k = k + 1
			if k == len(allnodes):
				brief_id = 0
				report_author_id = '0'
			else:
				brief_id = int(allnodes[k]['node']['gid'])
				if 'uid' in allnodes[k]['node']:
					report_author_id = allnodes[k]['node']['uid']
				else:
					report_author_id = '0'
		comment['author_id'] = allcomments[j]['comment']['uid']
		comment['brief_id'] = int(brief_id)
		# determine whether the author of the comment at hand is a member of the Edgeryders team:
		comment['author_team'] = 0
		for w in range (len(userlist)):
			if userlist[w]['user_id'] == comment['author_id']:
				comment['author_team'] = userlist[w]['team']
				
		# now determine the target of the comment. Begin by finding out whether the comment has a pid
		# i.e. it is a comment to a comment. If not, the target is the author of the mission report

		if 'pid' not in allcomments[j]['comment']:
			target_id = report_author_id
		# if the comment does have a pid, we need to look into comments.json
		else:
			parent_comment = allcomments[j]['comment']['pid']
			l = 0
			while l < len(allcomments) and allcomments[l]['comment']['cid'] != parent_comment:
				l = l + 1
			if l == len(allcomments):
				target_id = '0'
			else:
				target_id = allcomments[l]['comment']['uid']
		comment['target_id'] = target_id
	
		# get the length:
		if 'comment' in allcomments[j]['comment']:
			comment ['length'] = len (allcomments[j]['comment']['comment'])
		else: 
			comment ['length'] = len(allcomments[j]['comment']['subject'])
		
		# get the timestamp:
		comment['timestamp'] = int(allcomments[j]['comment']['timestamp'])
	
		commentslist.append(comment)
	
	print ('commentslist complete - containing ' + str(len(commentslist)) + ' comments')

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
		
	# now create edges. Loop over comments:
	
	for comment in commentslist:
		# comment

                # GM - the following line throws an exception 'KeyError'
                # GM - and says the 'nid' key does not exist
		print comment

		if not comment['author_id'] == '0' and not comment['target_id'] == 0: # we weed out comments that don't refer to valid users
		
			sid = int(comment['author_id'])
			tid = int(comment['target_id'])
			sNode = findNodeById(sid, graph, my_ID_var)
			tNode = findNodeById(tid, graph, my_ID_var)

			edge = graph.addEdge(sNode, tNode)

		# add property values to this edge
		# ...
			timeStamp = comment['timestamp']

			dateProperty[edge] = timeStamp
			
	
	# here starts the dynamic part. For the moment I am not including it, so I speed up the program. It is in the file comment_posts_counter.py.


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
userlist = [] # why are these two here?
commentslist = []
main(graph, userlist, commentslist)
