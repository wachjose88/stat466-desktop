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


# gui/players.py 
"""
This module provides a possibilty to create and edit players. Furthermore
it offers a list of players.
"""

import logging
import datetime
from PyQt4 import QtCore
from PyQt4.QtGui import *
from database.models import Player

        
class EditPlayer(QWidget):
    """
    This class offers the possibilty to create and edit players. 
    """
    
    def __init__(self, player = None, parent = None):
        """
        Constructor: inits all elements of the widget. It offers input
        textboxes for the name and the fullname of a player.
        It creates the actions and connects them to their methods.
        
        Keyword arguments:
        player -- a database.models.Player to edit, if None a new one 
                  is created
        parent -- parent widget
        """
        
        QWidget.__init__(self, parent)
        self.parent = parent
        self.player_to = player
        
        gtext = self.tr('Create a new Player')
        if player is not None:
            gtext = self.tr('Edit a Player')
        greet = QLabel(gtext, self)
        greet.setStyleSheet("""
            QLabel { 
                font-size: 12pt;
            }""")
        
        save = QPushButton(self.tr('Save Player'), self)
        self.connect(save, QtCore.SIGNAL('clicked()'), 
            self.__handle_save)
            
        chancel = QPushButton(self.tr('Chancel'), self)
        self.connect(chancel, QtCore.SIGNAL('clicked()'), 
            self.__handle_chancel) 
        
        lbl_name = QLabel(self.tr('Name:'), self)
        self.name = QLineEdit()
        lbl_fullname = QLabel(self.tr('Fullame:'), self)
        self.fullname = QLineEdit()
        
        if player is not None:
            self.name.setText(player.name)
            self.fullname.setText(player.fullname)
        
        hbox_name = QHBoxLayout()
        hbox_name.addWidget(lbl_name)
        hbox_name.addWidget(self.name)
        
        hbox_fullname = QHBoxLayout()
        hbox_fullname.addWidget(lbl_fullname)
        hbox_fullname.addWidget(self.fullname)
        
        hbox_btns = QHBoxLayout()
        hbox_btns.addStretch(2)
        hbox_btns.addWidget(save)
        hbox_btns.addWidget(chancel)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(greet)
        vbox.addStretch(1)
        vbox.addLayout(hbox_name)
        vbox.addStretch(1)
        vbox.addLayout(hbox_fullname)
        vbox.addStretch(1)
        vbox.addLayout(hbox_btns)
        vbox.addStretch(3)
        
        self.setLayout(vbox)
        
        
        
        
    def __handle_save(self):
        """
        Saves the current Player. 
        """
        n = unicode(self.name.text())
        fn = unicode(self.fullname.text())
        if len(n) <= 0 or len(fn) <= 0:
            QMessageBox.warning(self, self.tr('Fill all'),
                              self.tr("Please fill in all fields."))
            return
        
        if self.player_to is None:
            self.player_to = Player(name = n, fullname = fn)
        else:
            self.player_to.name = n
            self.player_to.fullname = fn
        
        self.player_to.save()
        self.name.setText('')
        self.fullname.setText('')
        logging.info('player saved in db - ' + self.player_to.info())
        QMessageBox.information(self, self.tr('Player saved'),
                              self.tr("The player was saved successfully."))
        self.player_to = None
        self.parent.go_home()
    

    def __handle_chancel(self):
        """
        Asks if the current Player realy should not be saved and 
        leaves the EditPlayer dialog.
        """
        reply = QMessageBox.question(self, self.tr('Chancel?'),
            self.tr("Are you sure you want to chancel and do not save the player?"), 
            QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.name.setText('')
            self.fullname.setText('')
            self.player_to = None
            self.parent.go_home()
            
    

        
class ListPlayers(QWidget):
    """
    This class offers a list of all players and the possibilty to load
    EditPlayer to edit the selected player. Furthermore the selected
    player could be deleted. 
    """
  
    def __init__(self, parent = None):
        """
        Constructor: inits all elements of the widget. It offers a 
        list of all players.
        It creates the actions and connects them to their methods.
        
        Keyword arguments:
        parent -- parent widget
        """
        
        QWidget.__init__(self, parent)
        self.parent = parent
        
        greet = QLabel(self.tr('Edit Players'), self)
        greet.setStyleSheet("""
            QLabel { 
                font-size: 12pt;
            }""")
        
        self.list_of_players = QListWidget()
        
        self.all_players = []
        self.__fill_list()
        
        edit = QPushButton(self.tr('Edit Player'), self)
        self.connect(edit, QtCore.SIGNAL('clicked()'), 
            self.__handle_edit)
        statistics = QPushButton(self.tr('Statistics'), self)
        self.connect(statistics, QtCore.SIGNAL('clicked()'), 
            self.__handle_statistics) 
        delete = QPushButton(self.tr('Delete Player'), self)
        self.connect(delete, QtCore.SIGNAL('clicked()'), 
            self.__handle_delete) 
        
        hbox_btns = QHBoxLayout()
        hbox_btns.addWidget(edit)
        hbox_btns.addWidget(statistics)
        hbox_btns.addWidget(delete)
        
        vbox = QVBoxLayout()
        vbox.addWidget(greet)
        vbox.addWidget(self.list_of_players)
        vbox.addLayout(hbox_btns)
        
        self.setLayout(vbox)
    

    def __fill_list(self):
        """
        Fills the QListWidget of the players with all players from db.
        """
        self.list_of_players.clear()
        self.all_players = Player.get()
        for p in self.all_players:
            self.list_of_players.addItem(p.name + ' ' + p.fullname)
        

    def __handle_delete(self):
        """
        Asks if the selected Player realy should be deleted and if yes
        the player is deleted.
        """
        reply = QMessageBox.question(self, self.tr('Delete?'),
            self.tr("Are you sure you want to delete the player? This also deletes all games he played"), 
            QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            p = self.all_players[self.list_of_players.currentRow()]
            t = p.info()
            p.delete()
            self.__fill_list()
            logging.info('player deleted - ' + t )
            
    

    def __handle_edit(self):
        """
        Loads EditPlayer with the selected Player to edit him.
        """
        edit = EditPlayer(parent=self.parent, 
            player= self.all_players[self.list_of_players.currentRow()])
        self.parent.setCentralWidget(edit)
           

    def __handle_statistics(self):
        """
        Loads PlayerStatistics with the selected Player to perform statistic
        """
        stat = PlayerStatistics(parent=self.parent, 
            player= self.all_players[self.list_of_players.currentRow()])
        self.parent.setCentralWidget(stat)
            
            

        
class PlayerStatistics(QWidget):
    """
    This class offers a statistic of all games played by a player.. 
    """
  
    def __init__(self, player = None, parent = None):
        """
        Constructor: inits all elements of the widget. It offers a 
        game statistic of a player.
        It creates the actions and connects them to their methods.
        
        Keyword arguments:
        player -- a database.models.Player to perform the statistics.
        parent -- parent widget
        """
        
        QWidget.__init__(self, parent)
        self.parent = parent
        self.player_to = player
        stat = self.player_to.getStatistics()
        
        back = QPushButton(self.tr('Back'), self)
        self.connect(back, QtCore.SIGNAL('clicked()'), 
            self.__handle_back)
        
        greet = QLabel(self.tr('Statistics of all Games of:'), self)
        greet.setStyleSheet("""
            QLabel { 
                font-size: 12pt;
            }""")
        name = QLabel(self.player_to.name + ' ' + self.player_to.fullname, self)
        
        hbox_name = QHBoxLayout() 
        hbox_name.addWidget(greet)
        hbox_name.addWidget(name)
        
        lbl_num = QLabel(self.tr('Games played:'), self)
        num = QLabel(unicode(stat['num']), self)
        hbox_num = QHBoxLayout()
        hbox_num.addWidget(lbl_num)
        hbox_num.addWidget(num)
        
        lbl_lost = QLabel(self.tr('Points lost:'), self)
        lost = QLabel(unicode(stat['lost']), self)
        hbox_lost = QHBoxLayout()
        hbox_lost.addWidget(lbl_lost)
        hbox_lost.addWidget(lost)
        
        lbl_won = QLabel(self.tr('Points won:'), self)
        won = QLabel(unicode(stat['won']), self)
        hbox_won = QHBoxLayout()
        hbox_won.addWidget(lbl_won)
        hbox_won.addWidget(won)

        hbox_btns = QHBoxLayout()
        hbox_btns.addWidget(back)
        
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox_name)
        vbox.addStretch(1)
        vbox.addLayout(hbox_num)
        vbox.addStretch(1)
        vbox.addLayout(hbox_won)
        vbox.addStretch(1)
        vbox.addLayout(hbox_lost)
        vbox.addStretch(1)
        vbox.addLayout(hbox_btns)
        vbox.addStretch(3)
        
        self.setLayout(vbox)
        
        logging.info('statistics of ' + self.player_to.name + ' ' 
		        + self.player_to.fullname + '\n' + unicode(stat))
        
        
        
    def __handle_back(self):
        """
        Loads ListPlayers.
        """
        listp = ListPlayers(parent=self.parent)
        self.parent.setCentralWidget(listp)
           