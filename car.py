from dronekit import connect, VehicleMode, LocationGlobalRelative,APIException
import time
import socket
import exceptions
import math
import argparse
################################

def connectMyCopter():
    parser =argparse.ArgumentParser(description='ccmmands')
    parser.add_argument('--connect')
    args= parser.parse_arge()
    
    connetction_string = args.connect
    baud_rate = 57600
    
    vehicle =connect(connection_string,baud=baud_rate,wait_ready=True)
    return vehicle

def arm():
    while vehicle.is_armable==False:
        print("Wating for vehicle to becom armable...")
        time.sleep(1)
    print("Yoooo vehicle is now armable")
    print("")
    
    vehicle.armed=True
    while vehicle.armed==False:
        print("Wating for vehicle to becom armable...")
        time.sleep(1)
        
    print("Vehicle is now armed")
    print("OMG props are spinning. LOCK OCT")
    return None
#############################
vehicle = connectMyCopter()
arm()
print("End of sleeps")