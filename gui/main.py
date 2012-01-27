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


# gui/main.py 
"""
This module provides the MainWindow and the Home/Start page of Stat466.
"""

import logging
from PyQt4 import QtGui, QtCore

from gui.players import EditPlayer, ListPlayers
from gui.games import EditGame, GameAnalysis

class MainWindow(QtGui.QMainWindow):
    """
    This class repressents the MainWindow of Stat466. It holds the menubar
    and the toolbar and their actions.
    """
    
    def __init__(self):
        """
        Constructor: inits all elements of the Window.
        It creates the actions and connects them to their methods.
        """
        
        QtGui.QMainWindow.__init__(self)

        self.resize(800, 600)
        self.setWindowTitle(self.tr('Stat466 - Statistics for Bauernschnapsen')
            + ' 0.2')
        self.center()
        
        self.statusBar().showMessage(self.tr('Welcome'))    
        self.go_home()

        exit = QtGui.QAction(QtGui.QIcon('resources/icons/exit.png'), self.tr('Exit'), self)
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip(self.tr('Exit Stat466'))
        self.connect(exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))


        about = QtGui.QAction(self.tr('About'), self)
        about.setStatusTip(self.tr('Infos about Stat466'))
        self.connect(about, QtCore.SIGNAL('triggered()'), self.__handle_about)


        new_player = QtGui.QAction(QtGui.QIcon('resources/icons/address-book-new-3.png'), 
                                   self.tr('Create Player'), self)
        new_player.setShortcut('Ctrl+P')
        new_player.setStatusTip(self.tr('Creates a new Player'))
        self.connect(new_player, QtCore.SIGNAL('triggered()'), self.__handle_new_player)

        list_players = QtGui.QAction(self.tr('Edit Players'), self)
        list_players.setStatusTip(self.tr('Lists all Players to edit them'))
        self.connect(list_players, QtCore.SIGNAL('triggered()'), self.__handle_list_player)


        new_game = QtGui.QAction(QtGui.QIcon('resources/icons/appointment-new-4.png'), 
                                   self.tr('Create Game'), self)
        new_game.setShortcut('Ctrl+G')
        new_game.setStatusTip(self.tr('Creates a new Game'))
        self.connect(new_game, QtCore.SIGNAL('triggered()'), self.__handle_new_game)

        game_analysis = QtGui.QAction(self.tr('Analysis'), self)
        game_analysis.setStatusTip(self.tr('Analysis of Games'))
        self.connect(game_analysis, QtCore.SIGNAL('triggered()'), self.__handle_game_analysis)


        self.toolbar = self.addToolBar(self.tr('Shortcuts'))
        self.toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon )
        self.toolbar.addAction(new_player)
        self.toolbar.addAction(new_game)
        self.toolbar.addAction(game_analysis)
        self.toolbar.addSeparator()
        self.toolbar.addAction(exit)
        
        self.menubar = self.menuBar()
        stat466 = self.menubar.addMenu(self.tr('&Stat466'))
        stat466.addAction(self.toolbar.toggleViewAction())   
        stat466.addAction(about)   
        stat466.addAction(exit)   
        
        player = self.menubar.addMenu(self.tr('&Player'))
        player.addAction(new_player)   
        player.addAction(list_players)   
        
        player = self.menubar.addMenu(self.tr('&Game'))
        player.addAction(new_game)   
        player.addAction(game_analysis)   
        
        
        
    def __handle_game_analysis(self):
        """
        Loads the GameAnalysis widget and sets it as the central widget
        of the MainWindow.
        """
        ga = GameAnalysis(parent = self)
        self.setCentralWidget(ga)
        
    def __handle_list_player(self):
        """
        Loads the ListPlayers widget and sets it as the central widget
        of the MainWindow.
        """
        listp = ListPlayers(parent = self)
        self.setCentralWidget(listp)
        
    def __handle_new_player(self):
        """
        Loads the EditPlayer widget and sets it as the central widget
        of the MainWindow.
        """
        edit = EditPlayer(parent = self)
        self.setCentralWidget(edit)
        
    def __handle_new_game(self):
        """
        Loads the EditGame widget and sets it as the central widget
        of the MainWindow.
        """
        edit = EditGame(parent = self)
        self.setCentralWidget(edit)
    
        
    def __handle_about(self):
        """
        Shows a QMessageBox with some Infos about Stat466.
        """
        QtGui.QMessageBox.about(self, self.tr('About Stat466'),
            self.tr(
        'Stat466 is a little application that provides '
        + 'the possibility to record game results of '
        + 'the famous card game Bauernschnapsen.') + '\n\n'
        + self.tr('Author:') + ' Josef Wachtler\n'
        + self.tr('e-mail:') + ' josef.wachtler@gmail.com\n'
        + self.tr('Web:') + ' sourceforge.net/projects/stat466/\n')
    
    
    def closeEvent(self, event):
        """
        Reimplements the closeEvent of the MainWindow and adds a question
        dialog.
        """
        reply = QtGui.QMessageBox.question(self, self.tr('Quit?'),
            self.tr("Are you sure to quit?"), QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


    def go_home(self):
        """
        Loads the Home widget and sets it as the central widget
        of the MainWindow.
        """
        home = Home() 
        self.setCentralWidget(home)

    def center(self):
        """
        Moves the MainWindow to the center of the screen.
        """
        screen = QtGui.QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
        
        
class Home(QtGui.QWidget):
    """
    This class repressents a Home/Start page.
    """
    
    def __init__(self):
        """
        Constructor: inits all elements of the widget.
        It shows a welcome message and an image with cards.
        """
        QtGui.QWidget.__init__(self)

        self.greet = QtGui.QLabel(self.tr('Welcome to'), self)
        self.greet.move(80, 30)
        self.name = QtGui.QLabel(self.tr('Stat466 - Statistics for Bauernschnapsen'), self)
        self.name.move(80, 60)
        self.cards = QtGui.QLabel(self)
        self.cards.setPixmap(QtGui.QPixmap('resources/icons/cards.jpg'))
        self.cards.setGeometry(80, 110, 280, 210)
