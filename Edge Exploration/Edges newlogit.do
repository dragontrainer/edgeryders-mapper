* don't use modularity and density because of collinearity with the weeks dummies
* estimation with pagerank

xtlogit edge l.sn_kcores l.tn_kcores l.sn_pagerank l.tn_pagerank ///
			l.sn_indegree l.sn_outdegree l.tn_indegree l.tn_outdegree  ///
			l.sn_posts l.tn_posts l.sn_comms_wr l.tn_comms_wr l.sn_team_comms_rec ///
			l.tn_team_comms_rec l.sn_non_team_comms_rec l.tn_non_team_comms_rec ///
			i.Weeks if sn_team=="False",fe 

outreg2 using "/Users/albertocottica/Dropbox/PhD/MyPhDdata/Stata/Edges_logit_1", stats(coef se pval)  excel dec(3) ctitle (w weeks dummies) 
* estimation with betweenness centrality

xtlogit edge l.sn_kcores l.tn_kcores l.sn_btw_cntrlty l.tn_btw_cntrlty ///
			l.sn_indegree l.sn_outdegree l.tn_indegree l.tn_outdegree  ///
			l.sn_posts l.tn_posts l.sn_comms_wr l.tn_comms_wr l.sn_team_comms_rec ///
			l.tn_team_comms_rec l.sn_non_team_comms_rec l.tn_non_team_comms_rec ///
			i.Weeks if sn_team=="False",fe 
			
outreg2 using "/Users/albertocottica/Dropbox/PhD/MyPhDdata/Stata/Edges_logit_1", stats(coef se pval)  excel dec(3) ctitle (w weeks dummies) // replace


