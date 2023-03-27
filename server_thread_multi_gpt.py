import socket
import threading

HOST = '0.0.0.0'
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
client_names = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
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

        print
