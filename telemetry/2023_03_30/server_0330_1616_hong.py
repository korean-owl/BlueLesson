import socket
import threading

HOST = '192.168.0.3'
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
client_names = []

def broadcast(coordinates):
    for client in clients:
        client.send(coordinates)

def handle(client):
    while True:
        try:
            coordinates = client.recv(1024)
            broadcast(coordinates)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            client_name = client_names[index]
            client_names.remove(client_name)
            broadcast(f'{client_name} disconnected.'.encode('utf-8'))
            break

def receive():
    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}')

        client.send('NAME'.encode('utf-8'))
        client_name = client.recv(1024).decode('utf-8')
        client_names.append(client_name)
        clients.append(client)

        print(f'{client_name} connected.')
        broadcast(f'{client_name} joined the coordinate sharing session!'.encode('utf-8'))

        client_thread = threading.Thread(target=handle, args=(client,))
        client_thread.start()

print("Server is listening...")
receive()

