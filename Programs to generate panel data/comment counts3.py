# This program counts the comments written by each user at each time period

# Start reading the files

import json
import csv
import datetime

# Here's the output file:
to_filename = '/Users/albertocottica/Documents/PhD/MyPhDdata/Extraction 2012-12-05-1623/comment_count_table.csv'
to_file = open(to_filename, 'w')

# load comments
comments_filename = '/Users/albertocottica/Documents/PhD/MyPhDdata/Extraction 2012-12-05-1623/json/comments.json'
comments_data = open(comments_filename)
jcomments = json.load(comments_data)

# load nodes
nodes_filename = '/Users/albertocottica/Documents/PhD/MyPhDdata/Extraction 2012-12-05-1623/json/nodes.json' #remember to change this name to /users.json
nodes_data = open(nodes_filename)
jnodes = json.load(nodes_data)

# load users
users_filename = '/Users/albertocottica/Documents/PhD/MyPhDdata/Extraction 2012-12-05-1623/json/users.json' #remember to change this name to /users.json
users_data = open(users_filename)
jusers = json.load(users_data)

# assign the time interval step in UNIX time: 4 weeks == 2419200

timestep = 2419200
time_0 = 1321228800  	# 2011-11-14 UTC
# time_1 = 1323648000  	# 2011-12-12
# time_2 = 1326067200 	# 2012-01-09
# time_3 = 1328486400 	# 2012-02-06
# time_4 = 1330992000 	# 2012-03-05
# time_5 = 1333324800		# 2012-04-02
# time_6 = # 2012-04-30
# time_7 = # 2012-05-28
# time_8 = # 2012-06-25
# time_9 = # 2012-07-23
# time_10 = # 2012-08-20
# time_11 = # 2012-09-17
# time_12 = # 2012-10-15
# time_13 = # 2012-11-12
# time_14 = # 2012-12-10

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

for i in range (1): # (len(userlist)):
	print(i)
	time = time_0
	 
	for t in range(15):
		user_i_time_t = []
		commentswritten = {} #I am making the accumulators for comments written and received dicts. Reason: so I don't get lost in lengthy indices.
		commentswritten['01 - Bootcamp'] = 0
		commentswritten['02 - Making a living'] = 0
		commentswritten['03 - We, the people'] = 0
		commentswritten['04 - Caring for commons'] = 0
		commentswritten['05 - Learning'] = 0
		commentswritten['06 - Living together'] = 0
		commentswritten['07 -Finale'] = 0
		commentswritten['08 - Resilience'] = 0
		commentswritten['00 - Undefined'] = 0
		
		commentsreceived = {}
		commentsreceived['01 - Bootcamp'] = 0
		commentsreceived['02 - Making a living'] = 0
		commentsreceived['03 - We, the people'] = 0
		commentsreceived['04 - Caring for commons'] = 0
		commentsreceived['05 - Learning'] = 0
		commentsreceived['06 - Living together'] = 0
		commentsreceived['07 -Finale'] = 0
		commentsreceived['08 - Resilience'] = 0
		commentsreceived['00 - Undefined'] = 0
		
		commentsreceived_team =  {}
		commentsreceived_team['01 - Bootcamp'] = 0
		commentsreceived_team['02 - Making a living'] = 0
		commentsreceived_team['03 - We, the people'] = 0
		commentsreceived_team['04 - Caring for commons'] = 0
		commentsreceived_team['05 - Learning'] = 0
		commentsreceived_team['06 - Living together'] = 0
		commentsreceived_team['07 -Finale'] = 0
		commentsreceived_team['08 - Resilience'] = 0
		commentsreceived_team['00 - Undefined'] = 0

		# this loop counts comments written and received by each user at each time period. 
		for j in range (len(commentslist)):
			
			# start with comments written by user i:
			if (commentslist[j]['author_id'] == userlist[i]['user_id']) and (commentslist[j]['timestamp'] > time) and (commentslist[j]['timestamp'] <= time + timestep):
				# determine what campaign the mission brief ids corresponds to and increase the value of the corresponding key in commentswritten. 
				# Source: http://edgeryders.wikispiral.org/campaigns-from-brief-ids
				if commentslist[j]['brief_id'] == (29 or 43 or 44 or 45):
					commentswritten['01 - Bootcamp'] = commentswritten['01 - Bootcamp'] + 1
				elif commentslist[j]['brief_id'] == (188 or 189 or 190 or 191):
					commentswritten['02 - Making a living'] = commentswritten['02 - Making a living'] + 1
				elif commentslist[j]['brief_id'] == (262 or 264 or 267 or 269):
					commentswritten['03 - We, the people'] = commentswritten['03 - We, the people'] + 1
				elif commentslist[j]['brief_id'] == (322 or 323 or 324):
					commentswritten['04 - Caring for commons'] = commentswritten['04 - Caring for commons'] + 1
				elif commentslist[j]['brief_id'] == (401 or 403 or 405 or 406):
					commentswritten['05 - Learning'] = commentswritten['05 - Learning'] + 1
				elif commentslist[j]['brief_id'] == (482 or 481 or 484 or 486 or 487):
					commentswritten['06 - Living together'] = commentswritten['06 - Living together'] + 1
				elif commentslist[j]['brief_id'] == (640 or 712 or 1162):
					commentswritten['07 -Finale'] = commentswritten['07 -Finale'] + 1
				elif commentslist[j]['brief_id'] == (682 or 683 or 688):
					commentswritten['08 - Resilience'] = commentswritten['08 - Resilience'] + 1
				else:
					commentswritten['00 - Undefined'] = commentswritten['00 - Undefined'] + 1

			if (commentslist[j]['target_id'] == userlist[i]['user_id']) and (int(allcomments[j]['comment']['timestamp']) > time) and (int(allcomments[j]['comment']['timestamp']) <= time + timestep):
				# determine what campaign the mission brief ids corresponds to and increase the value of the corresponding key in commentsreceived.
				# distinguish between comments received by team and nonteam users. 
				# Source: http://edgeryders.wikispiral.org/campaigns-from-brief-ids
								
				if commentslist[j]['author_team'] == 1:
					
					if commentslist[j]['brief_id'] == (29 or 43 or 44 or 45):
						commentsreceived_team['01 - Bootcamp'] = commentsreceived_team['01 - Bootcamp'] + 1
					elif commentslist[j]['brief_id'] == (188 or 189 or 190 or 191):
						commentsreceived_team['02 - Making a living'] = commentsreceived_team['02 - Making a living'] + 1
					elif commentslist[j]['brief_id'] == (262 or 264 or 267 or 269):
						commentsreceived_team['03 - We, the people'] = commentsreceived_team['03 - We, the people'] + 1
					elif commentslist[j]['brief_id'] == (322 or 323 or 324):
						commentsreceived_team['04 - Caring for commons'] = commentsreceived_team['04 - Caring for commons'] + 1
					elif commentslist[j]['brief_id'] == (401 or 403 or 405 or 406):
						commentsreceived_team['05 - Learning'] = commentsreceived_team['05 - Learning'] + 1
					elif commentslist[j]['brief_id'] == (482 or 481 or 484 or 486 or 487):
						commentsreceived_team['06 - Living together'] = commentsreceived_team['06 - Living together'] + 1
					elif commentslist[j]['brief_id'] == (640 or 712 or 1162):
						commentsreceived_team['07 -Finale'] = commentsreceived_team['07 -Finale'] + 1
					elif commentslist[j]['brief_id'] == (682 or 683 or 688):
						commentsreceived_team['08 - Resilience'] = commentsreceived_team['08 - Resilience'] + 1
					else:
						commentsreceived_team['00 - Undefined'] = commentsreceived_team['00 - Undefined'] + 1
					
				else:
					if commentslist[j]['brief_id'] == (29 or 43 or 44 or 45):
						commentsreceived['01 - Bootcamp'] = commentsreceived['01 - Bootcamp'] + 1
					elif commentslist[j]['brief_id'] == (188 or 189 or 190 or 191):
						commentsreceived['02 - Making a living'] = commentsreceived['02 - Making a living'] + 1
					elif commentslist[j]['brief_id'] == (262 or 264 or 267 or 269):
						commentsreceived['03 - We, the people'] = commentsreceived['03 - We, the people'] + 1
					elif commentslist[j]['brief_id'] == (322 or 323 or 324):
						commentsreceived['04 - Caring for commons'] = commentsreceived['04 - Caring for commons'] + 1
					elif commentslist[j]['brief_id'] == (401 or 403 or 405 or 406):
						commentsreceived['05 - Learning'] = commentsreceived['05 - Learning'] + 1
					elif commentslist[j]['brief_id'] == (482 or 481 or 484 or 486 or 487):
						commentsreceived['06 - Living together'] = commentsreceived['06 - Living together'] + 1
					elif commentslist[j]['brief_id'] == (640 or 712 or 1162):
						commentsreceived['07 -Finale'] = commentsreceived['07 -Finale'] + 1
					elif commentslist[j]['brief_id'] == (682 or 683 or 688):
						commentsreceived['08 - Resilience'] = commentsreceived['08 - Resilience'] + 1
					else:
						commentsreceived['00 - Undefined'] = commentsreceived['00 - Undefined'] + 1
				
		user_i_time_t.append(userlist[i]['user_id'])
		user_i_time_t.append(datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d'))
		user_i_time_t.append(commentswritten)
		user_i_time_t.append(commentsreceived)
		user_i_time_t.append(commentsreceived_team)
		bigtable.append(user_i_time_t)
		time = time + timestep
		
file_writer = csv.writer(to_file)

file_writer.writerow('userlist')
file_writer.writerow(userlist)
file_writer.writerow('commentslist')
file_writer.writerow(commentslist)

# Write bigtable into the file.

# Write the header of the CSV file
# file_writer.writerow(['comment ID','author community','comment length','topic','recipient community'])


# Write all the rows
file_writer.writerows('bigtable')
file_writer.writerows(bigtable)

to_file.close()

print ("end")
