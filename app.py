from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QPlainTextEdit, QLabel, QPushButton, QFileDialog, QTextEdit, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5 import QtCore
import sys
import os
import re

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.x = 183
        self.y = 84
        self.width = 1000
        self.height = 600
        self.currentOpening = ""
        self.suggestionList = set()
        self.backgroundColor = "black"

        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: black; color: white")
        self.setGeometry(self.x, self.y, self.width, self.height)
        self.setWindowTitle("Coditor 0.2")
        self.statusBar()
        self.filebar = self.menuBar()
        self.filebar.setStyleSheet("""
            background-color: #ffffff;
            color : black;
        """)
        #File
        self.exitAct = QAction('&Exit', self)
        self.exitAct.setShortcut('Ctrl+Q')
        self.exitAct.setStatusTip('Exit application')
        self.exitAct.triggered.connect(qApp.quit)

        self.saveAsAct = QAction('&Save As', self)
        self.saveAsAct.setShortcut('Ctrl+S')
        self.saveAsAct.setStatusTip('Save as')
        self.saveAsAct.triggered.connect(self.saveAs)

        self.saveAct = QAction('&Save', self)
        self.saveAct.setShortcut('Ctrl+L')
        self.saveAct.setStatusTip('Save')
        self.saveAct.triggered.connect(self.save)

        self.openAct = QAction('&Open', self)
        self.openAct.setShortcut('Ctrl+O')
        self.openAct.setStatusTip('Open file')
        self.openAct.triggered.connect(self.openFile)

        self.fileMenu = self.filebar.addMenu('&File')
        self.fileMenu.addAction(self.exitAct)
        self.fileMenu.addAction(self.saveAsAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.openAct)

        #Edit
        self.colorAct = QAction('&Change backgroud color', self)
        self.colorAct.setShortcut('Ctrl+Shift+V')
        self.colorAct.setStatusTip('Change background color')
        self.colorAct.triggered.connect(self.changeBackgroundColor)

        self.editMenu = self.filebar.addMenu('&Edit')
        self.editMenu.addAction(self.colorAct)

        # Create textbox
        self.textbox = QTextEdit(self)
        self.textbox.setGeometry(30, 21, self.width - 30, self.height - 41)
        self.textbox.textChanged.connect(self.updateCharacterCounter)
        # self.textbox.textChanged.connect(self.suggest)
        self.textbox.installEventFilter(self)

        #Characters
        self.characterCounter = QLabel(self)
        self.characterCounter.setGeometry(self.width - 200, self.height - 20, 200, 20)
        self.characterCounter.setText(f"{0} characters")

        self.suggestLabel = QPushButton(self)
        self.suggestLabel.setGeometry(self.width - 100, self.height - 18, 100, 20)
        self.suggestLabel.clicked.connect(self.applySuggestion)

        self.numberLabel = QLabel(self)
        self.numberLabel.setText('1')
        self.numberLabel.setGeometry(5, 23, 5, 20)

    def update(self):
        self.numberLabel.adjustSize()

    def changeBackgroundColor(self):
        if(self.backgroundColor == "black"):
            self.setStyleSheet("background-color: white; color: black")
            self.backgroundColor = "white"
        else:
            self.setStyleSheet("background-color: black; color: white")
            self.backgroundColor = "black"

    def saveAs(self):
        try:
            name, _ = QFileDialog.getSaveFileName(self)

            text = self.textbox.toPlainText()
            if(name != ''):
                with open(name, 'w') as f:
                    f.write(text)
                    self.suggestionList.update(re.split(' |\n', text))

                self.currentOpening = name

                self.setWindowTitle(f"{os.path.split(name)[1]} -- {os.path.split(name)[0]} -- Coditor 0.2")
        except:
            QMessageBox.about(self, "Error", "Can't save this file")

    def save(self):
        try:
            text = self.textbox.toPlainText()
            if(self.currentOpening != ''):
                with open(self.currentOpening, 'w') as f:
                    f.write(text)
            else:
                self.saveAs()
        except:
            QMessageBox.about(self, "Error", "Can't save this file")

    def openFile(self):
        try:
            name, _ = QFileDialog.getOpenFileName(self)

            if(name != ''):
                self.suggestionList = set()
                with open(name, 'r') as file:
                    text = file.read()
                    self.textbox.setText(text)
                    self.suggestionList.update(re.split(' |\n', text))

                self.currentOpening = name
                self.setWindowTitle(f"{os.path.split(name)[1]} -- {os.path.split(name)[0]} -- Coditor 0.2")

            #Update lines number
            numberOfLines = len(self.textbox.toPlainText().splitlines()) + 1
            text = ''
            counter = 1
            for i in range(numberOfLines):
                text += str(counter) + '\n'
                counter += 1

            self.numberLabel.setText(text)
            self.numberLabel.setGeometry(5, 27, 5, numberOfLines * 20)
            self.update()
        except:
            QMessageBox.about(self, "Error", "Can't open this file")

    def updateCharacterCounter(self):
        counter = len(self.textbox.toPlainText())
        self.characterCounter.setText(f"{counter} characters")

    def eventFilter(self, obj, event):
        # Suggestion
        cursor = self.textbox.textCursor()
        string_list = re.split(" |\n", self.textbox.toPlainText()[0: cursor.position()])
        string = string_list[len(string_list) - 1]
        for i in self.suggestionList:
            if(len(string) >= 1):
                if(i != '' and i[0 : len(string)] == string):
                    self.suggestLabel.setText(i)
                    self.update()
                    break
                else:
                    self.suggestLabel.setText("")
                    self.update()

        #Number lines
        if event.type() == QtCore.QEvent.KeyPress and obj is self.textbox:
            if event.key() == 16777220 and self.textbox.hasFocus():
                text = self.textbox.toPlainText()
                self.suggestionList.update(re.split(' |\n', text))

                numberOfLines = len(self.textbox.toPlainText().splitlines()) + 1
                text = ''
                counter = 1
                for i in range(numberOfLines):
                    text += str(counter) + '\n'
                    counter += 1

                self.numberLabel.setText(text)
                self.numberLabel.setGeometry(5, 27, 5, numberOfLines * 20)
                self.update()

        return super().eventFilter(obj, event)

    def applySuggestion(self):
        text = self.suggestLabel.text()

        cursor = self.textbox.textCursor()
        string_list = re.split(" |\n", self.textbox.toPlainText()[0: cursor.position()])
        x1 = cursor.position() - len(string_list[len(string_list) - 1])

        cursor.insertText(text)
        cursor.setPosition(x1, QtGui.QTextCursor.KeepAnchor)
        self.textbox.setTextCursor(cursor)

def RUN_APP():
    app = QApplication(sys.argv)
    win = MyWindow()

    win.show()
    sys.exit(app.exec_())
