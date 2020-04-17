-- <<<<<<< HEAD
-- =======
-- <<<<<<< HEAD
-- >>>>>>> a2dee79ba125e6a7a8537cb01ed582596ce87b1a
-- Winning Percentage for a player's team events
select sum(wins),sum(games_played) Winning_Percentage from team_analysis where tag = '#2LJYR2UU'

-- Winning Percentage for a player's showdown events
select sum(rank_1),sum(rank_2),sum(games_played) from showdown_analysis where tag = '#2LJYR2UU'

-- Winning Percentage for a player's showdown events with respect to showdown type
select 
	sum(rank_1),sum(rank_2),sum(games_played)
from
	showdown_analysis
where 
	tag = '#2LJYR2UU' and showdown_type = 2

-- Individual Players's Performance event map wise for team events
select 
	event_map,sum(wins),sum(games_played) 
from 
	team_analysis 
where 
	tag = '#2LJYR2UU' 
group by 
	event_map

-- Individual Players's Performance event map wise for showdown events irrespective to showdown type
select 
	event_map,sum(rank_1),sum(rank_2),sum(games_played) 
from 
	showdown_analysis 
where 
	tag = '#2LJYR2UU' 
group by 
	event_map

-- Individual Players's Performance event map wise for showdown events with respect to showdown type
select 
	event_map,sum(rank_1),sum(rank_2),sum(games_played) 
from 
	showdown_analysis 
where 
	tag = '#2LJYR2UU' and showdown_type = 2
group by 
	event_map


-- Individual Player's brawler performance for team event	
select
	brawler_name,sum(wins),sum(games_played)
from 
	team_analysis
where
	tag = '#2LJYR2UU'
group by
	brawler_name


-- Individual Player's brawer performance for showdown event irrespective of showdown type	
select
	brawler_name,sum(rank_1),sum(rank_2),sum(games_played)
from 
	showdown_analysis
where
	tag = '#2LJYR2UU'
group by
	brawler_name
	
-- Individual Player's Brawler prformance with respect to event map for team events	
select
	event_map,brawler_name,sum(wins),sum(games_played)
from 
	team_analysis
where
	tag = '#2LJYR2UU'
group by
	event_map,brawler_name
	

-- Individual Player's Brawler prformance with respect to event map for team events	irrespective of showdown type
select
	event_map,brawler_name,sum(rank_1),sum(rank_2),sum(games_played)
from 
	showdown_analysis
where
	tag = '#2LJYR2UU'
group by
	event_map,brawler_name
	
-- <<<<<<< HEAD

-- UPTO HERE DONE

-- =======
-- >>>>>>> a2dee79ba125e6a7a8537cb01ed582596ce87b1a
-- Overall Brawler's performance 
select
	brawler_name,sum(wins),sum(games_played)
from 
	team_analysis
group by
	brawler_name
	
-- Overall Brawler's Performance for showdown irrespective of showdown type
select
	brawler_name,sum(rank_1),sum(rank_2),sum(games_played)
from 
	showdown_analysis
group by
	brawler_name


-- Overall brawler's performance with respect to event map for team event	
select
	event_map,brawler_name,sum(wins),sum(games_played)
from 
	team_analysis
group by
	event_map,brawler_name
	

-- Overall brawler's performance with respect to event map for showdown event irrespective to shwodown type	
select
	event_map,brawler_name,sum(rank_1),sum(rank_2),sum(games_played)
from 
	showdown_analysis
group by
	event_map,brawler_name

-- Individual Player's brawer performance for showdown event with respect to showdown type	
select
	brawler_name,sum(rank_1),sum(rank_2),sum(games_played)
from 
	showdown_analysis
where
	tag = '#2LJYR2UU' and showdown_type = 2
group by
	brawler_name

-- Individual Player's Brawler prformance with respect to event map for team events	with respect to showdown type
select
	event_map,brawler_name,sum(rank_1),sum(rank_2),sum(games_played)
from 
	showdown_analysis
where
	tag = '#2LJYR2UU' and showdown_type = 1
group by
	event_map,brawler_name


-- Overall brawler's performance with respect to event map for showdown event with respect to shwodown type	
select
	brawler_name,sum(rank_1),sum(rank_2),sum(games_played)
from 
	showdown_analysis
where 
	showdown_type = 2
group by
	brawler_name
	
	
-- Overall brawler's performance with respect to event map for showdown event with respect to shwodown type	
select
	event_map,brawler_name,sum(rank_1),sum(rank_2),sum(games_played)
from 
	showdown_analysis
where
	showdown_type = 1
group by
	event_map,brawler_name

-- Calculate Average Brawler Trophies,Brawler Rank,Brawler Power for individual player
select floor(avg(brawler_trophies)),floor(avg(brawler_rank)),floor(avg(brawler_power)) from brawlers where tag = '#2LJYR2UU'

-- Calculate Average Brawler Trophies,Brawler Rank,Brawler Power for all
select floor(avg(brawler_trophies)),floor(avg(brawler_rank)),floor(avg(brawler_power)) from brawlers

select * from brawlers order by brawler_highest_trophies

-- <<<<<<< HEAD
-- select 
-- 	event_mode,event_map,sum(wins),sum(games_played) 
-- from 
-- 	team_analysis 
-- where 
-- 	tag = '#2LJYR2UU'
-- group by 
-- 	event_mode,event_map;
	
-- select 
-- 	event_mode,event_map,sum(wins),sum(games_played) 
-- from 
-- 	team_analysis 
-- group by 
-- 	event_mode,event_map
-- order by
-- 	event_mode
=======
select 
	event_mode,event_map,sum(wins),sum(games_played) 
from 
	team_analysis 
where 
	tag = '#2LJYR2UU'
group by 
	event_mode,event_map;
	
select 
	event_mode,event_map,sum(wins),sum(games_played) 
from 
	team_analysis 
group by 
	event_mode,event_map
order by
	event_mode
-- =======
-- Winning Percentage for a player's team events
select sum(wins),sum(games_played) Winning_Percentage from team_analysis where tag = '#2LJYR2UU'

-- Winning Percentage for a player's showdown events
select sum(rank_1),sum(rank_2),sum(games_played) from showdown_analysis where tag = '#2LJYR2UU'

-- Winning Percentage for a player's showdown events with respect to showdown type
select 
	sum(rank_1),sum(rank_2),sum(games_played)
from
	showdown_analysis
where 
	tag = '#2LJYR2UU' and showdown_type = 2

-- Individual Players's Performance event map wise for team events
select 
	event_map,sum(wins),sum(games_played) 
from 
	team_analysis 
where 
	tag = '#2LJYR2UU' 
group by 
	event_map

-- Individual Players's Performance event map wise for showdown events irrespective to showdown type
select 
	event_map,sum(rank_1),sum(rank_2),sum(games_played) 
from 
	showdown_analysis 
where 
	tag = '#2LJYR2UU' 
group by 
	event_map

-- Individual Players's Performance event map wise for showdown events with respect to showdown type
select 
	event_map,sum(rank_1),sum(rank_2),sum(games_played) 
from 
	showdown_analysis 
where 
	tag = '#2LJYR2UU' and showdown_type = 2
group by 
	event_map


-- Individual Player's brawler performance for team event	
select
	brawler_name,sum(wins),sum(games_played)
from 
	team_analysis
where
	tag = '#2LJYR2UU'
group by
	brawler_name


-- Individual Player's brawer performance for showdown event irrespective of showdown type	
select
	brawler_name,sum(rank_1),sum(rank_2),sum(games_played)
from 
	showdown_analysis
where
	tag = '#2LJYR2UU'
group by
	brawler_name
	
-- Individual Player's Brawler prformance with respect to event map for team events	
select
	event_map,brawler_name,sum(wins),sum(games_played)
from 
	team_analysis
where
	tag = '#2LJYR2UU'
group by
	event_map,brawler_name
	

-- Individual Player's Brawler prformance with respect to event map for team events	irrespective of showdown type
select
	event_map,brawler_name,sum(rank_1),sum(rank_2),sum(games_played)
from 
	showdown_analysis
where
	tag = '#2LJYR2UU'
group by
	event_map,brawler_name
	
-- Overall Brawler's performance 
select
	brawler_name,sum(wins),sum(games_played)
from 
	team_analysis
group by
	brawler_name
	
-- Overall Brawler's Performance for showdown irrespective of showdown type
select
	brawler_name,sum(rank_1),sum(rank_2),sum(games_played)
from 
	showdown_analysis
group by
	brawler_name


-- Overall brawler's performance with respect to event map for team event	
select
	event_map,brawler_name,sum(wins),sum(games_played)
from 
	team_analysis
group by
	event_map,brawler_name
	

-- Overall brawler's performance with respect to event map for showdown event irrespective to shwodown type	
select
	event_map,brawler_name,sum(rank_1),sum(rank_2),sum(games_played)
from 
	showdown_analysis
group by
	event_map,brawler_name

-- Individual Player's brawer performance for showdown event with respect to showdown type	
select
	brawler_name,sum(rank_1),sum(rank_2),sum(games_played)
from 
	showdown_analysis
where
	tag = '#2LJYR2UU' and showdown_type = 2
group by
	brawler_name

-- Individual Player's Brawler prformance with respect to event map for team events	with respect to showdown type
select
	event_map,brawler_name,sum(rank_1),sum(rank_2),sum(games_played)
from 
	showdown_analysis
where
	tag = '#2LJYR2UU' and showdown_type = 1
group by
	event_map,brawler_name


-- Overall brawler's performance with respect to event map for showdown event with respect to shwodown type	
select
	brawler_name,sum(rank_1),sum(rank_2),sum(games_played)
from 
	showdown_analysis
where 
	showdown_type = 2
group by
	brawler_name
	
	
-- Overall brawler's performance with respect to event map for showdown event with respect to shwodown type	
select
	event_map,brawler_name,sum(rank_1),sum(rank_2),sum(games_played)
from 
	showdown_analysis
where
	showdown_type = 1
group by
	event_map,brawler_name

-- Calculate Average Brawler Trophies,Brawler Rank,Brawler Power for individual player
select floor(avg(brawler_trophies)),floor(avg(brawler_rank)),floor(avg(brawler_power)) from brawlers where tag = '#2LJYR2UU'

-- Calculate Average Brawler Trophies,Brawler Rank,Brawler Power for all
select floor(avg(brawler_trophies)),floor(avg(brawler_rank)),floor(avg(brawler_power)) from brawlers

select * from brawlers order by brawler_highest_trophies
-- >>>>>>> 873f84f4c9607c5ee044b93235d8fea3ebeedd3d
-- >>>>>>> a2dee79ba125e6a7a8537cb01ed582596ce87b1a
