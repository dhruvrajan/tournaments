-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE players( id SERIAL,
                    name TEXT,
                    PRIMARY KEY (id) );

CREATE TABLE rounds ( id SERIAL,
                      PRIMARY KEY (id));

CREATE TABLE matches( round SERIAL REFERENCES rounds(id),
                      winner SERIAL REFERENCES players(id),
                      loser SERIAL REFERENCES players(id),
                      PRIMARY KEY (round, winner, loser) );


CREATE OR REPLACE FUNCTION numWins(integer) RETURNS bigint
    AS 'select count(*) from matches where winner=$1;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;

CREATE OR REPLACE FUNCTION numMatches(integer) RETURNS bigint
    AS 'select count(*) from matches where winner=$1 OR loser=$1;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;