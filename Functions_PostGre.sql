CREATE OR REPLACE FUNCTION WIN_TEAM(ptag varchar) RETURNS TABLE (
		w BIGINT,
		gp BIGINT
) AS $$
BEGIN
	RETURN QUERY SELECT
		sum(wins),
		sum(games_played)
	FROM
		team_analysis
	WHERE
		tag = ptag ;
END;
$$ LANGUAGE plpgsql;

select * from WIN_TEAM('#2LJYR2UU')

CREATE OR REPLACE FUNCTION WIN_SHOW(ptag varchar) RETURNS TABLE (
		r1 BIGINT,
		r2 BIGINT,
		gp BIGINT
) AS $$
BEGIN
	RETURN QUERY SELECT
		sum(rank_1),
		sum(rank_2),
		sum(games_played)
	FROM
		showdown_analysis
	WHERE
		tag = ptag ;
END;
$$ LANGUAGE plpgsql;

select * from WIN_SHOW('#2LJYR2UU')

CREATE OR REPLACE FUNCTION WIN_SHOWR(ptag varchar,st int) RETURNS TABLE (
		r1 BIGINT,
		r2 BIGINT,
		gp BIGINT
) AS $$
BEGIN
	RETURN QUERY SELECT 
		sum(rank_1),sum(rank_2),sum(games_played)
	FROM
		showdown_analysis
	WHERE 
		tag = ptag and showdown_type = st;
END;
$$ LANGUAGE plpgsql;

select * from WIN_SHOWR('#2LJYR2UU',2)

CREATE OR REPLACE FUNCTION IND_MAP(ptag varchar) RETURNS TABLE (
		emode VARCHAR,
		emap VARCHAR,
		w BIGINT,
		gp BIGINT
) AS $$
BEGIN
	RETURN QUERY SELECT 
		event_mode,event_map,sum(wins),sum(games_played)
	FROM
		team_analysis
	WHERE 
		tag = ptag
	GROUP BY
		event_mode,event_map
	ORDER BY
		event_mode;
END;
$$ LANGUAGE plpgsql;

select * from IND_MAP('#2LJYR2UU')

CREATE OR REPLACE FUNCTION IND_MAP_SHOW(ptag varchar) RETURNS TABLE (
		emap VARCHAR,
		r1 BIGINT,
		r2 BIGINT,
		gp BIGINT
) AS $$
BEGIN
	RETURN QUERY SELECT 
		event_map,sum(rank_1),sum(rank_2),sum(games_played)
	FROM
		showdown_analysis
	WHERE 
		tag = ptag
	GROUP BY
		event_map;
END;
$$ LANGUAGE plpgsql;

select * from IND_MAP_SHOW('#2LJYR2UU')

CREATE OR REPLACE FUNCTION IND_MAP_SHOWE(ptag varchar,st int) RETURNS TABLE (
		emap VARCHAR,
		r1 BIGINT,
		r2 BIGINT,
		gp BIGINT
) AS $$
BEGIN
	RETURN QUERY SELECT 
		event_map,sum(rank_1),sum(rank_2),sum(games_played)
	FROM
		showdown_analysis
	WHERE 
		tag = ptag and showdown_type = st
	GROUP BY
		event_map;
END;
$$ LANGUAGE plpgsql;

select * from IND_MAP_SHOWE('#2LJYR2UU',2);


CREATE OR REPLACE FUNCTION IND_BRAW(ptag varchar) RETURNS TABLE (
		bn VARCHAR,
		w BIGINT,
		gp BIGINT
) AS $$
BEGIN
	RETURN QUERY SELECT 
		brawler_name,sum(wins),sum(games_played)
	FROM
		team_analysis
	WHERE 
		tag = ptag
	GROUP BY
		brawler_name;
END;
$$ LANGUAGE plpgsql;

select * from IND_BRAW('#2LJYR2UU');

CREATE OR REPLACE FUNCTION IND_BRAW_SHOW(ptag varchar) RETURNS TABLE (
		bn VARCHAR,
		r1 BIGINT,
		r2 BIGINT,
		gp BIGINT
) AS $$
BEGIN
	RETURN QUERY SELECT 
		brawler_name,sum(rank_1),sum(rank_2),sum(games_played)
	FROM
		showdown_analysis
	WHERE 
		tag = ptag
	GROUP BY
		brawler_name;
END;
$$ LANGUAGE plpgsql;

select * from IND_BRAW_SHOW('#2LJYR2UU');

CREATE OR REPLACE FUNCTION IND_BRAW_SHOWR(ptag varchar,st int) RETURNS TABLE (
		bn VARCHAR,
		r1 BIGINT,
		r2 BIGINT,
		gp BIGINT
) AS $$
BEGIN
	RETURN QUERY SELECT 
		brawler_name,sum(rank_1),sum(rank_2),sum(games_played)
	FROM
		showdown_analysis
	WHERE 
		tag = ptag and showdown_type = st
	GROUP BY
		brawler_name;
END;
$$ LANGUAGE plpgsql;

select * from IND_BRAW_SHOWR('#2LJYR2UU',1);

CREATE OR REPLACE FUNCTION IND_BRAW_MAP_SHOW(ptag varchar) RETURNS TABLE (
		emap VARCHAR,
		bname VARCHAR,
		r1 BIGINT,
		r2 BIGINT,
		gp BIGINT
) AS $$
BEGIN
	RETURN QUERY SELECT 
		event_map,brawler_name,sum(rank_1),sum(rank_2),sum(games_played)
	FROM
		showdown_analysis
	WHERE 
		tag = ptag
	GROUP BY
		event_map,brawler_name;
END;
$$ LANGUAGE plpgsql;

drop function ind_braw_map_show

select * from IND_BRAW_MAP_SHOW('#2LJYR2UU')

CREATE OR REPLACE FUNCTION IND_BRAW_MAP_SHOWR(ptag varchar,st int) RETURNS TABLE (
		emap VARCHAR,
		bname VARCHAR,
		r1 BIGINT,
		r2 BIGINT,
		gp BIGINT
) AS $$
BEGIN
	RETURN QUERY SELECT 
		event_map,brawler_name,sum(rank_1),sum(rank_2),sum(games_played)
	FROM
		showdown_analysis
	WHERE 
		tag = ptag and showdown_type = st
	GROUP BY
		event_map,brawler_name;
END;
$$ LANGUAGE plpgsql;

drop function ind_braw_map_showr

select * from IND_BRAW_MAP_SHOWR('#2LJYR2UU',2)


CREATE OR REPLACE FUNCTION IND_BRAW_MAP(ptag varchar) RETURNS TABLE (
		emode VARCHAR,
		emap VARCHAR,
		bname VARCHAR,
		w BIGINT,
		gp BIGINT
) AS $$
BEGIN
	RETURN QUERY SELECT 
		event_mode,event_map,brawler_name,sum(wins),sum(games_played)
	FROM
		team_analysis
	WHERE 
		tag = ptag
	GROUP BY
		event_mode,event_map,brawler_name;
END;
$$ LANGUAGE plpgsql;

select * from IND_BRAW_MAP('#2LJYR2UU')

CREATE OR REPLACE FUNCTION OIND_BRAW_WINS() RETURNS TABLE(
    brname VARCHAR,
    w BIGINT,
    gp BIGINT
) AS $$
BEGIN
    RETURN QUERY SELECT 
        brawler_name,sum(wins),sum(games_played)
    FROM
        team_analysis
    GROUP BY
        brawler_name;           
END;
$$ LANGUAGE plpgsql;

SELECT * FROM OIND_BRAW_WINS()

CREATE OR REPLACE FUNCTION OSHOWDOWN_BRAW_WINS() RETURNS TABLE(
    brname VARCHAR,
    r1 BIGINT,
    r2 BIGINT,
    gp BIGINT
) AS $$
BEGIN
    RETURN QUERY SELECT 
        brawler_name,sum(rank_1),sum(rank_2),sum(games_played)
    FROM
        showdown_analysis
    GROUP BY
        brawler_name;           
END;
$$ LANGUAGE plpgsql;

SELECT * FROM OSHOWDOWN_BRAW_WINS()

CREATE OR REPLACE FUNCTION OTEAM_BRAW_MAP() RETURNS TABLE(
    emode VARCHAR,
    emap VARCHAR,
    brname VARCHAR,
    w BIGINT,
    gp BIGINT
) AS $$
BEGIN
    RETURN QUERY SELECT 
        event_mode,event_map,brawler_name,sum(wins),sum(games_played)
    FROM
        team_analysis
    GROUP BY
        event_mode,event_map,brawler_name;           
END;
$$ LANGUAGE plpgsql;

SELECT * FROM OTEAM_BRAW_MAP()

CREATE OR REPLACE FUNCTION OSHOWDOWN_BRAW_MAP() RETURNS TABLE(
    emap VARCHAR,
    brname VARCHAR,
    r1 BIGINT,
    r2 BIGINT,
    gp BIGINT
) AS $$
BEGIN
    RETURN QUERY SELECT 
        event_map,brawler_name,sum(rank_1),sum(rank_2),sum(games_played)
    FROM
        showdown_analysis
    GROUP BY
        event_map,brawler_name;           
END;
$$ LANGUAGE plpgsql;

SELECT * FROM OSHOWDOWN_BRAW_MAP()

CREATE OR REPLACE FUNCTION OSHOWDOWN_BRAW_TYPE(st int) RETURNS TABLE(
    brname VARCHAR,
    r1 BIGINT,
    r2 BIGINT,
    gp BIGINT
) AS $$
BEGIN
    RETURN QUERY SELECT 
        brawler_name,sum(rank_1),sum(rank_2),sum(games_played)
    FROM
        showdown_analysis
    WHERE
        showdown_type = st     
    GROUP BY
        brawler_name;           
END;
$$ LANGUAGE plpgsql;

SELECT * FROM OSHOWDOWN_BRAW_TYPE(2)

CREATE OR REPLACE FUNCTION OSHOWDOWN_BRAW_MAP_TYPE(st int) RETURNS TABLE(
    emap VARCHAR,
    brname VARCHAR,
    r1 BIGINT,
    r2 BIGINT,
    gp BIGINT
) AS $$
BEGIN
    RETURN QUERY SELECT 
        event_map,brawler_name,sum(rank_1),sum(rank_2),sum(games_played)
    FROM
        showdown_analysis
    WHERE
        showdown_type = st     
    GROUP BY
        event_map,brawler_name;           
END;
$$ LANGUAGE plpgsql;

SELECT * FROM OSHOWDOWN_BRAW_MAP_TYPE(2)

CREATE OR REPLACE FUNCTION AVG_BRAW_IND(ptag VARCHAR) RETURNS TABLE(
    avg_troph NUMERIC,
    avg_rank NUMERIC,
    avg_power NUMERIC
) AS $$
BEGIN
    RETURN QUERY SELECT 
        floor(avg(brawler_trophies)),floor(avg(brawler_rank)),floor(avg(brawler_power))
    FROM 
        brawlers
    WHERE 
        tag = ptag;     
END;
$$ LANGUAGE plpgsql;

SELECT * FROM AVG_BRAW_IND('#2LJYR2UU')


CREATE OR REPLACE FUNCTION AVG_BRAW() RETURNS TABLE(
    avg_troph NUMERIC,
    avg_rank NUMERIC,
    avg_power NUMERIC
) AS $$
BEGIN
    RETURN QUERY SELECT 
        floor(avg(brawler_trophies)),floor(avg(brawler_rank)),floor(avg(brawler_power))
    FROM 
        brawlers;    
END;
$$ LANGUAGE plpgsql;

SELECT * FROM AVG_BRAW()

CREATE OR REPLACE FUNCTION team_brawler_performance(ptag varchar) RETURNS TABLE(
		emode varchar,
		emap varchar,
		bn varchar,
		overall_winrate bigint,
		individual_winrate bigint
) AS $$
BEGIN
	RETURN QUERY SELECT 
		A.event_mode,A.event_map,A.brawler_name,(A.w*100)/A.gp,(B.w*100)/B.gp
	FROM 
		(SELECT event_mode,event_map,brawler_name,sum(wins) w,sum(games_played) gp FROM team_analysis GROUP BY event_mode,event_map,brawler_name) A 
	FULL OUTER JOIN 
		(SELECT event_mode,event_map,brawler_name,sum(wins) w,sum(games_played) gp FROM team_analysis WHERE tag = ptag GROUP BY event_mode,event_map,brawler_name) B 
	ON
		A.event_mode = B.event_mode and A.event_map = B.event_map and A.brawler_name = B.brawler_name; 
END;
$$ LANGUAGE plpgsql;	
	
CREATE OR REPLACE FUNCTION brawler_performance(ptag varchar) RETURNS TABLE(
		bn varchar,
		overall_winrate bigint,
		individual_winrate bigint
) AS $$
BEGIN
	RETURN QUERY SELECT 
		A.brawler_name,(A.w*100)/A.gp,(B.w*100)/B.gp
	FROM
		(SELECT brawler_name,sum(wins) w,sum(games_played) gp FROM team_analysis GROUP BY brawler_name) A
	FULL OUTER JOIN
		(SELECT brawler_name,sum(wins) w,sum(games_played) gp FROM team_analysis WHERE tag = ptag GROUP BY brawler_name) B
	ON
		A.brawler_name = B.brawler_name;
END;
$$ LANGUAGE plpgsql;