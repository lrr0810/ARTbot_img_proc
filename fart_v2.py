###
# The first version of the robot program that will include the image processing
# and the radio frequency communication in one file with no threading
# Written by: Eyob Gemechu
import sys
sys.path.append('/usr/local/lib/python3.4/site-packages')
sys.path.append('/usr/local/lib/python2.7/site-packages')
import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev
import numpy as np
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera

#####Initilize the NRFcomms######
# Set pin mode
GPIO.setmode(GPIO.BCM)

# the writing and reading addresses
pipes = [[0xE8,0xE8,0xF0,0xF0,0xE1],[0xF0,0xF0,0xF0,0xF0,0xE1]]

# initilize and assign the NRF24 object
radio = NRF24(GPIO,spidev.SpiDev())

# Initilize the SPI bus on the following (ce, csn) pins
radio.begin(0,17)

# the size of the data. max = 32
radio.setPayloadSize(32)

# specified channel to listen to. max = 127
radio.setChannel(0x75)

# the trasfer rate of the data(1MBPS, 2MBPS, 250KBPS)
radio.setDataRate(NRF24.BR_1MBPS)

# amount of power(MIN, LOW, HIGH, MAX, ERROR)
radio.setPALevel(NRF24.PA_MAX)
radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()
###############################

#####Initilize the camera######
width = 400
height = 400
mid = int(width/2)
camera = PiCamera()
camera.resolution = (width,height)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(width,height))
lower = np.array([100,100,100])
upper = np.array([130,255,255])
###############################

radio.openWritingPipe(pipes[0])
radio.openReadingPipe(1, pipes[1])
radio.printDetails()
time.sleep(0.1)


for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    img1 = frame.array
    hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask,None, iterations=2)
    _,contours,hierarchy=cv2.findContours(mask,1,cv2.CHAIN_APPROX_NONE)
    if len(contours)> 0:
        cnt = max(contours, key=cv2.contourArea)
        M = cv2.moments(cnt)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        cv2.line(img1,(cx,0),(cx,height),(0,0,255),1)
        cv2.line(img1,(mid,0),(mid,height),(0,255,255),1)
        cv2.line(img1,(0,cy),(width,cy),(0,0,255),1)
        cv2.drawContours(img1,contours,-1,(0,255,0),3)
        #print(cx)
        #command = "250"
        
        error = mid-cx
        print("mid is at "+str(mid)+" cx is at "+str(cx)+" and the error is "+str(error)+"\n")
        msg = list(str(error))
        while len(msg) < 32:
            msg.append(0)
        radio.write(msg)
        time.sleep(.08)

        
        radio.write(msg)
        #print("Sent the message: {}".format(msg))
        if error < -50:
            turnMsg = list("turn right\n")
            radio.write(turnMsg)

        if error > 50:
            turnMsg = list("turn left\n")
            radio.write(turnMsg)
        
        radio.startListening()
        receivedMessage = []
        radio.read(receivedMessage, radio.getDynamicPayloadSize())
        
        #print("reading from arduino "+(radio.read()))
        #print("reading from arduino: {}".format(receivedMessage))
    
    cv2.imshow('frame',img1) #show video
    key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)

    if key == ord("q"):
        break  




'''
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    img1 = frame.array
    hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask,None, iterations=2)
    _,contours,hierarchy=cv2.findContours(mask,1,cv2.CHAIN_APPROX_NONE)
    if len(contours)> 0:
        cnt = max(contours, key=cv2.contourArea)
        M = cv2.moments(cnt)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        cv2.line(img1,(cx,0),(cx,height),(0,0,255),1)
        cv2.line(img1,(mid,0),(mid,height),(0,255,255),1)
        cv2.line(img1,(0,cy),(width,cy),(0,0,255),1)
        cv2.drawContours(img1,contours,-1,(0,255,0),3)
        #print(cx)
        #command = "250"
        
        error = mid-cx
        print("mid is at "+str(mid)+" cx is at "+str(cx)+" and the error is "+str(error)+"\n")
        radio.write(list(str(error)))
        
        #mcomms.write(error)
        #print("reading from arduino "+str(mcomms.read()))
    cv2.imshow('frame',img1) #show video
    key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)

    if key == ord("q"):
        break    
    img1 = frame.array
    cv2.imshow('frame',img1) #show video
    key = cv2.waitKey(1) & 0xFF
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
'''















