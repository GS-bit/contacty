"""
History intends to store all actions done on a contactbook, enabling the user to undo or redo them.

All actions are described through commands. Each command is divided in type of action and arguments. The type of action is entirely uppercase. All types of action and arguments shall be separed by commas.
These are the commands:

MOVE_UPWARD,[index]: moved contact from the given index upward.
MOVE_DOWNWARD,[index]: moved contact from the given index downward.
NEW_CONTACT,[index],[name],[phone],[email],[website],[address],[city],[info]: created contact with given name, phone, email, website, address, city and info. The given index is its index in the contactbook.
EDIT_CONTACT,[index],[current name],[current phone] [current email] [current website] [current address] [current city] [current info] [new name] [new phone] [new email] [new website] [new address] [new city] [new info]: edited contact whose index in the contactbook was given. Current name became new name, current phone new phone, current email new email, current website new website, current address new address, current city new city and current info new info.
DELETE_CONTACT,[index],[name],[phone],[email],[website],[address],[city],[info],[moment_of_creation]: deleted contact whose index in the contactbook was given, along with its name, phone, email, website, address, city, info and moment of creation.
SORT,[descending],[attrib],[contact one's name],[contact one's phone],[contact one's email],[contact one's website],[contact one's address],[contact one's city],[contact one's info],[contact one's moment_of_creation][contact two's name],[contact two's phone],[contact one's email],[contact two's website],[contact two's address],[contact two's city],[contact two's info],[contact two's moment_of_creation],...,[contact N's name],[contact N's phone],[contact N's email],[contact N's website],[contact N's address],[contact N's city],[contact N's info],[contact N's moment_of_creation]: sorted a contactbook, descending or not, considering the given attribute attrib. There are N contacts, its information are in the command.

@param contactbook: the contactbook to handle
"""
class History:
    def __init__(self, contactbook):
        self.new(contactbook)

    """
    It adds a command into the list of actions made on the contactbook.
    @param command: the command
    """
    def add(self, command):
        self._history_stack.insert(self._pos, command)
        self._pos += 1

        self._history_stack = self._history_stack[:self._pos]

    """
    @return False if it is not possible to undo the last action made on the contactbook. True otherwise.
    """
    def canUndo(self):
        if self._pos == 0:
            return False
        else:
            return True

    """
    @return False if it is not possible to redo the next action made on the contactbook. True otherwise.
    """
    def canRedo(self):
        if len(self._history_stack) == self._pos:
            return False
        else:
            return True

    """
    It undoes the last action made on the contactbook.
    """
    def undo(self):
        if self.canUndo():
            data = self._history_stack[self._pos-1].split(',')

            if data[0] == "MOVE_UPWARD":
                self._contactbook.moveContact(int(data[1])-1, False)

            elif data[0] == "MOVE_DOWNWARD":
                self._contactbook.moveContact(int(data[1])+1, True)

            elif data[0] == "NEW_CONTACT":
                self._contactbook.deleteContact(int(data[1]))

            elif data[0] == "EDIT_CONTACT":
                self._contactbook.editContact(int(data[1]), data[2], data[3], data[4], data[5], data[6], data[7], data[8])

            elif data[0] == "DELETE_CONTACT":
                self._contactbook.newContact(data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], int(data[1]))

            elif data[0] == "SORT":
                self._contactbook.clear()

                for i in range(3, len(data)-1, 8):
                    self._contactbook.newContact(self._contactbook.oldChars(data[i]), data[i+1], data[i+2], data[i+3], self._contactbook.oldChars(data[i+4]), self._contactbook.oldChars(data[i+5]), self._contactbook.oldChars(data[i+6]), int(data[i+7]), "last")

            self._pos -= 1

    """
    It redoes the next action made on the contactbook.
    """
    def redo(self):
        if self.canRedo():
            data = self._history_stack[self._pos].split(',')

            if data[0] == "MOVE_UPWARD":
                self._contactbook.moveContact(data[1], True)
            elif data[0] == "MOVE_DOWNWARD":
                self._contactbook.moveContact(data[1], False)
            elif data[0] == "NEW_CONTACT":
                self._contactbook.newContact(data[2], data[3], data[4], data[5], data[6], data[7], data[1])
            elif data[0] == "EDIT_CONTACT":
                self._contactbook.editContact(int(data[1]), data[9], data[10], data[11], data[12], data[13], data[14], data[15])
            elif data[0] == "DELETE_CONTACT":
                self._contactbook.deleteContact(int(data[1]))
            elif data[0] == "SORT":
                self._contactbook.sort(True if data[1] == "True" else False, data[2])

            self._pos += 1

    """
    It creates a new history stack.
    @param contactbook: the contactbook to work with
    """
    def new(self, contactbook):
        self._contactbook = contactbook
        self._history_stack = []
        self._pos = 0  # Position of the user on the self._history_stack.
