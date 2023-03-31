#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2
import numpy as np
import socket
import threading
import time

# client.py part
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

# happy.py part
cap = cv2.VideoCapture(0)

while True:
    # 김현준 (happy.py 코드)영상처리
    ret, frame = cap.read()
    height, width, _ = frame.shape
    colors = ["RED", "YELLOW", "GREEN", "CYAN", "BLUE", "PURPLE", "PINK", "ORANGE"]
    color_dict = {
    "RED": (0, 0, 255),
    "YELLOW": (0, 255, 255),
    "GREEN": (0, 255, 0),
    "CYAN": (255, 255, 0),
    "BLUE": (255, 0, 0),
    "PURPLE": (255, 0, 255),
    "PINK": (203, 192, 255),
    "ORANGE": (0, 165, 255)
}
    name=1
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 색상 범위 지정 (10가지 색상)
    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    lower_green = np.array([50, 100, 100])
    upper_green = np.array([70, 255, 255])
    lower_cyan = np.array([90, 100, 100])
    upper_cyan = np.array([110, 255, 255])
    lower_blue = np.array([110, 100, 100])
    upper_blue = np.array([130, 255, 255])
    lower_purple = np.array([130, 100, 100])
    upper_purple = np.array([150, 255, 255])
    lower_pink = np.array([160, 100, 100])
    upper_pink = np.array([180, 255, 255])
    lower_orange = np.array([10, 100, 100])
    upper_orange = np.array([20, 255, 255])

    # 각 색상에 대한 마스크 생성
    mask_red = cv2.inRange(hsv_frame, lower_red, upper_red)
    mask_yellow = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)
    mask_green = cv2.inRange(hsv_frame, lower_green, upper_green)
    mask_cyan = cv2.inRange(hsv_frame, lower_cyan, upper_cyan)
    mask_blue = cv2.inRange(hsv_frame, lower_blue, upper_blue)
    mask_purple = cv2.inRange(hsv_frame, lower_purple, upper_purple)
    mask_pink = cv2.inRange(hsv_frame, lower_pink, upper_pink)
    mask_orange = cv2.inRange(hsv_frame, lower_orange, upper_orange)

    # 각 마스크에 대한 컨투어 (윤곽선) 검출
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_yellow, _ = cv2.findContours(mask_yellow, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_cyan, _ = cv2.findContours(mask_cyan, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_purple, _ = cv2.findContours(mask_purple, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_pink, _ = cv2.findContours(mask_pink, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_orange, _ = cv2.findContours(mask_orange, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 가장 큰 컨투어 (윤곽선)을 찾아 중심점 표시
    contour_list = [contours_red, contours_yellow, contours_green, contours_cyan, contours_blue, contours_purple, contours_pink, contours_orange]
    max_contour_area = 0
    max_center = None

    for i, contours in enumerate(contour_list):
        for contour in contours:
            contour_area = cv2.contourArea(contour)
            if contour_area > max_contour_area:
                max_contour_area = contour_area
                max_contour = contour
                name = colors[i]

                if max_contour is not None:
                    M = cv2.moments(max_contour)
                    center_x = int(M["m10"] / M["m00"])
                    center_y = int(M["m01"] / M["m00"])
                    max_center = (center_x, center_y)
    
   # if max_contour is not None:
    #color_index = contour_list.index(name)
    #color_name = colors[color_index]
    color_index = -1
    color_name = ""
    curr_x, curr_y = (0, 0)
    if max_contour is not None:
        color_name = name
        curr_x, curr_y = (colors.index(name), 0)   
   
    # 결과 영상에 중심점 표시
    
        #if max_contour is not None:
         #   color_name = colors[contour_list.index(max_contour)]
          #  cv2.putText(frame, color_name, (10,50), 0, 1, (255,0,0), 2)
    if max_center is not None:
        coordinate_x, coordinate_y = max_center
        wish_x = str((width / 2) - coordinate_x)
        wish_y = str((height / 2) - coordinate_y)
        position = f"{coordinate_x} , {coordinate_y} wish {wish_x} , {wish_y} {color_name}"
        cv2.putText(frame, position, (10, 50), 0, 1, (255, 0, 0), 2)
        cv2.circle(frame, max_center, 5, (255, 255, 255), -1)
    #happy.py 영상처리부분
    
    # 결과 영상 출력
    cv2.imshow("Frame", frame)

    # 좌표를 문자열로 변환하고 send_coordinates() 함수로 전송
    coordinates = f'{curr_x},{curr_y},{color_name}'
    send_coordinates(coordinates)

    # 키 입력 대기
    key = cv2.waitKey(1)

    # 'q' 키를 누르면 종료
    if key == ord('q'):
        break

# 종료
cap.release()
cv2.destroyAllWindows()

# 스레드 시작
receive_thread = threading.Thread(target=receive)
receive_thread.start()


# In[ ]:




