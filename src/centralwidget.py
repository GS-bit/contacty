from contactbook import Contactbook
from contactdialog import ContactDialog
from contactlistwidget import ContactListWidget
from history import *


from PyQt5.QtWidgets import (
    QWidget,
	QPushButton,
	QHBoxLayout,
	QVBoxLayout,
	QStyle,
	QLineEdit,
	QMessageBox
)

"""
CentralWidget is the central widget designed for the main window. It contains a ContactListWidget, which is derivated from a QListWidget, a History object, a QLineEdit for searches and some buttons for rapid access (New contact, edit contact, delete contact).
"""
class CentralWidget(QWidget): # TODO: seria bom adicionar os shortcuts do mainwindow na busca
    def __init__(self, filename):
        super().__init__(None)

        self._contactbook = Contactbook(filename)

        self.contactListWidget = ContactListWidget()
        self.contactListWidget.itemDoubleClicked.connect(self.editContactEvent)
        self.contactListWidget.currentItemChanged.connect(self.handleButtonsEvent)

        self.setWindowTitle("1") # We will often alternate window title to "0" and "1" using self.notify().

        self.contactListWidget.isSelected()

        self.searchLineEdit = QLineEdit()
        self.searchLineEdit.setPlaceholderText(_('Search contact'))
        self.searchLineEdit.textChanged.connect(self.searchEvent)

        self.history = History(self._contactbook)

        self.modified = False # This variable tells us if the contact book was modified or not

        self._createButtons()

        vbox = QVBoxLayout()
        vbox.addWidget(self.searchLineEdit)
        vbox.addWidget(self.contactListWidget)

        toolbar = QHBoxLayout()
        toolbar.addLayout(vbox)
        toolbar.addLayout(self._buttons)

        self.setLayout(toolbar)

        self.show()

    """
    It creates the rapid access buttons new, edit and delete contact.
    """
    def _createButtons(self):
        self.upwardBtn = QPushButton()
        self.upwardBtn.setIcon(self.style().standardIcon(getattr(QStyle, "SP_ArrowUp")))
        self.upwardBtn.clicked.connect(self.moveUpwardEvent)
        self.upwardBtn.setEnabled(False)

        self.downwardBtn = QPushButton()
        self.downwardBtn.setIcon(self.style().standardIcon(getattr(QStyle, "SP_ArrowDown")))
        self.downwardBtn.clicked.connect(self.moveDownwardEvent)
        self.downwardBtn.setEnabled(False)

        self.newContactBtn = QPushButton(_("New contact"))
        self.newContactBtn.setIcon(self.style().standardIcon(getattr(QStyle, "SP_FileDialogNewFolder")))
        self.newContactBtn.clicked.connect(self.newContactEvent)

        self.updateContactBtn = QPushButton(_("Edit contact"))
        self.updateContactBtn.setIcon(self.style().standardIcon(getattr(QStyle, "SP_FileLinkIcon")))
        self.updateContactBtn.clicked.connect(self.editContactEvent)
        self.updateContactBtn.setEnabled(False)

        self.deleteContactBtn = QPushButton(_("Delete contact"))
        self.deleteContactBtn.setIcon(self.style().standardIcon(getattr(QStyle, "SP_DialogDiscardButton")))
        self.deleteContactBtn.clicked.connect(self.deleteContactEvent)
        self.deleteContactBtn.setEnabled(False)

        self._buttons = QVBoxLayout()
        self._buttons.addWidget(self.upwardBtn)
        self._buttons.addWidget(self.downwardBtn)
        self._buttons.addWidget(self.newContactBtn)
        self._buttons.addWidget(self.updateContactBtn)
        self._buttons.addWidget(self.deleteContactBtn)

    """
    It is used to notify the main window about changes on the central widget, so the window can update things in it.
    """
    def notify(self):
        self.setWindowTitle(str(int(self.windowTitle()) * (-1)))

    """
    It decides whether the buttons upward, downward, edit contact and delete contact, all pertaining to the toolbar, shall be enabled or not.
    """
    def handleButtonsEvent(self):
        selected = self.contactListWidget.isSelected()

        self.upwardBtn.setEnabled(selected)
        self.downwardBtn.setEnabled(selected)
        self.updateContactBtn.setEnabled(selected)
        self.deleteContactBtn.setEnabled(selected)

        self.notify()

    """
    It moves the currently selected contact upward.
    """
    def moveUpwardEvent(self):
        index = self.contactListWidget.currentIndex()

        self._contactbook.moveContact(self.contactListWidget.currentIndex(), True)
        self.contactListWidget.showContactbook(self._contactbook)
        self.update()

        self.history.add("MOVE_UPWARD," + str(index))

        self.notify()

        self.modified = True

    """
    It moves the currently selected contact downward.
    """
    def moveDownwardEvent(self):
        index = self.contactListWidget.currentIndex()

        self._contactbook.moveContact(index, False)
        self.contactListWidget.showContactbook(self._contactbook)
        self.update()

        self.history.add("MOVE_DOWNWARD," + str(index))

        self.notify()

        self.modified = True

    """
    It adds a new contact into the contactbook.
    """
    def newContactEvent(self):
        dialog = ContactDialog(self, _("New contact"))
        if dialog.exec():
            data = dialog.getData()
            pos = self._contactbook.newContact(data[0], data[1], data[2], data[3], data[4], data[5], data[6])
            self.contactListWidget.showContactbook(self._contactbook)
            self.update()

            self.history.add("NEW_CONTACT," + str(pos) + "," + str(data[0]) + "," + str(data[1]) + "," + str(data[2]) + "," +  str(data[3]) + "," + str(data[4]) + "," + str(data[5]) + "," + str(data[6]))

            self.notify()

            self.modified = True

    """
    It edits the currently selected contact in the contactbook.
    """
    def editContactEvent(self):
        index = self.contactListWidget.currentIndex()

        dialog = ContactDialog(self, _("Edit contact"), {'name': self._contactbook.getContact(index)['name'], 'phone': self._contactbook.getContact(index)['phone'], 'email': self._contactbook.getContact(index)['email'], 'website': self._contactbook.getContact(index)['website'], 'address': self._contactbook.getContact(index)['address'], 'city': self._contactbook.getContact(index)['city'], 'info': self._contactbook.getContact(index)['info']})
        if dialog.exec():
            data = dialog.getData()

            self.history.add("EDIT_CONTACT," + str(index) + "," + str(self._contactbook.getContact(index)['name']) + "," + str(self._contactbook.getContact(index)['phone']) + "," + str(self._contactbook.getContact(index)['email']) + "," + str(self._contactbook.getContact(index)['website']) + "," + str(self._contactbook.getContact(index)['address']) + "," + str(self._contactbook.getContact(index)['city']) + "," + str(self._contactbook.getContact(index)['info']) + "," + str(data[0]) + "," + str(data[1]) + "," + str(data[2]) + "," + str(data[3]) + "," + str(data[4]) + "," + str(data[5]) + "," + str(data[6]))

            self._contactbook.editContact(index, data[0], data[1], data[2], data[3], data[4], data[5], data[6])
            self.contactListWidget.showContactbook(self._contactbook)
            self.update()

            self.notify()

            self.modified = True

    """
    It deletes the currently selected contact in the contactbook.
    """
    def deleteContactEvent(self):
        index = self.contactListWidget.currentIndex()

        self.history.add("DELETE_CONTACT," + str(index) + "," + str(self._contactbook.getContact(index)['name']) + "," + str(self._contactbook.getContact(index)['phone']) + "," + str(self._contactbook.getContact(index)['email']) + "," + str(self._contactbook.getContact(index)['website']) + "," + str( self._contactbook.getContact(index)['address']) + "," + str(self._contactbook.getContact(index)['city']) + "," + str(self._contactbook.getContact(index)['info']) + "," + str(self._contactbook.getContact(index)['moment_of_creation']))

        self._contactbook.deleteContact(index)

        self.contactListWidget.showContactbook(self._contactbook)
        self.update()

        self.notify()

        self.modified = True

    """
    It sorts the contacts.
    @param descending: True if descending, False if ascending.
    @param attrib: the attribute to consider in sorting.
    """
    def sortEvent(self, descending, attrib):
        contacts = ""
        for i in range(self._contactbook.numOfContacts()):
            contacts += self._contactbook.newChars(self._contactbook.getContact(i)['name']) + "," + \
            self._contactbook.getContact(i)['phone'] + "," + self._contactbook.getContact(i)[
            'email'] + "," + self._contactbook.getContact(i)['website'] + "," + self._contactbook.newChars(
            self._contactbook.getContact(i)['address']) + "," + self._contactbook.newChars(
            self._contactbook.getContact(i)['city']) + "," + self._contactbook.newChars(
            self._contactbook.getContact(i)['info']) + "," + str(
            self._contactbook.getContact(i)['moment_of_creation']) + ","

        self._contactbook.sort(descending, attrib)

        self.contactListWidget.showContactbook(self._contactbook)

        self.update()

        self.history.add("SORT," + str(descending) + "," + str(attrib) + "," + contacts)

        self.notify()

        self.modified = True

    """
    It searches for contacts using the text in self.searchLineEdit.
    """
    def searchEvent(self):
        indices = self._contactbook.find(self.searchLineEdit.text())
        contacts = []
        for i in indices:
            contacts.append(self._contactbook.getContact(i)['name'])

        self.contactListWidget.showList(contacts, indices)

    """
    It reads a contactbook onto the central widget.
    @param filename: contactbook filename. If it is None, then it means a new contactbook.
    @return 0 if reading was successful, 1 if it requires a newer Contacty version, 2 if file does not exist and 3 if other error occuried.
    """
    def read(self, filename):
        ret = self._contactbook.readBook(filename)
        if ret == 1:
            QMessageBox.critical(None, _("Error opening file"), _("File could not be open. It was made on a more recent Contacty version which is not compatible with the installed now."), QMessageBox.Ok)
            return 1
        elif ret == 2:
            QMessageBox.critical(None, _("Error opening file"), _("File could not be open. It does not exist."), QMessageBox.Ok)
            return 2
        elif ret == 3:
            QMessageBox.critical(None, _("Error opening file"), _("File could not be open. An error occuried."), QMessageBox.Ok)
            return 3
        else:
            self.contactListWidget.showContactbook(self._contactbook)
            self.history.new(self._contactbook)

            self.update()
            return 0

    """
    It saves the contactbook.
    @param filename: location to save
    """
    def save(self, filename):
        self._contactbook.saveBook(filename)

        self.modified = False

    """
    It undoes the last action made on the contactbook.
    """
    def undo(self):
        self.history.undo()
        self.contactListWidget.showContactbook(self._contactbook)
        self.update()

        self.notify()

    """
    It redoes the next action made on the contactbook.
    """
    def redo(self):
        self.history.redo()
        self.contactListWidget.showContactbook(self._contactbook)
        self.update()

        self.notify()

    """
    @return False if file is not modified. Otherwise True.
    """
    def isModified(self):
        return self.modified

    """
    @return a tuple in the format (isConsideringName, isConsideringPhone, isConsideringEmail, isConsideringWebsite, isConsideringAddress, isConsideringCity, isConsideringInfo, isConsideringSensitive), which indicates what criteria are being followed for searches in the contactbook.
    """
    def getSearch(self):
        return (self._contactbook.search_name, self._contactbook.search_phone, self._contactbook.search_email, self._contactbook.search_website, self._contactbook.search_address, self._contactbook.search_city, self._contactbook.search_info, self._contactbook.sensitive)

    """
    It sets the criteria to follow for searches in the contactbook.
    @param data: a tuple in the format (isConsideringName, isConsideringPhone, isConsideringEmail, isConsideringWebsite, isConsideringAddress, isConsideringCity, isConsideringInfo, isConsideringSensitive)
    """
    def setSearch(self, data):
        self._contactbook.search_name = data[0]
        self._contactbook.search_phone = data[1]
        self._contactbook.search_email = data[2]
        self._contactbook.search_website = data[3]
        self._contactbook.search_address = data[4]
        self._contactbook.search_city = data[5]
        self._contactbook.search_info = data[6]
        self._contactbook.sensitive = data[7]

    """
    @return a tuple in the format (descending, attribute), which indicates what criteria are being followed for contact insertions in the contactbook. Descending is a bool telling us if the order is descending or not and the attribute is a string telling us which attribute to consider for sorts.
    """
    def getInsert(self):
        return (self._contactbook.descending, self._contactbook.attrib)

    """
    It sets the criteria to follow for contact insertions in the contactbook.
    @param data: a tuple in the format (descending, attribute). Descending is a bool telling us if the order is descending or not and the attribute is a string telling us which attribute to consider for sorts.
    """
    def setInsert(self, data):
        self._contactbook.descending = data[0]
        self._contactbook.attrib = data[1]
