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

        
        temp = QLabel("Température")
        self.__linedeg = QLineEdit("")
        self.__lab1 = QLabel("°C")

        
        conv = QLabel("Conversion")
        self.__linekel = QLineEdit("")
        self.__lab2 = QLabel("K")

        button = QPushButton("Convertir")
        self.__choice = QComboBox()
        self.__choice.addItems(["°C -> K","K -> °C"])
        self.__linekel.setReadOnly(True)

        help = QPushButton("?")

        grid.addWidget(temp, 0, 0) 
        grid.addWidget(self.__linedeg, 0, 1)
        grid.addWidget(self.__lab1, 0, 3)

        grid.addWidget(button, 1, 1)
        grid.addWidget(self.__choice, 1, 2)        

        grid.addWidget(conv, 2, 0)
        grid.addWidget(self.__linekel, 2, 1)
        grid.addWidget(self.__lab2, 2, 3)

        grid.addWidget(help, 3, 3)

        button.clicked.connect(self.__actionConvert)
        self.__choice.currentIndexChanged.connect(self.__actionChange)
        help.clicked.connect(self.__actionHelp)

        self.setWindowTitle("Conversion de température")

    def __actionChange(self):
        var = self.__lab1.text()
        self.__lab1.setText(self.__lab2.text())
        self.__lab2.setText(var)

    def __actionConvert(self):
        if self.__lab1.text() == "K":
            var = self.__linedeg.text()
            try :
                var = round(float(var) + 273.15,2)
            except :
                return
            var = str(var)
            self.__linekel.setText(var)
        else :
            var = self.__linedeg.text()
            try:
                var = round(float(var) - 273.15,2)
            except:
                return
            var = str(var)
            self.__linekel.setText(var)

    def __actionHelp(self):
        app = QMessageBox(self)
        app.setWindowTitle("Aide")
        app.setText("Conversion d'une température en Kelvin vers Celcius et inversement.")
        app.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(350, 100)
    window.show()
    app.exec()