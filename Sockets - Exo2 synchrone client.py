import socket

if __name__ == "__main__":
    print("initialisation ...")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 8123))
    print("client connecté au serveur")

    message = ""
    while message != "bye" and message != "arret":
        message = str(input("message à envoyer : "))
        client_socket.send(message.encode())
        reply = client_socket.recv(1024).decode()
        print(f"réponse du serveur : '{reply}'")
    client_socket.close()