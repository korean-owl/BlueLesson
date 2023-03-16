#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2
import numpy as np

def nothing(x):
    pass

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
curr_x,curr_y=0,0
while True:
    _, frame=cap.read()
    hsv_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    h,w,_=frame.shape
    
    cx=int(w/2)
    cy=int(h/2)
    
#Pick pixel value
    pixel_center=hsv_frame[cy,cx]
    hue_value = pixel_center[0]
    
    color = "Undefined"
   
    color_name= str(hue_value)
    if hue_value<5:
        curr_x,curr_y=1,0
        color = "RED"+" "+color_name+" Coordinates: "+str(curr_x)+","+str(curr_y)+")"
    elif hue_value<22:
        curr_x,curr_y=2,0
        color = "ORANGE"+" "+color_name+" Coordinates: "+str(curr_x)+","+str(curr_y)+")"
       
    elif hue_value<33:
        curr_x,curr_y=3,0
        color = "YELLOW"+" "+color_name+'\n'+"Coordinates: "+str(curr_x)+","+str(curr_y)+")"
        
    elif hue_value<78:
        curr_x,curr_y=4,0
        color = "GREEN"+" "+color_name+" Coordinates: "+str(curr_x)+","+str(curr_y)+")"
        
    elif hue_value<131:
        curr_x,curr_y=5,0
        color = "BLUE"+" "+color_name+" Coordinates: "+str(curr_x)+","+str(curr_y)+")"
    elif hue_value<167:
        curr_x,curr_y=6,0
        color = "VIOLET"+" "+color_name+" Coordinates: "+str(curr_x)+","+str(curr_y)+")"
       
    else:
        color="RED"+" "+color_name+" Coordinates: "+str(curr_x)+","+str(curr_y)+")"
        
     
    pixel_center_bgr=frame[cy,cx]
    cv2.putText(frame,color,(10,50),0,1,(255,0,0),2)
    cv2.circle(frame,(cx,cy),5,(255,0,0),3)
    
    cv2.imshow("Frame",frame)
    key=cv2.waitKey(1)
    if key ==27:
        break
        
cap.release()
cv2.destoryAllWindows()


# In[ ]:





# In[ ]:




