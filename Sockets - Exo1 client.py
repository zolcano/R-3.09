import socket

if __name__ == "__main__":
    print("initialisation ...")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 8123))
    print("socket setting up : ok")
    message = "message from client"
    client_socket.send(message.encode())
    print(f"message '{message}' correctly sent")
    reply = client_socket.recv(1024).decode()
    print(f"answer received : '{reply}'")
    client_socket.close()