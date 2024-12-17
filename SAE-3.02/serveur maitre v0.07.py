import socket, threading, sys
def Console():
    """
    fonction de gestion de la console du serveur maître./
    """
    print("[CONSOLE] /help pour la liste des commandes")
    while not fin.is_set():
        ack = False
        commande = input("")
        if commande.lower() == '/help':
            ack = True
            print("[HELP] /stop : arrêt complet du serveur")
            print("[HELP] /server list : liste des serveurs esclaves connectés")
            print("[HELP] /kick server all : Déconnecte tous les serveurs esclaves")
            print("[HELP] /kick server [ip] [port] : Déconnecte le serveur esclave à l'adresse renseignée")
        if commande.lower() == '/server list':
            ack = True
            if len(liste_serveur) == 0:
                print("[CONSOLE] Aucun serveur esclave est connecté")
            for x in liste_serveur:
                print(f"[CONSOLE] connecté à l'addresse {x[1][0]}:{x[1][1]}")
        if commande.lower() == '/stop':
            ack = True
            print("[CONSOLE] Arrêt complet du serveur.")
            fin.set()
        if commande[:12].lower() == '/kick server':
            if commande[-3:].lower() == 'all':
                ack = True
                for x in liste_serveur:
                    print(f"[CONSOLE] {x[1][0]}:{x[1][1]} déconnecté")
                    x[0].close()
                    liste_serveur.remove(x)
            else:
                ack = True
                args = commande[13:].lower()
                args = args.split(" ")
                try:
                    args[1] = int(args[1])
                except:
                    print("[ERREUR] Port spécifié incorrect")
                t = False
                for x in liste_serveur:
                    if (x[1][0] == args[0]) and (x[1][1] == args[1]):
                        print(f"[CONSOLE] {args[0]}:{args[1]} déconnecté")
                        t = True
                        x[0].close()
                        liste_serveur.remove(x)
                    if t == False:
                        print("[ERREUR] Couple IP/PORT non trouvé")
        if ack == False:
            print("[CONSOLE] Commande inconnue.")
        

def AcceptClient():
    """
    fonction de gestion des connexions clientes entrant.
    """
    while not fin.is_set():
        try:
            conn, addr = client.accept()
            liste_client.append([conn, addr[0], addr[1]])
        except socket.timeout:
            continue
        except Exception as e:
            print(e)
            break
    fin.set()

def AcceptServeur():
    """
    fonction de gestion des connexions serveurs esclaves entrantes
    structure d'une indentation de liste_serveur : [[connexion], [addresse, port], [java, status, vers], [gcc, status, vers], [python, status, vers]]
    """
    while not fin.is_set():
        try:
            conn, addr = serveur.accept()
            langages = conn.recv(1024).decode("utf-8") #reception du résultat des tests du serveur esclave
            x = langages.split(',')
            if x[3] == 'None':
                x[3] = None
            if x[6] == 'None':
                x[6] = None
            if x[9] == 'None':
                x[9] = None
            liste_serveur.append([conn, [addr[0], addr[1]], [x[1], bool(x[2]), x[3]], [x[4], bool(x[5]), x[6]], [x[7], bool(x[8]), x[9]]])
            for x in liste_serveur:
                if x[0] == conn:
                    print(f"[INFO] Serveur esclave connecté à l'addresse {x[1][0]}:{x[1][1]}")
        except socket.timeout:
            continue
        except Exception as e:
            print(e)
            break
    fin.set()

if __name__ == "__main__":
    print("[INFO] Initialisation.")
    """
    création de 2 sockets client et serveur pour éviter les confusions et faciliter la gestion
    """
    try:
        serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serveur.bind(("127.0.0.1", 3218))
        serveur.settimeout(1)
        x = None
        while True:
            try:
                #x = int(input("[SETTINGS] Nombre de serveur esclave maximal souhaité > "))
                x = 2
                if x <= 0 :
                    print("[ERREUR] La valeur ne peut être nulle ou négative.")
                else:
                    break
            except :
                print("[ERREUR] La valeur entrée est incorrect")
                continue
        serveur.listen(x)

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.bind(("127.0.0.1", 8123))
        client.settimeout(1)
        while True:
            try:
                #x = int(input("[SETTINGS] Nombre de connexion client maximal souhaité > "))
                x = 2
                if x <= 0 :
                    print("[ERREUR] La valeur ne peut être nulle ou négative.")
                else:
                    break
            except :
                print("[ERREUR] La valeur entrée est incorrect")
                continue
        client.listen(x)
    except OSError:
        print("[ERREUR] impossible d'initialiser le socket, pool IP/PORT déjà utilisé par un autre programme.")
        sys.exit()
    
    print("[INFO] Serveur initialisé, en attente de connexion.")
    liste_client, liste_serveur = [], [] # création d'une liste référence qui contiendra les différentes informations des connexions.
    thAC = threading.Thread(daemon=True, target=AcceptClient)
    thAS = threading.Thread(daemon=True, target=AcceptServeur)
    fin = threading.Event() #création d'un event, qui une fois déclanché, coordonnera les différents thread pour tout stopper proprement
    thAC.start()
    thAS.start()

    thCONS = threading.Thread(daemon=True, target=Console) #thread pour la console du serveur
    thCONS.start()

    fin.wait() # attente du déclanchement de l'arrêt.
    sys.exit() # fermeture du programme