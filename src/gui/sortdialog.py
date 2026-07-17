from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QComboBox,
    QVBoxLayout
)

from PyQt6.QtCore import Qt

class SortDialog(QDialog):
    """
    SortDialog is a dialog thought to be used for sorting the contacts.

    @param parent: parent widget
    @param title: dialog's title
    """

    def __init__(self, parent, title="Contacty"):
        super().__init__(parent)

        self.setWindowTitle(title)

        self.vbox = QVBoxLayout(self)

        self.sortTypeCmbBox = QComboBox(self)
        self.sortTypeCmbBox.addItem(_('Ascending'))
        self.sortTypeCmbBox.addItem(_('Descending'))
        self.attribCmbBox = QComboBox(self)
        self.attribCmbBox.addItem(_('Moment of creation'))
        self.attribCmbBox.addItem(_('Name'))
        self.attribCmbBox.addItem(_('Phone'))
        self.attribCmbBox.addItem(_('Email'))
        self.attribCmbBox.addItem(_('Website'))
        self.attribCmbBox.addItem(_('Address'))
        self.attribCmbBox.addItem(_('City'))
        self.attribCmbBox.addItem(_('Additional information'))

        buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, self)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        layout = QFormLayout()
        layout.addRow(_('Order'), self.sortTypeCmbBox)
        layout.addRow(_('Attribute to consider'), self.attribCmbBox)
        layout.setHorizontalSpacing(20)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.vbox.addLayout(layout)
        self.vbox.addWidget(buttonBox)

    def getData(self):
        """
        @return a tuple in the format (descending, attrib).
        """

        descending = ""
        if self.sortTypeCmbBox.currentText() == _('Ascending'):
            descending = False
        else:
            descending = True

        attrib = ""
        if self.attribCmbBox.currentText() == _('Moment of creation'):
            attrib = 'moment_of_creation'
        elif self.attribCmbBox.currentText() == _('Name'):
            attrib = 'name'
        elif self.attribCmbBox.currentText() == _('Phone'):
            attrib = 'phone'
        elif self.attribCmbBox.currentText() == _('Email'):
            attrib = 'email'
        elif self.attribCmbBox.currentText() == _('Website'):
            attrib = 'website'
        elif self.attribCmbBox.currentText() == _('Address'):
            attrib = 'address'
        elif self.attribCmbBox.currentText() == _('City'):
            attrib = 'city'
        elif self.attribCmbBox.currentText() == _('Additional information'):
            attrib = 'info'

        return (descending, attrib)
