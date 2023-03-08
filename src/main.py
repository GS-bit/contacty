#!/usr/bin/env python3

"""
Contacty - Copyright © 2023 - Gabriel Soares

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

import sys
from mainwindow import *
from PyQt5.QtWidgets import QApplication
import locale, gettext
from os.path import join
from version import Version

"""
It shows the program help on the console.
"""
def help():
	print("./" + sys.argv[0] + _(" opens Contacty,"))
	print("./" + sys.argv[0] + _(" [filename] opens Contacty with a file,"))
	print("./" + sys.argv[0] + _(" --version shows Contacty version,"))
	print("./" + sys.argv[0] + _(" --help shows this message."))

"""
It starts the locale.
"""
def init_locale():
	locale.setlocale(locale.LC_ALL, )
	(loc, enc) = locale.getlocale()

	filename = join('lang', '{}.{}', 'LC_MESSAGES/messages.mo').format(loc, enc)

	try:
		t = gettext.GNUTranslations(open(filename, "rb"))
	except:
		t = gettext.NullTranslations()

	t.install()

if __name__ ==  '__main__':
	init_locale()

	app = QApplication(sys.argv)

	nOfArgs = len(sys.argv)
	if nOfArgs == 1:
		mainwindow = MainWindow()
	elif nOfArgs == 2:
		if sys.argv[1] == "--version":
			v = Version()
			print("Contacty v" + v.getVersion())
			sys.exit(0)
		elif sys.argv[1] == "--help":
			help()
			sys.exit(0)
		else:
			mainWindow = MainWindow(sys.argv[1])
	else:
		sys.stderr.write(_("Too many arguments. Run ./") + sys.argv[0] + _(" --help for help."))
		sys.exit(1)

	sys.exit(app.exec())
