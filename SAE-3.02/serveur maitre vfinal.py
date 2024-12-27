import socket, threading, sys, os

def Console():
    """
    fonction de gestion de la console et des commandes du serveur maître.
    /help pour afficher la liste des commandes dans le terminal
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
                if len(x) == 6:
                    print(f"[CONSOLE] {x[1][0]}:{x[1][1]}, {x[5]}%CPU > {info}")
                else:
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
            commande_split = commande.split(' ')
            if commande[2].lower() == 'all':
                ack = True
                for x in liste_serveur[::-1]:
                    try:
                        x[0].send('/arret'.encode("utf-8"))
                        print(f"[CONSOLE] serveur esclave {x[1][0]}:{x[1][1]} déconnecté.")
                        x[0].close()
                    except:
                        print(f"[ERREUR] serveur esclave {x[1][0]}:{x[1][1]} introuvable, suppression.")
                    liste_serveur.remove(x)
                    continue
            elif len(commande_split) == 4:
                ack = True
                aq = False
                try:
                    commande_split[3] = int(commande_split[3])
                except:
                    print("[ERREUR] Port spécifié incorrect.")
                try:
                    for x in liste_serveur:
                        if (x[1][0] == commande_split[2]) and (x[1][1] == commande_split[3]):
                            aq = True
                            x[0].send('/arret'.encode("utf-8"))
                            print(f"[CONSOLE] serveur esclave {x[1][0]}:{x[1][1]} déconnecté.")
                            x[0].close()
                            liste_serveur.remove(x)
                            continue
                    if aq == False:
                        print("[ERREUR] Couple IP/PORT non trouvé.")
                        continue
                except:
                    print("[ERREUR] serveur esclave introuvable, suppression.")
                    liste_serveur.remove(x)
                    continue
            
        if commande[:12].lower() == '/kick client':
            commande_split = commande.split(' ')
            if commande[2].lower() == 'all':
                ack = True
                for x in liste_client[::-1]:
                    try:
                        x[0].send('/arret'.encode("utf-8"))
                        print(f"[CONSOLE] client {x[1][0]}:{x[1][1]} déconnecté.")
                        x[0].close()
                    except:
                        print(f"[ERREUR] client {x[1][0]}:{x[1][1]} introuvable, suppression.")
                    liste_client.remove(x)
                    continue
            else:
                ack = True
                aq = False
                try:
                    commande_split[3] = int(commande_split[3])
                except:
                    print("[ERREUR] Port spécifié incorrect.")
                try:
                    for x in liste_client:
                        if (x[1][0] == commande_split[2]) and (x[1][1] == commande_split[3]):
                            aq = True
                            x[0].send('/arret'.encode("utf-8"))
                            print(f"[CONSOLE] client {x[1][0]}:{x[1][1]} déconnecté.")
                            x[0].close()
                            liste_client.remove(x)
                            continue
                    if aq == False:
                        print("[ERREUR] Couple IP/PORT non trouvé.")
                        continue
                except:
                    print(f"[ERREUR] client introuvable, suppression.")
                    liste_client.remove(x)
                    continue

        if ack == False:
            print("[CONSOLE] Commande inconnue.")
        
def Ecoute(conn, addr):
    """
    Fonction qui initialise un port d'écoute à chaque connexion au serveur maître.
    
    Protocole : 
    /stop = déconnexion distante
    /cpu = reception d'information de charge cpu
    /file = réception de fichier
    /err = réception d'erreur serveur esclave.
    """
    while not fin.is_set():
        try:
            message = conn.recv(1024).decode("utf-8")
            if not message:
                continue
            message_split = message.split(" ") #séparation des informations envoyés en un seul message si necessaire.

            if message == '/stop':
                for x in liste_serveur: # suppression de l'objet client ou serveur dans la liste respective si déconnexion.
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
                        if len(x) == 6: #par défaut, l'index 6 de l'objet serveur de la liste n'existe pas.
                            x[5] = round(float(message_split[1]),2)
                        else:
                            x.append(round(float(message_split[1]),2)) #remplacement par la nouvelle valeur si l'index existe déjà.
                        continue

            if message_split[0] == '/file': #envoi de fichier par un client.
                print("\n[INFO] Début de session.")
                extension = message_split[1].split('.')
                extension = extension[1]
                try:
                    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), message_split[1]) #écriture du fichier dans le même répertoire le terminal d'execution du serveur maître
                    with open(file_path, "wb") as file:
                        received_size = 0
                        while received_size < int(message_split[2]):
                            data = conn.recv(1024)
                            file.write(data)
                            received_size += len(data)
                        print(f"[INFO] {received_size} octet.s correctement reçu du client {addr[0]}:{addr[1]}.") #impression dans la console du serveur
                except Exception as e:
                    print(f"[ERREUR] {e}")
                    try:
                        msg = '/err' + '/////' + e
                        conn.send(msg.encode("utf-8"))
                        continue
                    except:
                        print(f"[ERREUR] connexion client {addr[0]}:{addr[1]} perdue")
                        for x in liste_client:
                            if conn == x[0]:
                                liste_client.remove(x)
                        continue

                temp = [] #liste temporaire pour stocker les serveurs esclave ayant le bon compilateur/executeur installé dans son environnement.
                if extension == 'java':
                    print('[INFO] Fichier .java détecté.')
                    for x in liste_serveur:
                        if x[2][1] == True:
                                temp.append([x[0],x[5],x[1][0],x[1][1]])
                if (extension == 'cc') or (extension == 'cpp') or (extension == 'c'):
                    print('[INFO] Fichier c ou c++ détecté.')
                    for x in liste_serveur:
                        if x[3][1] == True:
                                temp.append([x[0],x[5],x[1][0],x[1][1]])
                if extension == 'py':
                    print('[INFO] Fichier .py détecté.')
                    for x in liste_serveur:
                        if x[4][1] == True:
                                temp.append([x[0],x[5],x[1][0],x[1][1]])
                
                if len(temp) == 0:
                    try:
                        print(f"[ERREUR] Aucun serveur esclave connecté est capable de répondre à la demande du client.")
                        print("[INFO] Fin de session.\n")
                        msg = '/err' + '/////' + f"aucun serveur capable de traiter une demande en .{extension} est connecté"
                        conn.send(msg.encode("utf-8"))
                        continue
                    except:
                        print(f"[ERREUR] connexion client {addr[0]}:{addr[1]} perdue")
                        for x in liste_client:
                            if conn == x[0]:
                                liste_client.remove(x)
                        continue

                target = temp[0] #selection du serveur ayant le moins de charge à l'instant de recherche.
                for x in temp:
                    if x[1] < target[1]:
                        target = x
                
                for x in liste_serveur: #impression dans la console du serveur
                    if target[0] == x[0]:
                        print(f"[INFO] Serveur esclave selectionné : {x[1][0]}:{x[1][1]}.")
                print(f"[INFO] Envoi du fichier au serveur cible.")

                x = 0
                while x < 5:
                    try: #initialisation de l'envoi au serveur esclave pour l'execution du fichier.
                        m = '/file' + ' ' + message_split[1] + ' ' + str(message_split[2]) + ' ' + addr[0] + ' ' + str(addr[1])
                        target[0].send(m.encode('utf-8'))
                        with open(message_split[1], "rb") as file:
                            while chunk := file.read(1024):
                                target[0].sendall(chunk)
                        print(f"[INFO] {message_split[2]} octet.s correctement envoyé.")
                        x = 5
                    except Exception as e:
                        print(f"[ERREUR] Echec de l'envoi : {e}.")
                        x += 1
                        if x < 5:
                            print("[INFO] Nouvelle tentative d'envoi.")
                        else:
                            print("[ERREUR] Deconnexion forcée du serveur esclave.")
                            try:
                                target[0].send('/arret'.encode('utf-8'))
                                for x in liste_serveur:
                                    print(f"[CONSOLE] serveur esclave {x[1][0]}:{x[1][1]} déconnecté.")
                                    if target[0] == x:
                                        liste_serveur.remove(x)
                                    msg = '/err' + "/////" + 'Une erreur est survenue. Réessayez.'
                                    try:
                                        conn.send(msg.encode("utf-8"))
                                        continue
                                    except:
                                        print(f"[ERREUR] connexion client {addr[0]}:{addr[1]} perdue")
                                        for x in liste_client:
                                            if conn == x[0]:
                                                liste_client.remove(x)
                                        continue
                            except:
                                print(f"[CONSOLE] serveur esclave {x[1][0]}:{x[1][1]} déconnecté.")
                                for x in liste_serveur:
                                    if target[0] == x:
                                        liste_serveur.remove(x)
                                msg = '/err' + "/////" + 'Une erreur est survenue. Réessayez.'
                                try:
                                    conn.send(msg.encode("utf-8"))
                                    continue
                                except:
                                    print(f"[ERREUR] connexion client {addr[0]}:{addr[1]} perdue")
                                    for x in liste_client:
                                        if conn == x[0]:
                                            liste_client.remove(x)
                                    continue
            
            if message_split[0] == '/err':
                try:
                    message_split[2] = message_split[2].replace("#include","")
                except:
                    pass
                    print(message_split)
                for x in liste_client:
                    if x[1][0] == message_split[1] and x[1][1] == message_split[2]:
                        try:
                            conn.send('/err/////Erreur liée au traitement du fichier, réessayez'.encode("utf-8"))
                            continue
                        except:
                            print(f"[ERREUR] connexion client {addr[0]}:{addr[1]} perdue")
                            for x in liste_client:
                                if conn == x[0]:
                                    liste_client.remove(x)
                            continue

            if message[:4] == '/out':
                output = message.split("/////")
                ip = output[0].split(" ")
                port = int(ip[2])
                ip = ip[1]
                output = output[1]
                try:
                    ack = False
                    for x in liste_client:
                        if (x[1][0] == ip) and (x[1][1] == port):
                            print(f'###### Sortie {ip}:{port}: ######\n\n',output,'\n\n#####################################')
                            print("[INFO] Envoi du résultat au client.")
                            output = '/out' + '/////' + output
                            x[0].send((output).encode("utf-8"))
                            print("[INFO] Résultat envoyé.")
                            ack = True
                        if ack == False:
                            print("[ERREUR] Client déconnecté. Abandon de la session.")
                except:
                    print(f"[ERREUR] connexion client {addr[0]}:{addr[1]} perdue")
                    for x in liste_client:
                        if conn == x[0]:
                            liste_client.remove(x)
                    continue
                print("[INFO] Fin de session.\n")
        except:
            break
    return

def AcceptClient(limite : int):
    """
    fonction de gestion des connexions clientes entrant.
     structure d'une indentation de liste_client : [[connexion], [addresse, port]]
    """
    while not fin.is_set():
        try:
            conn, addr = client.accept() #acceptation des clients
            if len(liste_client) < limite:
                liste_client.append([conn, [addr[0], addr[1]]])
                for x in liste_client:
                    if x[0] == conn:
                        print(f"[INFO] Client connecté à l'addresse {x[1][0]}:{x[1][1]}.") #affichage des informations dans la console
                thECC = threading.Thread(daemon=True, target=Ecoute, args=[conn, addr]) #initialisation d'un thread d'écoute propre à la connexion
                thECC.start()
            else:
                print(f"[WARNING] Tentative de connexion client via {addr[0]}:{addr[1]}.")
                print(f"[WARNING] Serveur maître complet. Refus.")
                conn.send('/refus'.encode("utf-8"))
        except socket.timeout:
            continue
        except:
            break
    fin.set()

def AcceptServeur(limite : int):
    """
    fonction de gestion des connexions serveurs esclaves entrantes
    structure d'une indentation de liste_serveur : [[connexion], [addresse, port], [java, status, vers], [c/c++, status, vers], [python, status, vers], [cpu]]
    """
    while not fin.is_set():
        try:
            conn, addr = serveur.accept() #acceptation des serveurs esclaves
            if len(liste_serveur) < limite:
                langages = conn.recv(1024).decode("utf-8") #reception puis tri du résultat des tests du serveur esclave sur son environnement d'exécution
                x = langages.split(',')
                if x[3] == 'None':
                    x[3] = None
                if x[6] == 'None':
                    x[6] = None
                if x[9] == 'None':
                    x[9] = None
                if x[2] == 'False':
                    x[2] = False
                else:
                    x[2] = True
                if x[5] == 'False':
                    x[5] = False
                else:
                    x[5] = True
                if x[8] == 'False':
                    x[8] = False
                else:
                    x[8] = True
                liste_serveur.append([conn, [addr[0], addr[1]], [x[1], x[2], x[3]], [x[4], x[5], x[6]], [x[7], x[8], x[9]]]) #stockage des informations dans liste_serveur
                for x in liste_serveur:
                    if x[0] == conn:
                        print(f"[INFO] Serveur esclave connecté à l'addresse {x[1][0]}:{x[1][1]}.") #affichage des informations dans la console
                thECC = threading.Thread(daemon=True, target=Ecoute, args=[conn, addr]) #initialisation d'un thread d'écoute propre à la connexion
                thECC.start()
            else:
                print(f"[WARNING] Tentative de connexion serveur via {addr[0]}:{addr[1]}.")
                print(f"[WARNING] Serveur maître complet. Refus.")
                conn.send('/refus'.encode("utf-8"))
        except socket.timeout:
            continue
        except:
            break
    fin.set()

if __name__ == "__main__":
    print("[INFO] Initialisation.")
    """
    execution du programme seulement si celui-ci est exécuté dans un terminal.
    """
    try: #création de 2 sockets client et serveur pour éviter les confusions et faciliter la gestion
        ack = False
        while ack == False: #ip du serveur à rentrer
            ip = input("[SETTINGS] Entrez l'adresse ip du serveur maître > ")
            ipcheck = ip.split(".")
            try:
                if len(ipcheck) == 4:
                    for x in ipcheck:
                            y = int(x)
                else:
                    continue
                ack = True
            except:
                print("[ERREUR] Format d'adresse IP incorrect")
        serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ack = False
        while ack == False:
            try:
                porta = int(input("[SETTINGS] Entrez le port de connexion serveur esclave > "))
                ack = True
            except:
                print("[ERREUR] Port incorrect")
        serveur.bind((ip, porta))
        serveur.settimeout(1)
        x = None
        while True:
            try:
                s_limit = int(input("[SETTINGS] Nombre de serveur esclave maximal souhaité > "))
                if s_limit <= 0 :
                    print("[ERREUR] La valeur ne peut être nulle ou négative.")
                else:
                    break
            except :
                print("[ERREUR] La valeur entrée est incorrect.")
                continue
        serveur.listen(s_limit)

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ack = False
        while ack == False:
            try:
                portb = int(input("[SETTINGS] Entrez le port de connexion client > "))
                ack = True
            except:
                print("[ERREUR] Port incorrect")
        client.bind((ip, portb))
        client.settimeout(1)
        while True:
            try:
                c_limit = int(input("[SETTINGS] Nombre de connexion client maximal souhaité > "))
                if c_limit <= 0 :
                    print("[ERREUR] La valeur ne peut être nulle ou négative.")
                else:
                    break
            except :
                print("[ERREUR] La valeur entrée est incorrect.")
                continue
        client.listen(c_limit)

    except OSError:
        print("[ERREUR] impossible d'initialiser le socket, pool IP/PORT déjà utilisé par un autre programme.")
        sys.exit()
    
    print("[INFO] Serveur initialisé, en attente de connexion.")
    print(f"[WARNING] Veillez à bien ouvrir votre pare-feu pour les ports {porta} et {portb} en TCP/IP.")
    liste_client, liste_serveur = [], [] # création d'une liste référence qui contiendra les différentes informations des connexions.
    thAC = threading.Thread(daemon=True, target=AcceptClient, args=[c_limit])
    thAS = threading.Thread(daemon=True, target=AcceptServeur, args=[s_limit])
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