```plsql
CREATE OR REPLACE FUNCTION team_brawler_performance(ptag varchar) RETURNS TABLE(
		emode varchar,
		emap varchar,
		bn varchar,
		overall_winrate numeric,
		individual_winrate numeric
) AS $$
BEGIN
	RETURN QUERY SELECT 
		A.event_mode,A.event_map,A.brawler_name,ROUND((A.w::numeric*100)/A.gp::numeric,2),ROUND((B.w::numeric*100)/B.gp::numeric,2)
	FROM 
		(SELECT event_mode,event_map,brawler_name,sum(wins) w,sum(games_played) gp FROM team_analysis GROUP BY event_mode,event_map,brawler_name) A 
	FULL OUTER JOIN 
		(SELECT event_mode,event_map,brawler_name,sum(wins) w,sum(games_played) gp FROM team_analysis WHERE tag = '#2LJYR2UU' GROUP BY event_mode,event_map,brawler_name) B 
	ON
		A.event_mode = B.event_mode and A.event_map = B.event_map and A.brawler_name = B.brawler_name; 
END;
$$ LANGUAGE plpgsql;	
	
CREATE OR REPLACE FUNCTION brawler_performance(ptag varchar) RETURNS TABLE(
		bn varchar,
		overall_winrate numeric,
		individual_winrate numeric
) AS $$
BEGIN
	RETURN QUERY SELECT 
		A.brawler_name,(A.w::numeric*100)/A.gp::numeric,(B.w::numeric*100)/B.gp::numeric
	FROM
		(SELECT brawler_name,sum(wins) w,sum(games_played) gp FROM team_analysis GROUP BY brawler_name) A
	FULL OUTER JOIN
		(SELECT brawler_name,sum(wins) w,sum(games_played) gp FROM team_analysis WHERE tag = ptag GROUP BY brawler_name) B
	ON
		A.brawler_name = B.brawler_name;
END;
$$ LANGUAGE plpgsql;

	
CREATE OR REPLACE FUNCTION showdown_brawler_performance(ptag varchar) RETURNS TABLE(
		emap varchar,
		bname varchar,
		rank1_winrate numeric,
		rank2_winrate numeric
) AS $$
BEGIN
	RETURN QUERY SELECT 
		A.event_map,A.brawler_name,ROUND((A.r1::numeric*100)/A.gp::numeric,2),ROUND((A.r2::numeric*100)/A.gp::numeric,2),ROUND((B.r1::numeric*100)/B.gp::numeric,2),ROUND((B.r2::numeric*100)/B.gp::numeric,2)
	FROM
		(SELECT event_map,brawler_name,sum(rank_1) r1,sum(rank_2) r2,sum(games_played) gp FROM showdown_analysis GROUP BY event_map,brawler_name) A
	FULL OUTER JOIN
		(SELECT event_map,brawler_name,sum(rank_1) r1,sum(rank_2) r2,sum(games_played) gp FROM showdown_analysis WHERE tag = ptag GROUP BY event_map,brawler_name) B
	ON
		A.brawler_name = B.brawler_name;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION showdown_ind_brawler_performance(ptag varchar,st int) RETURNS TABLE(
		emap varchar,
		bname varchar,
		rank1_winrate numeric,
		rank2_winrate numeric
) AS $$
BEGIN
	RETURN QUERY SELECT 
		A.event_map,A.brawler_name,ROUND((A.r1::numeric*100)/A.gp::numeric,2),ROUND((A.r2::numeric*100)/A.gp::numeric,2),ROUND((B.r1::numeric*100)/B.gp::numeric,2),ROUND((B.r2::numeric*100)/B.gp::numeric,2)
	FROM
		(SELECT event_map,brawler_name,sum(rank_1) r1,sum(rank_2) r2,sum(games_played) gp FROM showdown_analysis WHERE showdown_type=st GROUP BY event_map,brawler_name) A
	FULL OUTER JOIN
		(SELECT event_map,brawler_name,sum(rank_1) r1,sum(rank_2) r2,sum(games_played) gp FROM showdown_analysis WHERE tag = ptag and showdown_type=st GROUP BY event_map,brawler_name) B
	ON
		A.brawler_name = B.brawler_name;
END;
$$ LANGUAGE plpgsql;
	
```

