import socket, sys, subprocess

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
        client.connect(("127.0.0.1", 3218))
    except:
        print("[INFO] Erreur lors de la connexion au serveur maitre")
        sys.exit()
    print("[INFO] Client connecté au serveur")
    languages = []
    environnement()

    message = "" #récupération des données de la liste, convertissement en string pour l'envoi au serveur
    for i in range(len(languages)):
        for x in languages[i]:
            if x == None:
                message += ",None"
            else:
                message += "," + str(x)
    
    client.send(message.encode("utf-8"))
    print("message envoyé !")
    print(message)
    while True:
        continue