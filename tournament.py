#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#


import psycopg2
import string


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def fix(name):
    """Fix names with apostrophes for SQL:
    O'Brien -> O''Brien"""
    return string.replace(name, "'", "''")


class Tournament:
    def __init__(self):
        self.current_round = 0
        self.new_round()

    def execute(self, sql_command):
        try:
            connection = connect()
            cursor = connection.cursor()
            cursor.execute(sql_command)
            try:
                result = cursor.fetchall()
            except:
                result = None
            connection.commit()
        finally:
            # Make sure to close connection even if exception is thrown
            connection.close()
        return result

    def deleteMatches(self):
        """Remove all the match records from the database."""
        self.execute("DELETE FROM matches")

    def deletePlayers(self):
        """Remove all the player records from the database."""
        self.execute("DELETE FROM players")

    def countPlayers(self):
        """Returns the number of players currently registered."""
        result = self.execute("SELECT count(*) FROM players")[0][0]
        return int(result)

    def registerPlayer(self, name):
        """Adds a player to the tournament database.

        The database assigns a unique serial id number for the player.  (This
        should be handled by your SQL database schema, not in your Python
        code.)

        Args:
          name: the player's full name (need not be unique).
        """
        self.execute("INSERT INTO players (name) VALUES ('%s')" % fix(name))

    def playerStandings(self):
        """Returns a list of the players and their win records, sorted by wins.

        The first entry in the list should be the player in first place, or a
        player
        tied for first place if there is currently a tie.

        Returns:
          A list of tuples, each of which contains (id, name, wins, matches):
            id: the player's unique id (assigned by the database)
            name: the player's full name (as registered)
            wins: the number of matches the player has won
            matches: the number of matches the player has played
        """
        connection = connect()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, name, numWins(id) as wins, numMatches(id) as matches \
            FROM players ORDER BY wins DESC, matches DESC, id DESC")
        results = cursor.fetchall()
        return results

    def reportMatch(self, winner, loser):
        """Records the outcome of a single match between two players.

        Args:
          winner:  the id number of the player who won
          loser:  the id number of the player who lost
        """
        # updates the winner/loser columns in matches; makes them accurate
        self.execute(
            """INSERT INTO matches (round, winner, loser)  \
            VALUES (%d, %d, %d)"""
            % (self.current_round, winner, loser))

    def swissPairings(self):
        """Returns a list of pairs of players for the next round of a match.

        Assuming that there are an even number of players registered, each
        player appears exactly once in the pairings. Each player is paired with
        another player with an equal or nearly-equal win record, that is, a
        player adjacent to him or her in the standings.

        Returns:
          A list of tuples, each of which contains (id1, name1, id2, name2)
            id1: the first player's unique id
            name1: the first player's name
            id2: the second player's unique id
            name2: the second player's name
        """
        self.new_round()
        return self.update_matches()

    def update_matches(self):
        """ Update the matches table with match - pairings. Returns a list of
        match-parings (tuples):

        (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
        """

        player_standings = self.playerStandings()
        assert len(player_standings) % 2 == 0

        #  Generate matchups from playerStandings
        #  player_standings is ordered, so consecutive players are paired up.
        matchups = [
            (player_standings[x][0], player_standings[x][1],
             player_standings[x + 1][0], player_standings[x + 1][1])
            for x in range(0, len(player_standings), 2)]
        for matchup in matchups:
            try:  # If Integrity error is thrown then the row already exists.
                #Insert matchups as rows in the matches table
                self.execute(
                    "INSERT INTO matches (round, winner, loser)  \
                    VALUES (%d, %d, %d)" % (
                        self.current_round, matchup[0], matchup[2]))
            except psycopg2.IntegrityError:
                print("INTEGRITY ERROR")

        return matchups

    def new_round(self):
        """Start a new round"""
        self.current_round += 1
        try:
            self.execute(
                "INSERT INTO rounds (id) VALUES (%d)" % self.current_round)
        except psycopg2.IntegrityError:
            pass


t = Tournament()


def deleteMatches():
    t.deleteMatches()


def deletePlayers():
    t.deletePlayers()


def countPlayers():
    return int(t.countPlayers())


def registerPlayer(name):
    t.registerPlayer(name)


def playerStandings():
    return t.playerStandings()


def reportMatch(winner, loser):
    t.reportMatch(winner, loser)


def swissPairings():
    return t.swissPairings()
