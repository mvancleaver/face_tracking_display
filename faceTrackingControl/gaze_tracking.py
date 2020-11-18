
############################################################################################################
###################################################### - Setup 
############################################################################################################

import cv2
import time
import board
import busio
import json
import adafruit_bno055
from adafruit_servokit import ServoKit
from gaze_tracking import GazeTracking

# IMU Init 
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)
x_home = sensor.euler[0]
y_home = sensor.euler[1]
z_home = sensor.euler[2]

# PWM Driver Init 
i2c_1 = busio.I2C(board.SCL_1, board.SDA_1)
kit = ServoKit(channels=16, i2c=i2c_1)

# Gaze Init 
gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

############################################################################################################
###################################################### - Control + Motion Primatives
############################################################################################################


# Axis Motion Primatives
def move_X():
    print("Moving X")

def move_Y():
    print("Moving Y")

def move_Z():
    print("Moving Z")

# Homing 
def home_X():
    print("Homing X")

def home_Y():
    print("Homing Y")

def home_Z():
    print("Homing Z")

def home_All():
    print("Homing X")
    print("Homing Y")
    print("Homing Z")

############################################################################################################
###################################################### - System Main 
############################################################################################################

while True:
   
# Grab a frame and process Gaze info 
    _, frame = webcam.read()
    gaze.refresh(frame)
    new_frame = gaze.annotated_frame()
    text = ""
    if gaze.is_right():
        text = "Looking right"
        move_X()
    elif gaze.is_left():
        text = "Looking left"
        move_X()
    elif gaze.is_center():
        text = "Looking center"
        home_ALL()

    cv2.putText(new_frame, text, (60, 60), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 0, 0), 2)
    cv2.imshow("Demo", new_frame)
    if cv2.waitKey(1) == 27:
        break

# Print Data to Terminal / JSON
    print("==========================================")
    print("Euler angle X: {}".format(sensor.euler[0]))
    print("Euler angle Y: {}".format(sensor.euler[1]))
    print("Euler angle Z: {}".format(sensor.euler[2]))
    print()
    data = {"eurler":{"X":sensor.euler[0],"Y":sensor.euler[1],"Z":sensor.euler[2]}}
    with open("data_file.json", "w") as write_file:
        json.dump(data, write_file)

    time.sleep(0.035) # Set to loop at ~30FPS