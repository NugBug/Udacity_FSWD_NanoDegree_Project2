#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import bleach
import psycopg2


def connect():
	"""Connect to the PostgreSQL database.  Returns a database connection."""
	return psycopg2.connect("dbname=tournament")

def registerTournament(name):
	"""Adds a tournament to the database.
	
	The database assigns a unique serial id number for the tournament.
	
	Args:
	  name: the name of the tournament
	"""
	db = connect()
	c = db.cursor()
	clean_content = bleach.clean(name)
	c.execute("INSERT INTO tournament (tournament_name) VALUES (%s)", (clean_content,))
	db.commit()
	db.close()

def deleteMatches():
	"""Remove all the match records from the database."""
	db = connect()
	c = db.cursor()
	c.execute("DELETE FROM matches")
	db.commit()
	db.close

def deletePlayers():
	"""Remove all the player records from the database."""
	db = connect()
	c = db.cursor()
	c.execute("DELETE FROM player_tournament")
	c.execute("DELETE FROM player")
	db.commit()
	db.close()
	
def deleteTournaments():
	"""Remove all the tournament records from the database."""
	db = connect()
	c = db.cursor()
	c.execute("DELETE FROM tournament")
	db.commit()
	db.close()

def countPlayers():
	"""Returns the number of players currently registered."""
	db = connect()
	c = db.cursor()
	c.execute("SELECT COUNT(*) FROM player")
	count = c.fetchone()
	db.commit()
	db.close()
	return count[0]

def registerPlayer(name):
	"""Adds a player to the tournament database.
  
	The database assigns a unique serial id number for the player.  (This
	should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
	db = connect()
	c = db.cursor()
	clean_content = bleach.clean(name)
	c.execute("INSERT INTO player (full_name) VALUES (%s)", (clean_content,))
	db.commit()
	db.close()
	
def enterPlayerTournament(tournament_id, player_id):
	"""Enters a player into a tournament.
	
	Args:
	  tournament_id: the tournament id to be entered in.
	  player_id: unique id for player being entered (found in the registration table).
    """
	db = connect()
	c = db.cursor()
	clean_tournament = bleach.clean(tournament_id)
	clean_player = bleach.clean(player_id)
	c.execute("INSERT INTO player_tournament (player_id, tournament_id) VALUES (%s, %s)", (clean_player, clean_tournament,))
	db.commit()
	db.close()

def playerStandings(tournament_id):
	"""Returns a list of the players and their win records, sorted by wins, for a specified tournament.

	The first entry in the list should be the player in first place, or a player
	tied for first place if there is currently a tie.

	Returns:
	  A list of tuples, each of which contains (id, name, wins, matches):
	    id: the player's unique id (assigned by the database)
	    name: the player's full name (as registered)
	    wins: the number of matches the player has won
	    matches: the number of matches the player has played
	"""
	db = connect()
	c = db.cursor()
	clean_id = bleach.clean(tournament_id)
	c.execute("SELECT player.player_id, player.full_name, player_tournament.wins, player_tournament.matches FROM player_tournament JOIN player ON player_tournament.player_id = player.player_id WHERE tournament_id = (%s) ORDER BY wins DESC", (clean_id,))
	playerStandings = []
	for row in c.fetchall():
		playerStandings.append((row[0], row[1], row[2], row[3]))
	db.commit()
	db.close()
	return playerStandings

def reportMatch(winner, loser, tournament_id):
	"""Records the outcome of a single match between two players.

	Args:
	  winner:  the id number of the player who won
	  loser:  the id number of the player who lost
	"""
 	db = connect()
	c = db.cursor()
	clean_id = bleach.clean(tournament_id)
	clean_winner = bleach.clean(winner)
	clean_loser = bleach.clean(loser)
	c.execute("UPDATE player_tournament SET wins = wins + 1, matches = matches + 1 WHERE player_id = (%s) AND tournament_id = (%s)", (clean_winner, clean_id,))
	c.execute("UPDATE player_tournament SET matches = matches + 1 WHERE player_id = (%s) AND tournament_id = (%s)", (clean_loser, clean_id,))
	c.execute("UPDATE player SET total_wins = total_wins + 1, total_matches = total_matches + 1 WHERE player_id = (%s)", (clean_winner,))
	c.execute("UPDATE player SET total_matches = total_matches + 1 WHERE player_id = (%s)", (clean_loser,))
	c.execute("INSERT INTO matches (tournament_id, winner_id, loser_id) VALUES (%s, %s, %s)", (clean_id, clean_winner, clean_loser,))
	db.commit()
	db.close()
 
def swissPairings(tournament_id):
	"""Returns a list of pairs of players for the next round of a match.
  
	Assuming that there are an even number of players registered, each player
	appears exactly once in the pairings.  Each player is paired with another
	player with an equal or nearly-equal win record, that is, a player adjacent
	to him or her in the standings.
  
	Returns:
	  A list of tuples, each of which contains (id1, name1, id2, name2)
	    id1: the first player's unique id
	    name1: the first player's name
	    id2: the second player's unique id
	    name2: the second player's name
	"""
	player_standings = playerStandings(tournament_id)
	swiss_pairings = []
	# For loop iterates through the player standings list and matches a player with the next opponent on the list assuming players are ordered by rank
	for i in range(len(player_standings)):
		if i%2 == 0:
			swiss_pairings.append((player_standings[i][0], player_standings[i][1], player_standings[i+1][0], player_standings[i+1][1]))
	return swiss_pairings

