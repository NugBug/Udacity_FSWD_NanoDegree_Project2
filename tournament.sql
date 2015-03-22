-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE tournament (
   tournament_id serial  NOT NULL,
   tournament_name varchar(255) NOT NULL,
   CONSTRAINT tournament_pk PRIMARY KEY (tournament_id)
);

CREATE TABLE player (
   player_id serial  NOT NULL,
   full_name varchar(255)  NOT NULL,
   total_wins int DEFAULT 0,
   total_matches int DEFAULT 0,
   CONSTRAINT player_pk PRIMARY KEY (player_id)
);

CREATE TABLE player_tournament (
   player_tournament_id serial NOT NULL,
   player_id int REFERENCES player,
   tournament_id int REFERENCES tournament,
   wins int DEFAULT 0,
   matches int DEFAULT 0,
   CONSTRAINT player_tournament_pk PRIMARY KEY (player_tournament_id)
);

CREATE TABLE matches (
   match_id serial  NOT NULL,
   tournament_id int REFERENCES tournament,
   winner_id int REFERENCES player (player_id),
   loser_id int REFERENCES player (player_id),
   CONSTRAINT match_pk PRIMARY KEY (match_id)
);
