from dronekit import connect, VehicleMode
import time

# Connect to the Pixhawk
connection_string = "/dev/ttyACM0"  # adjust based on your connection (e.g., "/dev/ttyUSB0")
baud_rate = 57600
vehicle = connect(connection_string, baud=baud_rate, wait_ready=True)

# Set the vehicle mode to MANUAL to allow motor control
vehicle.mode = VehicleMode("MANUAL")
time.sleep(1)

# Function to set motor throttle
def set_motor_throttle(throttle):
    vehicle.channels.overrides = {'3': throttle}
    time.sleep(1)

try:
    # Set motor throttle to 1500 (neutral)
    set_motor_throttle(1500)
    time.sleep(5)

    # Set motor throttle to 1700 (increase speed)
    set_motor_throttle(1700)
    time.sleep(5)

    # Set motor throttle to 1500 (neutral)
    set_motor_throttle(1500)
    time.sleep(5)

finally:
    # Clear channel overrides and disconnect
    vehicle.channels.overrides = {}
    vehicle.close()
