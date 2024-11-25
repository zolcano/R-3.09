#https://github.com/zolcano/R-3.09

import sys
from PyQt6.QtWidgets import *
from socket import *
class MainWindow(QMainWindow):
    def __init__(self):
        global arret
        super().__init__()
        self.__textarret = "Démarrage du serveur"
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)

        label1 = QLabel("Serveur")
        line1 = QLineEdit("0.0.0.0")
        label2 = QLabel("Port")
        line2 = QLineEdit("4200")
        label3 = QLabel("Nombre de clients maximum")
        line3 = QLineEdit("5")

        arret = QPushButton(self.__textarret)
        console = QTextEdit("test")
        console.setReadOnly(True)
        quit = QPushButton("Quitter")
        grid.addWidget(label1, 0, 0)
        grid.addWidget(line1, 0, 1)
        grid.addWidget(label2, 1, 0)
        grid.addWidget(line2, 1, 1)
        grid.addWidget(label3, 2, 0)
        grid.addWidget(line3, 2, 1)
        grid.addWidget(arret, 3, 0)
        grid.addWidget(console, 4, 0)
        grid.addWidget(quit, 5, 0)

        quit.clicked.connect(self.__actionQuitter)
        arret.clicked.connect(self.__demarrage)

    def __actionQuitter(self):
        QCoreApplication.exit(0)

    def __demarrage(self):
        global arret, x
        if x == 0:
            arret.setText("Arrêt du serveur")
            x = 1
            #server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #server_socket.bind(('0.0.0.0', 4200))
            #server_socket.listen(1)
        else :
            arret.setText("Démarrage du serveur")
            x = 0
            #server_socker.close()


    def __accept(self):

        return

if __name__ == '__main__':
    x = 0
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


