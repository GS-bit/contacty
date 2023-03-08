from PyQt5.QtWidgets import (
    QDialog,
    QLabel,
    QVBoxLayout,
    QDialogButtonBox,
    QTextEdit
)

from PyQt5.QtCore import Qt

from PyQt5.QtGui import QPixmap

from version import Version

"""
AboutDialog is a dialog about the program, showing its logo, name, purpose, version, copyright and license.
"""
class AboutDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.setWindowTitle(_("About"))

        self.setFixedSize(460, 350)

        pixmap = QPixmap("/usr/share/contacty/res/logo.png")
        image = QLabel()
        image.setAlignment(Qt.AlignCenter)
        image.setPixmap(pixmap)

        v = Version()
        version = QLabel("Contacty v" + v.getVersion())
        version.setAlignment(Qt.AlignCenter)
        description = QLabel(_("Contacty is a contact book management system."))
        description.setAlignment(Qt.AlignCenter)
        license = QTextEdit()
        license.setAlignment(Qt.AlignCenter)
        license.insertPlainText("""This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.""")
        license.scrollToAnchor("T") # Scrolling to the beginning of the QTextEdit
        license.setFixedHeight(80)
        license.setReadOnly(True)
        license.setStyleSheet("text-align: center;")
        copyright = QLabel("Copyright © 2023 - Gabriel Soares")
        copyright.setAlignment(Qt.AlignCenter)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok, self)
        buttonBox.accepted.connect(self.accept)

        layout = QVBoxLayout(self)
        layout.addWidget(image)
        layout.addWidget(version)
        layout.addWidget(description)
        layout.addWidget(license)
        layout.addWidget(copyright)
        layout.addWidget(buttonBox)

        self.setLayout(layout)

        self.show()
