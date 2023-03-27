import socket
import threading
import time
import random

# Replace this with the server's IP address
SERVER_IP = 'your_server_ip'
PORT = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, PORT))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NAME':
                client.send(client_name.encode('utf-8'))
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close()
            break

def send_sensor_data():
    while True:
        time.sleep(1)
        sensor_data = random.uniform(20, 30)  # Simulating sensor data
        message = f'{client_name}: {sensor_data:.2f}'
        client.send(message.encode('utf-8'))

client_name = input("Enter your client name: ")

receive_thread = threading.Thread(target=receive)
receive_thread.start()

send_sensor_data_thread = threading.Thread(target=send_sensor_data)
send_sensor_data_thread.start()
