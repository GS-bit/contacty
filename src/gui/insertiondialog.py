from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QComboBox,
    QLabel,
    QVBoxLayout
)

from PyQt6.QtCore import Qt

class InsertionDialog(QDialog):
    """
    InsertionDialog is a dialog thought to be used for setting how contacts shall be inserted.

    @param parent: parent widget
    @param states: a tuple in the format (descending, attrib)
    @param title: dialog's title
    """

    def __init__(self, parent, states=(False, "moment_of_creation"), title="Contacty"):
        super().__init__(parent)

        self.setWindowTitle(title)

        self.vbox = QVBoxLayout(self)

        self.label = QLabel(_("Future contacts shall be inserted following these criteria:"))

        self.sortTypeCmbBox = QComboBox(self)
        self.sortTypeCmbBox.addItem(_('Ascending'))
        self.sortTypeCmbBox.addItem(_('Descending'))
        self.sortTypeCmbBox.setCurrentIndex(self.orderToIndex(states[0]))
        self.attribCmbBox = QComboBox(self)
        self.attribCmbBox.addItem(_('Moment of creation'))
        self.attribCmbBox.addItem(_('Name'))
        self.attribCmbBox.addItem(_('Phone'))
        self.attribCmbBox.addItem(_('Email'))
        self.attribCmbBox.addItem(_('Website'))
        self.attribCmbBox.addItem(_('Address'))
        self.attribCmbBox.addItem(_('City'))
        self.attribCmbBox.addItem(_('Additional information'))

        self.attribCmbBox.setCurrentIndex(self.attribToIndex(states[1]))

        buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, self)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        layout = QFormLayout()
        layout.addRow(_("Order"), self.sortTypeCmbBox)
        layout.addRow(_("Attribute to consider"), self.attribCmbBox)
        layout.setHorizontalSpacing(20)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.vbox.addWidget(self.label)
        self.vbox.addSpacing(20)
        self.vbox.addLayout(layout)
        self.vbox.addWidget(buttonBox)

    def attribToIndex(self, attrib):
        """
        @param attrib: the attribute

        @return the corresponding item index in self.attribCmbBox
        """

        if attrib == 'moment_of_creation':
            return 0
        elif attrib == 'name':
            return 1
        elif attrib == 'phone':
            return 2
        elif attrib == 'email':
            return 3
        elif attrib == 'website':
            return 4
        elif attrib == 'address':
            return 5
        elif attrib == 'city':
            return 6
        elif attrib == 'info':
            return 7

    def orderToIndex(self, order):
        """
        @param order: the order

        @return the corresponding item index in self.sortTypeCmbBox
        """

        if order == False:
            return 0
        elif order == True:
            return 1

    def getData(self):
        """
        @return a tuple in the format (descending, attrib). Descending is a bool telling us if the order is descending or not and the attribute is a string telling us which attribute to consider for sorts.
        """

        descending = self.sortTypeCmbBox.currentText()
        attrib = self.attribCmbBox.currentText()

        if descending == _("Ascending"):
            descending = False
        elif descending == _("Descending"):
            descending = True

        if attrib == _('Moment of creation'):
            attrib = 'moment_of_creation'
        elif attrib == _('Name'):
            attrib = 'name'
        elif attrib == _('Phone'):
            attrib = 'phone'
        elif attrib == _('Email'):
            attrib = 'email'
        elif attrib == _('Website'):
            attrib = 'website'
        elif attrib == _('Address'):
            attrib = 'address'
        elif attrib == _('City'):
            attrib = 'city'
        elif attrib == _('Additional information'):
            attrib = 'info'

        return (descending, attrib)
