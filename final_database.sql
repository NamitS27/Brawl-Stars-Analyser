--
-- PostgreSQL database dump
--

-- Dumped from database version 12.2
-- Dumped by pg_dump version 12.2

-- Started on 2020-04-06 17:57:49

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 225 (class 1255 OID 40977)
-- Name: duo_analysis(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.duo_analysis() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    cur CURSOR FOR
        SELECT
            event_mode,event_map,battle_mode
        FROM
            battle_det
        WHERE
            tag = NEW.player_tag 
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
        SELECT count(*) INTO flag FROM showdown_analysis WHERE event_map = temp.event_map AND tag = NEW.player_tag AND showdown_type=2;  
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
                UPDATE showdown_analysis SET rank_1 = (SELECT rank_1 FROM showdown_analysis WHERE tag=NEW.player_tag AND event_map = temp.event_map) + 1,games_played = (SELECT games_played FROM showdown_analysis where tag=NEW.player_tag AND event_map = temp.event_map)+1 WHERE tag = NEW.player_tag AND event_map = temp.event_map;
            ELSIF(NEW.team_rank=2) THEN
                UPDATE showdown_analysis SET rank_2 = (SELECT rank_2 FROM showdown_analysis WHERE tag=NEW.player_tag AND event_map = temp.event_map) +1,games_played = (SELECT games_played FROM showdown_analysis WHERE tag=NEW.player_tag AND event_map = temp.event_map)+1 WHERE tag = NEW.player_tag AND event_map = temp.event_map;
            ELSE 
                UPDATE showdown_analysis SET games_played = (SELECT games_played FROM showdown_analysis WHERE tag=NEW.player_tag AND event_map = temp.event_map)+1 WHERE tag = NEW.player_tag AND event_map = temp.event_map;
            END IF;  
        END IF;
    END LOOP;
    CLOSE cur; 
    RETURN NEW;
END;
$$;


ALTER FUNCTION public.duo_analysis() OWNER TO postgres;

--
-- TOC entry 227 (class 1255 OID 40975)
-- Name: solo_analysis(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.solo_analysis() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    cur CURSOR FOR
        SELECT
            event_mode,event_map,battle_mode
        FROM
            battle_det
        WHERE
            tag = NEW.player_tag 
        AND
            battle_time = NEW.battle_time;
    temp RECORD;
    flag int;      
BEGIN
    OPEN cur;
    LOOP
        FETCH cur into temp;
        EXIT WHEN NOT found;
        SELECT count(*) INTO flag FROM showdown_analysis WHERE event_map = temp.event_map AND tag = NEW.player_tag AND showdown_type=1;  
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
                UPDATE showdown_analysis SET rank_1 = (SELECT rank_1 FROM showdown_analysis WHERE tag=NEW.player_tag AND event_map = temp.event_map) + 1,games_played = (SELECT games_played FROM showdown_analysis WHERE tag=NEW.player_tag AND event_map = temp.event_map)+1 WHERE tag = NEW.player_tag AND event_map = temp.event_map;
            ELSIF(NEW.battle_rank=2) THEN
                UPDATE showdown_analysis SET rank_2 = (SELECT rank_2 FROM showdown_analysis WHERE tag=NEW.player_tag AND event_map = temp.event_map) +1,games_played = (SELECT games_played FROM showdown_analysis WHERE tag=NEW.player_tag AND event_map = temp.event_map)+1 WHERE tag = NEW.player_tag AND event_map = temp.event_map;
            ELSE 
                UPDATE showdown_analysis SET games_played = (SELECT games_played FROM showdown_analysis WHERE tag=NEW.player_tag AND event_map = temp.event_map)+1 WHERE tag = NEW.player_tag AND event_map = temp.event_map;
            END IF;  
        END IF;
    END LOOP;
    CLOSE cur; 
    RETURN NEW;
END;
$$;


ALTER FUNCTION public.solo_analysis() OWNER TO postgres;

--
-- TOC entry 226 (class 1255 OID 40973)
-- Name: team_analysis(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.team_analysis() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    cur CURSOR FOR
        SELECT
            event_mode,event_map,battle_mode
        FROM
            battle_det
        WHERE
            tag = NEW.player_tag 
        AND
            battle_time = NEW.battle_time;
    temp RECORD;
    flag int;      
BEGIN
    OPEN cur;
    LOOP
        FETCH cur INTO temp;
        EXIT WHEN NOT found;
        SELECT count(*) INTO flag FROM team_analysis WHERE event_map = temp.event_map AND tag = NEW.player_tag;  
        IF(flag=0) THEN
            IF(NEW.battle_result='VICTORY') THEN
                INSERT INTO team_analysis VALUES(NEW.player_tag,temp.event_mode,temp.event_map,temp.battle_mode,NEW.brawler_name,1,1);
            ELSE
                INSERT INTO team_analysis VALUES(NEW.player_tag,temp.event_mode,temp.event_map,temp.battle_mode,NEW.brawler_name,0,1);
            END IF;  
        ELSE
             IF(NEW.battle_result='VICTORY') THEN
                UPDATE team_analysis SET wins = (SELECT wins FROM team_analysis WHERE tag=NEW.player_tag AND event_map = temp.event_map) + 1,games_played = (SELECT games_played FROM team_analysis WHERE tag=NEW.player_tag AND event_map = temp.event_map)+1 WHERE tag = NEW.player_tag AND event_map = temp.event_map;
            ELSE
               UPDATE team_analysis SET wins = (SELECT wins FROM team_analysis WHERE tag=NEW.player_tag AND event_map = temp.event_map),games_played = (SELECT games_played FROM team_analysis WHERE tag=NEW.player_tag AND event_map = temp.event_map)+1 WHERE tag = NEW.player_tag AND event_map = temp.event_map;
            END IF;  
        END IF;
    END LOOP;
    CLOSE cur; 
    RETURN NEW;
END;
$$;


ALTER FUNCTION public.team_analysis() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 203 (class 1259 OID 24618)
-- Name: battle_det; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.battle_det (
    tag character varying(20) NOT NULL,
    battle_time timestamp without time zone NOT NULL,
    event_id integer,
    event_mode character varying(40),
    event_map character varying(40),
    battle_type character varying(40),
    trophy_change integer,
    battle_mode character varying(40)
);


ALTER TABLE public.battle_det OWNER TO postgres;

--
-- TOC entry 207 (class 1259 OID 32802)
-- Name: battle_duo; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.battle_duo (
    hash_value character varying(20),
    battle_time timestamp without time zone NOT NULL,
    team_rank integer,
    player_team integer,
    player_tag character varying(20) NOT NULL,
    player_name character varying(20),
    brawler_id integer,
    brawler_name character varying(25),
    brawler_power integer,
    brawler_trophies integer
);


ALTER TABLE public.battle_duo OWNER TO postgres;

--
-- TOC entry 208 (class 1259 OID 32812)
-- Name: battle_solo; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.battle_solo (
    hash_value character varying(20),
    battle_time timestamp without time zone NOT NULL,
    battle_rank integer,
    player_tag character varying(20) NOT NULL,
    player_name character varying(20),
    brawler_id integer,
    brawler_name character varying(25),
    brawler_power integer,
    brawler_trophies integer
);


ALTER TABLE public.battle_solo OWNER TO postgres;

--
-- TOC entry 209 (class 1259 OID 32822)
-- Name: battle_team; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.battle_team (
    hash_value character varying(20),
    battle_time timestamp without time zone NOT NULL,
    battle_result character varying(20),
    battle_duration time without time zone,
    player_type character varying(20),
    player_team integer,
    player_tag character varying(20) NOT NULL,
    player_name character varying(20),
    brawler_id integer,
    brawler_name character varying(25),
    brawler_power integer,
    brawler_trophies integer
);


ALTER TABLE public.battle_team OWNER TO postgres;

--
-- TOC entry 206 (class 1259 OID 32794)
-- Name: brawlers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.brawlers (
    tag character varying(20),
    brawler_id integer,
    brawler_name character varying(30),
    brawler_power integer,
    brawler_rank integer,
    brawler_trophies integer,
    brawler_highest_trophies integer,
    brawler_star_power_1_id integer,
    brawler_star_power_1_name character varying(30),
    brawler_star_power_2_id integer,
    brawler_star_power_2_name character varying(30)
);


ALTER TABLE public.brawlers OWNER TO postgres;

--
-- TOC entry 204 (class 1259 OID 32781)
-- Name: club; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.club (
    club_tag character varying(20) NOT NULL,
    club_name character varying(30),
    club_trophies integer,
    club_required_t integer,
    club_type character varying(20),
    club_description character varying(200)
);


ALTER TABLE public.club OWNER TO postgres;

--
-- TOC entry 205 (class 1259 OID 32786)
-- Name: club_members; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.club_members (
    club_tag character varying(20),
    player_tag character varying(20),
    player_name character varying(20),
    player_nc character varying(20),
    player_role character varying(20),
    player_trophies integer
);


ALTER TABLE public.club_members OWNER TO postgres;

--
-- TOC entry 210 (class 1259 OID 32875)
-- Name: hash_values; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.hash_values (
    hash_value character varying(15)
);


ALTER TABLE public.hash_values OWNER TO postgres;

--
-- TOC entry 202 (class 1259 OID 24597)
-- Name: profile; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.profile (
    tag character varying(20) NOT NULL,
    name character varying(20),
    name_color character varying(20),
    trophies integer,
    highest_trophies integer,
    exp_level integer,
    exp_points integer,
    champ_q character varying(10),
    tvt_vict integer,
    solo_vict integer,
    duo_vict integer,
    rrt time without time zone,
    bbt time without time zone
);


ALTER TABLE public.profile OWNER TO postgres;

--
-- TOC entry 212 (class 1259 OID 32898)
-- Name: showdown_analysis; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.showdown_analysis (
    tag character varying(20) NOT NULL,
    event_mode character varying(40),
    event_map character varying(40) NOT NULL,
    battle_mode character varying(40),
    brawler_name character varying(25),
    showdown_type integer NOT NULL,
    rank_1 integer,
    rank_2 integer,
    games_played integer
);


ALTER TABLE public.showdown_analysis OWNER TO postgres;

--
-- TOC entry 211 (class 1259 OID 32878)
-- Name: team_analysis; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.team_analysis (
    tag character varying(20) NOT NULL,
    event_mode character varying(40),
    event_map character varying(40) NOT NULL,
    battle_mode character varying(40),
    brawler_name character varying(25),
    wins integer,
    games_played integer
);


ALTER TABLE public.team_analysis OWNER TO postgres;

--
-- TOC entry 2879 (class 0 OID 24618)
-- Dependencies: 203
-- Data for Name: battle_det; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.battle_det (tag, battle_time, event_id, event_mode, event_map, battle_type, trophy_change, battle_mode) FROM stdin;
\.


--
-- TOC entry 2883 (class 0 OID 32802)
-- Dependencies: 207
-- Data for Name: battle_duo; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.battle_duo (hash_value, battle_time, team_rank, player_team, player_tag, player_name, brawler_id, brawler_name, brawler_power, brawler_trophies) FROM stdin;
\.


--
-- TOC entry 2884 (class 0 OID 32812)
-- Dependencies: 208
-- Data for Name: battle_solo; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.battle_solo (hash_value, battle_time, battle_rank, player_tag, player_name, brawler_id, brawler_name, brawler_power, brawler_trophies) FROM stdin;
\.


--
-- TOC entry 2885 (class 0 OID 32822)
-- Dependencies: 209
-- Data for Name: battle_team; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.battle_team (hash_value, battle_time, battle_result, battle_duration, player_type, player_team, player_tag, player_name, brawler_id, brawler_name, brawler_power, brawler_trophies) FROM stdin;
\.


--
-- TOC entry 2882 (class 0 OID 32794)
-- Dependencies: 206
-- Data for Name: brawlers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.brawlers (tag, brawler_id, brawler_name, brawler_power, brawler_rank, brawler_trophies, brawler_highest_trophies, brawler_star_power_1_id, brawler_star_power_1_name, brawler_star_power_2_id, brawler_star_power_2_name) FROM stdin;
\.


--
-- TOC entry 2880 (class 0 OID 32781)
-- Dependencies: 204
-- Data for Name: club; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.club (club_tag, club_name, club_trophies, club_required_t, club_type, club_description) FROM stdin;
\.


--
-- TOC entry 2881 (class 0 OID 32786)
-- Dependencies: 205
-- Data for Name: club_members; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.club_members (club_tag, player_tag, player_name, player_nc, player_role, player_trophies) FROM stdin;
\.


--
-- TOC entry 2886 (class 0 OID 32875)
-- Dependencies: 210
-- Data for Name: hash_values; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.hash_values (hash_value) FROM stdin;
\.


--
-- TOC entry 2878 (class 0 OID 24597)
-- Dependencies: 202
-- Data for Name: profile; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.profile (tag, name, name_color, trophies, highest_trophies, exp_level, exp_points, champ_q, tvt_vict, solo_vict, duo_vict, rrt, bbt) FROM stdin;
\.


--
-- TOC entry 2888 (class 0 OID 32898)
-- Dependencies: 212
-- Data for Name: showdown_analysis; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.showdown_analysis (tag, event_mode, event_map, battle_mode, brawler_name, showdown_type, rank_1, rank_2, games_played) FROM stdin;
\.


--
-- TOC entry 2887 (class 0 OID 32878)
-- Dependencies: 211
-- Data for Name: team_analysis; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.team_analysis (tag, event_mode, event_map, battle_mode, brawler_name, wins, games_played) FROM stdin;
\.


--
-- TOC entry 2731 (class 2606 OID 24622)
-- Name: battle_det battle_det_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.battle_det
    ADD CONSTRAINT battle_det_pkey PRIMARY KEY (tag, battle_time);


--
-- TOC entry 2735 (class 2606 OID 32806)
-- Name: battle_duo battle_duo_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.battle_duo
    ADD CONSTRAINT battle_duo_pkey PRIMARY KEY (player_tag, battle_time);


--
-- TOC entry 2737 (class 2606 OID 32816)
-- Name: battle_solo battle_solo_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.battle_solo
    ADD CONSTRAINT battle_solo_pkey PRIMARY KEY (player_tag, battle_time);


--
-- TOC entry 2739 (class 2606 OID 32826)
-- Name: battle_team battle_team_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.battle_team
    ADD CONSTRAINT battle_team_pkey PRIMARY KEY (player_tag, battle_time);


--
-- TOC entry 2733 (class 2606 OID 32785)
-- Name: club club_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.club
    ADD CONSTRAINT club_pkey PRIMARY KEY (club_tag);


--
-- TOC entry 2729 (class 2606 OID 24601)
-- Name: profile profile_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.profile
    ADD CONSTRAINT profile_pkey PRIMARY KEY (tag);


--
-- TOC entry 2743 (class 2606 OID 32902)
-- Name: showdown_analysis showdown_analysis_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.showdown_analysis
    ADD CONSTRAINT showdown_analysis_pkey PRIMARY KEY (tag, event_map, showdown_type);


--
-- TOC entry 2741 (class 2606 OID 32882)
-- Name: team_analysis team_analysis_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.team_analysis
    ADD CONSTRAINT team_analysis_pkey PRIMARY KEY (tag, event_map);


--
-- TOC entry 2749 (class 2620 OID 40978)
-- Name: battle_duo duo_analysis_trig; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER duo_analysis_trig AFTER INSERT ON public.battle_duo FOR EACH ROW EXECUTE FUNCTION public.duo_analysis();


--
-- TOC entry 2750 (class 2620 OID 40976)
-- Name: battle_solo solo_analysis_trig; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER solo_analysis_trig AFTER INSERT ON public.battle_solo FOR EACH ROW EXECUTE FUNCTION public.solo_analysis();


--
-- TOC entry 2751 (class 2620 OID 40974)
-- Name: battle_team team_analysis_trig; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER team_analysis_trig AFTER INSERT ON public.battle_team FOR EACH ROW EXECUTE FUNCTION public.team_analysis();


--
-- TOC entry 2746 (class 2606 OID 32807)
-- Name: battle_duo battle_duo_player_tag_battle_time_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.battle_duo
    ADD CONSTRAINT battle_duo_player_tag_battle_time_fkey FOREIGN KEY (player_tag, battle_time) REFERENCES public.battle_det(tag, battle_time);


--
-- TOC entry 2747 (class 2606 OID 32817)
-- Name: battle_solo battle_solo_player_tag_battle_time_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.battle_solo
    ADD CONSTRAINT battle_solo_player_tag_battle_time_fkey FOREIGN KEY (player_tag, battle_time) REFERENCES public.battle_det(tag, battle_time);


--
-- TOC entry 2748 (class 2606 OID 32827)
-- Name: battle_team battle_team_player_tag_battle_time_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.battle_team
    ADD CONSTRAINT battle_team_player_tag_battle_time_fkey FOREIGN KEY (player_tag, battle_time) REFERENCES public.battle_det(tag, battle_time);


--
-- TOC entry 2745 (class 2606 OID 32797)
-- Name: brawlers brawlers_tag_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.brawlers
    ADD CONSTRAINT brawlers_tag_fkey FOREIGN KEY (tag) REFERENCES public.profile(tag);


--
-- TOC entry 2744 (class 2606 OID 32789)
-- Name: club_members club_members_club_tag_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.club_members
    ADD CONSTRAINT club_members_club_tag_fkey FOREIGN KEY (club_tag) REFERENCES public.club(club_tag);


-- Completed on 2020-04-06 17:57:50

--
-- PostgreSQL database dump complete
--

