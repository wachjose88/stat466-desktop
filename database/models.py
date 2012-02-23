#!/ usr/bin/env python
# -*- coding : utf -8 -*-

# Stat466 - Statistics for Bauernschnapsen
#
# Copyright 2011 Josef Wachtler
#
# This file is part of Stat466.
#
# Stat466 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Stat466 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Stat466.  If not, see <http://www.gnu.org/licenses/>.


# database/models.py 
"""
This module provides model classes for the tables of the database.
It uses database.db.DBConnector to interact with the db.
"""

import logging
from database.db import DBConnector
from database.db import Utils


class Player():
    """
    This class represents an entry in tbl_players and offers some
    (static) methods to interact with the data from db.
    """
    
    def __init__(self, name, fullname, id = None):
        """
        Constructor: inits a player
        
        Keyword arguments:
        name -- name of a player
        fullname -- fullname of a player
        id -- id of a player, None if player is new
        """
        self.name = name
        self.fullname  = fullname
        self.id = id
    

    def info(self):
        """
        A string of the players name is returned.
        """
        return self.name + u' ' + self.fullname

    def dump(self):
        """
        A string with all params of the player  is  returned.
        """
        p = {u'ID' : self.id, u'Name' : self.name, u'Fullname' : self.fullname }
        return Utils.info_box(u'Player', p)
        
    def save(self):
        """
        Saves the player to the db. If no id is set a new player is inserted
        otherwise the player is updated.
        """
        Player.create()
        dbc = DBConnector()
        dbc.connect()
        
        if self.id is None:
            r = dbc.execute("""SELECT MAX(pid) FROM tbl_players""")
            next_id = 0
            if r[0][0] is not None:
                next_id = r[0][0] + 1
            params = {'pid' : next_id, 'name' : self.name, 'fullname' : self.fullname}
            dbc.execute("""INSERT INTO tbl_players VALUES (:pid, :name, :fullname)""", params)
            self.id = next_id
        else:
            params = {'pid' : self.id, 'name' : self.name, 'fullname' : self.fullname}
            dbc.execute("""UPDATE tbl_players SET name=:name, fullname=:fullname WHERE pid=:pid""", params)
        dbc.close()
        logging.debug(u'saved ' + self.dump())
            
 
    def delete(self):
        """
        Deletes the player from the db.
        """
        Player.create()
        Game.create()
        dbc = DBConnector()
        dbc.connect()
        params = {'pid' : self.id }
        dbc.execute("""DELETE FROM tbl_players WHERE pid=:pid""", params)
        dbc.execute("""DELETE FROM tbl_games 
                       WHERE pid_t1p1=:pid
                       OR pid_t1p2=:pid
                       OR pid_t2p1=:pid
                       OR pid_t2p2=:pid""", params)
        dbc.close()
        logging.debug(u'deleted ' + self.dump())
        
        
        
    @staticmethod
    def create():
        """
        Creates the table tbl_players in db. 
        """
        dbc = DBConnector()
        dbc.connect()
        dbc.execute("""CREATE TABLE IF NOT EXISTS tbl_players ( 
                    pid INTEGER, 
                    name TEXT,
                    fullname TEXT,
                    PRIMARY KEY(pid))""")
        dbc.close()
            

    def getStatistics(self):
        """
        Returns an analysis of the games of the player as a dictionary.
        It contains:
        won -- sum of won points 
        lost -- sum of lost points 
        num -- number of played games
        """
        Game.create()
        Player.create()
        dbc = DBConnector()
        dbc.connect()
        points = {'won' : 0, 'lost' : 0, 'num' : 0}
        players = {'pid' : self.id}
        sql = """SELECT SUM(points_t1) AS st1, SUM(points_t2) AS st2, 
            COUNT(gid) AS sall FROM tbl_games WHERE
            pid_t1p1=:pid OR pid_t1p2=:pid """
        sums = dbc.execute(sql, players)
        if sums[0][0] is not None:
            points['lost'] += sums[0][0]
        if sums[0][1] is not None:
            points['won'] += sums[0][1]
        if sums[0][2] is not None:
            points['num'] += sums[0][2]
        sql = """SELECT SUM(points_t1) AS st1, SUM(points_t2) AS st2, 
            COUNT(gid) AS sall FROM tbl_games WHERE
            pid_t2p1=:pid OR pid_t2p2=:pid """
        sums = dbc.execute(sql, players)
        if sums[0][1] is not None:
            points['lost'] += sums[0][1]
        if sums[0][0] is not None:
            points['won'] += sums[0][0]
        if sums[0][2] is not None:
            points['num'] += sums[0][2]
        dbc.close()
        return points
 
    @staticmethod
    def get(clause = None, params = None):
        """
        This method returns a list of players. With clause and params
        it is possible to modify the query.
        
        Keyword arguments:
        clause -- a string which is added to the query
        params -- a list or dictionary of parameters suitable for clause
        """
        Player.create()
        dbc = DBConnector()
        dbc.connect()
        players = []
        sql = """SELECT * FROM tbl_players"""
        if clause is not None and params is not None:
            sql += clause
            players = dbc.execute(sql, params)
        else:
            players = dbc.execute(sql)
        all_players = []
        for p in players:
            n = Player(name = p[1],
                       fullname = p[2], id = p[0])
            all_players.append(n)
        dbc.close()
        return all_players

class Game():
    """
    This class represents an entry in tbl_games and offers some
    (static) methods to interact with the data from db.
    """
    
    def __init__(self, played_at, points_t1, points_t2, pid_t1p1, pid_t1p2, 
                 pid_t2p1, pid_t2p2, id = None):
        """
        Constructor: inits a player
        
        Keyword arguments:
        played_at -- datetime of the game
        points_t1 -- points lost by team 1
        points_t2 -- points lost by team 2 
        pid_t1p1 -- database.models.Player number 1 of team 1
        pid_t1p2 -- database.models.Player number 2 of team 1
        pid_t2p1 -- database.models.Player number 1 of team 2
        pid_t2p2 -- database.models.Player number 2 of team 2
        id -- id of a game, None if game is new
        """
        self.played_at = played_at
        self.points_t1  = points_t1
        self.points_t2 = points_t2
        self.pid_t1p1 = pid_t1p1
        self.pid_t1p2 = pid_t1p2
        self.pid_t2p1 = pid_t2p1
        self.pid_t2p2 = pid_t2p2
        self.id = id
    

    def info(self): 
        """
        A string with a short info of the game is returned.
        """
        i = u'played at: ' + unicode(self.played_at) + u', points: '
        i += unicode(self.points_t1) + u':' + unicode(self.points_t2) + u'\n'
        i += self.pid_t1p1.info() + u' and ' + self.pid_t1p2.info() + u' vs '
        i += self.pid_t2p1.info() + u' and ' + self.pid_t2p2.info()
        return i 
    

    def dump(self):
        """
        A string with all params of the game  is  returned.
        """
        p = {u'ID' : self.id, 
             u'Played at' : self.played_at, 
             u'Points Team 1' : self.points_t1,
             u'Points Team 2' : self.points_t2,
             u'Team 1 Player 1' : self.pid_t1p1.info(), 
             u'Team 1 Player 2' : self.pid_t1p2.info(), 
             u'Team 2 Player 1' : self.pid_t2p1.info(), 
             u'Team 2 Player 2' : self.pid_t2p2.info() }
        return Utils.info_box(u'Game', p)
        

    def save(self):
        """
        Saves the game to the db. If no id is set a new game is inserted
        otherwise the game is updated.
        """
        Game.create()
        dbc = DBConnector()
        dbc.connect()
        
        if self.id is None:
            r = dbc.execute("""SELECT MAX(gid) FROM tbl_games""")
            next_id = 0
            if r[0][0] is not None:
                next_id = r[0][0] + 1
            params = {'gid' : next_id, 
                      'played_at' : self.played_at, 
                      'points_t1' : self.points_t1, 
                      'points_t2' : self.points_t2, 
                      'pid_t1p1' : self.pid_t1p1.id, 
                      'pid_t1p2' : self.pid_t1p2.id,
                      'pid_t2p1' : self.pid_t2p1.id,
                      'pid_t2p2' : self.pid_t2p2.id}
            dbc.execute("""INSERT INTO tbl_games VALUES (:gid, :played_at, :points_t1, 
                           :points_t2, :pid_t1p1, :pid_t1p2, :pid_t2p1, :pid_t2p2)""", params)
            self.id = next_id
        else:
            params = {'gid' : self.id, 
                      'played_at' : self.played_at, 
                      'points_t1' : self.points_t1, 
                      'points_t2' : self.points_t2, 
                      'pid_t1p1' : self.pid_t1p1.id, 
                      'pid_t1p2' : self.pid_t1p2.id,
                      'pid_t2p1' : self.pid_t2p1.id,
                      'pid_t2p2' : self.pid_t2p2.id}
            dbc.execute("""UPDATE tbl_players SET 
                           played_at=:played_at, 
                           points_t1=:points_t1,
                           points_t2=:points_t2,
                           pid_t1p1=:pid_t1p1,
                           pid_t1p2=:pid_t1p2,
                           pid_t2p1=:pid_t2p1,
                           pid_t2p2=:pid_t2p2
                           WHERE gid=:gid""", params)
        dbc.close()
        logging.debug(u'saved ' + self.dump())
 
    @staticmethod
    def create():
        """
        Creates the table tbl_games in db. 
        """
        dbc = DBConnector()
        dbc.connect()
        dbc.execute("""CREATE TABLE IF NOT EXISTS tbl_games ( 
                    gid INTEGER, 
                    played_at TIMESTAMP,
                    points_t1 INTEGER,
                    points_t2 INTEGER,
                    pid_t1p1 INTEGER,
                    pid_t1p2 INTEGER,
                    pid_t2p1 INTEGER,
                    pid_t2p2 INTEGER,
                    PRIMARY KEY(gid))""")
        dbc.close()
            
 
    @staticmethod
    def getAnalysis(players):
        """
        Returns an analysis of the games of the players as a dictionary.
        It contains:
        t1 -- sum of the points of team 1
        t2 -- sum of the points of team 2 
        num -- number of played games
        
        Keyword arguments:
        players -- a dictionary with the id's of the players.
                   Keys: t1p1, t1p2, t2p1, t2p2
        """
        Game.create()
        Player.create()
        dbc = DBConnector()
        dbc.connect()
        points = {'t1' : 0, 't2' : 0, 'num' : 0}
        sql = """SELECT SUM(points_t1) AS st1, SUM(points_t2) AS st2, 
            COUNT(gid) AS sall FROM tbl_games WHERE
            played_at <= :to AND played_at >= :from AND (
            ( pid_t1p1=:t1p1 AND pid_t1p2=:t1p2 AND pid_t2p1=:t2p1 AND pid_t2p2=:t2p2 ) OR
            ( pid_t1p1=:t1p1 AND pid_t1p2=:t1p2 AND pid_t2p1=:t2p2 AND pid_t2p2=:t2p1 ) OR
            ( pid_t1p1=:t1p2 AND pid_t1p2=:t1p1 AND pid_t2p1=:t2p1 AND pid_t2p2=:t2p2 ) OR
            ( pid_t1p1=:t1p2 AND pid_t1p2=:t1p1 AND pid_t2p1=:t2p2 AND pid_t2p2=:t2p1 ) ) """
        sums = dbc.execute(sql, players)
        if sums[0][0] is not None:
            points['t1'] += sums[0][0]
        if sums[0][1] is not None:
            points['t2'] += sums[0][1]
        if sums[0][2] is not None:
            points['num'] += sums[0][2]
        sql = """SELECT SUM(points_t1) AS st1, SUM(points_t2) AS st2, 
            COUNT(gid) AS sall  FROM tbl_games WHERE
            played_at <= :to AND played_at >= :from AND (
            ( pid_t2p1=:t1p1 AND pid_t2p2=:t1p2 AND pid_t1p1=:t2p1 AND pid_t1p2=:t2p2 ) OR
            ( pid_t2p1=:t1p1 AND pid_t2p2=:t1p2 AND pid_t1p1=:t2p2 AND pid_t1p2=:t2p1 ) OR
            ( pid_t2p1=:t1p2 AND pid_t2p2=:t1p1 AND pid_t1p1=:t2p1 AND pid_t1p2=:t2p2 ) OR
            ( pid_t2p1=:t1p2 AND pid_t2p2=:t1p1 AND pid_t1p1=:t2p2 AND pid_t1p2=:t2p1 ) ) """
        sums = dbc.execute(sql, players)
        if sums[0][1] is not None:
            points['t1'] += sums[0][1]
        if sums[0][0] is not None:
            points['t2'] += sums[0][0]
        if sums[0][2] is not None:
            points['num'] += sums[0][2]
        dbc.close()
        return points
 
    @staticmethod
    def get(clause = None, params = None):
        """
        This method returns a list of games. With clause and params
        it is possible to modify the query.
        
        Keyword arguments:
        clause -- a string which is added to the query
        params -- a list or dictionary of parameters suitable for clause
        """
        Game.create()
        Player.create()
        dbc = DBConnector()
        dbc.connect()
        games = []
        sql = """SELECT * FROM tbl_games"""
        if clause is not None and params is not None:
            sql += clause
            games = dbc.execute(sql, params)
        else:
            games = dbc.execute(sql)
        dbc.close()
        all_games = []
        for g in games:
            p = {'pid' : g[4]}
            t1p1 = Player.get(clause = ' WHERE pid=:pid', params=p)
            p['pid'] = g[5]
            t1p2 = Player.get(clause = ' WHERE pid=:pid', params=p)
            p['pid'] = g[6]
            t2p1 = Player.get(clause = ' WHERE pid=:pid', params=p)
            p['pid'] = g[7]
            t2p2 = Player.get(clause = ' WHERE pid=:pid', params=p)
            n = Game(played_at = g[1],
                       points_t1 = g[2],
                       points_t2 = g[3],
                       pid_t1p1 = t1p1[0],
                       pid_t1p2 = t1p2[0],
                       pid_t2p1 = t2p1[0],
                       pid_t2p2 = t2p2[0], 
                       id = g[0])
            all_games.append(n)
        return all_games
    
    
    @staticmethod
    def getMinDate():
        """
        This method returns the lowest date of the games in the 
        database.
        """
        Game.create()
        Player.create()
        dbc = DBConnector()
        dbc.connect()
        sql = """SELECT MIN(played_at) FROM tbl_games"""
        dates = dbc.execute(sql)
        dbc.close()
        if len(dates) > 0 and len(dates[0]):
            return dates[0][0]
        return None