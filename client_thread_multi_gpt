import socket
import threading
import time

HOST = '192.168.0.3'  # Change this to the server IP if not running on the same machine
PORT = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def send_coordinates(coordinates):
    client.send(coordinates.encode('utf-8'))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NAME':
                client_name = input("Enter your name: ")
                client.send(client_name.encode('utf-8'))
            else:
                print(message)
        except:
            print("An error occurred.")
            client.close()
            break

def get_coordinates_from_external_source():
    # Replace this function with the actual method for getting coordinates from an external source
    # For example, getting coordinates from a GPS device
    while True:
        x, y = input("Enter coordinates (x,y): ").split(',')
        coordinates = f'{x},{y}'
        send_coordinates(coordinates)
        time.sleep(1)

def main():
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    external_source_thread = threading.Thread(target=get_coordinates_from_external_source)
    external_source_thread.start()

if __name__ == '__main__':
    main()
