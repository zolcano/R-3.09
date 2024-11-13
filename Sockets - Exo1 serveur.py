import socket, time

if __name__ == "__main__":

    print("initialisation ...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 8123))
    print("socket setting up : ok")
    server_socket.listen(1)
    print("socket en attente ...")
    conn, address = server_socket.accept()
    print(f"connexion by {address[0]} : accepted")
    message = conn.recv(1024).decode()
    print(f"message entrance : '{message}'")

    reply = "message received correctly"
    conn.send(reply.encode())
    print("connexion answered")
    conn.close() 
    print("entrance connexion closed")
    server_socket.close()