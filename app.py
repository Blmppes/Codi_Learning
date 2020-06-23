from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QPlainTextEdit, QLabel, QPushButton, QFileDialog, QTextEdit
from PyQt5.QtGui import QIcon
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

        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: black; color: white")
        self.setGeometry(self.x, self.y, self.width, self.height)
        self.setWindowTitle("NotePad+++")
        self.statusBar()
        self.filebar = self.menuBar()

        #File
        self.exitAct = QAction(QIcon('90833571-exit-red-glossy-circle-icon-button-design-vector-illustration.jpg'), '&Exit', self)
        self.exitAct.setShortcut('Ctrl+Q')
        self.exitAct.setStatusTip('Exit application')
        self.exitAct.triggered.connect(qApp.quit)

        self.saveAsAct = QAction('&Save As', self)
        self.saveAsAct.setShortcut('Ctrl+S+A')
        self.saveAsAct.setStatusTip('Save as')
        self.saveAsAct.triggered.connect(self.saveAs)

        self.saveAct = QAction('&Save', self)
        self.saveAct.setShortcut('Ctrl+S')
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
        self.colorAct.setShortcut('Ctrl+V')
        self.colorAct.setStatusTip('Change background color')
        self.colorAct.triggered.connect(self.changeBackgroundColor)

        self.editMenu = self.filebar.addMenu('&Edit')
        self.editMenu.addAction(self.colorAct)

        #Help
        # exitAct = QAction(QIcon('90833571-exit-red-glossy-circle-icon-button-design-vector-illustration.jpg'), '&Exit', self)
        # exitAct.setShortcut('Ctrl+Q')
        # exitAct.setStatusTip('Exit application')
        # exitAct.triggered.connect(qApp.quit)
        #
        # menubar = self.menuBar()
        # fileMenu = menubar.addMenu('&File')
        # fileMenu.addAction(exitAct)

        # Create textbox
        self.textbox = QTextEdit(self)
        self.textbox.setGeometry(0, 20, self.width, self.height - 40)
        self.textbox.textChanged.connect(self.updateCharacterCounter)
        self.textbox.textChanged.connect(self.suggest)

        #Characters
        self.characterCounter = QLabel(self)
        self.characterCounter.setGeometry(self.width - 200, self.height - 20, 200, 20)
        self.characterCounter.setText(f"{0} characters")

        self.suggestLabel = QLabel(self)
        self.suggestLabel.setGeometry(self.width - 100, self.height - 18, 100, 20)

    def update(self):
        self.suggestLabel.adjustSize()

    def changeBackgroundColor(self):
         self.setStyleSheet("background-color: yellow;")

    def saveAs(self):
        name, _ = QFileDialog.getSaveFileName(self)

        text = self.textbox.toPlainText()
        if(name != ''):
            with open(name, 'w') as f:
                f.write(text)
                self.suggestionList.update(re.split(' |\n', text))

            self.currentOpening = name

            self.setWindowTitle(f"{os.path.split(name)[1]} -- {os.path.split(name)[0]} -- Coditor 0.2")


    def save(self):
        text = self.textbox.toPlainText()
        self.suggestionList.update(re.split(' |\n', text))
        # self.fixSuggestionList()
        if(self.currentOpening != ''):
            with open(self.currentOpening, 'w') as f:
                f.write(text)
        else:
            self.saveAs()


    def openFile(self):
        name, _ = QFileDialog.getOpenFileName(self)

        if(name != ''):
            self.suggestionList = set()
            with open(name, 'r') as file:
                text = file.read()
                self.textbox.setText(text)
                self.suggestionList.update(re.split(' |\n', text))
                # self.fixSuggestionList()

            self.currentOpening = name
            self.setWindowTitle(f"{os.path.split(name)[1]} -- {os.path.split(name)[0]} -- Coditor 0.2")

    def updateCharacterCounter(self):
        counter = len(self.textbox.toPlainText())
        self.characterCounter.setText(f"{counter} characters")

    def suggest(self):
        #To get the word is being typed took me a lot of time, but finally i solved it =)
        #Get the word is being typed
        cursor = self.textbox.textCursor()
        string_list = re.split(" |\n", self.textbox.toPlainText()[0: cursor.selectionStart()])
        string = string_list[len(string_list) - 1]

        for i in self.suggestionList:
            if(i != '' and i[0 : len(string)] == string):
                print(i)
                print(self.suggestionList)
                self.suggestLabel.setText(i)
                self.update()
                break
            # else:
            #     self.suggestLabel.setText('')
            #     self.update()


    # def fixSuggestionList(self):
    #     for i in range(len(self.suggestionList)):
    #         list[i] = list[i].rstrip("\n")

def window():
    app = QApplication(sys.argv)
    win = MyWindow()

    win.show()
    sys.exit(app.exec_())

window()
