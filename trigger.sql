CREATE TRIGGER team_analysis_trig
    AFTER INSERT
    ON BATTLE_TEAM
    FOR EACH ROW
    EXECUTE PROCEDURE team_analysis();


CREATE OR REPLACE FUNCTION team_analysis()
    RETURNS TRIGGER AS
$$
DECLARE
    cur CURSOR FOR
        SELECT
            event_mode,event_map,battle_mode
        FROM
            battle_det
        WHERE
            tag = NEW.tag
        AND
            battle_time = NEW.battle_time;
    temp RECORD;
    flag int;      
BEGIN
    OPEN cur;
    LOOP
        FETCH cur INTO temp;
        EXIT WHEN NOT found;
        SELECT count(*) INTO flag FROM team_analysis WHERE event_map = temp.event_map AND tag = NEW.player_tag AND brawler_name = NEW.brawler_name;  
        IF(flag=0) THEN
            IF(NEW.battle_result='VICTORY') THEN
                INSERT INTO team_analysis VALUES(NEW.player_tag,temp.event_mode,temp.event_map,temp.battle_mode,NEW.brawler_name,1,1);
            ELSE
                INSERT INTO team_analysis VALUES(NEW.player_tag,temp.event_mode,temp.event_map,temp.battle_mode,NEW.brawler_name,0,1);
            END IF;  
        ELSE
             IF(NEW.battle_result='VICTORY') THEN
                UPDATE team_analysis SET wins = (SELECT wins FROM team_analysis WHERE tag=NEW.player_tag AND event_map = temp.event_map AND brawler_name = NEW.brawler_name) + 1,games_played = (SELECT games_played FROM team_analysis WHERE tag=NEW.player_tag AND event_map = temp.event_map AND brawler_name = NEW.brawler_name)+1 WHERE tag = NEW.player_tag AND event_map = temp.event_map AND brawler_name = NEW.brawler_name;
            ELSE
               UPDATE team_analysis SET wins = (SELECT wins FROM team_analysis WHERE tag=NEW.player_tag AND event_map = temp.event_map AND brawler_name = NEW.brawler_name),games_played = (SELECT games_played FROM team_analysis WHERE tag=NEW.player_tag AND event_map = temp.event_map AND brawler_name = NEW.brawler_name)+1 WHERE tag = NEW.player_tag AND event_map = temp.event_map AND brawler_name = NEW.brawler_name;
            END IF;  
        END IF;
    END LOOP;
    CLOSE cur; 
    RETURN NEW;
END;
$$
LANGUAGE plpgsql;




CREATE TRIGGER solo_analysis_trig
    AFTER INSERT
    ON BATTLE_SOLO
    FOR EACH ROW
    EXECUTE PROCEDURE solo_analysis();


CREATE TRIGGER duo_analysis_trig
    AFTER INSERT
    ON BATTLE_DUO
    FOR EACH ROW
    EXECUTE PROCEDURE duo_analysis();


CREATE TABLE team_analysis(
    tag varchar(20), 
    event_mode varchar(40),
    event_map varchar(40),
    battle_mode varchar(40),
    brawler_name varchar(25),
    wins int,
    games_played int,
    PRIMARY KEY (tag,event_map,brawler_name)
);

CREATE TABLE showdown_analysis(
    tag varchar(20),
    event_mode varchar(40),
    event_map varchar(40),
    battle_mode varchar(40),
    brawler_name varchar(25),
    showdown_type int,
    rank_1 int,
    rank_2 int,
    games_played int,
    PRIMARY KEY (tag,event_map,showdown_type,brawler_name)
);

CREATE OR REPLACE FUNCTION solo_analysis()
    RETURNS TRIGGER AS
$$
DECLARE
    cur CURSOR FOR
        SELECT
            event_mode,event_map,battle_mode
        FROM
            battle_det
        WHERE
            tag = NEW.tag        
        AND
            battle_time = NEW.battle_time;
    temp RECORD;
    flag int;      
BEGIN
    OPEN cur;
    LOOP
        FETCH cur into temp;
        EXIT WHEN NOT found;
        SELECT count(*) INTO flag FROM showdown_analysis WHERE event_map = temp.event_map AND tag = NEW.player_tag AND showdown_type=1 AND brawler_name = NEW.brawler_name;  
        IF(flag=0) THEN
            IF(NEW.battle_rank=1) THEN
                INSERT INTO showdown_analysis VALUES(NEW.player_tag,temp.event_mode,temp.event_map,temp.battle_mode,NEW.brawler_name,1,1,0,1);
            ELSIF(NEW.battle_rank=2) THEN
                INSERT INTO showdown_analysis VALUES(NEW.player_tag,temp.event_mode,temp.event_map,temp.battle_mode,NEW.brawler_name,1,0,1,1);
            ELSE
                INSERT INTO showdown_analysis VALUES(NEW.player_tag,temp.event_mode,temp.event_map,temp.battle_mode,NEW.brawler_name,1,0,0,1);
            END IF;  
        ELSE
            IF(NEW.battle_rank=1) THEN
                UPDATE showdown_analysis SET rank_1 = (SELECT rank_1 FROM showdown_analysis WHERE tag=NEW.player_tag AND event_map = temp.event_map AND brawler_name = NEW.brawler_name) + 1,games_played = (SELECT games_played FROM showdown_analysis WHERE tag=NEW.player_tag AND event_map = temp.event_map AND brawler_name = NEW.brawler_name)+1 WHERE tag = NEW.player_tag AND event_map = temp.event_map AND brawler_name = NEW.brawler_name;
            ELSIF(NEW.battle_rank=2) THEN
                UPDATE showdown_analysis SET rank_2 = (SELECT rank_2 FROM showdown_analysis WHERE tag=NEW.player_tag AND event_map = temp.event_map AND brawler_name = NEW.brawler_name) +1,games_played = (SELECT games_played FROM showdown_analysis WHERE tag=NEW.player_tag AND event_map = temp.event_map AND brawler_name = NEW.brawler_name)+1 WHERE tag = NEW.player_tag AND event_map = temp.event_map AND brawler_name = NEW.brawler_name;
            ELSE 
                UPDATE showdown_analysis SET games_played = (SELECT games_played FROM showdown_analysis WHERE tag=NEW.player_tag AND event_map = temp.event_map AND brawler_name = NEW.brawler_name)+1 WHERE tag = NEW.player_tag AND event_map = temp.event_map AND brawler_name = NEW.brawler_name;
            END IF;  
        END IF;
    END LOOP;
    CLOSE cur; 
    RETURN NEW;
END;
$$
LANGUAGE plpgsql;




CREATE OR REPLACE FUNCTION duo_analysis()
    RETURNS TRIGGER AS
$$
DECLARE
    cur CURSOR FOR
        SELECT
            event_mode,event_map,battle_mode
        FROM
            battle_det
        WHERE
            tag = NEW.tag 
        AND
            battle_time = NEW.battle_time;
    temp RECORD;
    flag int;      
BEGIN
    OPEN cur;
    LOOP
        FETCH cur into temp;
        exit
        WHEN NOT found;
        SELECT count(*) INTO flag FROM showdown_analysis WHERE event_map = temp.event_map AND tag = NEW.player_tag AND showdown_type=2 AND brawler_name = NEW.brawler_name;  
        IF(flag=0) THEN
            IF(NEW.team_rank=1) THEN
                INSERT INTO showdown_analysis VALUES(NEW.player_tag,temp.event_mode,temp.event_map,temp.battle_mode,NEW.brawler_name,2,1,0,1);
            ELSIF(NEW.team_rank=2) THEN
                INSERT INTO showdown_analysis VALUES(NEW.player_tag,temp.event_mode,temp.event_map,temp.battle_mode,NEW.brawler_name,2,0,1,1);
            ELSE
                INSERT INTO showdown_analysis VALUES(NEW.player_tag,temp.event_mode,temp.event_map,temp.battle_mode,NEW.brawler_name,2,0,0,1);
            END IF;  
        ELSE
            IF(NEW.team_rank=1) THEN
                UPDATE showdown_analysis SET rank_1 = (SELECT rank_1 FROM showdown_analysis WHERE tag=NEW.player_tag AND event_map = temp.event_map AND brawler_name = NEW.brawler_name) + 1,games_played = (SELECT games_played FROM showdown_analysis where tag=NEW.player_tag AND event_map = temp.event_map AND brawler_name = NEW.brawler_name)+1 WHERE tag = NEW.player_tag AND event_map = temp.event_map AND brawler_name = NEW.brawler_name;
            ELSIF(NEW.team_rank=2) THEN
                UPDATE showdown_analysis SET rank_2 = (SELECT rank_2 FROM showdown_analysis WHERE tag=NEW.player_tag AND event_map = temp.event_map AND brawler_name = NEW.brawler_name) +1,games_played = (SELECT games_played FROM showdown_analysis WHERE tag=NEW.player_tag AND event_map = temp.event_map AND brawler_name = NEW.brawler_name)+1 WHERE tag = NEW.player_tag AND event_map = temp.event_map AND brawler_name = NEW.brawler_name;
            ELSE 
                UPDATE showdown_analysis SET games_played = (SELECT games_played FROM showdown_analysis WHERE tag=NEW.player_tag AND event_map = temp.event_map AND brawler_name = NEW.brawler_name)+1 WHERE tag = NEW.player_tag AND event_map = temp.event_map AND brawler_name = NEW.brawler_name;
            END IF;  
        END IF;
    END LOOP;
    CLOSE cur; 
    RETURN NEW;
END;
$$
LANGUAGE plpgsql;

delete from team_analysis
delete from showdown_analysis
delete from battle_team
delete from battle_solo
delete from battle_duo
-- <<<<<<< HEAD
delete from battle_det

select * from team_analysis
select * from showdown_analysis
select * from battle_team
select * from battle_solo
select * from battle_duo
select * from battle_det
-- =======
-- delete from battle_det
-- >>>>>>> 7e32776cbe3ccd30f4f03462bfdecc66ecf026be
