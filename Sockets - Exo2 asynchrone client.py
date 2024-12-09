import socket, sys, threading

def arret(x): #fonction d'arret du client
    if x == 0:
        print("[INFO] Déconnexion au serveur.")
    elif x == 1:
        print("[INFO] Arrêt client et serveur.")
    endclient.set()


def envoi(): #envoi de message
    while True:
        x = None
        try:
            message = input("[CLIENT] > ")
            x = message.lower()
            if x == "bye":
                client.send("bye".encode('utf-8'))
                x = 0
                break
            elif x == "arret":
                client.send("arret".encode('utf-8'))
                x = 1
                break
            else:
                client.send(message.encode('utf-8'))
        except:
            print("[INFO] Problème lors de l'envoi.")
            break
    if x == 0 or x == 1:
        arret(x)
    

def recep(): #reception de message
    while True:
        x = None
        try:
            message = client.recv(1024).decode('utf-8')
            print(f"\n[SERVEUR] > {message}\n[CLIENT] > ", end="") #impression du message reçu, puis retour à la saisie.
            x = message.lower()
            if x == "bye":
                x = 0
                break
            elif x == "arret":
                x = 1
                break
        except:
            print("[INFO] Une erreur est survenue")
            break
    if x == 0 or x == 1:
        arret(x)


if __name__ == "__main__":
    print("[INFO] Démarrage du client.")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(("127.0.0.1", 8123))
    except:
        print("[INFO] Erreur lors de la connexion au serveur")
        sys.exit()
    print("[INFO] Client connecté au serveur")
    thread_envoi = threading.Thread(daemon=True, target=envoi)
    thread_recep = threading.Thread(daemon=True, target=recep)
    endclient = threading.Event() #déclarationd d'un déclancheur
    thread_envoi.start()
    thread_recep.start()
    endclient.wait() #attente du déclancheur
    client.close() #terminaison propre de la connexion
    sys.exit() #terminaison du programme