import numpy as np
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

img1 = cv2.imread('bluetape.jpg')
cv2.resize(img1,(320,240),interpolation = cv2.INTER_AREA)
hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
#red: [150,150,150],[180,255,255]
#blue: [110,50,50],[130,255,255]; [100,100,0][130,255,255]

#lower = np.array([150,150,150])
#upper= np.array([180,255,255])
lower = np.array([100,100,100])
upper = np.array([130,255,255])
mask = cv2.inRange(hsv, lower, upper)
img = cv2.bitwise_and(img1,img1, mask= mask)
img = cv2.medianBlur(img, 15)



#gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)#convert each frame to grayscale.
#blur=cv2.GaussianBlur(gray,(5,5),0)#blur the grayscale image
blur = cv2.Canny(img,50,150,apertureSize = 3)
ret,th1 = cv2.threshold(blur,35,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)#using threshold remave noise
ret1,th2 = cv2.threshold(th1,127,255,cv2.THRESH_BINARY_INV)# invert the pixels of the image frame


image, contours, hierarchy = cv2.findContours(th1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #find the contours
cv2.drawContours(img,contours,-1,(0,255,0),3)
cv2.imshow('frame',img) #show video
#cv2.imshow('frame',th1)
cv2.waitKey(0)
for cnt in contours:
   if cnt is not None:
       area = cv2.contourArea(cnt)# find the area of contour
   if area>=500 :
    # find moment and centroid
    M = cv2.moments(cnt)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])

print(str(cx))
