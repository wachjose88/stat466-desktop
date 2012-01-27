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
"""
This is the main module of Stat466. It calls the main method to init
and to start Stat466.
"""

import logging
import datetime
import sys
import os
from PyQt4 import QtGui, QtCore
from gui.main import MainWindow
from database import db


def main(args): 
    """
    This is the main method of Stat466. It inits the logger and creates
    the QApplication. Furthermore it loads and installs translators for
    Qt and Stat466. Finally it shows the MainWindow and enters the main
    loop of the app.
    """
    if len(args) == 1 and args[0] == '-d':
        logging.basicConfig(
            format='%(asctime)s %(levelname)s: %(message)s',
            level=logging.DEBUG)
    else:
        dir = os.path.expanduser('~/.stat466')
        if not os.path.exists(dir):
            os.makedirs(dir)
        db.PATH = dir + '/'
        logging.basicConfig(
            format='%(asctime)s %(levelname)s: %(message)s',
            filename=(dir + '/main.log'), 
            level=logging.INFO)
        
    logging.info('Start of Stat466')
    app = QtGui.QApplication(sys.argv)
    
    locale = QtCore.QLocale.system().name()
    qt_translator = QtCore.QTranslator()
    if qt_translator.load("qt_" + locale, 
                          QtCore.QLibraryInfo.location(
                          QtCore.QLibraryInfo.TranslationsPath)):
        app.installTranslator(qt_translator)
        
    translator = QtCore.QTranslator()
    if translator.load("stat466_" + locale + ".qm", "./resources/lang/"):
        app.installTranslator(translator)
        
    main = MainWindow()
    main.show()
    exit_status = app.exec_()
    logging.info('Stop of Stat466')
    return exit_status


if __name__ == "__main__": 
    sys.exit(main(sys.argv[1:]))