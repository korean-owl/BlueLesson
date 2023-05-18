import socket
import random
import numpy as np

# Change the port number
PORT = 12355

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
s.bind(('', PORT))

# Listen for incoming connections
s.listen(1)

print('Server is running and waiting for connections...')

# Set the thresholds for temperature, humidity, and CO level
TEMP_THRESHOLD = 27
HUMIDITY_THRESHOLD = 39
CO_THRESHOLD = 36

# Read the array from the txt file
with open('array.txt', 'r') as f:
    array_str = f.read().strip('()\n')  # strip parentheses and newline characters
    array = [int(x) for x in array_str.split(',')]

while True:
    # Wait for a connection
    conn, addr = s.accept()

    print('Connected by', addr)

    # Send the array to the client
    conn.send(str(array).encode())

    # Receive the data in small chunks
    data = conn.recv(1024)

    if data:
        print('Received data: ', data.decode())

        # Parse the received data
        data = data.decode().split(',')
        temp = float(data[0].split(': ')[1][:-2])
        humidity = float(data[1].split(': ')[1][:-1])
        co = int(data[2].split(': ')[1])
        sound = int(data[3].split(': ')[1])

        # Check if the thresholds are exceeded or sound is detected
        if temp > TEMP_THRESHOLD and humidity > HUMIDITY_THRESHOLD and co > CO_THRESHOLD and sound == 1:
            print("There is a fire.")

    # Close the connection
    conn.close()
