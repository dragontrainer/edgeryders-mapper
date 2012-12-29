## This program returns a list of all comments on the Edgeryders platform as a
## CSV file. There is one row per comment. There are 5 columms: (1) comment ID,
## (2) modularity partition class of the comment's author, (3) comment length
## in characters, (4) topic ID, (5) modularity partition class of the comment's
## recipient.

## The inputs are the json files exported from the Edgeryders database and a
## CSV file generated from a network analysis software that associates to each
## Edgeryders user its modularity partition class.

## ----------------------------------------------------

#import libraries

import json
# import tkinter
import csv

# "Save as" dialog
# to_filename = tkinter.filedialog.asksaveasfilename()
to_filename = '/Users/albertocottica/Documents/PhD/MyPhDdata/Extraction 2012-12-05-1623/exported_debugged_w_headers.csv'
to_file = open(to_filename, 'w', newline = '')



# load the files into python
# all the comments from drupal
comments_filename = '/Users/albertocottica/Documents/PhD/MyPhDdata/Extraction 2012-12-05-1623/json/comments.json' #remember to change this name to /comments.json
comments_data = open(comments_filename)
jcomments = json.load(comments_data)

# all the nodes (posts & co) from drupal
nodes_filename = '/Users/albertocottica/Documents/PhD/MyPhDdata/Extraction 2012-12-05-1623/json/nodes.json' #remember to change this name to /users.json
nodes_data = open(nodes_filename)
jnodes = json.load(nodes_data)

# the computed partitions
partition_filename = '/Users/albertocottica/Documents/PhD/MyPhDdata/Extraction 2012-12-05-1623/ER_people_by_modularity_class.csv'
partition_data = open(partition_filename, 'r', encoding = 'utf-8')

# we need to store the computed partitions somewhere to avoid the need to
# re-open the file at each comment iteration
saved_partition_data = {} # this will be a hash using the user id as a key
partition_data_reader = csv.DictReader(partition_data)
for row in partition_data_reader:
    saved_partition_data[int(row['Id'])] = row 

allcomments = jcomments['comments']
allnodes = jnodes['nodes']

bigtable = [] # create a nested list that contains the relevant info for each comment

for i in range (len(allcomments)): #the loop drives the whole program
	tablerow = [] #create an empty list to collect the data of an individual comment; re-initialize at each iteration
	
	# get the comment id
	comment_id = int(allcomments[i]['comment']['cid'])
	tablerow.append(comment_id)
	
	#get the author id
	author_id = int(allcomments[i]['comment']['uid'])
	
	# find the corresponding community using partition_data
    # line = partition_data.readline() # skip the header line
    # line = partition_data.readline()
    #
    # while line[:line.find(',')] != str(author_id) and line != '':
    #     line = partition_data.readline()
    # if line == '':
    #     author_community = 0 #catches "not found" errors
    # else:
    #     author_community = int(line[(line.find(',', -4) + 1):-1])
	author_community_row = saved_partition_data.get(author_id, {'Modularity Class':0}) # N.B. the second argument is the value to return if the author_id is not present
	author_community = int(author_community_row['Modularity Class'])
	
	tablerow.append(author_community)
	
	#get the comment length
	if 'comment' in allcomments[i]['comment']:
		comment_length = len(allcomments[i]['comment']['comment'])
	else:
		comment_length = 0
	tablerow.append(comment_length)
	
	#get the topic. Begin by getting the node that the comment is a comment to and store it in a variable
	node_id = allcomments[i]['comment']['nid']
	
	# find the node id that corresponds to the ith comment, and read its mission brief (group)
	# read also the author's id (uid)
	j = 0
	while j < len(allnodes) and  allnodes[j]['node']['nid'] != node_id:
		j = j + 1
		if j == len(allnodes):
			brief_id = 0
			report_author_id = 0
		else:
			brief_id = int(allnodes[j]['node']['gid'])
			if 'uid' in allnodes[j]['node']:
				report_author_id = int(allnodes[j]['node']['uid'])
			else:
				report_author_id = 0
	
	# determine what campaign the mission brief ids corresponds to. Source: http://edgeryders.ppa.coe.int/campaigns-from-brief-ids
	if brief_id == 29 or brief_id == 43 or brief_id == 44 or brief_id == 45:
		campaign = '01 - Bootcamp'
	elif brief_id == 188 or brief_id == 189 or brief_id == 190 or brief_id == 191:
		campaign = '02 - Making a living'
	elif brief_id == 262 or brief_id == 264 or brief_id == 267 or brief_id == 269:
		campaign = '03 - We, the people'
	elif brief_id == 322 or brief_id == 323 or brief_id == 324:
		campaign = '04 - Caring for commons'
	elif brief_id == 401 or brief_id == 403 or brief_id == 405 or brief_id == 406:
		campaign = '05 - Learning'
	elif brief_id == 482 or brief_id == 481 or brief_id == 484 or brief_id == 486 or brief_id == 487:
		campaign = '06 - Living together'
	elif brief_id == 640 or brief_id == 712 or brief_id == 1162:
		campaign = '07 -Finale'
	elif brief_id == 682 or brief_id == 683 or brief_id == 688:
		campaign = '08 - Resilience'
	else:
		campaign = '00 - Undefined'
	
	tablerow.append(campaign)
	
	# now determine the target of the comment. Begin by finding out whether the comment has a pid
	# i.e. it is a comment to a comment. If not, the target is the author of the mission report
	
	if 'pid' not in allcomments[i]['comment']:
		target_id = report_author_id
	# if the comment does have a pid, we need to look into comments.json
	else:
		parent_comment = allcomments[i]['comment']['pid']
		k = 0
		while k < len(allcomments) and allcomments[k]['comment']['cid'] != parent_comment:
			k = k + 1
		if k == len(allcomments):
			target_id = 0
		else:
			target_id = int(allcomments[k]['comment']['uid'])
	
	# target_id now identifies the comment's target. Find the community it belongs to as above.
    # line = partition_data.readline() # skip the header line
    # line = partition_data.readline()
    # while line[:line.find(',')] != str(target_id) and line != '':
    #     line = partition_data.readline()
    # if line == '':
    #     target_community = 0 #catches "not found" errors
    # else:
    #     target_community = int(line[(line.find(',', -4) + 1):-1])
	target_community_row = saved_partition_data.get(target_id, {'Modularity Class':0}) # N.B. the second argument is the value to return if the target_id is not present
	target_community = target_community_row['Modularity Class']
	
	tablerow.append(target_community)
	
	# the i-th table row is now appended to bigtable
	
	bigtable.append(tablerow)

# Write bigtable into a file.

file_writer = csv.writer(to_file)

# Write the header of the CSV file
file_writer.writerow(['comment ID','author community','comment length','topic','recipient community'])

# Write all the rows
file_writer.writerows(bigtable)

to_file.close()
