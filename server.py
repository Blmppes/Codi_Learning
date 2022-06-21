import socket
import sys
import cv2
import numpy as np
#
# from PyQt5 import QtGui
# from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QPushButton
# from PyQt5.QtGui import QPixmap
# from PyQt5.QtCore import pyqtSignal, Qt, QThread
#
# class App(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Qt live label demo")
#         self.setGeometry(300, 100, 600, 400)
#         self.display_width = 640
#         self.display_height = 480
#
#         self.initUI()
#
#     def initUI(self):
#         self.hostBtn = QPushButton(self)
#         self.hostBtn.setText("Create a new meeting")
#         self.hostBtn.clicked.connect(self.createNewMeeting)
#         self.hostBtn.setGeometry(100, 190, 120, 20)
#
#         self.joinBtn = QPushButton(self)
#         self.joinBtn.setText("Join a new meeting")
#         self.joinBtn.clicked.connect(self.joinNewMeeting)
#         self.joinBtn.setGeometry(400, 190, 110, 20)
#
#     def createNewMeeting(self):
#         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         s.bind((socket.gethostname(), 1234))
#         s.listen(5)
#         while True:
#             clientsocket, address = s.accept()
#             print(f"Connection from {address} has been established.")
#     def joinNewMeeting(self):
#         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         s.connect((socket.gethostname(), 1234))
#
# if __name__=="__main__":
#     app = QApplication(sys.argv)
#     a = App()
#     a.show()
#     sys.exit(app.exec_())

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1234))
s.listen(5)

while True:
    # now our endpoint knows about the OTHER endpoint.
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")
