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

# stat466.py 

import logging
import datetime
import sys
from PyQt4 import QtGui, QtCore
from gui.main import MainWindow
from database.db import DBConnector
from database.models import Player
from database.models import Game


def main(): 
    
    logging.basicConfig(
        format='%(asctime)s %(levelname)s: %(message)s',
        filename='logs/main.log', 
        level=logging.INFO)
    
    logging.info('Start of Stat466')
    app = QtGui.QApplication(sys.argv)
    locale = QtCore.QLocale.system().name()
    qt_translator = QtCore.QTranslator()
    if qt_translator.load("qt_" + locale, QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath)):
        app.installTranslator(qt_translator)
    translator = QtCore.QTranslator()
    if translator.load("stat466_" + locale + ".qm", "./resources/lang/"):
        app.installTranslator(translator)
    main = MainWindow()
    main.show()
    exit_status = app.exec_()
    logging.info('Stop of Stat466')
    sys.exit(exit_status)


if __name__ == "__main__": 
    main()