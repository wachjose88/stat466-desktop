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


# gui/games.py 
"""
This module provides a possibilty to create games. Furthermore
it offers an analysis of games.
"""

import logging
import datetime
from dateutil import parser
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from database.models import Player, Game

        
class GameAnalysis(QWidget):
    """
    This class offers the possibilty to perform an analysis of games. 
    """
     
    def __init__(self, parent = None):
        """
        Constructor: inits all elements of the widget. Ít offers an 
        analysis of games by specifying the players.
        It creates the actions and connects them to their methods.
        
        Keyword arguments:
        parent -- parent widget
        """
        QWidget.__init__(self, parent)
        self.parent = parent
        self.game = None
        self.all_players = Player.get()
        if len(self.all_players) < 4:
            error = QLabel(self.tr('Error!\nThere are not enough Players.'), self)
            error.move(30, 30)
            return
            
        greet = QLabel(self.tr('Analysis'), self)
        ok = QPushButton(self.tr('Show Analysis'), self)
        self.connect(ok, SIGNAL('clicked()'), 
            self.__handle_ok)
         
        lbl_num = QLabel(self.tr('Games played:'), self)
        self.num = QLabel(' ', self)
        hbox_num = QHBoxLayout()
        hbox_num.addWidget(lbl_num)
        hbox_num.addWidget(self.num)
        
        vbox_game = QVBoxLayout()
        vbox_game.addWidget(greet)
        vbox_game.addStretch(2)
        vbox_game.addLayout(hbox_num)
        vbox_game.addStretch(2)
        
        lbl_t1 = QLabel(self.tr('Team 1:'), self)
        vbox_game.addWidget(lbl_t1)
        self.combo_t1_p1 = self.__fill_combo()
        vbox_game.addWidget(self.combo_t1_p1)
        self.combo_t1_p2 = self.__fill_combo(1)
        vbox_game.addWidget(self.combo_t1_p2)
        self.points_t1 = QLabel(' ', self)
        hbox_pt1 = QHBoxLayout()
        lbl_p1 = QLabel(self.tr('Points:'), self)
        hbox_pt1.addWidget(lbl_p1)
        hbox_pt1.addWidget(self.points_t1)
        vbox_game.addLayout(hbox_pt1)
        self.avg_t1 = QLabel(' ', self)
        lbl_a1 = QLabel(self.tr(' AVG Points per Game:'), self)
        hbox_avg1 = QHBoxLayout()
        hbox_avg1.addWidget(lbl_a1)
        hbox_avg1.addWidget(self.avg_t1)
        vbox_game.addLayout(hbox_avg1)
        vbox_game.addStretch(1)
        lbl_t2 = QLabel(self.tr('Team 2:'), self)
        vbox_game.addWidget(lbl_t2)
        self.combo_t2_p1 = self.__fill_combo(2)
        vbox_game.addWidget(self.combo_t2_p1)
        self.combo_t2_p2 = self.__fill_combo(3)
        vbox_game.addWidget(self.combo_t2_p2)
        self.points_t2 = QLabel(' ', self)
        lbl_p2 = QLabel(self.tr('Points:'), self)
        hbox_pt2 = QHBoxLayout()
        hbox_pt2.addWidget(lbl_p2)
        hbox_pt2.addWidget(self.points_t2)
        vbox_game.addLayout(hbox_pt2)
        self.avg_t2 = QLabel(' ', self)
        lbl_a2 = QLabel(self.tr(' AVG Points per Game:'), self)
        hbox_avg2 = QHBoxLayout()
        hbox_avg2.addWidget(lbl_a2)
        hbox_avg2.addWidget(self.avg_t2)
        vbox_game.addLayout(hbox_avg2)
        vbox_game.addStretch(2)
        
        vbox_game.addWidget(ok)
        
        self.setLayout(vbox_game)

    

    def __fill_combo(self, index = 0):
        """
        Returns a new QComboBox with all players.
        """
        combo = QComboBox()
        for p in self.all_players:
            combo.addItem(p.name + ' ' + p.fullname)
        combo.setCurrentIndex(index)
        return combo
        
    def __handle_ok(self):
        """
        Performs the analysis of all games of the specified players.
        """
        t1p1 = self.all_players[self.combo_t1_p1.currentIndex()] 
        t1p2 = self.all_players[self.combo_t1_p2.currentIndex()] 
        t2p1 = self.all_players[self.combo_t2_p1.currentIndex()] 
        t2p2 = self.all_players[self.combo_t2_p2.currentIndex()]
        params = {'t1p1' : t1p1.id, 't1p2' : t1p2.id, 
            't2p1' : t2p1.id, 't2p2' : t2p2.id }
        p = Game.getAnalysis(params)
        self.points_t1.setText(unicode(p['t1']))
        self.points_t2.setText(unicode(p['t2']))
        a1 = 0
        a2 = 0
        if p['num'] > 0:
            a1 = p['t1'] / p['num']
            a2 = p['t2'] / p['num']
        self.avg_t1.setText(unicode(a1))
        self.avg_t2.setText(unicode(a2))
        self.num.setText(unicode(p['num']))
        logging.info(u'analysis of ' + t1p1.info() + u' and ' + t1p2.info()
            + u' vs. ' + t2p1.info() + u' and ' + t2p2.info() + u'\n'
            + u'num games: ' + unicode(p['num']) + u', points: '
            + unicode(p['t1']) + u':' + unicode(p['t2']) )
        
    

class EditGame(QWidget):
    """
    This class offers the possibilty to create games. 
    """
     
    def __init__(self, parent = None):
        """
        Constructor: inits all elements of the widget. Ít offers a 
        calendar, combo- and input boxes to create a game.
        It creates the actions and connects them to their methods.
        
        Keyword arguments:
        parent -- parent widget
        """
        QWidget.__init__(self, parent)
        self.parent = parent
        self.game = None
        self.all_players = Player.get()
        if len(self.all_players) < 4:
            error = QLabel(self.tr('Error!\nThere are not enough Players.'), self)
            error.move(30, 30)
            return
        
        greet = QLabel(self.tr('Create a new Game'), self)
        at_lbl = QLabel(self.tr('Played at:'), self)
        
        self.calendar = QCalendarWidget()
        self.calendar.setMinimumDate(QDate(1900, 1, 1))
        self.calendar.setMaximumDate(QDate(3000, 1, 1))
        self.calendar.setGridVisible(True)
        self.calendar.setFirstDayOfWeek(Qt.Monday)
        
        save = QPushButton(self.tr('Save Game'), self)
        self.connect(save, SIGNAL('clicked()'), 
            self.__handle_save)
            
        chancel = QPushButton(self.tr('Chancel'), self)
        self.connect(chancel, SIGNAL('clicked()'), 
            self.__handle_chancel) 
         
        lbl_time = QLabel(self.tr('Time:'), self)
        self.time = QLineEdit('12:34')
        hbox_time = QHBoxLayout()
        hbox_time.addWidget(lbl_time)
        hbox_time.addWidget(self.time)
        
        lbl_game = QLabel(self.tr('Game:'), self)
        vbox_game = QVBoxLayout()
        vbox_game.addWidget(lbl_game)
        vbox_game.addStretch(1)
        
        
        lbl_t1 = QLabel(self.tr('Team 1:'), self)
        vbox_game.addWidget(lbl_t1)
        self.combo_t1_p1 = self.__fill_combo()
        vbox_game.addWidget(self.combo_t1_p1)
        self.combo_t1_p2 = self.__fill_combo(1)
        vbox_game.addWidget(self.combo_t1_p2)
        self.points_t1 = QLineEdit()
        hbox_pt1 = QHBoxLayout()
        lbl_p1 = QLabel(self.tr('Points:'), self)
        hbox_pt1.addWidget(lbl_p1)
        hbox_pt1.addWidget(self.points_t1)
        vbox_game.addLayout(hbox_pt1)
        vbox_game.addStretch(1)
        lbl_t2 = QLabel(self.tr('Team 2:'), self)
        vbox_game.addWidget(lbl_t2)
        self.combo_t2_p1 = self.__fill_combo(2)
        vbox_game.addWidget(self.combo_t2_p1)
        self.combo_t2_p2 = self.__fill_combo(3)
        vbox_game.addWidget(self.combo_t2_p2)
        self.points_t2 = QLineEdit()
        lbl_p2 = QLabel(self.tr('Points:'), self)
        hbox_pt2 = QHBoxLayout()
        hbox_pt2.addWidget(lbl_p2)
        hbox_pt2.addWidget(self.points_t2)
        vbox_game.addLayout(hbox_pt2)
        vbox_game.addStretch(2)
        
        hbox_btns = QHBoxLayout()
        hbox_btns.addStretch(2)
        hbox_btns.addWidget(save)
        hbox_btns.addWidget(chancel)
        vbox_at = QVBoxLayout()
        vbox_at.addWidget(at_lbl)
        vbox_at.addWidget(self.calendar)
        vbox_at.addLayout(hbox_time)
        hbox_all = QHBoxLayout()
        hbox_all.addLayout(vbox_at)
        hbox_all.addLayout(vbox_game)
        vbox = QVBoxLayout()
        vbox.addWidget(greet)
        vbox.addLayout(hbox_all)
        vbox.addLayout(hbox_btns)
        
        self.setLayout(vbox)
        
    


    def __fill_combo(self, index = 0):
        """
        Returns a new QComboBox with all players.
        """
        combo = QComboBox()
        for p in self.all_players:
            combo.addItem(p.name + ' ' + p.fullname)
        combo.setCurrentIndex(index)
        return combo
        
    def __handle_save(self):
        """
        Saves the new game to db.
        """
        try:
            date = self.calendar.selectedDate()
            ds = '%d-%d-%d ' % (date.year(), date.month(), date.day())
            played_at = parser.parse(unicode(ds + self.time.text()))
            pt1 = int(self.points_t1.text())
            pt2 = int(self.points_t2.text())
            t1p1 = self.all_players[self.combo_t1_p1.currentIndex()] 
            t1p2 = self.all_players[self.combo_t1_p2.currentIndex()] 
            t2p1 = self.all_players[self.combo_t2_p1.currentIndex()] 
            t2p2 = self.all_players[self.combo_t2_p2.currentIndex()] 
            g = Game(played_at, pt1, pt2, t1p1, t1p2, t2p1, t2p2)
            g.save()
            logging.info('game saved - ' + g.info())
            QMessageBox.information(self, self.tr('Game saved'),
                                  self.tr('The game was saved succesfully.'))
            self.parent.go_home()
        
        except ValueError as detail:
            QMessageBox.warning(self, self.tr('Game not saved'),
                                  self.tr('An error ocured while saving: ')+ detail.args[0] )
        
    

    def __handle_chancel(self):
        """
        Asks if the new game realy should not be saved and 
        leaves the EditGame dialog.
        """
        reply = QMessageBox.question(self, self.tr('Chancel?'),
            self.tr("Are you sure you want to chancel and do not save the game?"), 
            QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.parent.go_home() 
            
    

        
