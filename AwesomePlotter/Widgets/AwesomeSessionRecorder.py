#!/usr/local/bin/python3

from PyQt5.QtWidgets import QWidget

class AwesomeSessionRecorder(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.show()