Structure of the json export
============================

nodes.js
--------

The structure of content in Edgeryders is: **mission reports** (roughly, answers) are members of groups called **mission briefs** (roughly, questions) that in turn are members of groups called **campaigns**.

Right now, the view in Drupal returns a variable called gid (group ID). That is the node ID of the group that the node being extracted is appended to. An extracted mission report looks like this:
 
```
	"node" : {         
		"nid" : "99",         
		"uid" : "51",         
		"type" : "Mission report",         
		"title" : "A world of peers ...",         
		"date" : "18 Oct 2011 - 23:28",         
		"gid" : "29"       
	}
```

"29" corresponds to a mission brief called "Share your ryde". The view returns all nodes, so you can look up the return for node 29 that looks like this:

```
      "node" : {
        "nid" : "29",
        "uid" : "1",
        "type" : "Mission brief",
        "title" : "Share your Ryde",
        "date" : "22 Nov 2011 - 12:18",
        "parent-gid" : "30"
      }
```

now, node 29 is member of node 30, that corresponds to the campaign called "Bootcamp". Let's look at node 30:

```
      "node" : {
        "nid" : "30",
        "uid" : "1",
        "type" : "Campaign",
        "title" : "BOOTCAMP",
        "date" : "12 Oct 2011 - 12:28"
      }
```

it has no gid, because it is a top-level node. 

The ```type``` attribute can have the following values:

* User profile
* Mission report
* Mission brief
* Campaign
