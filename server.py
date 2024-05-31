import socket
import threading

host=socket.gethostname()
ip=socket.gethostbyname(host)
print(ip)

def client_handler(client_socket, address):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            broadcast(message, client_socket)
        except:
            break

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                print("Connection closed")
                remove_client(client)

def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)
        client_socket.close()

def server():
    global clients
    clients = []

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, 59000))
    server_socket.listen(3)
    while True:
        client_socket, address = server_socket.accept()
        print(address)
        clients.append(client_socket)
        client_thread = threading.Thread(target=client_handler, args=(client_socket, address))
        client_thread.start()

if __name__ == "__main__":
    server()