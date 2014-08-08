
ge Weeks=(time-1321228800)/604800 +1
egen st_id=group( sn_user_id tn_user_id)
xtset st_id Weeks
xtreg edge l.sn_kcores l.sn_pagerank l.graphdensity l.sn_indegree l.sn_outdegree ///
			 l.tn_kcores l.tn_pagerank l.tn_indegree l.tn_outdegree tn_npostsin* i.Weeks if sn_team=="False",fe cluster(sn_user_id)

xtlogit edge l.sn_kcores l.sn_pagerank l.graphdensity l.sn_indegree l.sn_outdegree ///
			 l.tn_kcores l.tn_pagerank l.tn_indegree l.tn_outdegree tn_npostsin* i.Weeks if sn_team=="False",fe 
