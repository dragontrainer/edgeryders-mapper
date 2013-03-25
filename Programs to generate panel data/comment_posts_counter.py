# This program counts the comments and posts written and received (in the case of comments) by each user at each time period

# Start reading the files

import json
import csv
import datetime
import time

# define the function(s) needed:

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



# Here's the output file:
to_filename = '/Users/albertocottica/Dropbox/PhD/MyPhDdata/Extraction 2012-12-05-1623/comment_count_table.csv'
to_file = open(to_filename, 'w')

# load comments
comments_filename = '/Users/albertocottica/Dropbox/PhD/MyPhDdata/Extraction 2012-12-05-1623/json/comments.json'
comments_data = open(comments_filename)
jcomments = json.load(comments_data)

# load nodes
nodes_filename = '/Users/albertocottica/Dropbox/PhD/MyPhDdata/Extraction 2012-12-05-1623/json/nodes.json' #remember to change this name to /users.json
nodes_data = open(nodes_filename)
jnodes = json.load(nodes_data)

# load users
users_filename = '/Users/albertocottica/Dropbox/PhD/MyPhDdata/Extraction 2012-12-05-1623/json/users.json' #remember to change this name to /users.json
users_data = open(users_filename)
jusers = json.load(users_data)

# assign the time interval step in UNIX time: 4 weeks == 2419200

timestep = 2419200
time_0 = 1321228800  

allcomments = jcomments['comments']
allnodes = jnodes['nodes']
allusers = jusers['users']

# build a list of user ids and their (time-invariant) attributes

userlist = [] # this accumulator contains anagraphic information about active users

for i in range (len(allusers)):
	
	active = 0 # this loop weeds out inactive users
	for j in range (len(allcomments)): 
		if allcomments[j]['comment']['uid'] == allusers[i]['user']['uid']:
			active = active + 1
	if active > 0:
		user = {}
		user['user_id']= allusers[i]['user']['uid']
		user['user_name'] = allusers[i]['user']['name']
		user['joindate'] = datetime.datetime.fromtimestamp(int(allusers[i]['user']['created'])).strftime('%Y-%m-%d')
	
		if 'roles' in allusers[i]['user']:
			user['team'] = 1
		else:
			user['team'] = 0

		userlist.append(user)
		
print ('userlist complete')
		
# build a list of comments and store it to get rid of allcomments and speed up the program

commentslist = []

for j in range (len(allcomments)):
	comment = {}
	# get the comment id
	comment['comment_id'] = allcomments[j]['comment']['cid']
	
	#get the topic. Begin by getting the node that the comment is a comment to and store it in a variable
	node_id = allcomments[j]['comment']['nid']

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
	
print ('commentslist complete')


# this is the dynamic part.

bigtable = [] 

for i in range (len(userlist)):
	print(i)
	time = time_0
	 
	for t in range(15):
		user_i_time_t = []
		
		# I am making the accumulators for comments written and received dicts. Reason: so I don't get lost in indices while programming.
		# each accumulator dict's elements are lists of 2 elements. The first is the number of comments/posts; the second is 
		# the sum of their lengths, and can be thought of as effort level.
		
		commentswritten = {}  
		commentswritten['01 - Bootcamp'] = [0, 0] 
		commentswritten['02 - Making a living'] = [0, 0]
		commentswritten['03 - We, the people'] = [0, 0]
		commentswritten['04 - Caring for commons'] = [0, 0]
		commentswritten['05 - Learning'] = [0, 0]
		commentswritten['06 - Living together'] = [0, 0]
		commentswritten['07 -Finale'] = [0, 0]
		commentswritten['08 - Resilience'] = [0, 0]
		commentswritten['00 - Undefined'] = [0, 0]
		
		postswritten = {}
		postswritten['01 - Bootcamp'] = [0, 0]
		postswritten['02 - Making a living'] = [0, 0]
		postswritten['03 - We, the people'] = [0, 0]
		postswritten['04 - Caring for commons'] = [0, 0]
		postswritten['05 - Learning'] = [0, 0]
		postswritten['06 - Living together'] = [0, 0]
		postswritten['07 -Finale'] = [0, 0]
		postswritten['08 - Resilience'] = [0, 0]
		postswritten['00 - Undefined'] = [0, 0]
		
		commentsreceived = {}
		commentsreceived['01 - Bootcamp'] = [0, 0]
		commentsreceived['02 - Making a living'] = [0, 0]
		commentsreceived['03 - We, the people'] = [0, 0]
		commentsreceived['04 - Caring for commons'] = [0, 0]
		commentsreceived['05 - Learning'] = [0, 0]
		commentsreceived['06 - Living together'] = [0, 0]
		commentsreceived['07 -Finale'] = [0, 0]
		commentsreceived['08 - Resilience'] = [0, 0]
		commentsreceived['00 - Undefined'] = [0, 0]
		
		commentsreceived_team =  {}
		commentsreceived_team['01 - Bootcamp'] = [0, 0]
		commentsreceived_team['02 - Making a living'] = [0, 0]
		commentsreceived_team['03 - We, the people'] = [0, 0]
		commentsreceived_team['04 - Caring for commons'] = [0, 0]
		commentsreceived_team['05 - Learning'] = [0, 0]
		commentsreceived_team['06 - Living together'] = [0, 0]
		commentsreceived_team['07 -Finale'] = [0, 0]
		commentsreceived_team['08 - Resilience'] = [0, 0]
		commentsreceived_team['00 - Undefined'] = [0, 0]

		# this loop counts comments written and received by each user at each time period. 
		for j in range (len(commentslist)):
			
			# start with comments written by user i:
			if (commentslist[j]['author_id'] == userlist[i]['user_id']) and (commentslist[j]['timestamp'] > time) and (commentslist[j]['timestamp'] <= time + timestep):

				# determine what campaign the mission brief ids corresponds to and increase the value of the corresponding key in commentswritten. 
				# Source: http://edgeryders.wikispiral.org/campaigns-from-brief-ids
				if commentslist[j]['brief_id'] == 29 or commentslist[j]['brief_id'] == 43 or commentslist[j]['brief_id'] == 44 or commentslist[j]['brief_id'] == 45:
					commentswritten['01 - Bootcamp'][0] = commentswritten['01 - Bootcamp'][0] + 1
					commentswritten['01 - Bootcamp'][1] = commentswritten['01 - Bootcamp'][1] + commentslist[j]['length'] 
				elif commentslist[j]['brief_id'] == 188 or commentslist[j]['brief_id'] == 189 or commentslist[j]['brief_id'] == 190 or commentslist[j]['brief_id'] == 191:
					commentswritten['02 - Making a living'][0] = commentswritten['02 - Making a living'][0] + 1
					commentswritten['02 - Making a living'][1] = commentswritten['02 - Making a living'][1] + commentslist[j]['length']
				elif commentslist[j]['brief_id'] == 262 or commentslist[j]['brief_id'] == 264 or commentslist[j]['brief_id'] == 267 or commentslist[j]['brief_id'] == 269:
					commentswritten['03 - We, the people'][0] = commentswritten['03 - We, the people'][0] + 1
					commentswritten['03 - We, the people'][1] = commentswritten['03 - We, the people'][1] + commentslist[j]['length']
				elif commentslist[j]['brief_id'] == 322 or commentslist[j]['brief_id'] == 323 or commentslist[j]['brief_id'] == 324:
					commentswritten['04 - Caring for commons'][0] = commentswritten['04 - Caring for commons'][0] + 1
					commentswritten['04 - Caring for commons'][1] = commentswritten['04 - Caring for commons'][1] + commentslist[j]['length']
				elif commentslist[j]['brief_id'] == 401 or commentslist[j]['brief_id'] == 403 or commentslist[j]['brief_id'] == 405 or commentslist[j]['brief_id'] == 406:
					commentswritten['05 - Learning'][0] = commentswritten['05 - Learning'][0] + 1
					commentswritten['05 - Learning'][1] = commentswritten['05 - Learning'][1] + commentslist[j]['length']
				elif commentslist[j]['brief_id'] == 482 or commentslist[j]['brief_id'] == 481 or commentslist[j]['brief_id'] == 484 or commentslist[j]['brief_id'] == 486 or commentslist[j]['brief_id'] == 487:
					commentswritten['06 - Living together'][0] = commentswritten['06 - Living together'][0] + 1
					commentswritten['06 - Living together'][1] = commentswritten['06 - Living together'][1] + commentslist[j]['length']
				elif commentslist[j]['brief_id'] == 640 or commentslist[j]['brief_id'] == 712 or commentslist[j]['brief_id'] == 1162:
					commentswritten['07 -Finale'][0] = commentswritten['07 -Finale'][0] + 1
					commentswritten['07 -Finale'][1] = commentswritten['07 -Finale'][1] + commentslist[j]['length']
				elif commentslist[j]['brief_id'] == 682 or commentslist[j]['brief_id'] == 683 or commentslist[j]['brief_id'] == 688:
					commentswritten['08 - Resilience'][0] = commentswritten['08 - Resilience'][0] + 1
					commentswritten['08 - Resilience'][1] = commentswritten['08 - Resilience'][1] + commentslist[j]['length']
				else:
					commentswritten['00 - Undefined'][0] = commentswritten['00 - Undefined'][0] + 1
					commentswritten['00 - Undefined'][1] = commentswritten['00 - Undefined'][1] + commentslist[j]['length']

			if (commentslist[j]['target_id'] == userlist[i]['user_id']) and (int(allcomments[j]['comment']['timestamp']) > time) and (int(allcomments[j]['comment']['timestamp']) <= time + timestep):
				# determine what campaign the mission brief ids corresponds to and increase the value of the corresponding key in commentsreceived.
				# distinguish between comments received by team and nonteam users. 
				# Source: http://edgeryders.wikispiral.org/campaigns-from-brief-ids
								
				if commentslist[j]['author_team'] == 1:
					
					if commentslist[j]['brief_id'] == 29 or commentslist[j]['brief_id'] == 43 or commentslist[j]['brief_id'] == 44 or commentslist[j]['brief_id'] == 45:
						commentsreceived_team['01 - Bootcamp'][0] = commentsreceived_team['01 - Bootcamp'][0] + 1
						commentsreceived_team['01 - Bootcamp'][1] = commentsreceived_team['01 - Bootcamp'][1] + commentslist[j]['length'] 
					elif commentslist[j]['brief_id'] == 188 or commentslist[j]['brief_id'] == 189 or commentslist[j]['brief_id'] == 190 or commentslist[j]['brief_id'] == 191:
						commentsreceived_team['02 - Making a living'][0] = commentsreceived_team['02 - Making a living'][0] + 1
						commentsreceived_team['02 - Making a living'][1] = commentsreceived_team['02 - Making a living'][1] + commentslist[j]['length']
					elif commentslist[j]['brief_id'] == 262 or commentslist[j]['brief_id'] == 264 or commentslist[j]['brief_id'] == 267 or commentslist[j]['brief_id'] == 269:
						commentsreceived_team['03 - We, the people'][0] = commentsreceived_team['03 - We, the people'][0] + 1
						commentsreceived_team['03 - We, the people'][1] = commentsreceived_team['03 - We, the people'][1] + commentslist[j]['length']
					elif commentslist[j]['brief_id'] == 322 or commentslist[j]['brief_id'] == 323 or commentslist[j]['brief_id'] == 324:
						commentsreceived_team['04 - Caring for commons'][0] = commentsreceived_team['04 - Caring for commons'][0] + 1
						commentsreceived_team['04 - Caring for commons'][1] = commentsreceived_team['04 - Caring for commons'][1] + commentslist[j]['length']
					elif commentslist[j]['brief_id'] == 401 or commentslist[j]['brief_id'] == 403 or commentslist[j]['brief_id'] == 405 or commentslist[j]['brief_id'] == 406:
						commentsreceived_team['05 - Learning'][0] = commentsreceived_team['05 - Learning'][0] + 1
						commentsreceived_team['05 - Learning'][1] = commentsreceived_team['05 - Learning'][1] + commentslist[j]['length']
					elif commentslist[j]['brief_id'] == 482 or commentslist[j]['brief_id'] == 481 or commentslist[j]['brief_id'] == 484 or commentslist[j]['brief_id'] == 486 or commentslist[j]['brief_id'] == 487:
						commentsreceived_team['06 - Living together'][0] = commentsreceived_team['06 - Living together'][0] + 1
						commentsreceived_team['06 - Living together'][1] = commentsreceived_team['06 - Living together'][1] + commentslist[j]['length']
					elif commentslist[j]['brief_id'] == 640 or commentslist[j]['brief_id'] == 712 or commentslist[j]['brief_id'] == 1162:
						commentsreceived_team['07 -Finale'][0] = commentsreceived_team['07 -Finale'][0] + 1
						commentsreceived_team['07 -Finale'][1] = commentsreceived_team['07 -Finale'][1] + commentslist[j]['length']
					elif commentslist[j]['brief_id'] == 682 or commentslist[j]['brief_id'] == 683 or commentslist[j]['brief_id'] == 688:
						commentsreceived_team['08 - Resilience'][0] = commentsreceived_team['08 - Resilience'][0] + 1
						commentsreceived_team['08 - Resilience'][1] = commentsreceived_team['08 - Resilience'][1] + commentslist[j]['length']
					else:
						commentsreceived_team['00 - Undefined'][0] = commentsreceived_team['00 - Undefined'][0] + 1
						commentsreceived_team['00 - Undefined'][1] = commentsreceived_team['00 - Undefined'][1] + commentslist[j]['length']
					
				else:
					if commentslist[j]['brief_id'] == 29 or commentslist[j]['brief_id'] == 43 or commentslist[j]['brief_id'] == 44 or commentslist[j]['brief_id'] == 45:
						commentsreceived['01 - Bootcamp'][0] = commentsreceived['01 - Bootcamp'][0] + 1
						commentsreceived['01 - Bootcamp'][1] = commentsreceived['01 - Bootcamp'][1] + commentslist[j]['length'] 
					elif commentslist[j]['brief_id'] == 188 or commentslist[j]['brief_id'] == 189 or commentslist[j]['brief_id'] == 190 or commentslist[j]['brief_id'] == 191:
						commentsreceived['02 - Making a living'][0] = commentsreceived['02 - Making a living'][0] + 1
						commentsreceived['02 - Making a living'][1] = commentsreceived['02 - Making a living'][1] + commentslist[j]['length']
					elif commentslist[j]['brief_id'] == 262 or commentslist[j]['brief_id'] == 264 or commentslist[j]['brief_id'] == 267 or commentslist[j]['brief_id'] == 269:
						commentsreceived['03 - We, the people'][0] = commentsreceived['03 - We, the people'][0] + 1
						commentsreceived['03 - We, the people'][1] = commentsreceived['03 - We, the people'][1] + commentslist[j]['length']
					elif commentslist[j]['brief_id'] == 322 or commentslist[j]['brief_id'] == 323 or commentslist[j]['brief_id'] == 324:
						commentsreceived['04 - Caring for commons'][0] = commentsreceived['04 - Caring for commons'][0] + 1
						commentsreceived['04 - Caring for commons'][1] = commentsreceived['04 - Caring for commons'][1] + commentslist[j]['length']
					elif commentslist[j]['brief_id'] == 401 or commentslist[j]['brief_id'] == 403 or commentslist[j]['brief_id'] == 405 or commentslist[j]['brief_id'] == 406:
						commentsreceived['05 - Learning'][0] = commentsreceived['05 - Learning'][0] + 1
						commentsreceived['05 - Learning'][1] = commentsreceived['05 - Learning'][1] + commentslist[j]['length']
					elif commentslist[j]['brief_id'] == 482 or commentslist[j]['brief_id'] == 481 or commentslist[j]['brief_id'] == 484 or commentslist[j]['brief_id'] == 486 or commentslist[j]['brief_id'] == 487:
						commentsreceived['06 - Living together'][0] = commentsreceived['06 - Living together'][0] + 1
						commentsreceived['06 - Living together'][1] = commentsreceived['06 - Living together'][1] + commentslist[j]['length']
					elif commentslist[j]['brief_id'] == 640 or commentslist[j]['brief_id'] == 712 or commentslist[j]['brief_id'] == 1162:
						commentsreceived['07 -Finale'][0] = commentsreceived['07 -Finale'][0] + 1
						commentsreceived['07 -Finale'][1] = commentsreceived['07 -Finale'][1] + commentslist[j]['length']
					elif commentslist[j]['brief_id'] == 682 or commentslist[j]['brief_id'] == 683 or commentslist[j]['brief_id'] == 688:
						commentsreceived['08 - Resilience'][0] = commentsreceived['08 - Resilience'][0] + 1
						commentsreceived['08 - Resilience'][1] = commentsreceived['08 - Resilience'][1] + commentslist[j]['length']
					else:
						commentsreceived['00 - Undefined'][0] = commentsreceived['00 - Undefined'][0] + 1
						commentsreceived['00 - Undefined'][1] = commentsreceived['00 - Undefined'][1] + commentslist[j]['length']


		# While we are at it, we also count mission reports
		# this is the loop that does not work :-()
		for x in range (len(allnodes)):	
			if 'uid' in allnodes[x]['node']: # this gets rid of some incomplete records
				if (allnodes[x]['node']['uid'] == userlist[i]['user_id']) and (drupal_to_unix_time(allnodes[x]['node']['date']) > time) and (drupal_to_unix_time(allnodes[x]['node']['date']) <= time + timestep):
					if int(allnodes[x]['node']['gid']) == 29 or int(allnodes[x]['node']['gid']) == 43 or int(allnodes[x]['node']['gid']) == 44 or int(allnodes[x]['node']['gid']) == 45:
						postswritten['01 - Bootcamp'][0] = commentsreceived_team['01 - Bootcamp'][0] + 1
						if 'Full text' in allnodes[x]['node']: # this gets rid of an error, clearly a comment without body text
							postswritten['01 - Bootcamp'][1] = commentsreceived_team['01 - Bootcamp'][1] + len(allnodes[x]['node']['Full text'])
					elif int(allnodes[x]['node']['gid']) == 188 or int(allnodes[x]['node']['gid']) == 189 or int(allnodes[x]['node']['gid']) == 190 or int(allnodes[x]['node']['gid']) == 191:
						postswritten['02 - Making a living'][0] = postswritten['02 - Making a living'][0] + 1
						postswritten['02 - Making a living'][1] = postswritten['02 - Making a living'][1] + len(allnodes[x]['node']['Full text'])
					elif int(allnodes[x]['node']['gid']) == 262 or int(allnodes[x]['node']['gid']) == 264 or int(allnodes[x]['node']['gid']) == 267 or int(allnodes[x]['node']['gid']) == 269:
						postswritten['03 - We, the people'][0] = postswritten['03 - We, the people'][0] + 1
						if 'Full text' in allnodes[x]['node']: # this gets rid of an error, clearly a comment without body text
							postswritten['03 - We, the people'][1] = postswritten['03 - We, the people'][1] + len(allnodes[x]['node']['Full text'])
					elif int(allnodes[x]['node']['gid']) == 322 or int(allnodes[x]['node']['gid']) == 323 or int(allnodes[x]['node']['gid']) == 324:
						postswritten['04 - Caring for commons'][0] = postswritten['04 - Caring for commons'][0] + 1
						postswritten['04 - Caring for commons'][1] = postswritten['04 - Caring for commons'][1] + len(allnodes[x]['node']['Full text'])
					elif int(allnodes[x]['node']['gid']) == 401 or int(allnodes[x]['node']['gid']) == 403 or int(allnodes[x]['node']['gid']) == 405 or int(allnodes[x]['node']['gid']) == 406:
						postswritten['05 - Learning'][0] = postswritten['05 - Learning'][0] + 1
						postswritten['05 - Learning'][1] = postswritten['05 - Learning'][1] + len(allnodes[x]['node']['Full text'])
					elif int(allnodes[x]['node']['gid']) == 482 or int(allnodes[x]['node']['gid']) == 481 or int(allnodes[x]['node']['gid']) == 484 or int(allnodes[x]['node']['gid']) == 486 or int(allnodes[x]['node']['gid']) == 487:
						postswritten['06 - Living together'][0] = postswritten['06 - Living together'][0] + 1
						postswritten['06 - Living together'][1] = postswritten['06 - Living together'][1] + len(allnodes[x]['node']['Full text'])
					elif int(allnodes[x]['node']['gid']) == 640 or int(allnodes[x]['node']['gid']) == 712 or int(allnodes[x]['node']['gid']) == 1162:
						postswritten['07 -Finale'][0] = postswritten['07 -Finale'][0] + 1 
						postswritten['07 -Finale'][1] = postswritten['07 -Finale'][1] + len(allnodes[x]['node']['Full text'])
					elif int(allnodes[x]['node']['gid']) == 682 or int(allnodes[x]['node']['gid']) == 683 or int(allnodes[x]['node']['gid']) == 688:
						postswritten['08 - Resilience'][0] = postswritten['08 - Resilience'][0] + 1
						postswritten['08 - Resilience'][1] = postswritten['08 - Resilience'][1] + len(allnodes[x]['node']['Full text'])
					else:
						postswritten['00 - Undefined'][0] = postswritten['00 - Undefined'][0] + 1
						postswritten['00 - Undefined'][1] = postswritten['00 - Undefined'][1] + len(allnodes[x]['node']['Full text'])
					
		user_i_time_t.append(userlist[i]['user_id'])
		user_i_time_t.append(datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d'))
		user_i_time_t.append(postswritten)
		user_i_time_t.append(commentswritten)
		user_i_time_t.append(commentsreceived)
		user_i_time_t.append(commentsreceived_team)
		bigtable.append(user_i_time_t)
		time = time + timestep

			
file_writer = csv.writer(to_file)

# the following are for programming and testing the program only

# file_writer.writerow('userlist')
# file_writer.writerow(userlist)
# file_writer.writerow('commentslist')
# file_writer.writerow(commentslist)

# Write bigtable into the file.

# Write the header of the CSV file
file_writer.writerow(['user ID','end period','P01', 'P01E', 'P02', 'P02E', 'P03', 'P03E', 'P04', 'P04E', 'P05', 'P05E', 'P06', 'P06E', 'P07', 'P07E', 'P08', 'P08E', 'P00', 'P00E' 'CW01', 'CW01E', 'CW02', 'CW02E', 'CW03', 'CW03E', 'CW04', 'CW04E', 'CW05', 'CW05E', 'CW06', 'CW06E', 'CW07', 'CW07E', 'CW08', 'CW08E', 'CW00', 'CW00E', 'CRT01', 'CRT01E', 'CRT02', 'CRT02E', 'CRT03', 'CRT03E', 'CRT04', 'CRT04E', 'CRT05', 'CRT05E', 'CRT06', 'CRT06E', 'CRT07', 'CRT07E', 'CRT08', 'CRT08E', 'CRT00', 'CRT00E', 'CRN01', 'CRN01E', 'CRN02', 'CRN02E', 'CRN03', 'CRN03E', 'CRNO4', 'CRN04E', 'CRN05', 'CRN05E', 'CRN06', 'CRN06E', 'CRN07', 'CRN07E', 'CRN08', 'CRN08E', 'CRN00', 'CRN00E'])

# Write all the rows MUST CHANGE THE WRITER OBJECT

for r in range (len(bigtable)):
	# to_file.write (bigtable[r][0] + ',' + bigtable[r][1] + ',' + bigtable[r][2]['01 - Bootcamp'][0] + ',' + bigtable[r][2]['01 - Bootcamp'][1] + '\n')
	file_writer.writerow ([bigtable[r][0], bigtable[r][1], bigtable[r][2]['01 - Bootcamp'][0], bigtable[r][2]['01 - Bootcamp'][1], bigtable[r][2]['02 - Making a living'][0], bigtable[r][2]['02 - Making a living'][1], bigtable[r][2]['03 - We, the people'][0], bigtable[r][2]['03 - We, the people'][1], bigtable[r][2]['04 - Caring for commons'][0], bigtable[r][2]['04 - Caring for commons'][1], bigtable[r][2]['05 - Learning'][0], bigtable[r][2]['05 - Learning'][1], bigtable[r][2]['06 - Living together'][0], bigtable[r][2]['06 - Living together'][1], bigtable[r][2]['07 -Finale'][0], bigtable[r][2]['07 -Finale'][1], bigtable[r][2]['08 - Resilience'][0], bigtable[r][2]['08 - Resilience'][1], bigtable[r][2]['00 - Undefined'][0], bigtable[r][2]['00 - Undefined'][1], bigtable[r][3]['01 - Bootcamp'][0], bigtable[r][3]['01 - Bootcamp'][1], bigtable[r][3]['02 - Making a living'][0], bigtable[r][3]['02 - Making a living'][1], bigtable[r][3]['03 - We, the people'][0], bigtable[r][3]['03 - We, the people'][1], bigtable[r][3]['04 - Caring for commons'][0], bigtable[r][3]['04 - Caring for commons'][1], bigtable[r][3]['05 - Learning'][0], bigtable[r][3]['05 - Learning'][1], bigtable[r][3]['06 - Living together'][0], bigtable[r][3]['06 - Living together'][1], bigtable[r][3]['07 -Finale'][0], bigtable[r][3]['07 -Finale'][1], bigtable[r][3]['08 - Resilience'][0], bigtable[r][3]['08 - Resilience'][1], bigtable[r][3]['00 - Undefined'][0], bigtable[r][3]['00 - Undefined'][1], bigtable[r][4]['01 - Bootcamp'][0], bigtable[r][4]['01 - Bootcamp'][1], bigtable[r][4]['02 - Making a living'][0], bigtable[r][4]['02 - Making a living'][1], bigtable[r][4]['03 - We, the people'][0], bigtable[r][4]['03 - We, the people'][1], bigtable[r][4]['04 - Caring for commons'][0], bigtable[r][4]['04 - Caring for commons'][1], bigtable[r][4]['05 - Learning'][0], bigtable[r][4]['05 - Learning'][1], bigtable[r][4]['06 - Living together'][0], bigtable[r][4]['06 - Living together'][1], bigtable[r][4]['07 -Finale'][0], bigtable[r][4]['07 -Finale'][1], bigtable[r][4]['08 - Resilience'][0], bigtable[r][4]['08 - Resilience'][1], bigtable[r][4]['00 - Undefined'][0], bigtable[r][4]['00 - Undefined'][1], bigtable[r][5]['01 - Bootcamp'][0], bigtable[r][5]['01 - Bootcamp'][1], bigtable[r][5]['02 - Making a living'][0], bigtable[r][5]['02 - Making a living'][1], bigtable[r][5]['03 - We, the people'][0], bigtable[r][5]['03 - We, the people'][1], bigtable[r][5]['04 - Caring for commons'][0], bigtable[r][5]['04 - Caring for commons'][1], bigtable[r][5]['05 - Learning'][0], bigtable[r][5]['05 - Learning'][1], bigtable[r][5]['06 - Living together'][0], bigtable[r][5]['06 - Living together'][1], bigtable[r][5]['07 -Finale'][0], bigtable[r][5]['07 -Finale'][1], bigtable[r][5]['08 - Resilience'][0], bigtable[r][5]['08 - Resilience'][1], bigtable[r][5]['00 - Undefined'][0], bigtable[r][5]['00 - Undefined'][1]])

to_file.close()

print ("end")
