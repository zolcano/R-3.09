import socket, threading, sys, os

def Console():
    """
    fonction de gestion de la console et des commandes du serveur maître.
    """
    print("[CONSOLE] /help pour la liste des commandes.")
    while not fin.is_set():
        ack = False
        commande = input("")
        if commande.lower() == '/help':
            ack = True
            print("[HELP] /info : renvoie l'ip et le port utilisé par le.s socket.s .")
            print("[HELP] /stop : arrêt complet du serveur maître.")
            print("[HELP] /{server|client} list : liste des serveurs esclaves ou client connectés, ainsi que les compilateurs/interpreteur présents si serveur.")
            print("[HELP] /kick {server|client} all : Déconnecte tous les serveurs esclave ou client.")
            print("[HELP] /kick {server|client} [ip] [port] : Déconnecte le serveur esclave ou client à l'adresse renseignée.")

        if commande.lower() == "/info":
            ack = True
            sIP, sPORT = serveur.getsockname()
            cIP, cPORT = client.getsockname()
            print(f"[CONSOLE] le socket serveur utilise le couple IP/PORT suivant : {sIP}:{sPORT}.")
            print(f"[CONSOLE] le socket client utilise le couple IP/PORT suivant : {cIP}:{cPORT}.")

        if commande.lower() == '/server list':
            ack = True
            if len(liste_serveur) == 0:
                print("[CONSOLE] Aucun serveur esclave est connecté.")
                continue
            info = ""
            for x in liste_serveur:
                info = ""
                if x[2][1] == True:
                    info += '[' + x[2][0] + ' v' + x[2][2] + ']'
                if x[3][1] == True:
                    info += '[' + x[3][0] + ' v' + x[3][2] + ']'
                if x[4][1] == True:
                    info += '[' + x[4][0] + ' v' + x[4][2] + ']'
                print(f"[CONSOLE] {x[1][0]}:{x[1][1]} > {info}")

        if commande.lower() == '/client list':
            ack = True
            if len(liste_client) == 0:
                print("[CONSOLE] Aucun client est connecté.")
            for x in liste_client:
                print(f"[CONSOLE] client connecté à l'addresse {x[1][0]}:{x[1][1]}.")
                
        if commande.lower() == '/stop':
            ack = True
            print("[CONSOLE] Arrêt complet du serveur.")
            fin.set()

        if commande[:12].lower() == '/kick server':
            if commande[-3:].lower() == 'all':
                ack = True
                for x in liste_serveur[::-1]:
                    try:
                        x[0].send('/arret'.encode("utf-8"))
                        print(f"[CONSOLE] serveur esclave {x[1][0]}:{x[1][1]} déconnecté.")
                        x[0].close()
                    except:
                        print(f"[ERREUR] serveur esclave {x[1][0]}:{x[1][1]} introuvable, suppression.")
                    liste_serveur.remove(x)
            else:
                ack = True
                args = commande[13:].lower()
                args = args.split(" ")
                try:
                    args[1] = int(args[1])
                except:
                    print("[ERREUR] Port spécifié incorrect.")
                t = False
                for x in liste_serveur:
                    if (x[1][0] == args[0]) and (x[1][1] == args[1]):
                        t = True
                        try:
                            x[0].send('/arret'.encode("utf-8"))
                            print(f"[CONSOLE] serveur esclave {args[0]}:{args[1]} déconnecté.")
                            x[0].close()
                        except:
                            print("[ERREUR] serveur esclave introuvable, suppression.")
                        liste_serveur.remove(x)
                    if t == False:
                        print("[ERREUR] Couple IP/PORT non trouvé.")
            
        if commande[:12].lower() == '/kick client':
            if commande[-3:].lower() == 'all':
                ack = True
                for x in liste_client[::-1]:
                    try:
                        x[0].send('/arret'.encode("utf-8"))
                        print(f"[CONSOLE] client {x[1][0]}:{x[1][1]} déconnecté.")
                        x[0].close()
                    except:
                        print(f"[ERREUR] client {x[1][0]}:{x[1][1]} introuvable, suppression.")
                    liste_client.remove(x)
            else:
                ack = True
                args = commande[13:].lower()
                args = args.split(" ")
                try:
                    args[1] = int(args[1])
                except:
                    print("[ERREUR] Port spécifié incorrect.")
                t = False
                for x in liste_client:
                    if (x[1][0] == args[0]) and (x[1][1] == args[1]):
                        t = True
                        try:
                            x[0].send('/arret'.encode("utf-8"))
                            print(f"[CONSOLE] client {args[0]}:{args[1]} déconnecté.")
                            x[0].close()
                        except:
                            print(f"[ERREUR] client introuvable, suppression.")
                        liste_client.remove(x)
                    if t == False:
                        print("[ERREUR] Couple IP/PORT non trouvé.")

        if ack == False:
            print("[CONSOLE] Commande inconnue.")
        
def Ecoute(conn, addr):
    """
    Fonction qui initialise un port d'écoute à chaque connexion au serveur maître.
    """
    while not fin.is_set():
        try:
            message = conn.recv(1024).decode("utf-8")
            if not message:
                continue
            message_split = message.split(" ")

            if message == '/stop':
                for x in liste_serveur:
                    if conn == x[0]:
                        print(f"[INFO] Le serveur esclave à l'addresse {addr[0]}:{addr[1]} s'est déconnecté.")
                        liste_serveur.remove(x)
                for x in liste_client:
                    if conn == x[0]:
                        print(f"[INFO] Le client à l'addresse {addr[0]}:{addr[1]} s'est déconnecté.")
                        liste_client.remove(x)
                conn.close()
                break

            if message_split[0] == '/cpu':
                for x in liste_serveur:
                    if x[0] == conn:
                        if len(x) == 6:
                            x[5] = round(float(message_split[1]),2)
                        else:
                            x.append(round(float(message_split[1]),2))
                        continue

            if message_split[0] == '/file':
                extension = message_split[1].split('.')
                extension = extension[1]
                file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), message_split[1])
                with open(file_path, "wb") as file:
                    received_size = 0
                    while received_size < int(message_split[2]):
                        data = conn.recv(1024)
                        file.write(data)
                        received_size += len(data)
                    print(f"[INFO] {received_size} octet.s correctement reçu du client {addr[0]}:{addr[1]}.")
                temp = []
                if extension == 'java':
                    for x in liste_serveur:
                        if x[2][1] == True:
                                temp.append([x[0],x[5]])
                    target = [None, 100]
                    for x in temp:
                        print(x)
                        if x[1] < temp[1]:
                            target = x
                    continue

                if (extension == 'cc') or (extension == 'cpp') or (extension == 'c'):
                    for x in liste_serveur:
                        if x[3][1] == True:
                                temp.append([x[0],x[5]])
                    target = [None, 100]
                    for x in temp:
                        print(x)
                        if x[1] < temp[1]:
                            target = x
                    continue

                if extension == 'py':
                    for x in liste_serveur:
                        if x[4][1] == True:
                                temp.append([x[0],x[5]])
                    target = [None, 100]
                    for x in temp:
                        print(x)
                        if x[1] < temp[1]:
                            target = x
                    continue
        except:
            break
    return

def AcceptClient():
    """
    fonction de gestion des connexions clientes entrant.
    """
    while not fin.is_set():
        try:
            conn, addr = client.accept()
            liste_client.append([conn, [addr[0], addr[1]]])
            for x in liste_client:
                if x[0] == conn:
                    print(f"[INFO] Client connecté à l'addresse {x[1][0]}:{x[1][1]}.")
            thECC = threading.Thread(daemon=True, target=Ecoute, args=[conn, addr]) #initialisation d'un thread d'écoute propre à la connexion
            thECC.start()
        except socket.timeout:
            continue
        except Exception as e:
            print(e)
            break
    fin.set()

def AcceptServeur():
    """
    fonction de gestion des connexions serveurs esclaves entrantes
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
                    print(f"[INFO] Serveur esclave connecté à l'addresse {x[1][0]}:{x[1][1]}.")
            thECC = threading.Thread(daemon=True, target=Ecoute, args=[conn, addr]) #initialisation d'un thread d'écoute propre à la connexion
            thECC.start()
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
    structure d'une indentation de liste_serveur : [[connexion], [addresse, port], [java, status, vers], [c/c++, status, vers], [python, status, vers], [cpu]]
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
                print("[ERREUR] La valeur entrée est incorrect.")
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
                print("[ERREUR] La valeur entrée est incorrect.")
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
    thCONS = threading.Thread(daemon=True, target=Console) #initialisation d'un thread pour la console
    thCONS.start()

    fin.wait() # attente du déclanchement de l'arrêt.
    try:
        for x in liste_serveur:
            x[0].send('/stop'.encode("utf-8"))
        for x in liste_client:
            x[0].send('/stop'.encode("utf-8"))
    except Exception as e:
        print(f"[ERREUR] {e}.")
    sys.exit() # fermeture du programme