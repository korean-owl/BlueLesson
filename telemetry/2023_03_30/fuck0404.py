import time
from pymavlink import mavutil

connection_string = "/dev/ttyAMA0"

# Create a connection to the Pixhawk
master = mavutil.mavlink_connection(connection_string, baud=57600)

# Wait for a heartbeat to establish the connection
master.wait_heartbeat()

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

# Set the mode to MANUAL
set_mode("MANUAL")
time.sleep(1)

# Commands to control the rover
set_servo(4, 1580)  # Move forward
print("foward")
time.sleep(3)
set_servo(4, 1500)#go stop

set_servo(4, 1410)  # Move backward
print("back")
time.sleep(3)
set_servo(4, 1500)#back stop

#set_rc_channel(3, 1600)  # Turn right
set_servo(6,1600)
print("right")
time.sleep(3)
#set_rc_channel(3, 1300)  # Turn left
set_servo(6,1200)
print("left")
time.sleep(3)


# Reset controls to neutral positions
set_rc_channel(4, 1500)
set_rc_channel(3, 1500)
