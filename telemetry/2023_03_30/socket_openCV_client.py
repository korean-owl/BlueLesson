import socket
import threading
import cv2
import numpy as np

HOST = '192.168.0.3'  # Change this to the server IP if not running on the same machine
PORT = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def send_coordinates(coordinates):
    client.send(coordinates.encode('utf-8'))

def receive():
    global canvas
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NAME':
                client_name = input("Enter your name: ")
                client.send(client_name.encode('utf-8'))
            else:
                if ',' in message:
                    x, y = map(int, message.split(','))
                    cv2.circle(canvas, (x, y), 5, (0, 255, 0), -1)
                    cv2.imshow(window_name, canvas)
                    cv2.waitKey(1)
                else:
                    print(message)
        except:
            print("An error occurred.")
            client.close()
            break

def main():
    global canvas, window_name

    window_name = 'Coordinates Visualization'
    cv2.namedWindow(window_name)
    canvas = np.zeros((600, 800, 3), dtype=np.uint8)

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    while True:
        _, frame = cap.read()
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        h, w, _ = frame.shape

        cx = int(w / 2)
        cy = int(h / 2)

        pixel_center = hsv_frame[cy, cx]
        hue_value = pixel_center[0]

        # (previous color detection code)

        # Call send_coordinates with curr_x and curr_y
        coordinates = f"{curr_x},{curr_y}"
        send_coordinates(coordinates)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    receive_thread.join()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
