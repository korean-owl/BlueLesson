#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8
HOST = '192.168.0.49'
PORT = 12370
import numpy as np
import time
import Adafruit_DHT
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import RPi.GPIO as GPIO
import socket
from pymavlink import mavutil

# Function to get the array from the server
def get_array_from_server():
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    s.connect((HOST, PORT))

    # Receive the array
    array = s.recv(1024).decode()

    # Close the connection
    s.close()

    return array

# Get the array from the server
received_array = get_array_from_server()
# Display the received array
print("Received array from server: ", received_array)

# Define a global variable for the sound sensor state
sound_state = 0

# Configure GPIO pins
sound_pin = 17
temp_pin = 4
CLK  = 18  # Changed from 18 to 23
MISO = 23
MOSI = 24  # Changed from 24 to 25
CS   = 25  # Changed from 25 to 8

GPIO.setwarnings(False)  # Ignore warnings
GPIO.setmode(GPIO.BCM)
GPIO.setup(sound_pin, GPIO.IN)

# Configure temperature and humidity sensor
sensor = Adafruit_DHT.DHT22

# Configure MQ-7 sensor
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# A.py와 B.py 코드를 결합
# B.py의 코드 시작
connection_string = "/dev/ttyAMA0"
# Create a connection to the Pixhawk
master = mavutil.mavlink_connection(connection_string, baud=57600)

# Wait for a heartbeat to establish the connection
master.wait_heartbeat()

ESC=1500
SER=1500
# Function to handle sound detection events
def sound_detected(channel):
    print("Sound detected!")
    send_data(1)

# Rest of the code remains the same...

# Function to read sensor values
def read_sensor():
    # Read data from the temperature and humidity sensor
    humidity, temperature = Adafruit_DHT.read_retry(sensor, temp_pin)
    # Read data from the MQ-7 sensor
    CO_level = mcp.read_adc(0)
    # Read data from the sound sensor
    sound = GPIO.input(sound_pin)
    return temperature, humidity, CO_level, sound

# Function to send sensor data to the server
def send_data(sound):
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the server
    s.connect((HOST, PORT))
    
    temperature, humidity, CO_level, _ = read_sensor()
    # Send data to the server
    data = f'Temperature: {temperature}°C, Humidity: {humidity}%, CO level: {CO_level}, Sound: {sound}'
    s.sendall(data.encode())
    
    # Close the connection
    s.close()

# Register event for sound sensor
GPIO.add_event_detect(sound_pin, GPIO.RISING, callback=sound_detected, bouncetime=200)

# Rest of the code...

# Update the stop function to call send_data
#def stop(n):
#    print("stop")
#    set_servo(6,n)
#    set_servo(5,n)
#    time.sleep(1)
#    send_data(GPIO.input(sound_pin))

# Function to set the vehicle mode
def set_mode(mode):
    mode_mapping = {
        'MANUAL': 0,
        'GUIDED': 4,
        'HOLD': 2,
        'AUTO': 3,
        'STEERING': 1,
        'LOITER': 5,
        'RTL': 6,
        'SMART_RTL': 7,
        'GUIDED_NOGPS': 20
    }
    mode_id = mode_mapping.get(mode)
    
    if mode_id is None:
        print("Invalid mode specified")
        return

    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_MODE,
        0,
        mode_id,
        0, 0, 0, 0, 0, 0
    )

# Function to set the servo PWM value-servo
def set_servo(servo_num, pwm_value):
    master.mav.command_long_send(
        master.target_system, master.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_SERVO,
        0,  # Confirmation
        servo_num, pwm_value, 0, 0, 0, 0, 0
    )

def forward(n):
    set_servo(5,n+94)
    print("forward")
    time.sleep(1)

def backward(n):
    set_servo(5,n-86)
    print("backward")
    time.sleep(2)

def right(n):
    set_servo(6,n-350)
    print("right")
    time.sleep(2)

def left(n):
    set_servo(6,n+300)
    print("left")
    time.sleep(2)

def stop(n):
    print("stop")
    set_servo(6,n)
    set_servo(5,n)
    time.sleep(2)
    

def Trun_left(N):
    print("Turn_right")
    stop(ESC)
    left(ESC)
    for i in range(N):
       forward(ESC+10) 
    stop(ESC)
  
def perform_action():
    send_data(GPIO.input(sound_pin))
    print("action")
    temperature, humidity, CO_level, sound = read_sensor()
    print(f'Temperature: {temperature}°C, Humidity: {humidity}%, CO level: {CO_level}, Sound: {sound}')

def Go(N):
    for i in range(1*N):
        forward(ESC)
    #stop(ESC+80)
#Go(1)
    
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the server
    s.connect((HOST, PORT))
    
    # Send data to the server
   # data = f'Temperature: {temperature}°C, Humidity: {humidity}%, CO level: {CO_level}, Sound: {sound}'
    #s.sendall(data.encode())
    # Close the connection
    s.close()
#length=len(received_array)
#print(length)
number_array = []
for character in received_array:
    if character.isdigit():
        number_array.append(int(character))
print(number_array)
j=-1
for i in range (3):
    j+=1
    j=j%5
    Go(1)
    stop(ESC+80)
    #array_mingu = [1, 2, 3, 4, 5]
   # print(recieved_array[j])
    if number_array[j]==1:
        perform_action()
    #input_string = input("특정 숫자를 입력하세요 (1부터 5까지, 여러 개의 숫자를 공백으로 구분하여 입력): ")
    #target_numbers = list(map(int, input_string.split()))
    j+=1
    
    #print(recieved_array[j])
    set_servo(6,ESC-300)
    Go(1)
    stop(ESC+80)
    if number_array[j]==1:
        perform_action()
stop(ESC+50)


# 배열과 특정 숫자 입력 받기


# 함수 호출

