from gui.centralwidget import CentralWidget
from gui.aboutdialog import AboutDialog
from gui.sortdialog import SortDialog
from gui.finddialog import FindDialog
from gui.insertiondialog import InsertionDialog
from functools import partial

from PyQt6.QtWidgets import (
	QMainWindow,
	QStyle,
	QMenuBar,
	QMenu,
	QFileDialog,
	QMessageBox
)

from PyQt6.QtGui import (
	QIcon, 
	QKeySequence,
	QAction
)

from PyQt6.QtCore import QSettings

class MainWindow(QMainWindow):
    """
    This is, as the name suggests, the main window of the program.
    @param filename: the filename to open. By default, it is None, which means no file.
    """

    def __init__(self, filename=None):
        super().__init__()

        self.filename = filename

        self.setGeometry(100, 100, 500, 400)
        self.setWindowIcon(QIcon('../res/contacty.png'))

        self.qsettings = QSettings('Gabriel Soares', 'Contacty')

        self._createMenu()

        self.centralWidget = CentralWidget(filename)
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.windowTitleChanged.connect(self.handleActionsEvent)

        if self.filename == None:
            self.newFileEvent()
        else:
            self.openFile(self.filename)

        self.show()

    def _createMenu(self):
        """
        It creates the window menu.
        """

        menuBar = QMenuBar(self)

        """
        In menu bar, three menus are available:
        """
        fileMenu = QMenu(_('File'), self)
        editMenu = QMenu(_('Edit'), self)
        helpMenu = QMenu(_('Help'), self)

        """
        These are the actions inside the file menu:
        """
        newAction = QAction(self.style().standardIcon(getattr(QStyle.StandardPixmap, "SP_FileIcon")), _('New'), self)
        newAction.triggered.connect(self.newFileEvent)
        newAction.setShortcut(QKeySequence("Ctrl+Shift+N"))

        openAction = QAction(self.style().standardIcon(getattr(QStyle.StandardPixmap, "SP_DialogOpenButton")), _('Open'), self)
        openAction.triggered.connect(self.openFileEvent)
        openAction.setShortcut(QKeySequence("Ctrl+O"))

        saveAction = QAction(self.style().standardIcon(getattr(QStyle.StandardPixmap, "SP_DialogSaveButton")), _('Save'), self)
        saveAction.triggered.connect(self.saveFileEvent)
        saveAction.setShortcut(QKeySequence("Ctrl+S"))

        saveAsAction = QAction(self.style().standardIcon(getattr(QStyle.StandardPixmap, "SP_DialogSaveButton")), _('Save as'), self)
        saveAsAction.setShortcut(QKeySequence("Ctrl+Shift+S"))
        saveAsAction.triggered.connect(self.saveFileAsEvent)

        closeAction = QAction(self.style().standardIcon(getattr(QStyle.StandardPixmap, "SP_DialogCloseButton")), _('Close'), self)
        closeAction.triggered.connect(self.close)
        closeAction.setShortcut(QKeySequence("Ctrl+Q"))

        """
        Now adding the actions defined above into the file menu:
        """
        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)

        self.openRecentMenu = fileMenu.addMenu(_('Open recent'))
        self.openRecentMenu.setIcon(self.style().standardIcon(getattr(QStyle.StandardPixmap, "SP_DialogOpenButton")))
        self.openRecentMenu.aboutToShow.connect(self.openRecentEvent)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(saveAsAction)
        fileMenu.addAction(closeAction)
        fileMenu.insertSeparator(openAction)
        fileMenu.insertSeparator(saveAction)
        fileMenu.insertSeparator(closeAction)

        """
        These are the actions inside the edit menu:
        """
        self.undoAction = QAction(self.style().standardIcon(getattr(QStyle.StandardPixmap, "SP_ArrowLeft")), _('Undo'), self)
        self.undoAction.triggered.connect(self.undoEvent)
        self.undoAction.setShortcut(QKeySequence("Ctrl+Z"))
        self.undoAction.setEnabled(False)

        self.redoAction = QAction(self.style().standardIcon(getattr(QStyle.StandardPixmap, "SP_ArrowRight")), _('Redo'), self)
        self.redoAction.triggered.connect(self.redoEvent)
        self.redoAction.setShortcut(QKeySequence("Ctrl+Y"))
        self.redoAction.setEnabled(False)

        self.upwardAction = QAction(self.style().standardIcon(getattr(QStyle.StandardPixmap, "SP_ArrowUp")), _('Move contact upward'), self)
        self.upwardAction.setShortcut(QKeySequence("Ctrl+U"))
        self.upwardAction.triggered.connect(self.upwardEvent)
        self.upwardAction.setEnabled(False)

        self.downwardAction = QAction(self.style().standardIcon(getattr(QStyle.StandardPixmap, "SP_ArrowDown")), _('Move contact downward'), self)
        self.downwardAction.setShortcut(QKeySequence("Ctrl+D"))
        self.downwardAction.triggered.connect(self.downwardEvent)
        self.downwardAction.setEnabled(False)

        self.newContactAction = QAction(self.style().standardIcon(getattr(QStyle.StandardPixmap, "SP_FileDialogNewFolder")), _('New contact'), self)
        self.newContactAction.setShortcut(QKeySequence("Ctrl+N"))
        self.newContactAction.triggered.connect(self.newContactEvent)

        self.editContactAction = QAction(self.style().standardIcon(getattr(QStyle.StandardPixmap, "SP_FileLinkIcon")), _('Edit contact'), self)
        self.editContactAction.setShortcut(QKeySequence("Ctrl+E"))
        self.editContactAction.triggered.connect(self.editContactEvent)
        self.editContactAction.setEnabled(False)

        self.deleteContactAction = QAction(self.style().standardIcon(getattr(QStyle.StandardPixmap, "SP_DialogDiscardButton")), _('Delete contact'), self)
        self.deleteContactAction.setShortcut(QKeySequence("Del"))
        self.deleteContactAction.triggered.connect(self.deleteContactEvent)
        self.deleteContactAction.setEnabled(False)

        self.sortAction = QAction(self.style().standardIcon(getattr(QStyle.StandardPixmap, "SP_FileDialogListView")), _('Sort contacts'), self)
        self.sortAction.setShortcut(QKeySequence("Ctrl+R"))
        self.sortAction.triggered.connect(self.sortEvent)

        self.findAction = QAction(self.style().standardIcon(getattr(QStyle.StandardPixmap, "SP_FileDialogContentsView")), _('Search settings'), self)
        self.findAction.setShortcut(QKeySequence("Ctrl+F"))
        self.findAction.triggered.connect(self.findConfEvent)

        self.insertionConfAction = QAction(self.style().standardIcon(getattr(QStyle.StandardPixmap, "SP_FileDialogDetailedView")), _('Contact insertion settings'), self)
        self.insertionConfAction.setShortcut(QKeySequence("Ctrl+I"))
        self.insertionConfAction.triggered.connect(self.insertionConfEvent)

        """
        Now adding the actions defined above into the edit menu:
        """
        editMenu.addAction(self.undoAction)
        editMenu.addAction(self.redoAction)
        editMenu.addAction(self.upwardAction)
        editMenu.addAction(self.downwardAction)
        editMenu.addAction(self.newContactAction)
        editMenu.addAction(self.editContactAction)
        editMenu.addAction(self.deleteContactAction)
        editMenu.addAction(self.sortAction)
        editMenu.addAction(self.findAction)
        editMenu.addAction(self.insertionConfAction)

        editMenu.insertSeparator(self.upwardAction)
        editMenu.insertSeparator(self.newContactAction)
        editMenu.insertSeparator(self.sortAction)
        editMenu.insertSeparator(self.findAction)

        """
        These are the actions inside the help menu:
        """
        aboutAction = QAction(self.style().standardIcon(getattr(QStyle.StandardPixmap, 'SP_MessageBoxInformation')), _('About'), self)
        aboutAction.triggered.connect(self.aboutEvent)
        helpMenu.addAction(aboutAction)

        """
        Now adding the actions defined above into the help menu:
        """
        menuBar.addMenu(fileMenu)
        menuBar.addMenu(editMenu)
        menuBar.addMenu(helpMenu)

        self.setMenuBar(menuBar)

    def addRecentFile(self, filename):
        """
        It adds the given filename location into the recent files

        @param filename: the filename
        """

        keys = self.qsettings.allKeys()

        is_in_list = False
        pos = -1
        for i in range(len(keys)): # Checking if file is in list
            if self.qsettings.value(str(i)) == filename:
                is_in_list = True
                pos = i
                break

        if is_in_list == True: # Move the file to the top
            while pos > 0:
                aux = self.qsettings.value(str(pos-1))
                self.qsettings.setValue(str(pos-1), filename)
                self.qsettings.setValue(str(pos), aux)
                pos -= 1
        else: # Add it into the list
            for i in range(len(keys), 0, -1):
                self.qsettings.setValue(str(i), self.qsettings.value(str(i-1)))
            self.qsettings.setValue(str(0), filename)

    def openFile(self, filename):
        """
        It opens the given file

        @param filename: the filename
        """

        if self.centralWidget.read(filename) == 0:
            self.setWindowTitle("Contacty - " + str(filename))
            self.filename = filename

            self.addRecentFile(filename)

            self.undoAction.setEnabled(False)
            self.redoAction.setEnabled(False)

    """
    Events for menu:
    """

    def handleActionsEvent(self):
        """
        It decides whether the following actions, undo, redo, upward, downward, edit contact and delete contact, all pertaining to edit menu, shall be enabled or not.
        """

        self.undoAction.setEnabled(self.centralWidget.history.canUndo())
        self.redoAction.setEnabled(self.centralWidget.history.canRedo())

        selected = self.centralWidget.contactListWidget.isSelected()

        self.upwardAction.setEnabled(selected)
        self.downwardAction.setEnabled(selected)
        self.editContactAction.setEnabled(selected)
        self.deleteContactAction.setEnabled(selected)

    def newFileEvent(self):
        """
        It creates an empty contacty file and opens it.
        """

        self.setWindowTitle(_("Contacty - Untitled"))
        self.filename = None
        self.centralWidget.read(None)

        self.undoAction.setEnabled(False)
        self.redoAction.setEnabled(False)

    def openFileEvent(self):
        """
        It enables the user to open a contacty file through a dialog.

        @param filename: the filename
        """

        filename, tmp = QFileDialog.getOpenFileName(self, _('Open file'), '', _("Contacty files(*.ctcy)"))

        if filename != '':
            self.openFile(filename)

    def openRecentEvent(self):
        """
        It is called when the user puts the mouse on open recent action, showing the recent files.
        """

        self.openRecentMenu.clear()

        keys = self.qsettings.allKeys()

        if keys == []:
            self.openRecentMenu.addAction(_('No file'))
        else:
            for i in keys[:5]: # There is a limit of 5 files in the recent files list.
                action = QAction(self.qsettings.value(i), self)
                action.triggered.connect(partial(self.openFile, self.qsettings.value(i)))

                self.openRecentMenu.addAction(action)

            action = QAction(_('Clear list'), self)
            action.triggered.connect(self.qsettings.clear)
            self.openRecentMenu.insertSeparator(action)
            self.openRecentMenu.addAction(action)

    def saveFileEvent(self):
        """
        It saves the current file. If it is a new file, then self.saveFileAsEvent() is called.
        """

        if self.filename == None:
            self.saveFileAsEvent()
        else:
            self.centralWidget.save(self.filename)

    def saveFileAsEvent(self):
        """
        It saves the current file as other file through a dialog.
        """

        filename, tmp = QFileDialog.getSaveFileName(self, _('Save as'), '', _("Contacty files(*.ctcy)"))

        if filename:
            try:
                if filename[-5:] != ".ctcy":
                    filename = filename + ".ctcy"

                self.centralWidget.save(filename)
                self.openFile(filename)
            except:
                QMessageBox.critical(self, _("Error saving file"), _("File could not be saved."), QMessageBox.Ok)

    def undoEvent(self):
        """
        It undoes the last action made on the contactbook.
        """

        self.centralWidget.undo()

    def redoEvent(self):
        """
        It redoes the next action made on the contactbook.
        """

        self.centralWidget.redo()

    def sortEvent(self):
        """
        It shows the sort contact dialog, asking the user if the sort shall be made and how. After the user's answer, the sort is done.
        """

        dialog = SortDialog(self, _('Sort contacts'))
        if dialog.exec():
            data = dialog.getData()

            self.centralWidget.sortEvent(data[0], data[1])

    def upwardEvent(self):
        """
        It moves the currently selected contact upward.
        """

        self.centralWidget.moveUpwardEvent()

    def downwardEvent(self):
        """
        It moves the currently selected contact downward.
        """

        self.centralWidget.moveDownwardEvent()

    def newContactEvent(self):
        """
        It adds a new contact into the contactbook.
        """

        self.centralWidget.newContactEvent()

    def editContactEvent(self):
        """
        It edits the currently selected contact in the contactbook.
        """

        self.centralWidget.editContactEvent()

    def deleteContactEvent(self):
        """
        It deletes the currently selected contact in the contactbook.
        """

        self.centralWidget.deleteContactEvent()

    def aboutEvent(self):
        """
        It shows the about dialog.
        """

        AboutDialog(self)

    def closeEvent(self, event):
        """
        Function to be called after the user tries to close the main window. If the file was modified, the program will ask the user if he would like to save the changes before closing.
        """

        if self.centralWidget.isModified():
            reply = QMessageBox.question(self, 'Contacty', _('Would you like to save the changes?'), QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Yes)

            if reply == QMessageBox.Yes:
                self.saveFileEvent()
                event.accept()
            elif reply == QMessageBox.No:
                event.accept()
            elif reply == QMessageBox.Cancel:
                event.ignore()
        else:
            event.accept()

    def findConfEvent(self):
        """
        It shows the find dialog, enabling the user to decide how the searches shall be done.
        """

        dialog = FindDialog(self, self.centralWidget.getSearch(), _('Search settings'))
        if dialog.exec():
            data = dialog.getData()

            self.centralWidget.setSearch(data)

    def insertionConfEvent(self):
        """
        It shows the insertion dialog, enabling the user to decide how the contact insertions shall be done.
        """

        dialog = InsertionDialog(self, self.centralWidget.getInsert(), _('Contact insertion settings'))
        if dialog.exec():
            data = dialog.getData()

            self.centralWidget.setInsert(data)
