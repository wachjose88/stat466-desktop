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
        Constructor: inits all elements of the widget. It offers an 
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
        greet.setStyleSheet("""
            QLabel { 
                font-size: 12pt;
            }""")
         
        ok = QPushButton(self.tr('Print Analysis'), self)
        self.connect(ok, SIGNAL('clicked()'), 
            self.__handle_print)
         
        lbl_num = QLabel(self.tr('Games played:'), self)
        self.num = QLabel(' ', self)
        hbox_num = QHBoxLayout()
        hbox_num.addWidget(lbl_num)
        hbox_num.addWidget(self.num)
        
        lbl_start_date = QLabel(self.tr('From:'), self)
        self.start_date = QDateEdit(QDate(1900, 1, 1), self)
        self.start_date.setDisplayFormat('dd.MM.yyyy')
        self.start_date.setMinimumDate(QDate(1900, 1, 1))
        self.start_date.setMaximumDate(QDate(3000, 1, 1))
        lbl_end_date = QLabel(self.tr('To:'), self)
        self.end_date = QDateEdit(QDate.currentDate (), self)
        self.end_date.setDisplayFormat('dd.MM.yyyy')
        self.end_date.setMinimumDate(QDate(1900, 1, 1))
        self.end_date.setMaximumDate(QDate(3000, 1, 1))
        hbox_start_date = QHBoxLayout()
        hbox_start_date.addStretch(1)
        hbox_start_date.addWidget(lbl_start_date)
        hbox_start_date.addWidget(self.start_date)
        hbox_start_date.addSpacing(11)
        hbox_start_date.addWidget(lbl_end_date)
        hbox_start_date.addWidget(self.end_date)
        hbox_start_date.addStretch(1)
        
        vbox_game = QVBoxLayout()
        vbox_game.addWidget(greet)
        vbox_game.addStretch(2)
        vbox_game.addLayout(hbox_start_date)
        vbox_game.addStretch(2)
        vbox_game.addLayout(hbox_num)
        vbox_game.addStretch(1)
        
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
        self.diff_t1 = QLabel(' ', self)
        hbox_diff_t1 = QHBoxLayout()
        lbl_diff_t1 = QLabel(self.tr('Difference:'), self)
        hbox_diff_t1.addWidget(lbl_diff_t1)
        hbox_diff_t1.addWidget(self.diff_t1)
        vbox_game.addLayout(hbox_diff_t1)
        self.avg_t1 = QLabel(' ', self)
        lbl_a1 = QLabel(self.tr('AVG Points per Game:'), self)
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
        self.diff_t2 = QLabel(' ', self)
        hbox_diff_t2 = QHBoxLayout()
        lbl_diff_t2 = QLabel(self.tr('Difference:'), self)
        hbox_diff_t2.addWidget(lbl_diff_t2)
        hbox_diff_t2.addWidget(self.diff_t2)
        vbox_game.addLayout(hbox_diff_t2)
        self.avg_t2 = QLabel(' ', self)
        lbl_a2 = QLabel(self.tr('AVG Points per Game:'), self)
        hbox_avg2 = QHBoxLayout()
        hbox_avg2.addWidget(lbl_a2)
        hbox_avg2.addWidget(self.avg_t2)
        vbox_game.addLayout(hbox_avg2)
        vbox_game.addStretch(2)
        
        vbox_game.addWidget(ok)
        
        self.setLayout(vbox_game)
        
        self.preview = QPrintPreviewDialog()
        self.connect(self.preview,
            SIGNAL("paintRequested (QPrinter *)"),self.__print)
        self.connect(self.combo_t1_p1,
            SIGNAL("currentIndexChanged (int)"),self.__handle_ok)
        self.connect(self.combo_t1_p2,
            SIGNAL("currentIndexChanged (int)"),self.__handle_ok)
        self.connect(self.combo_t2_p1,
            SIGNAL("currentIndexChanged (int)"),self.__handle_ok)
        self.connect(self.combo_t2_p2,
            SIGNAL("currentIndexChanged (int)"),self.__handle_ok)
        self.connect(self.start_date,
            SIGNAL("dateChanged (const QDate&)"),self.__handle_ok)
        self.connect(self.end_date,
            SIGNAL("dateChanged (const QDate&)"),self.__handle_ok)
        self.__handle_ok()
    

    def __fill_combo(self, index = 0):
        """
        Returns a new QComboBox with all players.
        """
        combo = QComboBox()
        for p in self.all_players:
            combo.addItem(p.name + ' ' + p.fullname)
        combo.setCurrentIndex(index)
        return combo
    
    def __perform_analysis(self):
        """
        Performs the analysis of all games of the specified players.
        """
        t1p1 = self.all_players[self.combo_t1_p1.currentIndex()] 
        t1p2 = self.all_players[self.combo_t1_p2.currentIndex()] 
        t2p1 = self.all_players[self.combo_t2_p1.currentIndex()] 
        t2p2 = self.all_players[self.combo_t2_p2.currentIndex()]
        date_from = self.start_date.date().toPyDate()
        date_to = self.end_date.date().toPyDate()
        date_to1 = datetime.datetime.combine(date_to, datetime.time(23,59,59))
        params = {'t1p1' : t1p1.id, 't1p2' : t1p2.id, 
            't2p1' : t2p1.id, 't2p2' : t2p2.id,
            'from' : date_from, 'to' : date_to1 }
        p = Game.getAnalysis(params)
        a1 = 0
        a2 = 0
        if p['num'] > 0:
            a1 = p['t1'] / p['num']
            a2 = p['t2'] / p['num']
        p['a1'] = a1
        p['a2'] = a2
        p['d1'] = p['t2'] - p['t1']
        p['d2'] = p['t1'] - p['t2']
        logging.info(u'analysis of ' + t1p1.info() + u' and ' + t1p2.info()
            + u' vs. ' + t2p1.info() + u' and ' + t2p2.info() + u'\n'
            + u'num games: ' + unicode(p['num']) + u', points: '
            + unicode(p['t1']) + u':' + unicode(p['t2']) )
        return p
    
    def __handle_ok(self):
        """
        Performs the analysis of all games of the specified players
        and shows them.
        """
        p = self.__perform_analysis()
        self.points_t1.setText(unicode(p['t1']))
        self.points_t2.setText(unicode(p['t2']))
        self.diff_t1.setText(unicode(p['d1']))
        self.diff_t2.setText(unicode(p['d2']))
        self.avg_t1.setText(unicode(p['a1']))
        self.avg_t2.setText(unicode(p['a2']))
        self.num.setText(unicode(p['num']))
        
    
    def __handle_print(self):
        """
        Prints the analysis of all games of the specified players.
        """
        self.preview.exec_()
        
    def __print(self, printer):
        """
        Formats the analysis of all games of the specified players 
        for printing.
        """
        p = self.__perform_analysis()
        t1p1 = self.all_players[self.combo_t1_p1.currentIndex()] 
        t1p2 = self.all_players[self.combo_t1_p2.currentIndex()] 
        t2p1 = self.all_players[self.combo_t2_p1.currentIndex()] 
        t2p2 = self.all_players[self.combo_t2_p2.currentIndex()]
        date_from = self.start_date.date().toPyDate()
        date_to = self.end_date.date().toPyDate()
        
        fs_main = '-----------------------------------------------------------------\n'
        fs_main += ' {:s}\n'
        fs_main += '-----------------------------------------------------------------\n'
        
        fs_main += '\n {:<21s} {:s}\n {:<21s} {:s}\n\n {:<21s} {:d}'
        s_main = fs_main.format(self.tr('Stat466 - Analysis'),
            self.tr('From:'), unicode(date_from),
            self.tr('To:'), unicode(date_to),
            self.tr('Games played:'), p['num']
        )
        
        fs_stat = '\n\n-----------------------------------------------------------------\n' 
        fs_stat += ' {:<10s} {:>52s}\n'
        fs_stat += ' {:<38s} {:>24d}\n'
        fs_stat += ' {:<38s} {:>24d}\n'
        fs_stat += ' {:<38s} {:>24d}'
        fs_stat += '\n-----------------------------------------------------------------' 
        
        n_team1 = t1p1.name + ' ' + t1p1.fullname + ' ' + self.tr('and') 
        n_team1 += ' ' + t1p2.name + ' ' + t1p2.fullname
        s_team1 = unicode( fs_stat).format(
            self.tr('Team 1:'), n_team1,
            self.tr('Points:'), p['t1'],
            self.tr('Difference:'), p['d1'],
            self.tr('AVG Points per Game:'), p['a1']
        )
        n_team2 = t2p1.name + ' ' + t2p1.fullname + ' ' + self.tr('and') 
        n_team2 += ' ' + t2p2.name + ' ' + t2p2.fullname
        s_team2 = unicode( fs_stat).format(
            self.tr('Team 2:'), n_team2,
            self.tr('Points:'), p['t2'],
            self.tr('Difference:'), p['d2'],
            self.tr('AVG Points per Game:'), p['a2']
        )
        
        printLabel = QLabel(s_main + s_team1 + s_team2 )
         
        printLabel.setStyleSheet("""
            QLabel { 
                background-color : white; 
                color : black; 
                font-family: monospace;
                font-size: 12pt;
            }""")
        painter = QPainter(printer)
        printLabel.render(painter)
        painter.end() 
    

class EditGame(QWidget):
    """
    This class offers the possibilty to create games. 
    """
     
    def __init__(self, parent = None):
        """
        Constructor: inits all elements of the widget. It offers a 
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
        greet.setStyleSheet("""
            QLabel { 
                font-size: 12pt;
            }""")
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
        self.time = QTimeEdit(QTime.currentTime (), self)
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
            time = self.time.time()
            ds = '%d-%d-%d %d:%d' % (date.year(), date.month(), date.day(),
                time.hour(), time.minute())
            played_at = parser.parse(unicode(ds))
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
            
    

        
