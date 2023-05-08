#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import time
from pymavlink import mavutil

# A.py와 B.py 코드를 결합
# B.py의 코드 시작
connection_string = "/dev/ttyAMA0"
# Create a connection to the Pixhawk
master = mavutil.mavlink_connection(connection_string, baud=57600)

# Wait for a heartbeat to establish the connection
master.wait_heartbeat()

ESC=1500
SER=1500
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
    set_servo(4,n+85)
    
    print("foward")
    time.sleep(1)
def backward(n):
    set_servo(4,n-86)
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
    set_servo(4,n)
    time.sleep(1)
def Trun_left(N):
    print("Trun_right")
    stop(ESC)
    left(ESC)
    for i in range(N):
       forward(ESC+10) 
    stop(ESC)
  

def Go(N):
    for i in range(3*N):
        forward(ESC)
    stop(ESC)
#Go(1)
for i in range(2):
    set_servo(6,ESC)
    Go(1)
    set_servo(6,ESC-100)
    Go(1)
Trun_left(4)
for i in range(2):
    set_servo(6,ESC)
    Go(1)
    set_servo(6,ESC-100)
    Go(1)
Trun_left(4)
stop(ESC)

