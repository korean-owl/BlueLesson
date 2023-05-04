import Adafruit_DHT
import RPi.GPIO as GPIO
import time

# Sensor type
sensor = Adafruit_DHT.DHT22

# GPIO pin number (Data pin connected to GPIO4 for the temperature sensor)
temp_pin = 4

# GPIO pin number for the digital sound recognition sensor
sound_pin = 17

# Configure GPIO for sound sensor
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(sound_pin, GPIO.IN)

# Function to handle sound detection events
def sound_detected(channel):
    print("Sound detected!")

# Register event for sound sensor
GPIO.add_event_detect(sound_pin, GPIO.RISING, callback=sound_detected, bouncetime=200)

# Continuously read sensor data using an infinite loop.
try:
    while True:
        # Read data from the temperature and humidity sensor
        humidity, temperature = Adafruit_DHT.read_retry(sensor, temp_pin)

        if humidity is not None and temperature is not None:
            print(f'Temperature: {temperature:.1f}°C, Humidity: {humidity:.1f}%')
        else:
            print('Failed to get sensor data')

        # Set the delay time (here set to 2 seconds)
        time.sleep(2)

except KeyboardInterrupt:
    GPIO.cleanup()
