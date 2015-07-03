-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TYPE state AS ENUM('WIN', 'LOSS', 'DRAW', 'NOT PLAYED');

CREATE TABLE players( id SERIAL,
                    name TEXT,
                    PRIMARY KEY (id) );

CREATE TABLE rounds ( id SERIAL,
                      PRIMARY KEY (id));

CREATE TABLE matches( round SERIAL REFERENCES rounds(id),
                      player1_id SERIAL REFERENCES players(id),
                      player2_id SERIAL REFERENCES players(id),
                      winner_id integer default NULL,
                      PRIMARY KEY (round, player1_id, player2_id) );


CREATE OR REPLACE FUNCTION numWins(integer) RETURNS bigint
    AS 'select count(*) from matches where winner_id=$1;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;

CREATE OR REPLACE FUNCTION numMatches(integer) RETURNS bigint
    AS 'select count(*) from matches where player1_id=$1 OR player2_id=$1;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;