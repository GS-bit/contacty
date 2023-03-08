from PyQt5.QtWidgets import (
    QDialog,
    QLabel,
    QDialogButtonBox,
    QCheckBox,
    QVBoxLayout,
    QMessageBox,
    QFrame
)

"""
FindDialog is a dialog thought to be used for setting how the searchings shall be done.
@param parent: parent widget
@param states: a tuple in the format (isNameChecked, isPhoneChecked, isEmailChecked, isWebsiteChecked, isAddressChecked, isCityChecked, isInfoChecked, isCaseChecked)
@param title: dialog's title
"""
class FindDialog(QDialog):
    def __init__(self, parent, states, title="Contacty"):
        super().__init__(parent)

        self.title = title

        self.setWindowTitle(self.title)

        self.vbox = QVBoxLayout(self)

        self.considerLabel = QLabel(_('Consider in the searches:'))

        self.nameCheckbox = QCheckBox(_('Name'))
        self.nameCheckbox.setCheckState(states[0])
        self.nameCheckbox.setTristate(False)

        self.phoneCheckbox = QCheckBox(_('Phone'))
        self.phoneCheckbox.setCheckState(states[1])
        self.phoneCheckbox.setTristate(False)

        self.emailCheckbox = QCheckBox(_('Email'))
        self.emailCheckbox.setCheckState(states[2])
        self.emailCheckbox.setTristate(False)

        self.websiteCheckbox = QCheckBox(_('Website'))
        self.websiteCheckbox.setCheckState(states[3])
        self.websiteCheckbox.setTristate(False)

        self.addressCheckbox = QCheckBox(_('Address'))
        self.addressCheckbox.setCheckState(states[4])
        self.addressCheckbox.setTristate(False)

        self.cityCheckbox = QCheckBox(_('City'))
        self.cityCheckbox.setCheckState(states[5])
        self.cityCheckbox.setTristate(False)

        self.infoCheckbox = QCheckBox(_('Additional information'))
        self.infoCheckbox.setCheckState(states[6])
        self.infoCheckbox.setTristate(False)

        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.HLine)
        self.frame.setFrameShadow(QFrame.Sunken)

        self.caseCheckbox = QCheckBox(_("Differentiate upper and lower cases"))
        self.caseCheckbox.setCheckState(states[7])
        self.caseCheckbox.setTristate(False)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttonBox.accepted.connect(self.process)
        buttonBox.rejected.connect(self.reject)

        self.vbox.addWidget(self.considerLabel)
        self.vbox.addWidget(self.nameCheckbox)
        self.vbox.addWidget(self.phoneCheckbox)
        self.vbox.addWidget(self.emailCheckbox)
        self.vbox.addWidget(self.websiteCheckbox)
        self.vbox.addWidget(self.addressCheckbox)
        self.vbox.addWidget(self.cityCheckbox)
        self.vbox.addWidget(self.infoCheckbox)
        self.vbox.addWidget(self.frame)
        self.vbox.addWidget(self.caseCheckbox)
        self.vbox.addWidget(buttonBox)
        
    """
    It hinders the user to uncheck all the checkboxes and press okay.
    """
    def process(self):
        if self.nameCheckbox.checkState() == False and self.phoneCheckbox.checkState() == False and self.emailCheckbox.checkState() == False and self.websiteCheckbox.checkState() == False and self.addressCheckbox.checkState() == False and self.cityCheckbox.checkState() == False and self.infoCheckbox.checkState() == False:
            error = QMessageBox.critical(None, self.title, _("Select at least one contact attribute."), QMessageBox.Ok)
        else:
            self.accept()

    """
    @return a tuple in the format (isNameChecked, isPhoneChecked, isEmailChecked, isWebsiteChecked, isAddressChecked, isCityChecked, isInfoChecked, isCaseChecked), where each element is a bool.
    """
    def getData(self):
        isNameChecked = True if self.nameCheckbox.checkState() > 0 else False
        isPhoneChecked = True if self.phoneCheckbox.checkState() > 0 else False
        isEmailChecked = True if self.emailCheckbox.checkState() > 0 else False
        isWebsiteChecked = True if self.websiteCheckbox.checkState() > 0 else False
        isAddressChecked = True if self.addressCheckbox.checkState() > 0 else False
        isCityChecked = True if self.cityCheckbox.checkState() > 0 else False
        isInfoChecked = True if self.infoCheckbox.checkState() > 0 else False
        isCaseChecked = True if self.caseCheckbox.checkState() > 0 else False

        return (isNameChecked, isPhoneChecked, isEmailChecked, isWebsiteChecked, isAddressChecked, isCityChecked, isInfoChecked, isCaseChecked)
