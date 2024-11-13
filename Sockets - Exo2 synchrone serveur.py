import socket

def chat(conn):
    message = ""
    while (message != "bye") and (message != "arret"):
        message = conn.recv(1024).decode()
        print(f"message entrant : '{message}'")
        reply = "ok"
        conn.send(reply.encode())
        print(f"message envoyé : {reply}")
    if message == "arret":
        return(False)
    return True

if __name__ == "__main__":
    print("### initialisation ...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 8123))
    server_socket.listen(1)

    stop = True
    while stop :
        print("### serveur en attente...")
        conn, address =  server_socket.accept()
        print(f"### connexion by {address[0]} : accepted")
        stop = chat(conn)
    print("### fermeture du serveur")
    server_socket.close()