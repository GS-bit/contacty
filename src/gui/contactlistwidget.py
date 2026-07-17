from PyQt6.QtWidgets import QListWidget

class ContactListWidget(QListWidget):
    """
    ContactListWidget has much in common to its superclass, QListWidget, but it was made for a more integrated use with Contactbooks.
    """

    def __init__(self):
        super().__init__(None)

        self.indices = [] # This list associates each QListWidget item index to an index in a contactbook. This way, self.indices[n] = k means that the nth QListWidget item is associated to the kth index of a contactbook.

    def showContactbook(self, contactbook):
        """
        It shows the contactbook contacts and also provides indices for self.indices.

        @param contactbook: the contactbook
        """

        self.clear()

        for i in range(contactbook.numOfContacts()):
            self.addItem(contactbook.getContact(i)['name'])

        self.indices = [i for i in range(contactbook.numOfContacts())]

    def showList(self, listToShow, indices):
        """
        It shows a list of contacts.

        @param listToShow: the list to show
        @param indices: the indices for self.indices
        """

        self.clear()

        for i in listToShow:
            self.addItem(i)

        self.indices = indices[:]

    def currentIndex(self):
        """
        @return the index of the currently selected contact.
        """

        return self.indices[self.currentRow()]

    def isSelected(self):
        """
        @return True if a contact is selected. False otherwise.
        """

        if self.currentItem() == None:
            return False
        else:
            return True
