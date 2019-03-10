#!/usr/local/bin/python3

from PyQt5.QtWidgets import QErrorMessage

class ErrorDialog(QErrorMessage):
    def __init__(self, parent, message):
        super().__init__()
        self.parent = parent
        self.message = message
        self.initUI()

    def initUI(self):
        errorDialog = QErrorMessage(self.parent)
        errorDialog.showMessage(self.message)