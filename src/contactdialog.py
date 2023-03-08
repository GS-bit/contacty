from PyQt5.QtWidgets import (
    QDialog,
    QLineEdit,
    QDialogButtonBox,
    QFormLayout,
    QTextEdit,
    QMessageBox
)

from re import fullmatch

"""
ContactDialog is a dialog thought to be used for adding/editing contacts.
"""
class ContactDialog(QDialog):
    def __init__(self, parent, title="Contacty", values={'name': "", 'phone': "", 'email': "", 'website': "", 'address': "", 'city': "", 'info': ""}):
        super().__init__(parent)

        self.title = title

        self.setWindowTitle(self.title)

        self.lineEdits = {'name': QLineEdit(self), 'phone': QLineEdit(self), 'email': QLineEdit(self), 'website': QLineEdit(self), 'address': QLineEdit(self), 'city': QLineEdit(self)}

        self.addInfo = QTextEdit(self)
        self.addInfo.setPlainText(values['info']) # Setting text of additional info text edit
        self.addInfo.setFixedHeight(80)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttonBox.accepted.connect(self.check)
        buttonBox.rejected.connect(self.reject)

        layout = QFormLayout(self)
        layout.addRow(_('Name(*)'), self.lineEdits['name'])
        layout.addRow(_('Phone'), self.lineEdits['phone'])
        layout.addRow(_('Email'), self.lineEdits['email'])
        layout.addRow(_('Website'), self.lineEdits['website'])
        layout.addRow(_('Address'), self.lineEdits['address'])
        layout.addRow(_('City'), self.lineEdits['city'])
        layout.addRow(_('Additional information'), self.addInfo)
        layout.addWidget(buttonBox)

        """
        Setting texts of line edits
        """
        for i in self.lineEdits:
            self.lineEdits[i].setText(values[i])

    """
    It checks if the contact's data are in apropriate format.
    """
    def check(self):
        invalidName = False
        invalidPhone = False
        invalidEmail = False
        invalidWebsite = False

        if self.lineEdits['name'].text() == "":
            invalidName = True

        if not fullmatch(r'[0-9\s()+\-]*', self.lineEdits['phone'].text()):
            invalidPhone = True

        if not fullmatch(r'[A-Za-z0-9._-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}', self.lineEdits['email'].text()) and self.lineEdits['email'].text() != '':
            invalidEmail = True

        if not fullmatch(r'[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}', self.lineEdits['website'].text()) and self.lineEdits['website'].text() != '':
            invalidWebsite= True

        if invalidName == True or invalidPhone == True or invalidEmail == True or invalidWebsite == True:
            errorMsg = _('The following errors were found:<ul>')

            if invalidName == True:
                errorMsg += _('<li>There is no contact name</li>')

            if invalidPhone == True:
                errorMsg += _('<li>Invalid phone format</li>')

            if invalidEmail == True:
                errorMsg += _('<li>Invalid email format</li>')

            if invalidWebsite == True:
                errorMsg += _('<li>Invalid website format</li>')

            error = QMessageBox.critical(None, self.title, errorMsg + '</ul>', QMessageBox.Ok)

        else:
            self.accept()

    """
    @return a tuple containg contact's attributes in this order: name, phone, email, website, address, city and info.
    """
    def getData(self):
        ret = []

        for i in self.lineEdits:
            ret.append(self.lineEdits[i].text())

        ret.append(self.addInfo.toPlainText())

        return tuple(ret)
