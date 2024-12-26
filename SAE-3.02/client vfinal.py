import sys, os, socket, threading
from PyQt6.QtWidgets import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._file_path = ""

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
        self._Exec.clicked.connect(self._MExec)
        self._Info.clicked.connect(self._MInfo)
        self._Quit.clicked.connect(self._MQuit)

        self._Cons.setPlainText("[INFO] Fenêtre initialisée.")

    def _MQuit(self):
        """
        Methode de gestion d'arrêt du client.
        """
        if self._Conn.text() == 'Disconnect':
            self._MConn()
        self._Cons.append(f"[INFO] Fermeture du client.")
        QApplication.processEvents()
        QApplication.exit(0)

    def _MInfo(self):
        """
        Methode qui retourne le status du client
        """
        try:
            x, y = self._client.getpeername()
            self._Cons.append(f"[INFO] Connecté à l'adresse {x}:{y}")
        except:
            self._Cons.append("[INFO] Client non connecté.")    

    def _MConn(self):
        """
        Methode de gestion de la connexion au serveur maître.
        """
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
                    self._thECC = threading.Thread(daemon=True, target=self._MEcoute)
                    self._thECC.start()
                except Exception as e:
                    self._Cons.append(f"[ERREUR] Connexion impossible : {e}")
            
        elif self._Conn.text() == 'Disconnect':
            self._Cons.append(f"[INFO] Déconnexion au serveur.")
            self._client.send('/stop'.encode("utf-8"))
            self._client.close()
            self._Conn.setText("Connect")

    def _MFileS(self):
        """
        Methode de selection de fichier du client.
        """
        self._file_path, a = QFileDialog.getOpenFileName(self,"Sélectionnez un fichier", "", "C++ (*.cpp *.cc);;C (*.c);;Java (*.java);;Python (*.py)")
        if self._file_path:
            x = self._file_path.split('/')
            self._Cons.append(f"[FILE] Fichier : '{x[-1]}' sélectionné avec succès")
        else:
            self._Cons.append(f"[FILE] Interruption de la sélection de fichier.")

    def _MExec(self):
        try:
            self._client.getpeername()
            if self._file_path:
                file_size = os.path.getsize(self._file_path)
                x = self._file_path.split("/")
                self._Cons.append(f"[INFO] Traitement du fichier '{x[-1]}' en cour.")
                m = '/file' + ' ' + x[-1] + ' ' + str(file_size)
                self._client.send(m.encode("utf-8"))
                with open(self._file_path, "rb") as file:
                    while chunk := file.read(1024):
                        self._client.sendall(chunk)
            else:
                self._Cons.append("[ERREUR] Aucun fichier de selectionné.") 
        except :
            self._Cons.append("[ERREUR] Client non connecté.")   

    def _MEcoute(self):
        """
        Methode d'écoute dédié à la communication entre le client et le sevreur maître.
        """
        while True:
            try:
                message = self._client.recv(1024).decode("utf-8")
                message_split = message.split('/////')
                if not message:
                    continue
                print(message)
                if message == "/stop":
                    self._Cons.append("[INFO] Arrêt du serveur Maître, déconnexion automatique.")
                    self._client.close()
                    self._Conn.setText("Connect")
                if message == "/refus":
                    self._Cons.append("[ERREUR] Serveur complet.")
                    self._client.close()
                    self._Conn.setText("Connect")
                if message_split[0] == '/err':
                    self._Cons.append("[ERREUR] Une erreur est survenue :")
                    self._Cons.append(f"[ERREUR] {message_split[1]}.")
                if message == "/arret":
                    self._Cons.append("[INFO] Arrêt demandé par le serveur maître, deconnexion.")
                    self._client.close()
                    self._Conn.setText("Connect")
                if message_split[0] == '/out':
                    self._Cons.append("[INFO] Fichier correctement exécuté, affichage du résultat.")
                    self._Cons.append(f"###### Sortie : ######\n\n{message_split[1]}\n\n###################")
            except:
                break

    def closeEvent(self, a0):
        """
        Redéfinition de la methode closeEvent() pour la gestion de la déconnexion au serveur si le client est fermé brutalement.
        """
        if self._Conn.text() == 'Disconnect':
            self._MConn()
        return super().closeEvent(a0)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(450, 400)
    window.show()
    app.exec()