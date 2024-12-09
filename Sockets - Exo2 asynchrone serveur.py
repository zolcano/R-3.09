import socket, sys, threading

def init(): #initialisation d'une connexion
    global endconn, loop
    loop = True
    while loop:
        print("[INFO] Serveur en attente.")
        conn, address = serveur.accept()
        print(f"[INFO] connexion via {address[0]} : acceptée")
        thread_envoi = threading.Thread(daemon=True, target=envoi, args=[conn])
        thread_recep = threading.Thread(daemon=True, target=recep, args=[conn, address])
        endconn = threading.Event()
        thread_envoi.start()
        thread_recep.start()
        endconn.wait()

def arret(x : int): #gestion des arrets
    global loop
    if x == 0:
        print("\n[INFO] Arrêt client et serveur.")
        loop = False
        endconn.set()
        serveur.close() #fermeture propre du socket
        sys.exit() #terminaison du programme
    elif x == 1:
        print("\n[INFO] Déconnexion du client.")
        endconn.set()
        

def envoi(conn): #envoi de message
    while True:
        x = None
        try:
            message = input("[SERVEUR] > ")
            x = message.lower()
            if not message:
                break
            if x == "bye":
                conn.send(x.encode('utf-8'))
                x = 1
                break
            elif x == "arret":
                conn.send(x.encode('utf-8'))
                x = 0
                break
            else:
                conn.send(message.encode('utf-8'))
        except:
            print("[INFO] Une erreur est survenue. listen")
            x = 0
            break
    if x == 0 or x == 1:
        arret(x)


def recep(conn, address): #reception de message
    while True:
        x = None
        try:
            message = conn.recv(1024).decode('utf-8')
            x = message.lower()
            if not message:
                break
            if x == "bye":
                x = 1
                break
            elif x == "arret":
                x = 0
                break
            print(f"\n[{address[0]}] > {message}\n[SERVEUR] > ", end="") #impression du message reçu, puis retour à la saisie.
        except:
            print("[INFO] Une erreur est survenue.")
            break
    if x == 1 or x == 0:
        arret(x)


if __name__ == "__main__":
    print("[INFO] Démarrage du serveur.")
    serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serveur.bind(("127.0.0.1", 8123))
    serveur.listen(1)
    init()