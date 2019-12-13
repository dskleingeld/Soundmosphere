import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QTimer, QRect
from PyQt5.QtGui import QFont

class App(QWidget):

    def __init__(self, pipe):
        super().__init__()
        self.title = 'Soundmosphere'
        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 140
        self.initUI(pipe)
    
    def initUI(self, pipe):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
        newfont = QFont("Sans", 14) 
        button = DragAndDrog(self, pipe)
        button.setGeometry(QRect(50, 20, 300, 100)) #(x, y, width, height)
        button.setFont(newfont)
        
        self.show()
    
class DragAndDrog(QLabel):
    
    def __init__(self, parent, pipe):
        super().__init__("Drop music folders here", parent)
        self.setAcceptDrops(True)
        self.new_file_tx = pipe

    def dragEnterEvent(self, e):
        text = e.mimeData().text()
        if text.startswith("file://"):
            path = text[7:].strip()
            if os.path.isdir(path):
                e.accept()
                return
        
        e.ignore()
    
    def dropEvent(self, e):
        path = e.mimeData().text()[7:].strip()
        self.new_file_tx.send(path)
        self.setText("Added a music folder")
        QTimer.singleShot(1500, self.resetLabel)

    def resetLabel(self):
        self.setText("Drop music folders here")