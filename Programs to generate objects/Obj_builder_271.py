# This program rearranges raw Egderyders data and builds two lists of dicts, userlist and ciommentslist, containing 
# of the data needed to buildm graphs. These objects are then saved into files.
import json
import csv
import datetime
import time

# Start reading the files
dirPath = '/Users/albertocottica/Dropbox/PhD/MyPhDdata/Extraction 2012-12-05-1623/json/'
# dirPath = '/Users/melancon/Documents/Recherche/Proposals/FP7 MD/Panel data/'
# Here's the output files:
to_filename = dirPath + 'comment_count_table.csv'
to_file = open(to_filename, 'w')

# load comments
comments_filename = dirPath + 'comments.json'
comments_data = open(comments_filename, 'r')
jcomments = json.load(comments_data)

# load nodes
nodes_filename = dirPath + 'nodes.json' #remember to change this name to /users.json
nodes_data = open(nodes_filename, 'r')
jnodes = json.load(nodes_data)

# load users
users_filename = dirPath + 'users.json' #remember to change this name to /users.json
users_data = open(users_filename, 'r')
jusers = json.load(users_data)

# assign the time interval step in UNIX time: 4 weeks == 2419200

timestep = 2419200
time_0 = 1321228800  

allcomments = jcomments['comments']
allnodes = jnodes['nodes']
allusers = jusers['users']

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
#		user['user_name'] = allusers[i]['user']['name']
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
	# add the topic
	find_topic(comment)
	commentslist.append(comment)
	print ('Comment ' + comment['comment_id'] + ' added to commentslist')

print ('commentslist complete - containing ' + str(len(commentslist)) + ' comments')

# build a list of nodes for symmetry

templist = [] #need a first pass to get rid of the {'node: {...}} outer layer

for node in allnodes:
	templist.append (node['node'])
	
nodeslist = []

for t in range (len (templist)):	
	post = {}
	if 'uid' in templist[t]:
		post ['nid'] = templist [t]['nid']
		post['author_id'] = templist[t]['uid']
		post['brief_id'] = int(templist[t] ['gid'])
		post ['date'] = templist[t] ['date']
		# determine whether the author of the post at hand is a member of the Edgeryders team:
		post['author_team'] = 0
		for w in range (len(userlist)):
			if userlist[w]['user_id'] == post['author_id']:
				post['author_team'] = userlist[w]['team']
		if 'Full text' in templist[t]:
			post['effort'] = len (templist[t]['Full text']) + len (templist[t] ['title'])
		else:
			post['effort'] = len (templist[t] ['title']) 
		# add the topic
		find_topic(post)
		nodeslist.append(post)
	

## write the assembled objects into files. Rewrite using class Dictwriter. 

users_to_filename = '/Users/albertocottica/Dropbox/PhD/MyPhDdata/Extraction 2012-12-05-1623/userlist.csv'
users_to_file = open(users_to_filename, 'w')

user_fieldnames = [ 'user_id', 'team', 'joindate'] # 'user_name' belongs here, but I need to get rid of the goddamn Unicode first-
users_file_writer = csv.DictWriter(users_to_file, delimiter = ',', fieldnames = user_fieldnames)
users_file_writer.writerow(dict((fn,fn) for fn in user_fieldnames))
for row in userlist:
	users_file_writer.writerow(row)

users_to_file.close()
print (users_to_filename + ' written.')

comments_to_filename = '/Users/albertocottica/Dropbox/PhD/MyPhDdata/Extraction 2012-12-05-1623/commentslist.csv'
comments_to_file = open(comments_to_filename, 'w')

comment_fieldnames = ['comment_id', 'timestamp', 'author_id', 'target_id', 'effort', 'nid', 'topic', 'brief_id','author_team']
comment_file_writer = csv.DictWriter(comments_to_file, delimiter = ',', fieldnames = comment_fieldnames)
comment_file_writer.writerow(dict((fn,fn) for fn in comment_fieldnames))
for row in commentslist:
	comment_file_writer.writerow(row)

comments_to_file.close()
print (comments_to_filename + ' written.')

posts_to_filename = '/Users/albertocottica/Dropbox/PhD/MyPhDdata/Extraction 2012-12-05-1623/postslist.csv'
posts_to_file = open(posts_to_filename, 'w')

posts_fieldnames = ['nid', 'author_id', 'author_team', 'topic', 'brief_id', 'date', 'effort']
posts_file_writer = csv.DictWriter(posts_to_file, delimiter = ',', fieldnames = posts_fieldnames)
posts_file_writer.writerow(dict((fn,fn) for fn in posts_fieldnames))
for row in nodeslist:
	posts_file_writer.writerow(row)

posts_to_file.close()
print (posts_to_filename + ' written.')

print ('The End.')

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

def find_topic (o):
	'''
	(Dict)-  -> NoneType
	adds to Dict o a key called 'topic', and assigns to o['topic'] the appropriate value.
	
	>>> comment = {'comment_id': '57', 'brief_id: 29}
	>>> find_topic (comment)
	>>> comment
	{'comment_id': '57', 'brief_id: 29, 'topic': '01 - Bootcamp' }
	'''
	if o['brief_id'] == 29 or o['brief_id'] == 43 or o['brief_id'] == 44 or o['brief_id'] == 45:
		o['topic'] = '01 - Bootcamp'
	elif o['brief_id'] == 188 or o['brief_id'] == 189 or o['brief_id'] == 190 or o['brief_id'] == 191:
		o['topic'] = '02 - Making a living'
	elif o['brief_id'] == 262 or o['brief_id'] == 264 or o['brief_id'] == 267 or o['brief_id'] == 269:
		o['topic'] = '03 - We, the people'
	elif o['brief_id'] == 322 or o['brief_id'] == 323 or o['brief_id'] == 324:
		o['topic'] = '04 - Caring for commons'
	elif o['brief_id'] == 401 or o['brief_id'] == 403 or o['brief_id'] == 405 or o['brief_id'] == 406:
		o['topic'] = '05 - Learning'
	elif o['brief_id'] == 482 or o['brief_id'] == 481 or o['brief_id'] == 484 or o['brief_id'] == 486 or o['brief_id'] == 487:
		o['topic'] = '06 - Living together'
	elif o['brief_id'] == 640 or o['brief_id'] == 712 or o['brief_id'] == 1162:
		o['topic'] = '07 -Finale'
	elif o['brief_id'] == 682 or o['brief_id'] == 683 or o['brief_id'] == 688:
		o['topic'] = '08 - Resilience'
	else:
		o['topic'] = '00 - Undefined'