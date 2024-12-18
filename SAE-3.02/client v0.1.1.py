import sys, socket, threading
from PyQt6.QtWidgets import *

class MainWindow(QMainWindow):    
    def __init__(self):
        super().__init__()

        widget = QWidget() #définition de l'objet de la classe QWidget.
        self.setCentralWidget(widget) #définition en objet central
        grid = QGridLayout()
        widget.setLayout(grid) #définition du layout de l'objet
        self.setWindowTitle("Client")
        
        self._labIP = QLineEdit("127.0.0.1")
        self._labIP.setPlaceholderText("IP")
        self._labPORT = QLineEdit("8123")
        self._labPORT.setPlaceholderText("PORT")
        self._Cons = QTextEdit()
        self._Cons.setReadOnly(True)
        self._Conn = QPushButton("Connect")
        self._FileS = QPushButton("Select file")
        self._Exec = QPushButton("Execute")
        self._Info = QPushButton("Info")
        self._Quit = QPushButton("Quit")

        grid.addWidget(self._labIP, 0, 0, 1, 2) 
        grid.addWidget(self._labPORT, 0, 2)
        grid.addWidget(self._Conn, 0, 3)
        grid.addWidget(self._FileS, 1, 3)
        grid.addWidget(self._Exec, 2, 3)

        grid.addWidget(self._Info, 4, 3)
        grid.addWidget(self._Quit, 5, 3)
        grid.addWidget(self._Cons, 1, 0, 5, 3)

        self._Conn.clicked.connect(self._MConn)
        self._FileS.clicked.connect(self._MFileS)
        self._Info.clicked.connect(self._MInfo)
        self._Quit.clicked.connect(self._MQuit)

        self._Main()

    def _MQuit(self):
        QApplication.exit(0)

    def _MInfo(self):
        try:
            x, y = self._client.getpeername()
            self._Cons.append(f"[INFO] Connecté à l'adresse {x}:{y}")
        except:
            self._Cons.append("[INFO] Client non connecté.")    

    def _MConn(self):
        if self._Conn.text() == 'Connect':
            x = self._labIP.text()
            check = x.split(".")
            ack = True
            if len(check) != 4:
                self._Cons.append(f"[ERREUR] Format de l'adresse IP incorrecte.")
                ack = False
            try:
                y = int(self._labPORT.text())
            except:
                self._Cons.append(f"[ERREUR] Port incorrect.")
                ack = False
            if ack == True:
                self._Cons.append(f"[INFO] Connexion au serveur à l'addresse {x}:{y} ...")
                """"""
                QApplication.processEvents()
                try:
                    self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self._client.connect((x, y))
                    self._Cons.append(f"[INFO] Connecté avec succès.")
                    self._Conn.setText("Disconnect")
                except Exception as e:
                    self._Cons.append(f"[ERREUR] Connexion impossible : {e}")
            
        elif self._Conn.text() == 'Disconnect':
            self._Cons.append(f"[INFO] Déconnexion au serveur.")
            self._client.close()
            self._Conn.setText("Connect")

    def _MFileS(self):
        return

    def _MEcoute(self):
        while True:
            try:
                message = self._client.recv(1024).decode("utf-8")
                if not message:
                    continue
                if message == "/stop":
                    self._Cons.append("[INFO] Arrêt du serveur Maître, déconnexion automatique.")
                    self._client.close()
                    self._Conn.setText("Connect")
                if message == "/arret":
                    self._Cons.append("[INFO] Arrêt demandé par le serveur maître, deconnexion.")
                    self._client.close()
                    self._Conn.setText("Connect")
            except:
                break

    def _Main(self):
        self._Cons.setPlainText("[INFO] Fenêtre initialisée.")
        thECC = threading.Thread(daemon=True, target=self._MEcoute)
        thECC.start()

        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(400, 350)
    window.show()
    app.exec()