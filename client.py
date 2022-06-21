from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, Qt, QThread

import sys
import cv2
import numpy as np
from PIL import ImageGrab
import socket

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def run(self):
        # capture from web cam
        while True:
            img = ImageGrab.grab()
            cv_img = np.array(img)
            self.change_pixmap_signal.emit(cv_img)


class Client(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qt live label demo")
        self.display_width = 640
        self.display_height = 480

        self.initUI()

    def initUI(self):
        # create the label that holds the image
        self.image_label = QLabel(self)
        self.image_label.resize(self.display_width, self.display_height)
        # create a text label
        self.textLabel = QLabel('Webcam')

        self.startBtn = QPushButton(self)
        self.startBtn.setText("Start")
        self.startBtn.clicked.connect(self.start)

        # create a vertical box layout and add the two labels
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addWidget(self.textLabel)
        vbox.addWidget(self.startBtn)
        # set the vbox layout as the widgets layout
        self.setLayout(vbox)

    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.display_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def host(self):
        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)

    def client(self):
        self.update_image()

if __name__=="__main__":
    app = QApplication(sys.argv)
    a = Client()
    a.show()
    sys.exit(app.exec_())
