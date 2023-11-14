import sys

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QTableWidgetItem

from app.database import Database
from app.ui.getInfo_form import GetNote_Ui_Dialog
from app.ui.main_form import Ui_MainWindow
from app.ui.newNote_form import AddNote_Ui_Dialog

APP_WIDTH, APP_HEIGHT = 650, 440


class NotesApp(QMainWindow):
    TABLE_COLUMN_COUNT = 2
    TABLE_COLUMN_WIDTH = 298
    TABLE_COLUMN_HEIGHT = 70

    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.changeTableData()

        # Slots
        self.ui.addNote_btn.clicked.connect(self.addNoteClick)
        self.ui.tableNotes_widget.cellClicked.connect(self.viewInfoNote)

        # Create timer update data in table
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.changeTableData)
        self.timer.start(500)

    def changeTableData(self):
        keyword = self.ui.search_lineEdit.text()
        getRows = db.get_notes()

        if len(keyword) > 0:
            getRows = db.get_note(keyword)

        self.ui.tableNotes_widget.setRowCount(len(getRows))
        self.ui.tableNotes_widget.setColumnCount(self.TABLE_COLUMN_COUNT)

        for i in range(len(getRows)):
            for j in range(len(getRows[i])):
                self.ui.tableNotes_widget.setItem(i, j, QTableWidgetItem(str(getRows[i][j])))
                self.ui.tableNotes_widget.setColumnWidth(i, self.TABLE_COLUMN_WIDTH)
                self.ui.tableNotes_widget.setRowHeight(i, self.TABLE_COLUMN_HEIGHT)

    def viewInfoNote(self, row):
        get_dialog = GetNoteDialogWindow(row)
        get_dialog.exec()

    def addNoteClick(self):
        add_dialog = AddNoteDialogWindow()
        add_dialog.exec()


class AddNoteDialogWindow(QDialog):

    def __init__(self):
        super().__init__()
        self.ui = AddNote_Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.save_btn.clicked.connect(self.saveNote)

    def saveNote(self):
        title = self.ui.lineEdit_title.text()
        content = self.ui.textEdit_content.toPlainText()
        if len(title) > 0 and len(content) > 0:
            db.add_note(title, content)
            self.close()


class GetNoteDialogWindow(QDialog):

    def __init__(self, index):
        super().__init__()

        self.index = index

        self.ui = GetNote_Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.del_btn.clicked.connect(self.deleteNote)

        self.getNote()

    def getNote(self):
        notes = db.get_notes()[self.index]
        self.ui.titel_lineEdit.setReadOnly(True)
        self.ui.content_plainTextEdit.setReadOnly(True)
        self.ui.titel_lineEdit.setText(notes[0])
        self.ui.content_plainTextEdit.setPlainText(notes[1])

    def deleteNote(self):
        notes = db.get_notes()[self.index]
        db.del_note(notes[0])
        self.close()


if __name__ == '__main__':
    db = Database(path="app/database/app.db")
    app = QApplication(sys.argv)
    login_window = NotesApp()
    login_window.setFixedSize(APP_WIDTH, APP_HEIGHT)
    login_window.show()
    sys.exit(app.exec())
