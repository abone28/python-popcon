--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: popcon_snap_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE popcon_snap_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: popcon_snap; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE popcon_snap (
    snap_id integer DEFAULT nextval('popcon_snap_seq'::regclass),
    snap_time timestamp with time zone NOT NULL,
    popcon_url text NOT NULL,
    submissions bigint,
    CONSTRAINT popcon_snap_id_c01 CHECK ((snap_id IS NOT NULL))
);


--
-- Name: popcon_stats; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE popcon_stats (
    snap_id integer,
    package text,
    vote integer,
    olde integer,
    recent integer,
    nofiles integer
);


--
-- Name: popcon_submission_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE popcon_submission_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: popcon_submission; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE popcon_submission (
    submission_id integer DEFAULT nextval('popcon_submission_seq'::regclass) NOT NULL,
    host_id uuid NOT NULL,
    submit_time timestamp with time zone NOT NULL
);


--
-- Name: popcon_submission_data; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE popcon_submission_data (
    submission_id integer NOT NULL,
    package text NOT NULL,
    path text,
    atime timestamp with time zone,
    ctime timestamp with time zone,
    tag text
);


--
-- Name: popcon_snap_id; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY popcon_snap
    ADD CONSTRAINT popcon_snap_id UNIQUE (snap_id);


--
-- Name: popcon_snap_pk; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY popcon_snap
    ADD CONSTRAINT popcon_snap_pk PRIMARY KEY (snap_time, popcon_url);


--
-- Name: popcon_submission_data_pk; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY popcon_submission_data
    ADD CONSTRAINT popcon_submission_data_pk PRIMARY KEY (submission_id, package);


--
-- Name: popcon_submission_id; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY popcon_submission
    ADD CONSTRAINT popcon_submission_id UNIQUE (submission_id);


--
-- Name: popcon_submission_pk; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY popcon_submission
    ADD CONSTRAINT popcon_submission_pk PRIMARY KEY (host_id, submit_time);


--
-- Name: popcon_stats_pk; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX popcon_stats_pk ON popcon_stats USING btree (snap_id, package);


--
-- Name: popcon_submission_data_submission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY popcon_submission_data
    ADD CONSTRAINT popcon_submission_data_submission_id_fkey FOREIGN KEY (submission_id) REFERENCES popcon_submission(submission_id);

