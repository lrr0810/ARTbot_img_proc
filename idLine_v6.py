import numpy as np
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import NRF24L01
import _thread

cx = 0
camera = PiCamera()
camera.resolution = (400,304)
camera.framerate = 45
rawCapture = PiRGBArray(camera, size=(400,304))
#red: [150,150,150],[180,255,255]
#blue: [110,50,50],[130,255,255]; [100,100,0][130,255,255]

#lower = np.array([150,150,150])
#upper= np.array([180,255,255])
lower = np.array([100,100,100])
upper = np.array([130,255,255])


time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
   img1 = frame.array
   hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
   mask = cv2.inRange(hsv, lower, upper)
   img = cv2.bitwise_and(img1,img1, mask= mask)
   #img = cv2.medianBlur(img, 15)
   gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)#convert each frame to grayscale.
   img=cv2.GaussianBlur(gray,(5,5),0)#blur the grayscale image
   blur = cv2.Canny(img,50,150,apertureSize = 3)
   image, contours, hierarchy = cv2.findContours(blur,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #find the contours
   cv2.drawContours(img1,contours,-1,(0,255,0),3)
   for cnt in contours:
      if cnt is not None:
          area = cv2.contourArea(cnt)# find the area of contour
      if area>=500 :
       # find moment and centroid
       M = cv2.moments(cnt)
       cx = int(M['m10']/M['m00'])
       cy = int(M['m01']/M['m00'])
   print(str(cx))
   # Starts new thread for radio lstening/ transmitting cx
   #_thread.start_new_thread(radio_comm(cx))

   cv2.imshow('frame',img1) #show video
   key = cv2.waitKey(1) & 0xFF
   # clear the stream in preparation for the next frame
   rawCapture.truncate(0)

   # if the `q` key was pressed, break from the loop
   if key == ord("q"):
         break

# Definition for radio comm thread function
"""def radio_comm(cx):
   radio.write(cx)
   radio.startListening
   
    while not radio.available(0):
        time.sleep(1/100)
        if time.time() - start >2:
            print("Timed out.")
            break
"""
