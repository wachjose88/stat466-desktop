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


# database/db.py 
"""
This module provides some useful database related classes.
"""
import logging
import sqlite3

class Utils():
    """
    A helper class which provides some useful methods.
    """
    
    @staticmethod
    def info_box(name, values):
        """
        This static method returns a box list of debug values.
        
        Keyword arguments:
        name -- a headline for the box list
        values -- a dictionary of values to show in the box list
        """
        box = name + u': \n'
        temp = u''
        length = 0
        for key, value in values.items():
            t = key + ' '
            t += (18 - len(t)) * u' '
            t += u': ' + unicode(value)
            l = len(t)
            if l > length:
                length = l 
            temp += t + u'\n'
        if length > 60:
            length = 60
        box += length * u'-'
        box += u'\n' + temp
        box += length * u'-'
        return box
        

PATH = ''

class DBConnector():
    """
    A class which offers connection to the database in a simple form.
    This version works with sqlite3.
    So it acts as a database wrapper and could be replaced for other DBMS.
    """
    
    def __init__(self):
        """
        Constructor: inits connection wrapper for sqlite3 
        
        Members:
        db -- filename of sqlite3 db file 
        connection -- connection to db
        cursor -- cursor of db
        """
        self.db = unicode(PATH) +  u'main.db'
        self.connection = None
        self.cursor = None
        
    
    def connect(self):
        """
        This method connects to the given db file and enables an automatic
        detection of the data types between python and sqlite3. Furthermore
        it inits the cursor.
        """
        self.connection = sqlite3.connect(self.db, detect_types=sqlite3.PARSE_DECLTYPES)
        self.cursor = self.connection.cursor()
        logging.debug('connected to db: ' + self.db)
        
    
    def execute(self, query, params = None):
        """
        Executes the given query with the params on the current
        cursor. The result of the query is returned.
        
        Keyword arguments:
        query -- query to execute in sql 
        params -- parameters for the query 
        
        """
        logging.debug('execute query: ' + query)
        if params is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, params)
        self.connection.commit()
        return self.cursor.fetchall()
    
    
    def close(self):
        """
        Closes the cursor and the connection to db.
        """
        
        self.cursor.close()
        self.connection.close()
        logging.debug('connection to db closeed')
        
        