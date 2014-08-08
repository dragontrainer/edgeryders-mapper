* create a discrete-time variable (weeks)
ge Weeks=(time-1321228800)/604800 +1
egen st_id=group( sn_user_id tn_user_id)
xtset st_id Weeks

* aggregate content across the different topics into "bin" variables
* summarizing the activity by type conducted by (_posts and _comms_wr)
* and directed to (_comms_rec) the user in question

ge sn_posts = sn_npostsin00 + sn_npostsin01 + sn_npostsin02 + sn_npostsin03 + sn_npostsin04 ///
	+ sn_npostsin05 + sn_npostsin06 + sn_npostsin07 + sn_npostsin08

label variable sn_posts "Number of posts written by source node"
	
ge tn_posts = tn_npostsin00 + tn_npostsin01 + tn_npostsin02 + tn_npostsin03 + tn_npostsin04 ///
	+ tn_npostsin05 + tn_npostsin06 + tn_npostsin07 + tn_npostsin08
	
label variable tn_posts "Number of posts written by target node"
	
ge sn_comms_wr = sn_ncommswrittenin00 + sn_ncommswrittenin01 + sn_ncommswrittenin02 /// 
	+ sn_ncommswrittenin03 + sn_ncommswrittenin04 + sn_ncommswrittenin05 ///
	+ sn_ncommswrittenin06 + sn_ncommswrittenin07 + sn_ncommswrittenin08

label variable sn_comms_wr "Number of comments written by source node"

ge tn_comms_wr = tn_ncommswrittenin00 + tn_ncommswrittenin01 + tn_ncommswrittenin02 /// 
	+ tn_ncommswrittenin03 + tn_ncommswrittenin04 + tn_ncommswrittenin05 ///
	+ tn_ncommswrittenin06 + tn_ncommswrittenin07 + tn_ncommswrittenin08

label variable tn_comms_wr "Number of comments written by source node"

ge sn_team_comms_rec = sn_nteamcommsreceivedin00 + sn_nteamcommsreceivedin01 + sn_nteamcommsreceivedin02 ///
	+ sn_nteamcommsreceivedin03 + sn_nteamcommsreceivedin04 + sn_nteamcommsreceivedin05 ///
	+ sn_nteamcommsreceivedin06 + sn_nteamcommsreceivedin07 + sn_nteamcommsreceivedin08

label variable sn_team_comms_rec "Number of comments by moderators received by source node"

ge tn_team_comms_rec = tn_nteamcommsreceivedin00 + tn_nteamcommsreceivedin01 + tn_nteamcommsreceivedin02 ///
	+ tn_nteamcommsreceivedin03 + tn_nteamcommsreceivedin04 + tn_nteamcommsreceivedin05 ///
	+ tn_nteamcommsreceivedin06 + tn_nteamcommsreceivedin07 + tn_nteamcommsreceivedin08

label variable tn_team_comms_rec "Number of comments by moderators received by target node"

ge sn_non_team_comms_rec = sn_ncommsreceivedin00 + sn_ncommsreceivedin01 + sn_ncommsreceivedin02 ///
	+ sn_ncommsreceivedin03 + sn_ncommsreceivedin04 + sn_ncommsreceivedin05 + sn_ncommsreceivedin06 ///
	+ sn_ncommsreceivedin07 + sn_ncommsreceivedin08 

label variable sn_non_team_comms_rec "Number of comments by non-moderators received by source node"

ge tn_non_team_comms_rec = tn_ncommsreceivedin00 + tn_ncommsreceivedin01 + tn_ncommsreceivedin02 ///
	+ tn_ncommsreceivedin03 + tn_ncommsreceivedin04 + tn_ncommsreceivedin05 + tn_ncommsreceivedin06 ///
	+ tn_ncommsreceivedin07 + tn_ncommsreceivedin08 

label variable tn_non_team_comms_rec "Number of comments by non-moderators received by target node"

rename tn_betweennesscentralitycount tn_btw_cntrlty
rename sn_betweennesscentralitycount sn_btw_cntrlty
label variable tn_btw_cntrlty "Betweenness centrality of the target node"
label variable sn_btw_cntrlty "Betweenness centrality of the source node"


* now drop all binned variables

drop sn_npostsin00 sn_npostsin01 sn_npostsin02 sn_npostsin03 sn_npostsin04 sn_npostsin05 sn_npostsin06 ///
 	sn_npostsin07 sn_npostsin08 tn_npostsin00 tn_npostsin01 tn_npostsin02 tn_npostsin03 tn_npostsin04 ///
	tn_npostsin05 tn_npostsin06 tn_npostsin07 tn_npostsin08 sn_ncommswrittenin00 sn_ncommswrittenin01 /// 
	sn_ncommswrittenin02 sn_ncommswrittenin03 sn_ncommswrittenin04 sn_ncommswrittenin05 /// 
	sn_ncommswrittenin06 sn_ncommswrittenin07 sn_ncommswrittenin08 tn_ncommswrittenin00 ///
	tn_ncommswrittenin01 tn_ncommswrittenin02 tn_ncommswrittenin03 tn_ncommswrittenin04 ///
	tn_ncommswrittenin05 tn_ncommswrittenin06 tn_ncommswrittenin07 tn_ncommswrittenin08 ///
	tn_nteamcommsreceivedin00 tn_nteamcommsreceivedin01 tn_nteamcommsreceivedin02 tn_nteamcommsreceivedin03 ///
	tn_nteamcommsreceivedin04 tn_nteamcommsreceivedin05 tn_nteamcommsreceivedin06 tn_nteamcommsreceivedin07 ///
	tn_nteamcommsreceivedin08 sn_ncommsreceivedin00 sn_ncommsreceivedin01 sn_ncommsreceivedin02 ///
	sn_ncommsreceivedin03 sn_ncommsreceivedin04 sn_ncommsreceivedin05 sn_ncommsreceivedin06 ///
	sn_ncommsreceivedin07 sn_ncommsreceivedin08 tn_ncommsreceivedin00 tn_ncommsreceivedin01 ///
	tn_ncommsreceivedin02 tn_ncommsreceivedin03 tn_ncommsreceivedin04 tn_ncommsreceivedin05 ///
	tn_ncommsreceivedin06 tn_ncommsreceivedin07 tn_ncommsreceivedin08 

