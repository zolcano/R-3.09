import socket, sys, subprocess, threading, psutil, time, os, sys, random
def console():
    """
    fonction de gestion de la console du serveur maître.
    /help dans le terminal pour afficher la liste des commandes.
    """
    print("[CONSOLE] /help pour la liste des commandes")
    while not fin.is_set():
        ack = False
        commande = input("")
        if commande.lower() == "/help":
            ack = True
            print("[HELP] /info : renvoie IP/PORT local et connexion distante.")
            print("[HELP] /cpu : Renvoie la charge actuel du processeur en %")
            print("[HELP] /stop : arrêt complet du serveur esclave.")
        if commande.lower() == "/stop":
            ack = True
            ip, port = client.getsockname()
            print(f"[CONSOLE] Arrêt du serveur esclave à l'adresse {ip}:{port}.")
            try:
                client.send('/stop'.encode("utf-8"))
            except:
                pass
            fin.set()
        if commande.lower() == "/cpu":
            ack = True
            cpu = psutil.cpu_percent(interval=1)
            print(f"[CONSOLE] {cpu}%")
        if commande.lower() == "/info":
            ack = True
            IP, PORT = client.getpeername()
            cIP, cPORT = client.getsockname()
            print(f"[CONSOLE] Connecté à {IP}:{PORT} via {cIP}:{cPORT}.")
        if ack == False:
            print("[ERREUR] Commande inconnue.")

def ecoute():
    """
    Cette fonction sert de port d'écoute à la communication inter-serveur

    Protocole:
    /file = réception de fichier
    /stop = arrêt du serveur maître
    /arret = déconnexion forcée par le serveur maître
    """
    while not fin.is_set():
        try:
            message = client.recv(1024).decode("utf-8")
            if not message:
                continue
            message_split = message.split(" ") #séparation des informations envoyés en un seul message si necessaire.
            print(message_split)
            if message_split[0] == "/file": #envoi de fichier par le serveur maître.
                extension = message_split[1].split('.')
                print("\n[INFO] Début de session.")
                print(f"[INFO] Reception d'un fichier en cour.")
                ack = False
                while ack == False:
                    try:
                        temp_name = 'temp'+str(random.randint(0,99999)) #création d'un dossier temp aléatoire pour y stocker les fichiers de la session.
                        os.mkdir(temp_name)
                        ack=True
                    except Exception as e:
                        print(e)
                with open(os.path.join(temp_name,message_split[1]), "wb") as file: #écriture du fichier envoyé dans le dossier généré
                    received_size = 0
                    while received_size < int(message_split[2]):
                        data = client.recv(1024)
                        file.write(data)
                        received_size += len(data)
                    print(f"[INFO] {received_size} octet.s correctement reçu") #impression des informations dans la console

                if extension[1] == "java": #algorithme à effectuer en fonction de l'extension de fichier détecté.
                    try:
                        print('[INFO] Fichier .java détecté.')
                        print("[INFO] Execution dans",temp_name)
                        print(f'[INFO] Compilation de {message_split[1]}')
                        os.chdir(temp_name)
                        subprocess.run(args=["javac",message_split[1]], capture_output=True)
                        print(f'[INFO] Fichier compilé {extension[0]}.class créé')
                        print(f'[INFO] Execution de : {extension[0]}.class.')
                        exec = subprocess.run(args=["java",extension[0]], capture_output=True)
                        os.chdir(os.path.dirname(os.path.abspath(__file__)))
                    except Exception as e:
                        print(e)
                        continue

                if extension[1] == "cc" or extension[1] == "cpp":
                    try:
                        print('[INFO] Fichier C++ détecté.')
                        print("[INFO] Execution dans",temp_name)
                        print(f'[INFO] Compilation de {message_split[1]}')
                        os.chdir(temp_name)
                        out = extension[0]+'.o'
                        subprocess.run(args=["g++", '-c', message_split[1], '-o', out], capture_output=True)
                        print(f'[INFO] Fichier compilé {extension[0]}.o créé')
                        subprocess.run(args=["g++", out, '-o', extension[0]], capture_output=True)
                        print(f"[INFO] exécutable {extension[0]}.exe créé.")
                        print(f'[INFO] Execution de : {extension[0]}.exe .')
                        exe = extension[0] + '.exe'
                        exec = subprocess.run(args=[exe], capture_output=True)
                        os.chdir(os.path.dirname(os.path.abspath(__file__)))
                    except Exception as e:
                        print(e)
                        continue

                if extension[1] == "c":
                    try:
                        print('[INFO] Fichier C détecté.')
                        print("[INFO] Execution dans",temp_name)
                        print(f'[INFO] Compilation de {message_split[1]}')
                        os.chdir(temp_name)
                        out = extension[0]+'.o'
                        subprocess.run(args=["gcc", '-c', message_split[1], '-o', out], capture_output=True)
                        print(f'[INFO] Fichier compilé {extension[0]}.o créé')
                        subprocess.run(args=["gcc", out, '-o', extension[0]], capture_output=True)
                        print(f"[INFO] exécutable {extension[0]}.exe créé.")
                        print(f'[INFO] Execution de : {extension[0]}.exe .')
                        exe = extension[0] + '.exe'
                        exec = subprocess.run(args=[exe], capture_output=True)
                        os.chdir(os.path.dirname(os.path.abspath(__file__)))
                    except Exception as e:
                        print(e)
                        continue

                if extension[1] == "py":
                    try:
                        print('[INFO] Fichier .py détecté.')
                        print("[INFO] Execution dans",temp_name)
                        print(f'[INFO] Execution de : {message_split[1]} .')
                        exec = subprocess.run(args=['python', message_split[1]], capture_output=True)
                        os.chdir(os.path.dirname(os.path.abspath(__file__)))
                    except Exception as e:
                        print(e)
                        continue

                if exec.stdout: #impression dans la console de la sortie
                    print('###### Sortie : ######\n\n',exec.stdout.decode('utf-8').strip(),'\n\n######################')
                    output =exec.stdout.decode('utf-8').strip()
                if exec.stderr:
                    print('###### Exception : ######\n\n',exec.stderr.decode('utf-8').strip(),'\n\n##########################')
                    output =exec.stderr.decode('utf-8').strip()
                print("[INFO] Envoi du résultat au serveur maître.")
                output = '/out' + ' ' + message_split[3] + ' ' + message_split[4] + "/////" + output #renvoi au serveur maitre de la sortie, + ip/port client
                client.send(output.encode("utf-8"))
                print("[INFO] Envoi terminé.")
                print("[INFO] Fin de session.\n")

            if message == "/stop":
                print(f"[INFO] Arrêt du serveur Maître, déconnexion automatique.")
                fin.set()
            if message == "/arret":
                print(f"[INFO] Arrêt demandé par le serveur maître, deconnexion.")
                fin.set()
        except:
            break

def Monitoring():
    """
    Envoi des informations de charge cpu au serveur principal toutes les 5 secondes.
    """
    while not fin.is_set():
        cpu = psutil.cpu_percent(interval=1)
        client.send(("/cpu " + str(round(cpu,2))).encode("utf-8"))
        time.sleep(5)

def environnement():
    """
    Cette fonction effectue plusieurs tests afin de connaître l'environnement dans lequel le serveur esclave est exécuté.
    """
    try : #test de la présence du compilateur java
        jdk = subprocess.run(args=["javac","--version"], capture_output=True)
        retour = jdk.stdout.decode("utf-8") #décodage de la sortie en utf-8 puis stockage de la version
        jdk = True
        jdk_ver = ""
        y = False
        for x in retour:
            if x == " " and y == False:
                y = True
            if y == True and x != " ":
                jdk_ver += x
        languages.append(['jdk', jdk, jdk_ver.strip()])
    except:
        jdk = False
        languages.append(['jdk', jdk, None])

    if jdk == False: #test de la présence de l'environnement java si le compilateur n'est pas installé
        try:
            jre = subprocess.run(args=["java","-version"], capture_output=True) #test de la présence de java JRE dans le PATH
            jre = True
            print("[WARNING] uniquement l'environnement de java est installé, compilateur non présent sur la machine.")
        except:
            jre = False
    
    try :
        gcc = subprocess.run(args=["gcc","--version"], capture_output=True) #test de la présence de Gnu Compilater Collection (GCC) pour le c et c++
        retour = gcc.stdout.decode("utf-8") #décodage de la sortie en utf-8 puis stockage de la version
        gcc = True
        gcc_ver = ""
        for i in range (19,30):
            if retour[i] == ")":
                break
            gcc_ver += retour[i]
        languages.append(['gcc', gcc, gcc_ver.strip()])
    except:
        gcc = False
        languages.append(['gcc', gcc, None])

    try :
        py = subprocess.run(args=["python","--version"], capture_output=True)
        retour = py.stdout.decode("utf-8") #décodage de la sortie en utf-8 puis stockage de la version
        py = True
        py_ver = ""
        y = False
        for x in retour:
            if x == " " and y == False:
                y = True
            if y == True and x != " ":
                py_ver += x
        languages.append(['py', py, py_ver.strip()])
    except:
        py = False
        languages.append(['py', py, None]) #censé ne jamais se produire

if __name__ == "__main__":
    print("[INFO] Initialisation du serveur esclave.")
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        ack = False
        while ack == False: #ip du serveur maitre à rentrer
            ip = input("[SETTINGS] Entrez l'adresse ip du serveur maître (127.0.0.1 > localhost) : ")
            ipcheck = ip.split(".")
            try:
                if len(ipcheck) == 4:
                    for x in ipcheck:
                            y = int(x)
                ack = True
            except:
                print("[ERREUR] Format d'adresse IP incorrect")
    
        ack = False
        while ack == False:
            try:
                port = int(input("[SETTINGS] Entrez le port de connexion serveur esclave : "))
                ack = True
            except:
                print("[ERREUR] Port incorrect")
        client.connect((ip, port))
    except:
        print("[INFO] Erreur lors de la connexion au serveur maître")
        sys.exit()
    print("[INFO] Client connecté au serveur maître")

    languages = [] # liste qui contiendra les paramètres définis par la fonction environnement
    environnement()
    message = "" # récupération des données de la liste, convertissement en string pour l'envoi au serveur
    for i in range(len(languages)):
        for x in languages[i]:
            if x == None:
                message += ",None"
            else:
                message += "," + str(x)
    client.send(message.encode("utf-8")) #envoi des informations au client
    print("[INFO] Configuration partagée.")

    fin = threading.Event()
    thCONS = threading.Thread(daemon=True, target=console) #initiation d'un thread pour la console
    thCONS.start()
    thECC = threading.Thread(daemon=True, target=ecoute)
    thECC.start()
    thMON = threading.Thread(daemon=True, target=Monitoring)
    thMON.start()

    fin.wait() # empêche l'arret du serveur (thread principal) tant que l'event stop n'est pas déclanché.
    client.close()
    sys.exit()