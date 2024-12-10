import socket, sys, threading, time

def init(): #initialisation d'une connexion
    global event, loop
    print("[INFO] Serveur initialisé, en attente de connexion.")
    loop = True #contrôle de la boucle
    while loop:
        try:
            event = threading.Event()
            conn, address = serveur.accept()
            clients.append(conn)
            print(f"[INFO] connexion via {address[0]}:{address[1]} acceptée")
            thread_chat = threading.Thread(daemon=True, target=chat, args=[conn, address])
            thread_chat.start()
            event.set() #déclanchement de event si un arret est demandé
        except socket.timeout:
            continue

def arret(x : int, conn, address): #gestion des arrets
    global loop
    if x == 0:
        print("\n[INFO] Arrêt du serveur et clients")
        loop = False
        event.wait() #attente d'arrêt d'écoute de connexion
        time.sleep(1)
        serveur.close() #fermeture propre du socket
        sys.exit() #terminaison du programme
    elif x == 1:
        clients.remove(conn)
        print(f"\n[INFO] Déconnexion de {address[0]}:{address[1]}.")
        
def chat(conn, address): #gestion de la discussion
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
                for x in clients:
                    if x != conn :
                        x.send(message.encode('utf-8'))
                x = 0
                break
            message = address[0] + ":" + str(address[1]) + " > " + message
            for x in clients:
                if x != conn:
                    x.send(message.encode('utf-8'))
            print(f"[LOG] {message}")
        except:
            print("[INFO] Une erreur est survenue.")
            break
    if x == 1 or x == 0:
        arret(x, conn, address)


if __name__ == "__main__":
    print("[NOTE] plusieurs clients sont requis au serveur de discussion")
    print("[NOTE] commande bye pour une deconnexion de client, arret pour stop le serveur")
    clients = []
    print("[INFO] Démarrage du serveur.")
    serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serveur.bind(("127.0.0.1", 8123))
    serveur.settimeout(1)
    serveur.listen(5)
    init()