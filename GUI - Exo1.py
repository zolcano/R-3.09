#Ce code requiert la bibliothèque PyQT6 pour fonctionner.

from PyQt6.QtWidgets import *
import sys

class MainWindow(QMainWindow):    
    def __init__(self):
        super().__init__()

        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)

        lab = QLabel("Saisir votre nom")
        self.__text = QLineEdit("")
        ok = QPushButton("Ok")
        self.__label = QLabel("")
        quit = QPushButton("Quitter")
        grid.addWidget(lab, 0, 0) 
        grid.addWidget(self.__text, 1, 0)
        grid.addWidget(ok, 3, 0)
        grid.addWidget(self.__label, 4, 0)
        grid.addWidget(quit, 5, 0)

        ok.clicked.connect(self.__actionOk)
        quit.clicked.connect(self.__actionQuitter)
        self.setWindowTitle("Une première fenêtre")

    def __actionOk(self):
        self.__label.setText(f"Bonjour {self.__text.text()}")
    def __actionQuitter(self):
        QApplication.exit(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(300, 100)
    window.show()
    app.exec()